"""
Form should have... birthday, including time if possible. Have that part be optional. Prefill 00:00:000
Name
Year, month, day, hour, minute, second
"""
from datetime import date
from django.utils import timezone
from django import forms
# from .custom_widgets import SplitSelectDateTimeWidgetA, SplitSelectDateTimeWidgetB
from django.utils.translation import ugettext_lazy as _


class FortuneForm(forms.Form):
    """
    need initial fill in for bday field, do in view. Get birthday from user model if in there.
    http://stackoverflow.com/questions/14015426/formatting-timefield
    http://stackoverflow.com/questions/11959789/how-to-work-with-time-picker-widget-in-django-template
    http://stackoverflow.com/questions/6622341/is-there-a-selectdatetime-widget-for-django-forms
    https://djangosnippets.org/snippets/1206/
    https://www.djangosnippets.org/snippets/1202/
    https://github.com/sean-wallace/django-select-time-widget/blob/master/select_time_widget.py
    http://jonthornton.github.io/jquery-timepicker/
    http://stackoverflow.com/questions/5827590/css-styling-in-django-forms
    http://stackoverflow.com/questions/7729523/timefield-format-in-django-template
    http://stackoverflow.com/questions/26741213/set-input-to-am-pm-in-django-timefield
    http://stackoverflow.com/questions/2913700/django-forms-timefield-validation
    """
    year = date.today().year
    now = timezone.now()
    sex = forms.ChoiceField(choices=(("male", _("Male")),
                                     ("female", _("Female"))),
                            widget=forms.RadioSelect,
                            label=_("Gender"))
    # birthday = forms.SplitDateTimeField(widget=SplitSelectDateTimeWidgetA(years=[y for y in range(year, 1900, -1)]),
    #                                     )
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=[y for y in range(year, 1900, -1)]),
                               label=_("Birthday"))
    birthtime = forms.TimeField(initial=now,widget=forms.TimeInput(attrs={'class':'timepicker'}), input_formats=["%I:%M%p"],
                                label=_("Birth Time"))  # YEAH!