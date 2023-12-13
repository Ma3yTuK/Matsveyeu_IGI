from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("image_tag", "role")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["number", "timezone", "image", "role"]}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["number", "timezone", "image", "role"]}),)

admin.site.register(models.User, CustomUserAdmin)

# Register your models here.
