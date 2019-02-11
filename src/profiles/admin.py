from django.contrib import admin
from django.contrib.auth import get_user_model

from mezzanine.accounts.admin import ProfileInline
from mezzanine.accounts.admin import UserProfileAdmin
from profiles.models import Membership

# Register your models here.
#
# ProfileInline.template ="/admin/profiles_inline.html"
ProfileInline.min_num = 1

#### User Admin ####
#
User = get_user_model()

#### Membership Admin ####
class MembershipInline(admin.TabularInline):
    model = Membership
UserProfileAdmin.inlines += (MembershipInline,)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)