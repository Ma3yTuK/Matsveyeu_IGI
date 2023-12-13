from django.contrib import admin
from . import models

class VacancyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": (
                "name",
                "info"
            )
        }),
    ]
    list_display = ("name", "info")
    search_fields = ("name",)


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": (
                "question",
                "answer"
            )
        }),
    ]
    list_display = ("question",)
    search_fields = ("question",)


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": (
                "header",
                "body",
                "image",
            )
        }),
    ]
    list_display = ("header", "body", "image_tag")
    search_fields = ("header",)

class IntervalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": (
                "interval",
            )
        }),
    ]
    list_display = ("interval",)
    search_fields = ("interval",)


admin.site.register(models.Vacancy, VacancyAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Interval, IntervalAdmin)

# Register your models here.
