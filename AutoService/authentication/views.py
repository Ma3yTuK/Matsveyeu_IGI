from django.shortcuts import render
from django.views import generic
from . import models
from django.contrib.auth import mixins
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from DreamService import settings
from django.core.exceptions import ObjectDoesNotExist


class UserUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    form_class = forms.UserUpdateForm

    def get_redirect_field_name(self):
        return None

    def get_success_url(self):
        return self.request.GET.get('next', settings.HOME_URL)

    def get_object(self, queryset=None):
        return self.request.user


class UserCreateView(generic.CreateView):
    form_class = forms.UserCreateForm

    def get_success_url(self):
        return self.request.GET.get('next', settings.HOME_URL)

    def form_valid(self, form):
        form.save()
        login(self.request, form.get_user())
        return super().form_valid(form)


class AuthenticateView(generic.FormView):
    form_class = forms.AuthenticationForm

    def get_success_url(self):
        return self.request.GET.get('next', settings.HOME_URL)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(mixins.LoginRequiredMixin, generic.RedirectView):

    def get_redirect_field_name(self):
        return None

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER', settings.HOME_URL)


# Create your views here.
