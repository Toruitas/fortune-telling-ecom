from cartridge.shop.models import Product, ProductVariation
from django.db import models

#### override Product.copy_default_variation ####
# since the version from Priced just checks prices on itself, not any injected ones
# double check with GOOGLE first

# def copy_price_fields_to_product_monkey(self, obj_to):
#     """
#     Copies each of the fields for the ``Priced`` model from one
#     instance to another. Used for synchronising the denormalised
#     fields on ``Product`` instances with their default variation.
#     """
#     for field in Product._meta.fields:
#         if not isinstance(field, models.AutoField):
#             setattr(obj_to, field.name, getattr(self, field.name))
#     obj_to.save()
#
# def copy_default_variation_monkey(self):
#     """
#     Copies the price and image fields from the default variation
#     when the product is updated via the change view.
#     """
#     default = self.variations.get(default=True)
#     default.copy_price_fields_to_product_monkey(self)
#     if default.image:
#         self.image = default.image.file.name
#     self.save()
#
# Product.copy_default_variation = copy_default_variation_monkey

