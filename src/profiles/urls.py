from django.conf.urls import url
from mezzanine.conf import settings

from .views import user_profile_view, signup_view, change_membership_view, membership_confirm, \
    update_email_view, update_address_view, update_birthday_view, update_orientation_view


ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL",
                     "/%s/signup/" % ACCOUNT_URL.strip("/"))

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash),
        signup_view, name="signup"),
    url(r'^$', user_profile_view, name='profile'),
    url(r'^update/email/$', update_email_view, name='update_email'),
    # url(r'^update/address/$', update_address_view, name='update_address'),
    url(r'^update/birthday/$', update_birthday_view, name='update_birthday'),
    url(r'^update/orientation/$', update_orientation_view, name='update_orientation'),
    url(r'^upgrade/$', change_membership_view, name='upgrade'),
    url(r'^upgrade/(?P<level>\w+)/$', membership_confirm, name='membership_confirm'),
    # url(r'^test-revoke/$',test_aws_revoke, name="test_revoke")
    # url(r'^upgrade/pay/', pay_for_membership_view, name='pay_for_membership'),
]