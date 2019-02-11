from django.conf.urls import url

from .views import email_received


urlpatterns = [
    url(r'^thanks/$', email_received, name='email_received'),
]