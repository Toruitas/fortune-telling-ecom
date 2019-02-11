from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from mezzanine.conf import settings

from cartridge.shop.checkout import CheckoutError

import stripe


def process(request, order_form, order):
    """
    Depending on the tokens, etc submitted, processes using different methods

    https://developers.braintreepayments.com/start/hello-client/javascript/v3
    https://github.com/braintree/braintree_flask_example/tree/master/templates/checkouts

    :param request:
    :param order_form:
    :param order:
    :return:
    """
    #STRIPE
    # if request.POST.get('stripeToken'):
    #     stripe.api_key = settings.STRIPE_API_KEY
    #     token = request.POST.get('stripeToken')
    #
    #     data = {
    #         "amount": int((order.total * 100).to_integral()),
    #         "currency": getattr(settings, "STRIPE_CURRENCY", "usd"),
    #         "source":token,
    #     }
    #     if request.POST.get('payment_type') == 'card':
    #         data.update({})
    #     elif request.PSOT.get('payment_type') == 'alipay':
    #         pass
    #
    #     try:
    #         response = stripe.Charge.create(**data)
    #     except stripe.CardError:
    #         raise CheckoutError(_("Transaction declined"))
    #     except Exception as e:
    #         raise CheckoutError(_("A general error occured: ") + str(e))
    #     return response.id
    # # PAYPAL
    # if paypal:
    #     paypal_dict = {
    #         "business": "receiver_email@example.com",
    #         "amount": "10000000.00",
    #         "item_name": "name of the item",
    #         "invoice": "unique-invoice-id",
    #         "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
    #         "return_url": "https://www.example.com/your-return-location/",
    #         "cancel_return": "https://www.example.com/your-cancel-location/",
    #         "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    #     }
    #
    #     # Create the instance.
    #     form = PayPalPaymentsForm(initial=paypal_dict)
    #     context = {"form": form}

    # https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
    # https://developer.paypal.com/webapps/developer/docs/classic/paypal-payments-standard/integration-guide/cart_upload/

