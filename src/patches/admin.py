from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
# from .models import Author, Book
from copy import deepcopy
from django.contrib import admin
from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.galleries.models import Gallery
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost
from cartridge.shop.models import Product, Order, DiscountCode
from cartridge.shop.admin import ProductAdmin, OrderAdmin, ProductVariationAdmin, DiscountCodeAdmin
from payments.utils import send_details_email, send_order_email
from django.utils.translation import ugettext as _




# author_extra_fieldsets = ((None, {"fields": ("dob",)}),)
#
# ###### CUSTOM ADMIN ######
#
# class BookInline(admin.TabularInline):
#     model = Book
#
# class AuthorAdmin(PageAdmin):
#     inlines = (BookInline,)
#     fieldsets = deepcopy(PageAdmin.fieldsets) + author_extra_fieldsets
#
# admin.site.register(Author, AuthorAdmin)


#### Blog post injections ###

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
# blog_fieldsets[0][1]["fields"].insert(-1, "image2")
# blog_fieldsets[0][1]["fields"].extend(["image2", "content2",
#                                        "image3", "content3",
#                                        "image4", "content4",
#                                        "image5", "content5",
#                                        "image6", "content6"])
blog_fieldsets[0][1]["fields"].insert(4,"frontpage")
blog_fieldsets[0][1]["fields"].insert(5,"blogpage")
blog_list_display = deepcopy(BlogPostAdmin.list_display)
blog_list_display.extend(['frontpage','blogpage'])
blog_list_editable = list(deepcopy(BlogPostAdmin.list_editable))
blog_list_editable.extend(['frontpage','blogpage'])


class MyBlogPostAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets
    list_display = blog_list_display
    list_editable = blog_list_editable

admin.site.unregister(BlogPost)  # must first unregister then register
admin.site.register(BlogPost, MyBlogPostAdmin)


# Product inline admin edits
# product_fieldsets = deepcopy(ProductAdmin.fieldsets)
# product_fieldsets[0][1]["fields"].extend(["member_price"
#                                        ])
# class MyProductAdmin(ProductAdmin):
#     # fieldsets = product_fieldsets
#     inlines +=

# admin.site.unregister(ProductAdmin)  # must first unregister then register
# admin.site.register(ProductAdmin, MyProductVariationAdmin)


#### product variation injections ####
variation_fields = ["sku", "num_in_stock", "price_hkd","unit_price",
                    "gold_member_price_hkd","gold_member_price_rmb",
                    "diamond_member_price_hkd","diamond_member_price_rmb",
                    "sale_price", "sale_from", "sale_to", "image"]
ProductVariationAdmin.fields = variation_fields

#### order injections ####
order_fieldsets = deepcopy(OrderAdmin.fieldsets)
order_fieldsets[0][1]["fields"].extend(["shipping_id", "shipping_url",
                                       ])
order_fieldsets[0][1]["fields"].extend(["paid","paid_time"])
order_list_display = list(deepcopy(OrderAdmin.list_display))
order_list_display.extend(["paid"])
class MyOrderAdmin(OrderAdmin):
    fieldsets = order_fieldsets
    list_display = order_list_display
    actions = ['send_order_email']

    def send_order_email(self,request,queryset):
        for order in queryset:
            send_order_email(request, order)
    send_order_email.short_description = _("Send user email with delivery information")



admin.site.unregister(Order)
admin.site.register(Order, MyOrderAdmin)


### Product injections ###
product_fieldsets = deepcopy(ProductAdmin.fieldsets)
product_fieldsets[0][1]["fields"].insert(4,"frontpage")
product_fieldsets[0][1]["fields"].insert(5,"frontbanner")
product_fieldsets[0][1]["fields"].insert(6,"shoppage")
product_fieldsets[0][1]["fields"].insert(7,"product_type")
# product_fieldsets[0][1]["fields"].insert(8,"is_class")
# product_fieldsets[0][1]["fields"].insert(9,"is_membership_level")
product_fieldsets[0][1]["fields"].extend(["num_sold","featured_image"])
product_list_display = deepcopy(ProductAdmin.list_display)
product_list_display.extend(['frontpage','frontbanner','shoppage']) #,'shoppage'
product_list_editable = list(deepcopy(ProductAdmin.list_editable))
product_list_editable.extend(['frontpage','frontbanner','shoppage']) # ,'shoppage'
class MyProductAdmin(ProductAdmin):
    fieldsets = product_fieldsets
    list_display = product_list_display
    list_editable = product_list_editable
admin.site.unregister(Product)
admin.site.register(Product, MyProductAdmin)


discount_code_fieldsets = deepcopy(DiscountCodeAdmin.fieldsets)
discount_code_fieldsets[0][1]["fields"] = list(discount_code_fieldsets[0][1]["fields"])
discount_code_fieldsets[0][1]["fields"].append("membership_level")
class MyDiscountCodeAdmin(DiscountCodeAdmin):
    fieldsets = discount_code_fieldsets
admin.site.unregister(DiscountCode)
admin.site.register(DiscountCode, MyDiscountCodeAdmin)