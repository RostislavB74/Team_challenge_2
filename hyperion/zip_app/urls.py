from django.urls import path
from . import views

app_name = "zip_app"

urlpatterns = [
    path("firms/", views.zip_firms_list, name="firms_list"),
    path("orders/", views.zip_orders_list, name="orders_list"),
    path("catalogues/", views.zip_catalogue_list, name="catalogues_list"),
]
