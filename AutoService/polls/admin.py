from django.contrib import admin
from . import models


class JobToOrderInline(admin.TabularInline):
    fieldsets = (
        ("Many-to-One", {
            "fields": (
                "service",
                "order",
                "device",
                "part",
            )
        }),
    )
    model = models.Job
    fk_name = "order"
    extra = 3


class CartAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Many-to-one", {
            "fields": (
                "promo",
            ),
        }),
    ]
    list_display = ("user", "order", "promo")


class RoleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": (
                "name",
            )
        }),
    ]
    list_display = ("name",)
    search_fields = ("name",)


class DeviceTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": (
                "name",
            )
        }),
    ]
    list_display = ("name",)
    search_fields = ("name",)


class ServiceTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "part_required",
            ),
        }),
    )
    list_display = ("name", "part_required")
    list_filter = ("part_required",)
    search_fields = ("name",)


class PartTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
            ),
        }),
    )
    list_display = ("name",)
    search_fields = ("name",)


class MasterTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Many-to-one", {
            "fields": (
                "servicetype",
                "devicetype",
            ),
        }),
    )
    list_display = ("id", "servicetype", "devicetype")
    list_filter = ("servicetype__name", "devicetype__name")
    search_fields = ("id", "servicetype__name", "devicetype__name")
   

class DeviceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
            ),
        }),
        ("Many-to-One", {
            "fields": (
                "devicetype",
            )
        }),
    )
    list_display = ("name", "devicetype")
    list_filter = ("devicetype__name",)
    search_fields = ("name", "devicetype__name")


class ServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "price",
                "duration",
            ),
        }),
        ("Many-to-one", {
            "fields": (
                "servicetype",
                "devicetype",
                "parttype",
            )
        }),
    )
    list_display = ("id", "price", "duration", "servicetype", "devicetype", "parttype")
    list_filter = ("servicetype__name", "devicetype__name", "parttype__name") 
    search_fields = ("id", "price", "duration", "servicetype__name", "devicetype__name", "parttype__name")


class MasterAdmin(admin.ModelAdmin):
    fieldsets = (
        ("One-to-One", {
            "fields": (
                "user",
            )
        }),
        ("Many-to-Many", {
            "fields": (
                "mastertypes",
            )
        }),
    )
    list_display = ("user",)
    search_fields = ("user__username",)


class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
            ),
        }),
    )
    list_display = ("name",)
    search_fields = ("name",)


class PartAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "price",
                "image",
                "info",
            ),
        }),
        ("Many-to-One", {
            "fields": (
                "parttype",
            )
        }),
        ("Many-to-Many", {
            "fields": (
                "devices",
            )
        }),
    )
    list_display = ("name", "price", "parttype", "image_tag")
    list_filter = ("parttype__name",)
    search_fields = ("name", "price", "parttype__name")


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "info",
                "processing",
                "datetime",
            ),
        }),
        ("Many-to-One", {
            "fields": (
                "user",
                "promo",
            )
        }),
        ("Many-to-Many", {
            "fields": (
                "parts",
            )
        }),
    )
    inlines = (JobToOrderInline,)
    list_display = ("id", "price", "user", "info", "promo", "processing", "datetime")
    list_filter = ("user__username", "datetime")
    search_fields = ("id", "price", "user__username", "info", "promo__name")


class JobAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Many-to-One", {
            "fields": (
                "service",
                "order",
                "device",
                "part",
            )
        }),
    )
    list_display = ("id", "datetime", "service", "master", "order", "device", "part")
    list_filter = ("datetime", "service__id", "master__id", "order__id", "device__id", "part__id")
    search_fields = ("id", "datetime", "service__id", "master__id", "order__id", "device__id", "part__id")


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.DeviceType, DeviceTypeAdmin)
admin.site.register(models.ServiceType, ServiceTypeAdmin)
admin.site.register(models.PartType, PartTypeAdmin)
admin.site.register(models.MasterType, MasterTypeAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Master, MasterAdmin)
admin.site.register(models.Part, PartAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Job, JobAdmin)



# Register your models here.
