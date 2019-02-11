from calendar import month_name
from itertools import chain
from json import dumps
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.messages import info
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse

from cartridge.shop import checkout
from cartridge.shop.forms import ( CartItemFormSet
                                  )  # order form DiscountFormAddProductForm,
from cartridge.shop.models import Product, ProductVariation, Order, DiscountCode,Category
from cartridge.shop.utils import recalculate_cart, sign

from el_pagination.decorators import page_template

from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.views import render, set_cookie, paginate
from mezzanine.conf import settings
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.generic.models import Keyword

from forex_python.converter import CurrencyRates
from payments.utils import get_or_update_discount


from paypal.standard.forms import PayPalPaymentsForm

from .forms import OrderForm, DiscountForm, AddProductForm
from .utils import increment_num_sold, check_membership_purchase_order, process_member_discounts, \
    check_fortune_purchase_order, check_class_purchase_order, send_class_email

User = get_user_model()



handler = lambda s: import_dotted_path(s) if s else lambda *args: None
billship_handler = handler(settings.SHOP_HANDLER_BILLING_SHIPPING)
tax_handler = handler(settings.SHOP_HANDLER_TAX)
payment_handler = handler(settings.SHOP_HANDLER_PAYMENT)
order_handler = handler(settings.SHOP_HANDLER_ORDER)


# Create your views here.
# def test_app(request):
#     context = {"yes":"worked"}
#     return TemplateResponse(request,"test_mez/test_view.html",context)


#### Cartridge views replacements ####

def product(request, slug, template="shop/product.html",
            form_class=AddProductForm, extra_context=None):
    """
    Display a product - convert the product variations to JSON as well as
    handling adding the product to either the cart or the wishlist.
    """
    published_products = Product.objects.published(for_user=request.user)
    product = get_object_or_404(published_products, slug=slug)
    fields = [f.name for f in ProductVariation.option_fields()]
    variations = product.variations.all()
    variations_json = dumps([dict([(f, getattr(v, f))
        for f in fields + ["sku", "image_id"]]) for v in variations])
    to_cart = (request.method == "POST" and
               request.POST.get("add_wishlist") is None)
    initial_data = {}
    if variations:
        initial_data = dict([(f, getattr(variations[0], f)) for f in fields])
    initial_data["quantity"] = 1
    add_product_form = form_class(request.POST or None, product=product,
                                  initial=initial_data, to_cart=to_cart)
    if request.method == "POST":
        if add_product_form.is_valid():
            if to_cart:
                quantity = add_product_form.cleaned_data["quantity"]
                request.cart.add_item(add_product_form.variation, quantity)
                recalculate_cart(request)
                info(request, _("Item added to cart"))
                return redirect("shop_cart")
            else:
                skus = request.wishlist
                sku = add_product_form.variation.sku
                if sku not in skus:
                    skus.append(sku)
                info(request, _("Item added to wishlist"))
                response = redirect("shop_wishlist")
                set_cookie(response, "wishlist", ",".join(skus))
                return response
    related = []
    if settings.SHOP_USE_RELATED_PRODUCTS:
        related = product.related_products.published(for_user=request.user)
    try:
        # set title = membership level + product slug ("statue+gold")
        # discount = DiscountCode.objects.filter(title="{}+{}".format(product.sku, request.user.membership.level))[0]
        discount = get_or_update_discount(request,sku=product.sku)
        # discount_percent = (100 - discount.discount_percent)/100
        discount_deduction = discount.discount_deduct
    except:
        discount_deduction = 0
    try:
        c = CurrencyRates()
        hkd_rate = c.get_rate('CNY','HKD')
    except:
        hkd_rate = 1.1584

    context = {
        "product": product,
        "editable_obj": product,
        "images": product.images.all(),
        "variations": variations,
        "variations_json": variations_json,
        "has_available_variations": any([v.has_price() for v in variations]),
        "related_products": related,
        "add_product_form": add_product_form,
        "discount": discount_deduction,
        "hkd_rate":hkd_rate
    }
    context.update(extra_context or {})
    templates = [u"shop/%s.html" % str(product.slug), template]
    return TemplateResponse(request, templates, context)


@never_cache
def cart(request, template="shop/cart.html",
         cart_formset_class=CartItemFormSet,
         discount_form_class=DiscountForm,
         extra_context=None):
    """
    Display cart and handle removing items from the cart.
    """
    discount_form = discount_form_class(request, request.POST or None)
    process_member_discounts(request, discount_form)
    cart_formset = cart_formset_class(instance=request.cart)

    if request.method == "POST":
        valid = True
        if request.POST.get("update_cart"):
            valid = request.cart.has_items()
            if not valid:
                # Session timed out.
                info(request, _("Your cart has expired"))
            else:
                cart_formset = cart_formset_class(request.POST,
                                                  instance=request.cart)
                valid = cart_formset.is_valid()
                if valid:
                    cart_formset.save()
                    recalculate_cart(request)
                    info(request, _("Cart updated"))
                else:
                    # Reset the cart formset so that the cart
                    # always indicates the correct quantities.
                    # The user is shown their invalid quantity
                    # via the error message, which we need to
                    # copy over to the new formset here.
                    errors = cart_formset._errors
                    cart_formset = cart_formset_class(instance=request.cart)
                    cart_formset._errors = errors
        else:
            # todo: code isn't working...! Add to URL args/cookie
            valid = discount_form.is_valid()
            if valid:
                discount_form.set_discount()
            # Potentially need to set shipping if a discount code
            # was previously entered with free shipping, and then
            # another was entered (replacing the old) without
            # free shipping, *and* the user has already progressed
            # to the final checkout step, which they'd go straight
            # to when returning to checkout, bypassing billing and
            # shipping details step where shipping is normally set.
            # recalculate_cart(request)
        if valid:
            return redirect("shop_cart")
    context = {"cart_formset": cart_formset,
               "discount_percent": settings.MEMBERSHIP_MULTIPLIER}
    context.update(extra_context or {})
    settings.use_editable()
    if (settings.SHOP_DISCOUNT_FIELD_IN_CART and
            DiscountCode.objects.active().exists()):
        context["discount_form"] = discount_form
    return TemplateResponse(request, template, context)


@never_cache
def checkout_steps_patch(request, form_class=OrderForm, extra_context=None):
    """
    Display the order form and handle processing of each step.
    """

    # Do the authentication check here rather than using standard
    # login_required decorator. This means we can check for a custom
    # LOGIN_URL and fall back to our own login view.
    authenticated = request.user.is_authenticated()
    if settings.SHOP_CHECKOUT_ACCOUNT_REQUIRED and not authenticated:
        url = "%s?next=%s" % (settings.LOGIN_URL, reverse("shop_checkout"))
        return redirect(url)

    try:
        settings.SHOP_CHECKOUT_FORM_CLASS
    except AttributeError:
        pass
    else:
        from warnings import warn
        warn("The SHOP_CHECKOUT_FORM_CLASS setting is deprecated - please "
             "define your own urlpattern for the checkout_steps view, "
             "passing in your own form_class argument.")
        form_class = import_dotted_path(settings.SHOP_CHECKOUT_FORM_CLASS)

    initial = checkout.initial_order_data(request, form_class)
    step = int(request.POST.get("step", None) or
               initial.get("step", None) or
               checkout.CHECKOUT_STEP_FIRST)
    form = form_class(request, step, initial=initial)
    data = request.POST
    checkout_errors = []

    # PAYMENT CHECKOUT STEP
    # Give all payment keys here
    if step == checkout.CHECKOUT_STEP_PAYMENT:
        # for STRIPE - can't use after all
        extra_context = {
            # "stripe_pk":settings.STRIPE_PK,
        }
    if request.POST.get("back") is not None:
        # Back button in the form was pressed - load the order form
        # for the previous step and maintain the field values entered.
        step -= 1
        form = form_class(request, step, initial=initial)
    elif request.method == "POST" and request.cart.has_items():
        form = form_class(request, step, initial=initial, data=data)
        if form.is_valid():
            # Copy the current form fields to the session so that
            # they're maintained if the customer leaves the checkout
            # process, but remove sensitive fields from the session
            # such as the credit card fields so that they're never
            # stored anywhere.
            request.session["order"] = dict(form.cleaned_data)
            sensitive_card_fields = ("card_number", "card_expiry_month",
                                     "card_expiry_year", "card_ccv")
            for field in sensitive_card_fields:
                if field in request.session["order"]:
                    del request.session["order"][field]

            # FIRST CHECKOUT STEP - handle discount code. This needs to
            # be set before shipping, to allow for free shipping to be
            # first set by a discount code.
            if step == checkout.CHECKOUT_STEP_FIRST:
                form.set_discount()

            # ALL STEPS - run billing/tax handlers. These are run on
            # all steps, since all fields (such as address fields) are
            # posted on each step, even as hidden inputs when not
            # visible in the current step.
            try:
                billship_handler(request, form)
                tax_handler(request, form)
            except checkout.CheckoutError as e:
                checkout_errors.append(e)

            # FINAL CHECKOUT STEP - run payment handler and process order.
            if step == checkout.CHECKOUT_STEP_LAST and not checkout_errors:
                # Create and save the initial order object so that
                # the payment handler has access to all of the order
                # fields. If there is a payment error then delete the
                # order, otherwise remove the cart items from stock
                # and send the order receipt email.
                order = form.save(commit=False)
                order.setup(request)
                # Try payment.
                try:
                    transaction_id = payment_handler(request, form, order)
                except checkout.CheckoutError as e:
                    # Error in payment handler.
                    order.delete()
                    checkout_errors.append(e)
                    if settings.SHOP_CHECKOUT_STEPS_CONFIRMATION:
                        step -= 1
                else:
                    # Finalize order - ``order.complete()`` performs
                    # final cleanup of session and cart.
                    # ``order_handler()`` can be defined by the
                    # developer to implement custom order processing.
                    # Then send the order email to the customer.
                    order.transaction_id = transaction_id
                    order.complete(request)
                    order_handler(request, form, order)

                    # checks if a member object is in cart, and if it is, updates membership
                    # check of membership status in 1 year set by model method
                    # all moved to payment step
                    # increment_num_sold(order)
                    # membership_ordered, level = check_membership_purchase_order(order)
                    # class_ordered, classes = check_class_purchase_order(order)
                    # fortune_ordered, fortune = check_fortune_purchase_order(order)
                    # prayer_ordered, prayer = check_fortune_purchase_order(order)
                    # # checkout.send_order_email(request, order)
                    # if membership_ordered:
                    #     request.user.membership.update_membership(level)
                    # if class_ordered:
                    #     send_class_email(request, order, classes)
                    # if fortune_ordered:
                    #     pass
                    # if prayer_ordered:
                    #     pass
                    # Set the cookie for remembering address details
                    # if the "remember" checkbox was checked.
                    # response = redirect("shop_complete")
                    response = redirect("payments:pay")
                    set_cookie(response, "order_id", order.id, secure=request.is_secure())
                    if form.cleaned_data.get("remember"):
                        remembered = "%s:%s" % (sign(order.key), order.key)
                        set_cookie(response, "remember", remembered,
                                   secure=request.is_secure())
                    else:
                        response.delete_cookie("remember")
                    return response

            # If any checkout errors, assign them to a new form and
            # re-run is_valid. If valid, then set form to the next step.
            form = form_class(request, step, initial=initial, data=data,
                              errors=checkout_errors)
            if form.is_valid():
                step += 1
                form = form_class(request, step, initial=initial)

    # Update the step so that we don't rely on POST data to take us back to
    # the same point in the checkout process.
    try:
        request.session["order"]["step"] = step
        request.session.modified = True
    except KeyError:
        pass

    step_vars = checkout.CHECKOUT_STEPS[step - 1]
    template = "shop/%s.html" % step_vars["template"]
    context = {"CHECKOUT_STEP_FIRST": step == checkout.CHECKOUT_STEP_FIRST,
               "CHECKOUT_STEP_LAST": step == checkout.CHECKOUT_STEP_LAST,
               "CHECKOUT_STEP_PAYMENT": (settings.SHOP_PAYMENT_STEP_ENABLED and
                   step == checkout.CHECKOUT_STEP_PAYMENT),
               "step_title": step_vars["title"], "step_url": step_vars["url"],
               "steps": checkout.CHECKOUT_STEPS, "step": step, "form": form,
               "stripe_total": request.cart.total_price() * 100,
               "stripe_currency": settings.STRIPE_CURRENCY,
               "payment_method": request.POST.get("payment_type") or initial.get("payment_type")
               }
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def track_order(request, order_id, template="shop/track_order.html", extra_context=None):
    """
    Display a plain text invoice for the given order. The order must
    belong to the user which is checked via session or ID if
    authenticated, or if the current user is staff.
    """
    try:
        order = Order.objects.get_for_user(order_id, request)
    except Order.DoesNotExist:
        raise Http404
    # if None...
    context = {"order": order}
    context.update(order.details_as_dict())
    context.update(extra_context or {})
    return render(request, template, context)


def home_view(request, template="index.html", extra_context=None):
    """
    Top: slider with featured blog posts/items
    Middle: 1 or 2 class promotions
    Bottom: 2 blog items & 2 products
    http://stackoverflow.com/questions/431628/how-to-combine-2-or-more-querysets-in-a-django-view
    http://pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/


    :param request:
    :param template:
    :param extra_context:
    :return:
    """
    # takes the most recent frontpage blog items and products and constructs them into a 3-slider
    blog_slider_items = BlogPost.objects.filter(frontpage=True).order_by('-publish_date')[:3]
    product_slider_items = Product.objects.filter(frontbanner=True).order_by('-publish_date')[:3]
    # for p in product_slider_items:
    #     p.featured_image = p.image
    slider_items = sorted(
        chain(blog_slider_items, product_slider_items),
        key=lambda item: item.publish_date,
        reverse=True
    )[:3]
    # featured_classes = Product.objects.filter(is_class=True, frontpage=True).order_by('-publish_date')[:2]
    # featured_products = Product.objects.filter(frontpage=True).order_by('-publish_date')[:2]
    # blog_posts = BlogPost.objects.all().order_by('-publish_date')[:settings.HOMEPAGE_BLOG_POSTS]
    blog_posts = BlogPost.objects.all().order_by('-publish_date').first()
    products = Product.objects.filter(frontpage=True).order_by('-publish_date')[:3]
    # day, month = blog_posts.publish_date.day, blog_posts.publish_date.month
    # print(day)
    # print(month)
    # exclude categories without a parent and anything 3rd tier,
    # which should thusly only give us the first level shop subcategories
    # top_level = Category.objects.filter(parent=None)
    # categories = Category.objects.filter(parent=top_level)
    context = {"slider_items":slider_items,
               "blog_post":blog_posts,
               "products":products,
               # "categories":categories,
               # "featured_classes":featured_classes,
               # "featured_products":featured_products
               }
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@page_template('blog/blog_post_list_page.html')
def blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html",
                   extra_context=None):
    """
    Patched version of Mezzanine's blog / blog_post_list
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    # for 2 featured blogposts
    if tag or year or category or username:
        # don't show featured posts if viewing by category, tag, year, username
        featured_posts = None
    else:
        featured_posts = BlogPost.objects.published(for_user=request.user).filter(blogpage=True)[:2]
    # for all blogposts
    blog_posts = BlogPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        blog_posts = blog_posts.filter(keywords__keyword=tag)
    if year is not None:
        blog_posts = blog_posts.filter(publish_date__year=year)
        if month is not None:
            blog_posts = blog_posts.filter(publish_date__month=month)
            try:
                month = month_name[int(month)]
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(categories=category)
        templates.append(u"blog/blog_post_list_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        blog_posts = blog_posts.filter(user=author)
        templates.append(u"blog/blog_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    # blog_posts = paginate(blog_posts, request.GET.get("page", 1),
    #                       settings.BLOG_POST_PER_PAGE,
    #                       settings.MAX_PAGING_LINKS)
    context = {"blog_posts": blog_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author, "featured_posts":featured_posts}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)
