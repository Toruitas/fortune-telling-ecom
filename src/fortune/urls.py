from django.conf.urls import url
from mezzanine.conf import settings

from .views import fortune_view, fortune_display_view, prayers_view


urlpatterns = [
    url(r'^prayers/$', prayers_view, name='prayers'),
    # url(r'^upgrade/pay/', pay_for_membership_view, name='pay_for_membership'),
    url(r'^fortune/$', fortune_view, name='fortune'),
]