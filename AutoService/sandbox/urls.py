from django.urls import path
from django.views import generic

app_name = "sandbox"
urlpatterns = [
    path("sandbox", generic.TemplateView.as_view(template_name="sandbox/sandbox.html"), name="sandbox"),
    path("sandbox-css", generic.TemplateView.as_view(template_name="sandbox/sandbox-css.html"), name="sandbox-css"),
    path("sandbox-js", generic.TemplateView.as_view(template_name="sandbox/sandbox-js.html"), name="sandbox-js"),
]