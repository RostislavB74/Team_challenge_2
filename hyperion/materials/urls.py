from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("orders/", views.orders, name="orders"),
]
app_name = "materials"
