# from cartridge.shop.models import Order
# from django.shortcuts import get_object_or_404
#
# from cartridge.shop.models import Product, Order
from cartridge.shop.models import Product, ProductVariation, Order, DiscountCode,Category
from django.template.loader import get_template, TemplateDoesNotExist


from mezzanine.conf import settings
from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.email import send_mail_template


from locale import setlocale, LC_MONETARY, Error as LocaleError
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _


def check_membership_purchase_order(order):
    """
    checks it with order info
    :param user_id:
    :param levels:
    :return:
    """
    items = order.items.all()
    for item in items:
        item = ProductVariation.objects.get(sku=item.sku)
        item = item.product
        if item.is_membership_level:
            return True, item.slug  # slug = level
    return False, "regular"


def check_class_purchase_order(order):
    """
    checks it with order info
    if mroe than one class purchase, emails list to User and Kiki.
    :param user_id:
    :param levels:
    :return:
    """
    items = order.items.all()
    classes = []
    has_class = False
    for item in items:
        item = ProductVariation.objects.get(sku=item.sku)
        item = item.product
        if item.is_class:
            classes.append(item)
            has_class = True
    if has_class:

        return True, classes
    return False, "regular product"


def send_class_email(request, order, classes):
    """
    Send order receipt email on successful order.
    """
    settings.use_editable()
    order_context = {"order": order, "request": request,
                     "classes": classes}
    # order_context.update(classes.details_as_dict())
    try:
        get_template("shop/email/class_confirm.html")
    except TemplateDoesNotExist:
        receipt_template = "email/class_confirm"
    else:
        receipt_template = "shop/email/class_confirm"
        from warnings import warn
        warn("Shop email receipt templates have moved from "
             "templates/shop/email/ to templates/email/")
    send_mail_template(settings.SHOP_ORDER_EMAIL_SUBJECT,
                       receipt_template, settings.SHOP_ORDER_FROM_EMAIL,
                       order.billing_detail_email, context=order_context,
                       addr_bcc=settings.SHOP_ORDER_EMAIL_BCC or None)


def check_fortune_purchase_order(order):
    """
    checks it with order info
    If more than one fortune purchased, sends list to Kiki.
    :param user_id:
    :param levels:
    :return:
    """

    items = order.items.all()
    fortunes = []
    has_fortune = False
    for item in items:
        item = ProductVariation.objects.get(sku=item.sku)
        item = item.product
        if item.is_fortune:
            fortunes.append(item)
        if has_fortune:
            return True, fortunes  # slug = level
    return False, "regular product"


def clear_session(request, *names):
    """
    Removes values for the given session variables names
    if they exist.
    """
    for name in names:
        try:
            del request.session[name]
        except KeyError:
            pass


def recalculate_cart_patch(request):
    """
    Updates an existing discount code, shipping, and tax when the
    cart is modified.
    todo: show only best price
    """
    from cartridge.shop import checkout
    from cartridge.shop.forms import DiscountForm
    from cartridge.shop.models import Cart

    # Rebind the cart to request since it's been modified.
    if request.session.get('cart') != request.cart.pk:
        request.session['cart'] = request.cart.pk
    request.cart = Cart.objects.from_request(request)

    discount_code = request.session.get("discount_codes", "")
    if discount_code:
        # Clear out any previously defined discount code
        # session vars.
        names = ("free_shipping", "discount_codes", "discount_total")
        clear_session(request, *names)
        discount_form = DiscountForm(request, {"discount_codes": discount_code})
        if discount_form.is_valid():
            discount_form.set_discount()

    handler = lambda s: import_dotted_path(s) if s else lambda *args: None
    billship_handler = handler(settings.SHOP_HANDLER_BILLING_SHIPPING)
    tax_handler = handler(settings.SHOP_HANDLER_TAX)
    try:
        if request.session["order"]["step"] >= checkout.CHECKOUT_STEP_FIRST:
            billship_handler(request, None)
            tax_handler(request, None)
    except (checkout.CheckoutError, ValueError, KeyError):
        pass


def set_locale():
    """
    Sets the locale for currency formatting.
    todo: mod to track currency via language flag?
    """
    currency_locale = str(settings.SHOP_CURRENCY_LOCALE)
    try:
        if setlocale(LC_MONETARY, currency_locale) == "C":
            # C locale doesn't contain a suitable value for "frac_digits".
            raise LocaleError
    except LocaleError:
        msg = _("Invalid currency locale specified for SHOP_CURRENCY_LOCALE: "
                "'%s'. You'll need to set the locale for your system, or "
                "configure the SHOP_CURRENCY_LOCALE setting in your settings "
                "module.")
        raise ImproperlyConfigured(msg % currency_locale)


def process_member_discounts(request,discount_form):
    discount_form = discount_form
    discounts = []
    request.session["discount_codes"] = []
    discount_form._discount = discounts
    try:  # try to get membership
        if request.user.membership.is_member:
            for i, cart_product in enumerate(request.cart):
                # 22 for test product sku
                variation = ProductVariation.objects.get(sku=cart_product.sku)
                original_price = variation.price()
                # change slug to sku for easier and more reliable use
                title = "{}+{}".format(variation.product.sku, request.user.membership.level)
                try:
                    discount = DiscountCode.objects.get(
                        products=variation.product,
                        membership_level="{}".format(request.user.membership.level),
                        active=True,
                    )
                except:
                    # can't create it directly because meta class reasons, so first
                    # create the Code, then alter its meta properties
                    # http://stackoverflow.com/questions/20056077/django-typeerror-is-active-is-an-invalid-keyword-argument-for-this-function
                    # http://stackoverflow.com/questions/12764347/django-invalid-keyword-argument-for-this-function
                    discount = DiscountCode.objects.create(
                        # products=variation.product,
                        code=title,
                        title=title,
                        active=True,
                        membership_level="{}".format(request.user.membership.level),
                        # discount_deduct=(original_price - variation.gold_member_price_rmb)
                    )
                    discount.products = [variation.product, ]
                    if request.user.membership.level == "diamond":
                        member_price = variation.diamond_member_price_rmb
                    elif request.user.membership.level == "gold":
                        member_price = variation.gold_member_price_rmb
                    else:
                        # deduction = 0 !!!!
                        member_price = original_price
                    discount.discount_deduct = (original_price - member_price)
                    discount.save()
                # can I pass a parameter to discount_form.set_discount()?
                # set as dict?
                discounts.append(discount)
                request.session["discount_codes"].append(discount.code)
            # discount_form.member_discount = product_discounts
            # recalculate_cart(request)
    except:
        pass  # as no membership, and proceed as whatever
    try:
        if request.session.get("discount_code"):
            code = request.session.get('discount_code', "")
            if code not in request.session.get("discount_codes"):
                discount = DiscountCode.objects.get(code=code)
                request.session["discount_codes"].append(discount.code)
                discounts.append(discount)
    except:
        pass
    discount_form._discount = discounts
    discount_form.set_discount()


def increment_num_sold(order):
    items = order.items.all()
    for item in items:
        item = ProductVariation.objects.get(sku=item.sku)
        item = item.product
        item.num_sold += 1
        item.save()