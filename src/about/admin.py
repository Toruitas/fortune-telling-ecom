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
from .models import Aboutpg, Employee, Terms, Privacy

###### CUSTOM ADMIN ######

class EmployeeInline(admin.TabularInline):
    model = Employee

extra_fieldsets = ((None, {"fields": ("content1","image1")}),)
extra_fieldsets_2 = ((None, {"fields": ("content",)}),)


class AboutpgAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + extra_fieldsets


class TermsAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + extra_fieldsets_2


class PrivacyAdmin(PageAdmin):
    fieldsets = deepcopy(PageAdmin.fieldsets) + extra_fieldsets_2

# blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
# blog_fieldsets[0][1]["fields"].insert(-1, "image2")
# blog_fieldsets[0][1]["fields"].extend(["image2", "content2",
#                                        "image3", "content3",
#                                        "image4", "content4",
#                                        "image5", "content5"])

# class MyBlogPostAdmin(BlogPostAdmin):
#     fieldsets = blog_fieldsets

admin.site.register(Aboutpg, AboutpgAdmin)
# admin.site.unregister(BlogPost)  # must first unregister then register
# admin.site.register(BlogPost, MyBlogPostAdmin)
admin.site.register(Terms, TermsAdmin)
admin.site.register(Privacy, PrivacyAdmin)
