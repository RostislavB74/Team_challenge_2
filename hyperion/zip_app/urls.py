from django.urls import path
from . import views

app_name = "zip_app"

urlpatterns = [
    path("firms/", views.zip_firms_list, name="firms_list"),
]
