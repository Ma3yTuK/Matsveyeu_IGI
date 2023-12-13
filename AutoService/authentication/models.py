from django.db import models
from django.contrib.auth.models import AbstractUser
from polls.models import Cart, Role, TimeZone
from django.utils.timezone import get_current_timezone_name
from django.db import DEFAULT_DB_ALIAS
from . import validators
from base.forms import TimeZoneForm
import zoneinfo
from django.utils.html import mark_safe


MODELS_MEDIA="authentication/models/"

class User(AbstractUser):
    MODELS_MEDIA_USERS = MODELS_MEDIA+"users"
    DEFAULT_USER_IMAGE = MODELS_MEDIA_USERS + '/default.jpg'

    def timezone_default():
        return TimeZone.objects.get(name=get_current_timezone_name()).id

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    timezone = models.ForeignKey(TimeZone, on_delete=models.SET_DEFAULT, default=timezone_default)
    number = models.CharField(verbose_name="Phone number", max_length=9, unique=True, validators=[validators.NumberValidator()])
    image = models.ImageField(upload_to=MODELS_MEDIA_USERS, default=DEFAULT_USER_IMAGE)

    def image_tag(self):
        if self.image != None:
            return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))
    image_tag.short_description = 'Image'
    
    def setup(self):
        self.cart = Cart()
        self.cart.save()

    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        if self._state.adding:
            self.setup()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def delete(self, *args, **kwargs):
        self.cart.delete()
        return super().delete(*args, **kwargs)