from django.shortcuts import render
from . import models
import requests
from django.views import generic
from DreamService import settings
import json
import base64
from polls.models import Order
from base.helper_functions import get_quote
from . import forms


class VacanciesView(generic.ListView):
    model = models.Vacancy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = get_quote()
        return context


class QuestionsView(generic.ListView):
    model = models.Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = get_quote()
        return context


class ArticlesView(generic.ListView):
    model = models.Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = get_quote()
        return context


class ArticleView(generic.DetailView):
    model = models.Article


class HomeView(generic.DetailView):
    model = models.Article

    def get_object(self, *args, **kwargs):
        return models.Article.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervalo = models.Interval.objects.all().first()
        context["interval"] = intervalo.interval
        return context
    


class StatsView(generic.TemplateView):

    def chart_js_gen():
        date_list = Order.objects.dates('datetime', 'year', order="ASC")
        year_list = []
        orders_list = []
        for years in date_list:
            year_list.append(years.year)
            orders_list.append(Order.objects.filter(datetime__year=years.year).count())

        return json.dumps({
            "type": 'bar',
            "data": {
                "labels": year_list,
                "datasets": [{
                    "label": 'Number of orders',
                    "data": orders_list
                }]
            }
        })

    def get_chart():
        api_url = 'https://quickchart.io/chart?c=' + StatsView.chart_js_gen()
        return api_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chart"] = StatsView.get_chart()
        return context

# Create your views here.
