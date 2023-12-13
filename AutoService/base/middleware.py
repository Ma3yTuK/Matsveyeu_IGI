import zoneinfo
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get("django_timezone")
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            try:
                timezone.activate(zoneinfo.ZoneInfo(request.user.timezone.name))
            except AttributeError:
                timezone.deactivate()
        return self.get_response(request)