from django.urls import path
from .views import tile_list

urlpatterns = [
    path('', tile_list, name='tile_list'),
]