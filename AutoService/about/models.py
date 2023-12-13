from django.db import models
from django.utils.html import mark_safe
from django.core import validators


MODELS_MEDIA="about/models/"

class Vacancy(models.Model):
    id = models.BigAutoField(verbose_name="promo id", primary_key=True)
    name = models.CharField(verbose_name="vacancy", max_length=16, unique=True)
    info = models.TextField(verbose_name="description", max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "vacancies"

class Interval(models.Model):
    id = models.BigAutoField(verbose_name="promo id", primary_key=True)
    interval = models.IntegerField(validators=[validators.MinValueValidator(2000), validators.MaxValueValidator(2000000)])


class Question(models.Model):
    id = models.BigAutoField(verbose_name="promo id", primary_key=True)
    question = models.CharField(max_length=64, unique=True)
    answer = models.TextField(max_length=1024)

    def __str__(self):
        return self.question


class Article(models.Model):
    MODELS_MEDIA_ARTICLES = MODELS_MEDIA+"articles"

    id = models.BigAutoField(verbose_name="article id", primary_key=True)
    header = models.CharField(max_length=128, unique=True)
    body = models.TextField(max_length=8192)
    image = models.ImageField(upload_to=MODELS_MEDIA_ARTICLES)
    datetime = models.DateTimeField(verbose_name="Date and time", auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))
    image_tag.short_description = 'Image'

    class Meta:
        ordering = ["datetime"]


# Create your models here.
