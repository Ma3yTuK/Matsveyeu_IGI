from . import forms

def timezone_form(request):
    return {
        "timezone_form": forms.TimeZoneForm(),
    }