from django import forms
from . import models
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name", "number", "email", "timezone"]


class UserCreateForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        self.user_cache = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password1"])
        return user

    def get_user(self):
        return self.user_cache

    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name", "number", "email", "timezone"]


class AuthenticationForm(forms.Form):
    error_messages = {
        'invalid_login': _("Please enter a correct username and password. Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        self.user_cache = authenticate(username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )
        else:
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache