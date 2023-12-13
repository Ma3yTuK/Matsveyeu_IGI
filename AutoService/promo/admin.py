from django.contrib import admin
from . import models

class PromoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "is_active",
                "info"
            )
        }),
    )
    list_display = ("name", "is_active", "info")
    list_filter = ("is_active",)
    search_fields = ("name",)

admin.site.register(models.Promo, PromoAdmin)

# Register your models here.
