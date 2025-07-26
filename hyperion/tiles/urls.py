from django.urls import path
from .views import tile_list, caliber_tile_list

urlpatterns = [
    path('', tile_list, name='tile_list'),
    path('caliber/', caliber_tile_list, name='caliber_tile_list'),
]