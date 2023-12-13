from django.db import models
import marshal
from . import apply_functions
from . import is_valid_functions
from django import forms
from django.utils.translation import gettext as _


class Promo(models.Model):
    error_messages = {
        "No data": _("Can't get promo data"),
    }

    id = models.BigAutoField(verbose_name="promo id", primary_key=True)
    name = models.CharField(verbose_name="promo code", max_length=16, unique=True)
    is_active = models.BooleanField(default=True)
    info = models.TextField(verbose_name="description", max_length=1024, null=True, blank=True)

    def apply(self, order):
        return getattr(apply_functions, "promo_"+self.name)(order)

    def is_valid(self, order):
        return getattr(is_valid_functions, "promo_"+self.name)(order)

    def clean(self):
        if getattr(apply_functions, "promo_"+self.name, None) == None or getattr(is_valid_functions, "promo_"+self.name, None) == None:
            raise forms.ValidationError(
                self.error_messages["No data"],
                code="No data",
            )

    def __str__(self):
        return self.name

# Create your models here.
