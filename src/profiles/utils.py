from django.shortcuts import get_object_or_404
from cartridge.shop.models import Product, Order
from mezzanine.utils.email import send_mail_template, subject_template
from django.contrib.auth import get_user_model
from mezzanine.conf import settings
from django.utils.translation import ugettext_lazy as _


def check_membership_purchase(user_id, level):
    """
    UNUSED in favor of a direct check in checkout process, kept for reference purposes
    :param user_id:
    :param level:
    :return:
    """
    order = Order.objects.filter(user_id=user_id).order_by("-time").first()
    print(order.time)
    items = order.items.all()
    member_product = get_object_or_404(Product, slug=level)  # slug for product would be en
    for item in items:
        if item.sku == member_product.sku:
            print("Membership item {} purchased".format(level))
            return True
    return False


def alert_membership_expiration_near(request, user_id, date_end):
    """
    sends notification email to user warning them that their membership expires on end_date, but nothing else
    :param id:
    :param user_id:
    :param end_date:
    :return:
    """
    User = get_user_model()
    user = User.objects.get(id=user_id)
    context = {"name":user.username,
               "request": request,
               "end_date":date_end}
    # subject = subject_template("email/membership_alert_subject.txt", context)
    subject = _("Your membership is about to expire")
    send_mail_template(subject, template='email/membership_alert', addr_from=settings.DEFAULT_FROM_EMAIL, addr_to=user.email,
                       context=context, attachments=None, fail_silently=None, addr_bcc=None,
                       headers=None)


def membership_expiration_annual_check(request, user_id, date_end):
    # check on date of expiration if they had renewed
    User = get_user_model()
    user = User.objects.get(id=user_id)
    user.membership.expire_membership()
    context = {"request": request,
               # "comment_url": add_cache_bypass(comment.get_absolute_url()),
               "name": user.username,
               "end_date": date_end}
    # subject = subject_template("email/membership_expired_subject.txt", context)
    subject = _("Your membership has expired - renew asap to regain benefits!")
    send_mail_template(subject, template='email/membership_expired', addr_from=settings.DEFAULT_FROM_EMAIL,
                       addr_to=user.email,
                       context=context, attachments=None, fail_silently=None, addr_bcc=None,
                       headers=None)