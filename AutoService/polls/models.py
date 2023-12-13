from django.db import models
from django.core import validators
from django.contrib import admin
from django.db.models import F, Sum
from django.db import DEFAULT_DB_ALIAS
from DreamService import settings
from django.utils.html import mark_safe
from datetime import timedelta
from promo.models import Promo
from django.utils.translation import gettext as _
import zoneinfo
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django import forms


MODELS_MEDIA="polls/models/"

class TimeZone(models.Model):
    id = models.BigAutoField(verbose_name="zone id", primary_key=True)
    name = models.CharField(verbose_name="time zone", max_length=32, unique=True)

    def generate():
        TimeZone.objects.all().delete()
        for timezone_name in zoneinfo.available_timezones():
            TimeZone(name=timezone_name).save()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
   

class Role(models.Model):
    id = models.BigAutoField(verbose_name="role id", primary_key=True)
    name = models.CharField(verbose_name="role", max_length=64, unique=True)

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    id = models.BigAutoField(verbose_name="device type id", primary_key=True)
    name = models.CharField(verbose_name="device type", max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    id = models.BigAutoField(verbose_name="service type id", primary_key=True)
    name = models.CharField(verbose_name="service type", max_length=64, unique=True)
    part_required = models.BooleanField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PartType(models.Model):
    id = models.BigAutoField(verbose_name="service type id", primary_key=True)
    name = models.CharField(verbose_name="part type", max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MasterType(models.Model):
    id = models.BigAutoField(verbose_name="master id", primary_key=True)
    servicetype = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    devicetype = models.ForeignKey(DeviceType, on_delete=models.CASCADE)

    class Meta:
        ordering = ["servicetype"]

    def __str__(self):
        return "Master type " + str(self.id)


class Device(models.Model):
    MODELS_MEDIA_DEVICES = MODELS_MEDIA+"devices"

    id = models.BigAutoField(verbose_name="master id", primary_key=True)
    devicetype = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="device", max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    MIN_PRICE = 0
    MAX_PRICE = 9999999

    MIN_DURATION = 0
    MAX_DURATION = 2400

    id = models.BigAutoField(verbose_name="service id", primary_key=True)
    servicetype = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    devicetype = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    parttype = models.ForeignKey(PartType, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(validators=[validators.MinValueValidator(MIN_PRICE), validators.MaxValueValidator(MAX_PRICE)])
    duration = models.IntegerField(validators=[validators.MinValueValidator(MIN_DURATION), validators.MaxValueValidator(MAX_DURATION)])

    class Meta:
        ordering = ["servicetype"]
    
    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if update_fields == None or "price" in update_fields:
            for job in self.job_set.all():
                job.order.save(force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=("price",))
        
    def __str__(self):
        return self.servicetype.name + ' for ' + self.devicetype.name


class Master(models.Model):
    MASTER_ROLE_NAME = "master"

    id = models.BigAutoField(verbose_name="master id", primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mastertypes = models.ManyToManyField(MasterType)

    class Meta:
        ordering = ["user__username"]

    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        self.user.role = Role.objects.get(name=Master.MASTER_ROLE_NAME)
        self.user.save()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        
    def __str__(self):
        return self.user.username


class Part(models.Model):
    MODELS_MEDIA_PARTS = MODELS_MEDIA+"parts"

    MIN_PRICE = 0
    MAX_PRICE = 9999999

    id = models.BigAutoField(verbose_name="part id", primary_key=True)
    devices = models.ManyToManyField(Device)
    parttype = models.ForeignKey(PartType, verbose_name="Part type", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Part name", max_length=64, unique=True)
    price = models.IntegerField(verbose_name="Price", validators=[validators.MinValueValidator(MIN_PRICE), validators.MaxValueValidator(MAX_PRICE)])
    image = models.ImageField(upload_to=MODELS_MEDIA_PARTS)
    info = models.TextField(verbose_name="Additional info", max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))
    image_tag.short_description = 'Image'
    
    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if update_fields == None or "price" in update_fields:
            for order in self.order_set.all():
                order.save(force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=("price",))

    def delete(self, using=DEFAULT_DB_ALIAS, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

    def __str__(self):
        return self.name


class Order(models.Model):
    error_messages = {
        'promo_requirements_not_met': _("Promo requirements are not met"),
    }

    id = models.BigAutoField(verbose_name="order id", primary_key=True)
    datetime = models.DateTimeField(verbose_name="Date and time", blank=True, null=True)
    info = models.TextField(max_length=1024, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField(editable=False, default=0)
    parts = models.ManyToManyField(Part)
    processing = models.BooleanField(default=True)

    class Meta:
        ordering = ["datetime"]

    def calculate_price(self):
        price = 0
        for job in Job.objects.filter(order=self.id):
            price += job.service.price
        for part in self.parts.all():
            price += part.price
        if self.promo != None and self.promo.is_valid(self):
            price -= self.promo.apply(self)
        return int(price)

    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        if self.datetime == None and not self.processing:
            self.datetime = timezone.now()
            if not self._state.adding:
                for job in self.job_set.all():
                    job.setup()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        self.price = self.calculate_price()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return "Order " + str(self.id)


class Job(models.Model):
    error_messages = {
        'no_such_master': _("Suitable master not found"),
        'no_such_part_in_order': _("There is no such part in the order"),
        'not_suitable_part': _("Part is not compatible with device"),
        'part_required': _("Part is required for this service"),
        'part_not_required': _("Part is not required for this service"),
    }

    id = models.BigAutoField(verbose_name="job id", primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, editable=False, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(verbose_name="Date and time", editable=False, null=True)

    class Meta:
        ordering = ["datetime"]

    def clean(self):
        masters = Master.objects.filter(mastertypes__servicetype=self.service.servicetype, mastertypes__devicetype=self.service.devicetype).distinct()
        if not masters:
            raise forms.ValidationError(
                self.error_messages['no_such_master'],
                code='no_such_master',
            )
        if self.part != None:
            if not self.service.servicetype.part_required:
                raise forms.ValidationError(
                        self.error_messages['part_not_required'],
                        code='part_not_required',
                    )
            if self.part.devices:
                try:
                    self.part.devices.get(id=self.device.id)
                except ObjectDoesNotExist:
                    forms.ValidationError(
                        self.error_messages['not_suitable_part'],
                        code='not_suitable_part',
                    )
            else:
                raise forms.ValidationError(
                    self.error_messages['not_suitable_part'],
                    code='not_suitable_part',
                )
        elif self.service.servicetype.part_required:
            raise forms.ValidationError(
                    self.error_messages['part_required'],
                    code='part_required',
                )

    def setup(self):
        if self.service.duration == 0:
            return

        mastertypes = MasterType.objects.filter(servicetype=self.service.servicetype, devicetype=self.service.devicetype)
        masters = Master.objects.filter(mastertypes__in=mastertypes)
        jobs = Job.objects.filter(datetime__gt=timezone.now(), master__in=masters)

        job_dict = {}
        duration = timedelta(hours=self.service.duration)
        checked_masters_counter = 0

        if not jobs:
            self.datetime = timezone.now()
            self.master = Master.objects.filter(mastertypes__servicetype=self.service.servicetype, mastertypes__devicetype=self.service.devicetype).first()
            return

        self.datetime = jobs.latest("datetime").datetime + timedelta(hours=Service.MAX_DURATION)

        for job in jobs:
            if job.master not in job_dict:
                job_dict[job.master] = [self.datetime]
            elif job_dict[job_master][-1] == None:
                continue

            possible_datetime = job_dict[job.master][-1].datetime + duration

            if possible_datetime <= job.datetime:
                if possible_datetime < self.datetime:
                    self.master = job.master
                    self.datetime = possible_datetime
                if checked_masters_counter == 0:
                    checked_masters_counter += 1

            if checked_masters_counter == len(masters):
                return

            if checked_masters_counter > 0:
                checked_masters_counter += 1
                job_dict[job_master].append(None)
            else:
                job_dict[job.master].append(job)

        for master in masters:
            if master in job_dict:
                if job_dict[master][-1] != None:
                    possible_datetime = job_dict[master][-1].datetime + duration
                else:
                    possible_datetime = job_dict[master][-2].datetime + duration
                if possible_datetime < self.datetime:
                    self.master = master
                    self.datetime = possible_datetime

    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        if self._state.adding and not self.order.processing:
            self.setup()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return "Job " + str(self.id)


class Cart(models.Model):
    error_messages = {
        'promo_requirements_not_met': _("Promo requirements are not met"),
    }

    def create_order():
        order = Order()
        order.save()
        return order

    id = models.BigAutoField(verbose_name="cart id", primary_key=True)
    order = models.OneToOneField(Order, editable=False, on_delete=models.SET_NULL, null=True)
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.order == None:
            self.order = Cart.create_order()
            self.save()

    def promo_invalid(self):
        if self.promo != None and not self.promo.is_valid(self.order):
            return True
        return False

    def calculate_price(self):
        price = self.order.calculate_price()
        if self.promo != None and self.promo.is_valid(self.order):
            price -= self.promo.apply(self.order)
        return int(price)

    def make_order(self):
        self.order.processing = False
        if not self.promo_invalid():
            self.order.promo = self.promo
        self.order.user = self.user
        self.order.save()
        self.order = Cart.create_order()
        self.save()

    def clean(self):
        return self.order.clean()
    
    def save(self, force_insert=False, force_update=False, using=DEFAULT_DB_ALIAS, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        self.order.save()

    def __str__(self):
        return "Cart " + str(self.id)


class Review(models.Model):
    MIN_MARK = 0
    MAX_MARK = 5

    id = models.BigAutoField(verbose_name="review id", primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    header = models.CharField(max_length=32)
    body = models.TextField()
    mark = models.IntegerField(validators=[validators.MinValueValidator(MIN_MARK), validators.MaxValueValidator(MAX_MARK)])

    class Meta:
        ordering = ["-mark"]


# Create your models here

