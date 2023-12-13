from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("part/<int:pk>", views.PartView.as_view(template_name="polls/part.html"), name="part"),
    path("parts", views.PartsView.as_view(template_name="polls/parts.html"), name="parts"),
    path("add_part_to_cart/<int:part_id>", views.AddPartToCartView.as_view(), name="add_part_to_cart"),
    path("cart_part_remove/<int:part_id>", views.CartPartRemoveView.as_view(), name="cart_part_remove"),
    path("order_cart", views.OrderCartView.as_view(), name="order_cart"),
    path("services", views.ServicesView.as_view(template_name="polls/services.html"), name="services"),
    path("timezone", views.TimeZoneView.as_view(), name="timezone"),
    path("cart", views.CartView.as_view(template_name="polls/cart.html"), name="cart"),
    path("reviews", views.ReviewsView.as_view(template_name="polls/reviews.html"), name="reviews"),
    path("review", views.ReviewView.as_view(template_name="polls/review.html"), name="review"),
    path("workers", views.WorkersView.as_view(template_name="polls/workers.html"), name="workers"),
    path("jobs", views.JobsView.as_view(template_name="polls/jobs.html"), name="jobs"),
]
