from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from django.contrib.messages import info
from mezzanine.utils.urls import login_redirect, next_url
from django.contrib.auth import (login as auth_login, authenticate,
                                 logout as auth_logout, get_user_model)
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from .forms import ProfileForm, MembershipForm, AddressForm, BirthdayForm, EmailForm, ConfirmationForm, DirectionForm
from .models import Membership
from cartridge.shop.models import Product, ProductVariation, Order
from cartridge.shop.utils import recalculate_cart
from django.db.models import Sum
from .tasks import alert_membership_expiration_near_task,membership_expiration_annual_check_task



# Create your views here.
User = get_user_model()


# can do custom register / login page. Put a URL in urls.py before the Mezz ones to supersede it.
@login_required
def user_profile_view(request,template="profiles/profile.html", extra_context=None):
    """
    Show:
    User name
    User fortunes
    User Member level and link to upgrade
    Link to User's shopping cart
    Link to user's shopping history
    User's posts
    Link to change user's name, password, etc
    :param request:
    :return:
    """
    lookup = {"username__iexact": request.user.username, "is_active": True}
    context = {"profile_user": get_object_or_404(User, **lookup)}
    context.update(extra_context or {})
    return render(request, template, context)


def signup_view(request, template="accounts/account_signup.html",
           extra_context=None):
    """
    Signup form.
    """
    profile_form = ProfileForm
    form = profile_form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        new_user = form.save()
        new_membership, created = Membership.objects.get_or_create(user=new_user)
        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                send_approve_mail(request, new_user)
                info(request, _("Thanks for signing up! You'll receive "
                                "an email when your account is activated."))
            else:
                send_verification_mail(request, new_user, "signup_verify")
                info(request, _("A verification email has been sent with "
                                "a link for activating your account."))
            return redirect(next_url(request) or "/")
        else:
            info(request, _("Successfully signed up"))
            auth_login(request, new_user)
            return login_redirect(request)
    context = {"form": form, "title": _("Sign up")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def update_email_view(request, template="profiles/change_generic_form.html", extra_context=None):
    """
    Uses generic profile edit template plus email form to update it
    http://stackoverflow.com/questions/3047700/how-can-i-update-only-certain-fields-in-a-django-model-form
    http://stackoverflow.com/questions/10211493/django-update-certain-fields-of-a-modelform

    """
    form = EmailForm(request.POST or None, instance=request.user)
    # email = request.user.email
    # print(email)
    if request.method == "POST" and form.is_valid():
        form.save()
        info(request, _("Your email address has been updated"))
        return redirect("profile")
    context = {"form": form,
               "title": _("Update Email")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def update_address_view(request, template="profiles/change_generic_form.html", extra_context=None):
    """
    Uses generic profile edit template plus email form to update it
    """
    form = AddressForm(request.POST or None, instance=request.user.myprofile)
    if request.method == "POST" and form.is_valid():
        form.save()
        info(request, _("Your address has been updated"))
        return redirect("profile")
    context = {"form": form, "title": _("Update address")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def update_orientation_view(request, template="profiles/change_generic_form.html", extra_context=None):
    """
    Uses generic profile edit template plus email form to update it
    """
    form = DirectionForm(request.POST or None, instance=request.user.myprofile)
    if request.method == "POST" and form.is_valid():
        form.save()
        info(request, _("Your orientations have been updated"))
        return redirect("profile")
    context = {"form": form, "title": _("Update orientation")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def update_birthday_view(request, template="profiles/change_generic_form.html", extra_context=None):
    """
    Uses generic profile edit template plus email form to update it
    """
    form = BirthdayForm(request.POST or None, instance=request.user.myprofile)
    if request.method == "POST" and form.is_valid():
        form.save()
        info(request, _("Your birthday has been updated"))
        return redirect("profile")
    context = {"form": form, "title": _("Update birthday")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


# @login_required
# def change_membership_view(request, template="profiles/change_membership.html"):
#     """
#     Change from regular account to next level... or jump two levels
#
#     if not the same as before, change pricing etc...
#
#     Show benefits of it too, then let user choose.
#
#     http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
#
#     http://www.vi-solutions.de/en/documentations/bootstrap-3-layouts/docu-bt3layout/655-create-a-multi-column-form-with-bootstrap-3-layout
#     https://docs.djangoproject.com/en/1.10/topics/forms/#rendering-fields-manually
#     https://docs.djangoproject.com/en/1.10/topics/forms/
#     https://docs.djangoproject.com/en/1.10/ref/forms/api/#ref-forms-api-outputting-html
#     http://stackoverflow.com/questions/6766994/in-a-django-form-how-do-i-render-a-radio-button-so-that-the-choices-are-separat
#     http://stackoverflow.com/questions/10237140/how-to-render-individual-radio-button-choices-in-django
#     http://stackoverflow.com/questions/25061804/how-to-manually-render-a-part-of-a-django-form
#
#
#     Click on whole tile to select
#     Add cool FS images to each level
#     https://evernote.com/pricing/ for inspiration
#
#     ---
#     Normal Member:
#     HK$ 0/ year or RMB￥ 0/ year
#     Entitle to read the first paragraph of the essay only
#     Shop at Regular Price for Normal Member (no discount)
#     ---
#     HK$200/ year or RMB￥160/ year
#     Entitle to read all the contents in the website.
#     Receive the Feng Shui tips through email minimum twice a year
#      Will get the Feng Shui calendar (Selling Price at HK$200) as a free gift (Members need to settle the postage, courier cost)
#     Enjoy Gold card member price for all products/ course.
#     Priority of Feng Shui (normal price)
#     Post any question on the Forum and answer will be provide periodically.
#     ---
#     Diamond level member:
#     HK $1000/年 or RMB￥800/年
#     could see all the contents in the website.
#     Receive the Feng Shui tips through email 12 times / year
#      Will get the Feng Shui calendar (Selling Price at HK$200) as a free gift (Members need to settle the postage, courier cost)
#     Free 8 Character tips (Such as color, direction)
#     1 time online Feng Shui tip (Member to provide the floor plan)
#     Priority of Feng Shui(normal price)
#     Diamond level member price for all products/ course.
#     Post any question on the Forum and answer will be provide periodically.
#
#     :param request:
#     :param template:
#     :return:
#     """
#     member_form = MembershipForm(request.POST or None)  # keep POST/None
#     membership = Membership.objects.get(user=request.user)
#     membership_level = membership.level
#     prices = settings.MEMBERSHIPS
#     submit_btn_class = "text-center"
#     if request.method == "POST" and member_form.is_valid():
#         new_member_level = member_form.cleaned_data.get("level")
#         if new_member_level != membership_level:
#             if new_member_level == "regular":
#                 membership.auto_renew = 0
#                 membership.save()
#                 info(request, message="You have unsubscribed successfully")
#                 # schedule cron job to reduce member level on expiry
#                 return redirect("profile")
#             if new_member_level is not "regular":
#                 # request.session["membership_prices"] = settings.MEMBERSHIPS[new_member_level]
#                 request.session["new_membership_level"] = new_member_level
#                 print(request.session)
#                 # set cron job to renew/ remind to renew
#                 return redirect("pay_for_membership")
#
#     context = {
#         "membership_level": membership_level,
#         "member_form": member_form,
#         "submit_btn": _("Select"),
#         "prices": prices,
#         "submit_btn_class": submit_btn_class
#     }
#     return TemplateResponse(request, template, context)

@login_required
def change_membership_view(request, template="profiles/change_membership.html"):
    # check for existence of membership products
    membership_levels = settings.MEMBERSHIPS
    submit_btn_class = "text-center"
    #### testing async membercheck func
    # level = "gold"
    # check_membership_purchase_task.apply_async((request.user.id,level), countdown=5)
    ### end test
    context = {
        "membership_level": "regular",
        "submit_btn": _("Select"),
        "membership_levels": membership_levels,
        "submit_btn_class": submit_btn_class
    }
    return TemplateResponse(request, template, context)


@login_required
def membership_confirm(request, level, template="profiles/membership_confirm.html"):
    """
    http://stackoverflow.com/questions/38566456/how-to-run-a-celery-worker-on-aws-elastic-beanstalk
    http://stackoverflow.com/questions/12813586/running-pythons-celery-on-elastic-beanstalk-with-django
    http://stackoverflow.com/questions/14761468/how-do-you-run-a-worker-with-aws-elastic-beanstalk
    http://stackoverflow.com/questions/26851257/can-celery-run-on-elastic-beanstalk
    http://stackoverflow.com/questions/41231489/run-celery-with-django-on-aws-elastic-beanstalk-using-environment-variables
    https://www.caktusgroup.com/blog/2011/12/19/using-django-and-celery-amazon-sqs/
    http://kronosapiens.github.io/blog/2015/04/28/rabbitmq-aws.html
    http://stackoverflow.com/questions/8048556/celery-with-amazon-sqs
    http://pkj.no/2015/12/deploying-modern-django-apps-to-aws-beanstalk/
    https://www.reddit.com/r/django/comments/3eei3s/celery_and_aws/
    http://stackoverflow.com/questions/15079176/should-django-model-object-instances-be-passed-to-celery

    vvvvvvvvvvvvvvvv
    http://docs.celeryproject.org/en/latest/getting-started/brokers/sqs.html
    ^^^^^^^^^^^^^^^^^
    :param request:
    :param level:
    :param template:
    :return:
    """
    if level not in ["regular","gold","diamond"]:
        return redirect("change_membership_view")
    confirm_level = settings.MEMBERSHIPS[level]
    lookup = {"user": request.user}
    membership = get_object_or_404(Membership, **lookup)  # get user's membership object
    form = ConfirmationForm(request.POST or None, initial={'level': level})
    if request.method == "POST" and form.is_valid():
        # published_products = Product.objects.published(for_user=request.user)
        # if chosen membership product doesn't exist, create it, and its default variation
        member_product, created = Product.objects.get_or_create(slug=level,
                                                       unit_price=settings.MEMBERSHIPS[level]["price"][0],
                                                       # price_hkd=settings.MEMBERSHIPS[level]["price"][1],
                                                       title="{} Membership".format(level.upper()),
                                                       description="{} membership".format(level.upper()))  # slug for each membership would be EN
        if created:
            variation, created_var = ProductVariation.objects.get_or_create(product=member_product,
                                                                    unit_price=settings.MEMBERSHIPS[level]["price"][0],
                                                                    price_hkd=settings.MEMBERSHIPS[level]["price"][1],
                                                                    default=True)
        member_product = member_product.variations.first()  # this gets first variation, which has a sku, or just made
        quantity = 1
        request.cart.add_item(member_product, quantity)
        recalculate_cart(request)
        info(request, _("Your membership will activate after purchase"))
        # check purchase 15 minutes
        # check_membership_purchase_task.apply_async((request.user.id,level),countdown=15)
        return redirect("shop_cart")
    context = {"membership":membership, "confirm_level":confirm_level, "form":form, "submit_btn":_("Confirm membership"),
               "title":level.capitalize()}
    return TemplateResponse(request, template, context)

#
# def test_aws_revoke(request):
#     from celery.result import AsyncResult
#     from celery.task.control import revoke
#     print("testing revoke")
#     test_task = test_aws_revoke_task.apply_async(countdown=15)
#     test_task.revoke()
#     return TemplateResponse(request, template="test/test-revoke.html",context=None)