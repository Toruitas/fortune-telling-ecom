from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _



# Create your views here.
def test_app(request):
    context = {"yes":"worked"}
    return render(request,"test_mez/test_view.html",context)


def email_received(request):
    context = {"title":_("Thanks for the email"),
               "meta_title": _("Thanks for the email")}
    return TemplateResponse(request,"about/thanks.html",context)