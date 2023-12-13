from django.urls import path
from . import views

app_name = "promo"
urlpatterns = [
    path("promos", views.PromosView.as_view(template_name="promo/promos.html"), name="promos"),
]
