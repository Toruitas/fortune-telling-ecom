from datetime import date
from decimal import Decimal

from django.db import models
from mezzanine.pages.models import Page, PageMoveException
from django.db.models import CharField, Q, F
from django.utils.translation import (ugettext, ugettext_lazy as _,
                                      pgettext_lazy as __)
from cartridge.shop.models import Cart, ProductVariation, Order
from mezzanine.conf import settings




# Create your models here.
# The members of Page will be inherited by the Author model, such
# as title, slug, etc. For authors we can use the title field to
# store the author's name. For our model definition, we just add
# any extra fields that aren't part of the Page model, in this
# case, date of birth.


# class Author(Page):
#     dob = models.DateField("Date of birth")
#     trivia = models.TextField("Trivia")
#
#     def can_add(self, request):
#         return self.children.count() == 0
#
#     def can_delete(self, request):
#         return request.user.is_superuser or self.parent is not None
#
#     def can_move(self, request, new_parent):
#         if new_parent is None:
#             msg = 'An author page cannot be a top-level page'
#             raise PageMoveException(msg)
#
#
# class Book(models.Model):
#     author = models.ForeignKey("Author")
#     title = models.CharField(null=False, blank=False, max_length=120)
#     cover = models.ImageField(upload_to="authors")
#     date_published = models.DateField("Date published", default=date.today)


def calculate_discount_patch(self, discount):
        """
        Calculates the discount based on the items in a cart, some
        might have the discount, others might not.
        Original works for 1 code
        """
        # Discount applies to cart total if not product specific.
        products = discount.all_products()
        print("calc discount patch")
        if products.count() == 0:
            return discount.calculate(self.total_price())
        total = Decimal("0")
        # Create a list of skus in the cart that are applicable to
        # the discount, and total the discount for appllicable items.
        lookup = {"product__in": products, "sku__in": self.skus()}
        discount_variations = ProductVariation.objects.filter(**lookup)
        discount_skus = discount_variations.values_list("sku", flat=True)
        for item in self:
            if item.sku in discount_skus:
                total += discount.calculate(item.unit_price) * item.quantity
        return total

Cart.calculate_discount_patch = calculate_discount_patch


def total_price_gold(self):
    """
    Template helper function - sum of all costs of item quantities.
    """
    return sum([item.total_price for item in self])

Cart.total_price_gold = total_price_gold


def total_price_diamond(self):
    """
    Template helper function - sum of all costs of item quantities.
    """
    return sum([item.total_price for item in self])

Cart.total_price_diamond = total_price_diamond

Order.billing_detail_postcode = CharField(_("Postcode"), max_length=10, null=True, blank=True)
Order.shipping_detail_postcode = CharField(_("Postcode"), max_length=10, null=True, blank=True)
