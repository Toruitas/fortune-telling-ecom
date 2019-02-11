from __future__ import unicode_literals
from future.builtins import str
from mezzanine.conf import settings

from decimal import Decimal
import locale
import platform

from django import template

# from cartridge.shop.utils import set_locale
from babel.numbers import format_currency


register = template.Library()


def _order_totals(context):
    """
    Add shipping/tax/discount/order types and totals to the template
    context. Use the context's completed order object for email
    receipts, or the cart object for checkout.
    """
    fields = ["shipping_type", "shipping_total", "discount_total",
              "tax_type", "tax_total"]
    if "order" in context:
        for field in fields + ["item_total"]:
            context[field] = getattr(context["order"], field)
    else:
        context["item_total"] = context["request"].cart.total_price()
        if context["item_total"] == 0:
            # Ignore session if cart has no items, as cart may have
            # expired sooner than the session.
            context["tax_total"] = 0
            context["discount_total"] = 0
            context["shipping_total"] = 0
        else:
            for field in fields:
                context[field] = context["request"].session.get(field, None)
        context["order_total"] = context.get("item_total", None)
    # get user, do math
    # u = context['request'].user
    # if u.is_authenticated(): # check for authentication
    #     if u.membership.level == 'gold':
    #         context["discount_total"] = (context.get('item_total', None) * Decimal(settings.MEMBERSHIP_DISCOUNT_DECIMAL))
    #     # Add membership discount to discount
    if context.get("shipping_total", None) is not None:
        context["order_total"] += Decimal(str(context["shipping_total"]))
    if context.get("discount_total", None) is not None:
        context["order_total"] -= Decimal(str(context["discount_total"]))
    if context.get("tax_total", None) is not None:
        context["order_total"] += Decimal(str(context["tax_total"]))
    return context

#
# @register.inclusion_tag("shop/includes/order_totals.html", takes_context=True)
# def order_totals_patch(context):
#     """
#     HTML version of order_totals.
#     """
#     return _order_totals(context)
#
# def _product_member_price(context):
#     pass
#
# @register.inclusion_tag("pages/shop.html")
# def product_member_price(context):
#     pass


@register.filter
def currency_2(value):
    """
    Format a value as currency according to locale.
    """
    # set_locale()

    en_HK_locale ={'decimal_point': '.',
                   'thousands_sep': ',',
                   'int_curr_symbol': 'HKD ',
                   'negative_sign': '-',
                   'currency_symbol': 'HK$',
                   'p_sep_by_space': 0,
                   'frac_digits': 2,
                   'mon_thousands_sep': ',',
                   'n_sign_posn': 0,
                   'positive_sign': '',
                   'int_frac_digits': 2,
                   'n_cs_precedes': 1,
                   'p_cs_precedes': 1,
                   'grouping': [3, 0],
                   'p_sign_posn': 1,
                   'mon_grouping': [3, 0],
                   'n_sep_by_space': 0,
                   'mon_decimal_point': '.'}


    zh_CN_locale = {'decimal_point': '.',
                    'thousands_sep': ',',
                    'int_curr_symbol': 'CNY ',
                    'negative_sign': '-',
                    'currency_symbol': '￥',
                    'p_sep_by_space': 0,
                    'frac_digits': 2,
                    'mon_thousands_sep': ',',
                    'n_sign_posn': 4,
                    'positive_sign': '',
                    'int_frac_digits': 2,
                    'n_cs_precedes': 1,
                    'p_cs_precedes': 1,
                    'grouping': [3, 0],
                    'p_sign_posn': 4,
                    'mon_grouping': [3, 0],
                    'n_sep_by_space': 0,
                    'mon_decimal_point': '.'}


    if not value:
        value = 0
    # value = locale.currency(Decimal(value), grouping=True)
    # if platform.system() == 'Windows':
    #     try:
    #         value = str(value, encoding=locale.getpreferredencoding())
    #     except TypeError:
    #         pass
    value = format_currency(value,'CNY',locale='zh_CN')
    # value = format_currency(value,'HKD',locale='zh_HK')
    return value