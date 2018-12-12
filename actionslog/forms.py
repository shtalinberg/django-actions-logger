
from django import forms
from django.utils.functional import lazy

from . import settings as app_conf

def get_action_choices():
    return app_conf.LOG_ACTION_CHOICES

class LogActionForm(forms.ModelForm):
    # lots of fields like this
    action = forms.ChoiceField(choices=lazy(get_action_choices, list)())
