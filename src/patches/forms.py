from __future__ import absolute_import, unicode_literals
from future.builtins import filter, int, range, str, super, zip
from future.utils import with_metaclass

from collections import OrderedDict
from copy import copy
from datetime import date
from decimal import Decimal
from itertools import dropwhile, takewhile
from locale import localeconv
from re import match

from django import forms
from django.forms.models import BaseInlineFormSet, ModelFormMetaclass
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import thumbnail

from cartridge.shop import checkout
from cartridge.shop.forms import FormsetForm
from cartridge.shop.models import Product, ProductOption, ProductVariation
from cartridge.shop.models import Cart, CartItem, Order, DiscountCode
from cartridge.shop.utils import (make_choices, set_locale, set_shipping,
                                  clear_session)


class DiscountForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ("discount_code",)

    def __init__(self, request, data=None, initial=None, **kwargs):
        """
        Store the request so that it can be used to retrieve the cart
        which is required to validate the discount code when entered.
        """
        super(DiscountForm, self).__init__(
                data=data, initial=initial, **kwargs)
        self._request = request

    def clean_discount_code(self):
        """
        Validate the discount code if given, and attach the discount
        instance to the form.
        """
        code = self.cleaned_data.get("discount_code", "")
        cart = self._request.cart
        if code:
            try:
                discount = DiscountCode.objects.get_valid(code=code, cart=cart)
                self._discount.append(discount)
                self._request.session["discount_code"] = discount.code
            except DiscountCode.DoesNotExist:
                error = _("The discount code entered is invalid.")
                raise forms.ValidationError(error)
        return code

    def set_discount(self):
        """
        Assigns the session variables for the discount.
        """
        discounts = getattr(self, "_discount", None)
        # member_discount = getattr(self, "member_discount", None)

        if discounts is not None:
            total = Decimal("0")
            names = ("free_shipping", "discount_codes", "discount_total")
            clear_session(self._request, *names)
            for discount in discounts:
                # Clear out any previously defined discount code
                # session vars.
                total += self._request.cart.calculate_discount(discount)
                if discount.free_shipping:
                    set_shipping(self._request, _("Free shipping"), 0)
                    self._request.session["free_shipping"] = discount.free_shipping
                else:
                    # A previously entered discount code providing free
                    # shipping may have been entered prior to this
                    # discount code beign entered, so clear out any
                    # previously set shipping vars.
                    clear_session(self._request, "shipping_type", "shipping_total")
                self._request.session["discount_codes"] = discount.code
                self._request.session["discount_total"] = str(total)
            # print(total)

    # def set_discount_patch(self):
    #     """
    #     Assigns the session variables for the discount.
    #     http://stackoverflow.com/questions/6930144/underscore-vs-double-underscore-with-variables-and-methods
    #     http://stackoverflow.com/questions/1301346/the-meaning-of-a-single-and-a-double-underscore-before-an-object-name-in-python
    #     """
    #     discount = getattr(self, "_discount", None)
    #     # new discount object for membership?
    #     if discount is not None: #  or self._request.user.membership is "gold"
    #         print("discount patch is a go")
    #         # Clear out any previously defined discount code
    #         # session vars.
    #         names = ("free_shipping", "discount_code", "discount_total","member_discount")
    #         clear_session(self._request, *names)
    #         total = self._request.cart.calculate_discount_patch(discount)
    #         if discount.free_shipping:
    #             set_shipping(self._request, _("Free shipping"), 0)
    #         else:
    #             # A previously entered discount code providing free
    #             # shipping may have been entered prior to this
    #             # discount code beign entered, so clear out any
    #             # previously set shipping vars.
    #             clear_session(self._request, "shipping_type", "shipping_total")
    #         self._request.session["free_shipping"] = discount.free_shipping
    #         self._request.session["discount_code"] = discount.code
    #         self._request.session["member_discount"] = discount.membership
    #         self._request.session["discount_total"] = str(total)
        # if self._request.user.membership is "gold":
        #     total = self._request.session.get("discount_total", 0)
        #     self._request.session["discount_total"] = total *= settings.MEMBERSHIP_DISCOUNT_DECIMAL
        #     try to get discount_total
        #     add cart value * 10% to it (member discount comes before discount code - more savings!)


class OrderForm(FormsetForm, DiscountForm):
    """
    Main Form for the checkout process - ModelForm for the Order Model
    with extra fields for credit card. Used across each step of the
    checkout process with fields being hidden where applicable.
    """

    step = forms.IntegerField(widget=forms.HiddenInput())
    same_billing_shipping = forms.BooleanField(required=False, initial=True,
        label=_("My delivery details are the same as my billing details"))
    remember = forms.BooleanField(required=False, initial=True,
        label=_("Remember my address for next time"))
    # card_name = forms.CharField(label=_("Cardholder name"))
    # card_type = forms.ChoiceField(label=_("Card type"),
    #     widget=forms.RadioSelect,
    #     choices=make_choices(settings.SHOP_CARD_TYPES))
    # card_number = forms.CharField(label=_("Card number"))
    # card_expiry_month = forms.ChoiceField(label=_("Card expiry month"),
    #     initial="%02d" % date.today().month,
    #     choices=make_choices(["%02d" % i for i in range(1, 13)]))
    # card_expiry_year = forms.ChoiceField(label=_("Card expiry year"))
    # card_ccv = forms.CharField(label=_("CCV"), help_text=_("A security code, "
    #     "usually the last 3 digits found on the back of your card."))
    # payment_type = forms.ChoiceField(required=True,choices=[("alipay",_("Alipay")),
    #                                                         ("wechat", _("WeChat")),
    #                                                         ("credit", _("Credit Card")),
    #                                                         ("paypal", _("PayPal"))])
    billing_detail_postcode = forms.CharField(label=_("Zip/Postcode"), initial="00852")
    shipping_detail_postcode = forms.CharField(label=_("Zip/Postcode"), initial="00852")

    class Meta:
        model = Order
        fields = ([f.name for f in Order._meta.fields if
                   f.name.startswith("billing_detail") or
                   f.name.startswith("shipping_detail")] +
                   ["additional_instructions", "discount_code"])

    def __init__(
            self, request, step, data=None, initial=None, errors=None,
            **kwargs):
        """
        Setup for each order form step which does a few things:

        - Calls OrderForm.preprocess on posted data
        - Sets up any custom checkout errors
        - Hides the discount code field if applicable
        - Hides sets of fields based on the checkout step
        - Sets year choices for cc expiry field based on current date
        """

        # ``data`` is usually the POST attribute of a Request object,
        # which is an immutable QueryDict. We want to modify it, so we
        # need to make a copy.
        data = copy(data)

        # Force the specified step in the posted data, which is
        # required to allow moving backwards in steps. Also handle any
        # data pre-processing, which subclasses may override.
        if data is not None:
            data["step"] = step
            data = self.preprocess(data)
        if initial is not None:
            initial["step"] = step

        super(OrderForm, self).__init__(
                request, data=data, initial=initial, **kwargs)
        self._checkout_errors = errors

        # Hide discount code field if it shouldn't appear in checkout,
        # or if no discount codes are active.
        settings.use_editable()
        if not (settings.SHOP_DISCOUNT_FIELD_IN_CHECKOUT and
                DiscountCode.objects.active().exists()):
            self.fields["discount_code"].widget = forms.HiddenInput()

        # Determine which sets of fields to hide for each checkout step.
        # A ``hidden_filter`` function is defined that's used for
        # filtering out the fields to hide.
        is_first_step = step == checkout.CHECKOUT_STEP_FIRST
        is_last_step = step == checkout.CHECKOUT_STEP_LAST
        is_payment_step = step == checkout.CHECKOUT_STEP_PAYMENT
        hidden_filter = lambda f: False
        if settings.SHOP_CHECKOUT_STEPS_SPLIT:
            if is_first_step:
                # Hide cc fields for billing/shipping if steps are split.
                hidden_filter = lambda f: f.startswith("card_")
            elif is_payment_step:
                # Hide non-cc fields for payment if steps are split.
                hidden_filter = lambda f: not f.startswith("card_")
                # hidden_filter = lambda f: not f.startswith("payment_type")
        elif not settings.SHOP_PAYMENT_STEP_ENABLED:
            # Hide all cc fields if payment step is not enabled.
            hidden_filter = lambda f: f.startswith("card_")
        if settings.SHOP_CHECKOUT_STEPS_CONFIRMATION and is_last_step:
            # Hide all fields for the confirmation step.
            hidden_filter = lambda f: True
        for field in filter(hidden_filter, self.fields):
            self.fields[field].widget = forms.HiddenInput()
            self.fields[field].required = False

        # Set year choices for cc expiry, relative to the current year.
        year = now().year
        choices = make_choices(list(range(year, year + 21)))
        # self.fields["card_expiry_year"].choices = choices

    @classmethod
    def preprocess(cls, data):
        """
        A preprocessor for the order form data that can be overridden
        by custom form classes. The default preprocessor here handles
        copying billing fields to shipping fields if "same" checked.
        """
        if data.get("same_billing_shipping", "") == "on":
            for field in data:
                bill_field = field.replace("shipping_detail", "billing_detail")
                if field.startswith("shipping_detail") and bill_field in data:
                    data[field] = data[bill_field]
        return data

    # def clean_card_expiry_year(self):
    #     """
    #     Ensure the card expiry doesn't occur in the past.
    #     """
    #     try:
    #         month = int(self.cleaned_data["card_expiry_month"])
    #         year = int(self.cleaned_data["card_expiry_year"])
    #     except ValueError:
    #         # Haven't reached payment step yet.
    #         return
    #     n = now()
    #     if year == n.year and month < n.month:
    #         raise forms.ValidationError(_("A valid expiry date is required."))
    #     return str(year)

    def clean(self):
        """
        Raise ``ValidationError`` if any errors have been assigned
        externally, via one of the custom checkout step handlers.
        """
        if self._checkout_errors:
            raise forms.ValidationError(self._checkout_errors)
        return super(OrderForm, self).clean()

ADD_PRODUCT_ERRORS = {
    "invalid_options": _("The selected options are currently unavailable."),
    "no_stock": _("The selected options are currently not in stock."),
    "no_stock_quantity": _("The selected quantity is currently unavailable."),
}


class AddProductForm(forms.Form):
    """
    A form for adding the given product to the cart or the
    wishlist.

    qty is hidden, since who buys more than 1 red small sweatshirt anyway?
    """
    quantity = forms.IntegerField(label=_("Quantity"), min_value=1, widget=forms.HiddenInput())
    sku = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        """
        Handles adding a variation to the cart or wishlist.

        When adding from the product page, the product is provided
        from the view and a set of choice fields for all the
        product options for this product's variations are added to
        the form. When the form is validated, the selected options
        are used to determine the chosen variation.

        A ``to_cart`` boolean keyword arg is also given specifying
        whether the product is being added to a cart or wishlist.
        If a product is being added to the cart, then its stock
        level is also validated.

        When adding to the cart from the wishlist page, a sku is
        given for the variation, so the creation of choice fields
        is skipped.
        """
        self._product = kwargs.pop("product", None)
        self._to_cart = kwargs.pop("to_cart")
        super(AddProductForm, self).__init__(*args, **kwargs)
        # Adding from the wishlist with a sku, bail out.
        if args[0] is not None and args[0].get("sku", None):
            return
        # Adding from the product page, remove the sku field
        # and build the choice fields for the variations.
        del self.fields["sku"]
        option_fields = ProductVariation.option_fields()
        if not option_fields:
            return
        option_names, option_labels = list(zip(*[(f.name, f.verbose_name)
            for f in option_fields]))
        option_values = list(zip(*self._product.variations.filter(
            unit_price__isnull=False).values_list(*option_names)))
        if option_values:
            for i, name in enumerate(option_names):
                values = [_f for _f in set(option_values[i]) if _f]
                if values:
                    field = forms.ChoiceField(label=option_labels[i],
                                              choices=make_choices(values),
                                              widget=forms.RadioSelect())
                    self.fields[name] = field
                    print(i,name)
                    print(self.fields[name].choices)

    def clean(self):
        """
        Determine the chosen variation, validate it and assign it as
        an attribute to be used in views.
        """
        if not self.is_valid():
            return
        # Posted data will either be a sku, or product options for
        # a variation.
        data = self.cleaned_data.copy()
        quantity = data.pop("quantity")
        # Ensure the product has a price if adding to cart.
        if self._to_cart:
            data["unit_price__isnull"] = False
        error = None
        if self._product is not None:
            # Chosen options will be passed to the product's
            # variations.
            qs = self._product.variations
        else:
            # A product hasn't been given since we have a direct sku.
            qs = ProductVariation.objects
        try:
            variation = qs.get(**data)
        except ProductVariation.DoesNotExist:
            error = "invalid_options"
        else:
            # Validate stock if adding to cart.
            if self._to_cart:
                if not variation.has_stock():
                    error = "no_stock"
                elif not variation.has_stock(quantity):
                    error = "no_stock_quantity"
        if error is not None:
            raise forms.ValidationError(ADD_PRODUCT_ERRORS[error])
        self.variation = variation
        return self.cleaned_data