from django.http import HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for
from .models import Aboutpg
from .forms import ContactForm
from django.shortcuts import redirect
from mezzanine.utils.email import send_mail_template
from django.contrib.messages import info, error
from mezzanine.conf import settings
from django.utils.translation import ugettext_lazy as _


@processor_for(Aboutpg)
def about_pg(request,page):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST or None)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            # Form processing goes here.
            context={"from_email":from_email,
                     "name":name,
                     "message":message,
                     "subject":subject,
                     "request":request}
            send_mail_template("About pg contact form submission | {}".format(subject), "email/thanks",
                               settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_RECEIVE_EMAIL,
                               context=context)
            # # info(request, _(""))
            return redirect("email_received")
    return {"form": form}