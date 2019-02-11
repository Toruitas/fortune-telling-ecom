from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import ugettext as _
from mezzanine.conf import settings
from django.contrib.auth.decorators import login_required
from cartridge.shop.models import Order
from cartridge.shop import checkout
from django.core.urlresolvers import reverse
import json
import stripe
from forex_python.converter import CurrencyRates

from .utils import payments_order_processor

# Create your views here.

sk = settings.PING_SK
stripe.api_key = settings.STRIPE_SK


@login_required
def pay_for_membership_view(request, template="payments/pay_for_membership.html"):
    """
    Imitate checkout. Maybe make a transaction report as well just like that. Or, just have Memberhsip be
    a product itself, just disincluded from the shopping page?

    Get payment params from cookie, and offer Ping ++ or Stripe
    Create order number too
    :param request:
    :param template:
    :return:
    """
    new_membership_level = request.session.get("new_membership_level")
    prices = settings.MEMBERSHIPS[new_membership_level]
    context = {
        "membership_level":new_membership_level,
        "prices": prices
    }
    return TemplateResponse(request, template, context)


@login_required
@ensure_csrf_cookie
def pay(request, template="payments/pay.html", **kwargs):
    """
    https://stripe.com/docs/sources/alipay
    https://stripe.com/docs/api#bank_accounts
    https://stripe.com/docs/sources/cards
    https://stripe.com/docs/elements#setup
    https://stripe.com/docs/elements/examples
    https://stripe.com/docs/stripe.js
    https://dashboard.stripe.com/test/dashboard

    First step for payment with AliPay or WeChat
    Only step for CC payments

    ensure csrf cookie as we are submitting to ajax during it

    :param request:
    :param template:
    :return:
    """
    try:
        order_id = kwargs['order_id']
    except:
        order_id = None
    if order_id == None:
        try:
            order_id = request.COOKIES.get('order_id')
        except:
            order_id = None
    try:
        order = Order.objects.get(pk=order_id)
    except:
        template = "payments/order_not_found_or_paid.html"
        context = {
            "message": _("This order cannot be found - please contact customer service.")
        }
        return TemplateResponse(request, template, context)
    # order = Order.objects.get(pk=order_id)
    # order = get_object_or_404(Order, pk=order_id)
    if order.paid:
        template = "payments/order_not_found_or_paid.html"
        context = {
            "message":_("This order has already been paid for. Thanks!")
        }
        return TemplateResponse(request, template, context)
    c = CurrencyRates()
    # convert the CNY price to HKD for display
    total_hkd = c.convert('CNY', 'HKD', order.total)
    total = int(order.total * 100)

    if request.method == 'POST':
        # customer = stripe.Customer.create(
        #     email='paying.user@example.com',
        #     source='src_18eYalAHEMiOZZp1l9ZTjSU0',
        # )
        source = request.POST["stripeSource"]
        charge = stripe.Charge.create(
            amount=total,
            currency='cny',
            # customer='cus_AFGbOSiITuJVDs',
            source=source,
        )
        order.source_id = source
        # post-payment order processing
        order = payments_order_processor(request, order)
        order.save()
        response = redirect('payments:payment_received')
        response.delete_cookie("order_id")
        return response
    else:
        context = {
            "order_id": order_id,
            "total": total,
            "stripe_pk":settings.STRIPE_PK,
            "total_display":order.total
        }
        return TemplateResponse(request, template, context)


@login_required
def ajax_get_source_id(request, format=None):
    """
    Updates the order with a source object if AliPay/WeChat is chosen

    http://www.duanqu.tech/questions/2245732/django-request-post-json
    settings.SHOP_ORDER_STATUS_CHOICES[0][0] is unprocessed
    :param request:
    :param format:
    :return:
    """
    # todo: errors
    if request.is_ajax() and request.method == 'POST':
        json_str = ((request.body).decode('utf-8'))
        received_json_data = json.loads(json_str)
        # print(received_json_data)
        # print(received_json_data["source"]["id"])
        order = Order.objects.get(pk=received_json_data["order_id"])
        order.source_obj = received_json_data["source"]
        order.source_id = received_json_data["source"]['id']
        order.save()
        return HttpResponse(200)


@login_required
def payment_received(request, template="payments/payment_received.html"):
    context = {
        "message":_("Your payment has been processed, and order is on the way soon.")
    }
    return TemplateResponse(request, template, context)


@login_required
def alipay_payment_received(request, template="payments/payment_received.html"):
    """
    This is a webhook.
    todo: errors
    :param request
    :param template:
    :return:
    """
    # todo: errors

    client_secret = request.GET.get('client_secret', '')
    source = request.GET.get('source', '')
    order = get_object_or_404(Order,source_id=source)
    # order = Order.objects.get(source_id=source)
    total = int(order.total * 100)
    # c = CurrencyRates()
    # # convert the CNY price to HKD
    # total = c.convert('CNY', 'HKD', order.total)
    # total = int(total * 100)
    try:
        charge = stripe.Charge.create(
            amount=total,
            currency='cny',
            source=source,
        )
        message = _('Your payment has been processed, and order is on the way soon.')
        link = None
    except:
        message = _("There was an error with your AliPay payment")
        link = reverse("payments:pay")
    # post-payment order processing
    order = payments_order_processor(request,order)
    order.save()
    context = {
        "total": order,
        "source": source,
        "message":message,
        "link":link
    }
    # delete the order's cookie
    response = redirect('payments:payment_received')
    response.delete_cookie("order_id")
    return response
    # return TemplateResponse(request, template, context)

