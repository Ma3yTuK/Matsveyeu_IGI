from django import forms
from . import models
from django.contrib.auth import authenticate
from polls.models import TimeZone
from django.utils.translation import gettext as _
from django.utils.timezone import get_current_timezone_name
import zoneinfo

class TimeZoneForm(forms.Form):
    def timezone_choice():
        return [ (value.name, value.name) for value in TimeZone.objects.all() ]
    
    timezone = forms.TypedChoiceField(label="Time zone", coerce=TimeZone, choices=timezone_choice, initial=get_current_timezone_name)