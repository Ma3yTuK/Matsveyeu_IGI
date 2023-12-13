from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path("profile", views.UserUpdateView.as_view(template_name="authentication/profile.html"), name="profile"),
    path("registration", views.UserCreateView.as_view(template_name="authentication/registration.html"), name="registration"),
    path("login", views.AuthenticateView.as_view(template_name="authentication/login.html"), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
]