from django.shortcuts import render
from . import models
from django.views import generic
from base.helper_functions import get_quote

class PromosView(generic.ListView):
    model = models.Promo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = get_quote()
        return context

    def get_queryset(self):
        return models.Promo.objects.filter(is_active=True)
    

# Create your views here.
