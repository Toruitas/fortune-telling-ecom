from django import forms
from django.utils.translation import ugettext_lazy as _



class ContactForm(forms.Form):
    """
    http://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html#crispy-tag-forms
    """
    from_email = forms.EmailField(required=True, label=_("Email"))
    name = forms.CharField(required=True, label=_("Name"))
    subject = forms.CharField(required=True, label=_("Subject"))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_("Message"))