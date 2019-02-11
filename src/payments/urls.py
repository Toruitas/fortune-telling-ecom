from django.conf.urls import url

from .views import pay, ajax_get_source_id, alipay_payment_received,payment_received


urlpatterns = [
    url(r'^pay/(?P<order_id>\d+)$', pay, name='pay'),
    url(r'^pay/$', pay, name='pay'),
    url(r'^ajax_get_source_id/$', ajax_get_source_id, name='ajax_get_source_id'),
    url(r'^alipay_payment_received/$', alipay_payment_received, name='alipay_payment_received'),
    url(r'^payment_received/$', payment_received, name='payment_received'),
]