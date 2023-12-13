from django import forms
from . import models
from promo.models import Promo
from django.db.models import QuerySet
from django.core import validators
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist


class PartsFilterForm(forms.Form):

    class DeviceChoice:

        def __init__(self, filter_form):
            self.filter_form = filter_form
            return super().__init__()

        def __call__(self):
            try:
                device_type = self.filter_form['devicetype'].value()
                if len(device_type) != 0:
                    return [ (value.id, value.name) for value in models.Device.objects.filter(devicetype__in=self.filter_form['devicetype'].value()) ]
            except AttributeError:
                pass
            return [ (value.id, value.name) for value in models.Device.objects.all() ]

    def device_type_choice():
        return  [ (value.id, value.name) for value in models.DeviceType.objects.all() ]

    def part_type_choice():
        return  [ (value.id, value.name) for value in models.PartType.objects.all() ]

    devices = forms.TypedMultipleChoiceField(coerce=int, empty_value=None, required=False) 
    devicetype = forms.TypedMultipleChoiceField(coerce=int, empty_value=None, required=False, choices=device_type_choice)
    parttype = forms.TypedMultipleChoiceField(coerce=int, empty_value=None, required=False, choices=part_type_choice)
    price_from = forms.IntegerField(required=False, validators=[validators.MinValueValidator(models.Part.MIN_PRICE), validators.MaxValueValidator(models.Part.MAX_PRICE)])
    price_to = forms.IntegerField(required=False, validators=[validators.MinValueValidator(models.Part.MIN_PRICE), validators.MaxValueValidator(models.Part.MAX_PRICE)])

    def __init__(self, *args, **kwargs):
        self.base_fields['devices'].choices = PartsFilterForm.DeviceChoice(self)
        super().__init__(*args, **kwargs)

    def get_results(self, queryset: QuerySet):
        cleaned_data = self.cleaned_data

        parttype=cleaned_data['parttype']
        if parttype != None:
            queryset = queryset.filter(parttype__in=parttype)
        devicetype=cleaned_data['devicetype']
        if devicetype != None:
            queryset = queryset.filter(devices__devicetype__in=devicetype)
        price_from=cleaned_data['price_from']
        if price_from != None:
            queryset = queryset.filter(price__gte=price_from)
        price_to=cleaned_data['price_to']
        if price_to != None:
            queryset = queryset.filter(price__lte=price_to)
        devices=cleaned_data['devices']
        if devices != None:
            queryset = queryset.filter(devices__in=devices)

        return queryset.distinct()


class PartsSearchForm(forms.Form):
    search = forms.CharField(max_length=128, required=False)

    def get_results(self, queryset: QuerySet):
        cleaned_data = self.cleaned_data

        search = cleaned_data['search']
        if search != None:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class PartsOrderForm(forms.Form):
    FIELDS = [
        "parttype",
        "name",
        "price",
    ]

    def get_order_choice():
        return [ (value, models.Part._meta.get_field(value).verbose_name) for value in PartsOrderForm.FIELDS ]

    order = forms.ChoiceField(required=False, choices=get_order_choice)

    def get_results(self, queryset: QuerySet):
        cleaned_data = self.cleaned_data

        order = cleaned_data['order']
        if order != '':
            queryset = queryset.order_by(order)
        return queryset


class ServiceFilterForm(forms.Form):

    def service_type_choice():
        return  [ (value.id, value.name) for value in models.ServiceType.objects.all() ]

    def device_type_choice():
        return  [ (value.id, value.name) for value in models.DeviceType.objects.all() ]

    def part_type_choice():
        return  [ (value.id, value.name) for value in models.PartType.objects.all() ]

    servicetype = forms.TypedMultipleChoiceField(coerce=int, empty_value=None, required=False, choices=service_type_choice)
    devicetype = forms.TypedMultipleChoiceField(coerce=int, empty_value=None, required=False, choices=device_type_choice)
    parttype = forms.TypedMultipleChoiceField(coerce=int, empty_value=None, required=False, choices=part_type_choice)
    price_from = forms.IntegerField(required=False, validators=[validators.MinValueValidator(models.Service.MIN_PRICE), validators.MaxValueValidator(models.Service.MAX_PRICE)])
    price_to = forms.IntegerField(required=False, validators=[validators.MinValueValidator(models.Service.MIN_PRICE), validators.MaxValueValidator(models.Service.MAX_PRICE)])

    def get_results(self, queryset: QuerySet):
        cleaned_data = self.cleaned_data

        parttype=cleaned_data['parttype']
        if parttype != None:
            queryset = queryset.filter(parttype__in=parttype)
        devicetype=cleaned_data['devicetype']
        if devicetype != None:
            queryset = queryset.filter(devicetype__in=devicetype)
        price_from=cleaned_data['price_from']
        if price_from != None:
            queryset = queryset.filter(price__gte=price_from)
        price_to=cleaned_data['price_to']
        if price_to != None:
            queryset = queryset.filter(price__lte=price_to)
        servicetype=cleaned_data['servicetype']
        if servicetype != None:
            queryset = queryset.filter(servicetype__in=servicetype)

        return queryset.distinct()
        

class ServiceSearchForm(forms.Form):
    search = forms.CharField(max_length=128, required=False)

    def get_results(self, queryset: QuerySet):
        cleaned_data = self.cleaned_data

        search = cleaned_data['search']
        if search != None:
            queryset = queryset.filter(servicetype__name__icontains=search)
        return queryset


class ServiceOrderForm(forms.Form):
    FIELDS = [
        "parttype",
        "servicetype",
        "devicetype",
        "price",
    ]

    def get_order_choice():
        return [ (value, models.Part._meta.get_field(value).verbose_name) for value in PartsOrderForm.FIELDS ]

    order = forms.ChoiceField(required=False, choices=get_order_choice)

    def get_results(self, queryset: QuerySet):
        cleaned_data = self.cleaned_data
        
        order = cleaned_data['order']
        if order != '':
            queryset = queryset.order_by(order)
        return queryset


class CartPromoForm(forms.Form):
    error_messages = {
        'promo_invalid': _("No such promo"),
    }

    promo = forms.CharField(label="Promo code", max_length=16, required=False)

    def clean(self):
        super().clean()
        if len(self.get_promo()) == 0:
            return
        try:
            Promo.objects.get(name=self.get_promo())
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages['promo_invalid'],
                code='promo_invalid',
            )

    def get_promo(self):
        try:
            return self.cleaned_data["promo"]
        except (AttributeError, KeyError):
            return self.get_initial_for_field(self.fields["promo"], "promo")


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["header", "body", "mark"]
        help_texts = {
            'header': 'Review theme',
            "body": 'Reviw',
            "mark": 'Mark',
        }
