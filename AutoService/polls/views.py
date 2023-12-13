from django.shortcuts import render
from django.views import generic
from django.contrib.auth import mixins
from . import models
from django.urls import reverse_lazy
from base.forms import TimeZoneForm
from authentication.models import User
from . import forms
from django.urls import reverse
from DreamService import settings
import requests
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from base.helper_functions import get_quote


class PartView(generic.DetailView):
    model = models.Part


class PartsView(generic.ListView):
    model = models.Part

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        context["filter_form"] = self.filter_form
        context["order_form"] = self.order_form
        context["quote"] = get_quote()
        return context

    def get_queryset(self):
        self.search_form = forms.PartsSearchForm(self.request.GET)
        self.filter_form = forms.PartsFilterForm(self.request.GET)
        self.order_form = forms.PartsOrderForm(self.request.GET)
        self.search_form.is_valid()
        self.filter_form.is_valid()
        self.order_form.is_valid()
        return self.order_form.get_results(self.search_form.get_results(self.filter_form.get_results(self.model.objects.all())))


class AddPartToCartView(mixins.LoginRequiredMixin, generic.RedirectView):

    def get_redirect_field_name(self):
        return None

    def dispatch(self, request, part_id, *args, **kwargs):
        try:
            part = models.Part.objects.get(pk=part_id)
        except Question.DoesNotExist:
            raise Http404("Part does not exist")
        request.user.cart.order.parts.add(part)
        request.user.cart.save()
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('polls:cart')


class CartView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Cart

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["promo_form"] = self.promo_form
        return context

    def get_object(self):
        cart = self.request.user.cart
        form_promo_field = "promo"
        if form_promo_field in self.request.GET:
            self.promo_form = forms.CartPromoForm(self.request.GET)
            if self.promo_form.is_valid():
                if len(self.promo_form.get_promo()) > 0:
                    cart.promo = models.Promo.objects.get(name=self.promo_form.get_promo())
                else:
                    cart.promo = None
                cart.save()
        else:
            if cart.promo:
                self.promo_form = forms.CartPromoForm(initial={form_promo_field: cart.promo.name})
            else:
                self.promo_form = forms.CartPromoForm()
        return cart


class CartPartRemoveView(mixins.LoginRequiredMixin, generic.RedirectView):

    def get_redirect_field_name(self):
        return None

    def dispatch(self, request, part_id, *args, **kwargs):
        request.user.cart.order.parts.remove(models.Part.objects.get(id=part_id))
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER', settings.HOME_URL)


class OrderCartView(mixins.LoginRequiredMixin, generic.RedirectView):

    def get_redirect_field_name(self):
        return None

    def dispatch(self, request, *args, **kwargs):
        request.user.cart.make_order()
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.GET.get('next', settings.HOME_URL)


class ServicesView(generic.ListView):
    model = models.Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        context["filter_form"] = self.filter_form
        context["order_form"] = self.order_form
        context["quote"] = get_quote()
        return context

    def get_queryset(self):
        self.search_form = forms.ServiceSearchForm(self.request.GET)
        self.filter_form = forms.ServiceFilterForm(self.request.GET)
        self.order_form = forms.ServiceOrderForm(self.request.GET)
        self.search_form.is_valid()
        self.filter_form.is_valid()
        self.order_form.is_valid()
        return self.order_form.get_results(self.search_form.get_results(self.filter_form.get_results(self.model.objects.all())))


class TimeZoneView(generic.RedirectView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            request.session["django_timezone"] = request.POST['timezone']
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER', settings.HOME_URL)


class ReviewsView(generic.ListView):
    model = models.Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = get_quote()
        return context


class ReviewView(mixins.LoginRequiredMixin, generic.UpdateView):
    form_class = forms.ReviewCreateForm

    def get_success_url(self):
        return reverse("polls:reviews")

    def get_object(self, queryset=None):
        return models.Review(user=self.request.user)


class WorkersView(generic.ListView):
    COLUMN_COUNT = 3

    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = []
        for a in enumerate(context['object_list']):
            if a[0] % WorkersView.COLUMN_COUNT == 0:
                table.append([])
            table[a[0] // WorkersView.COLUMN_COUNT].append(a[1])
        context["table"] = table
        context["quote"] = get_quote()
        return context

    def get_queryset(self):
        return User.objects.filter(role__isnull=False)


class JobsView(mixins.UserPassesTestMixin, generic.ListView):
    model = models.Job

    def test_func(self):
        try:
            models.Master.objects.get(user=self.request.user.id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quote"] = get_quote()
        return context

    def get_queryset(self):
        return models.Job.objects.filter(order__processing=False, datetime__gte=timezone.now() - timedelta(hours=models.Service.MAX_DURATION), master=self.request.user.master)


# Create your views here.    path("workers", views.WorkersView.as_view(template_name="authentication/workers.html"), name="workers"),

