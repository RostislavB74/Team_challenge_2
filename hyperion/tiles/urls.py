from django.urls import path
from . import views
from .views import TileListView, CaliberTileListView
urlpatterns = [
    path("designs/", views.TileListView, name="design_list"),
    path("caliber/", views.CaliberTileListView, name="caliber_list"),
    path("tiles/options/", views.filtered_options, name="filtered_options"),
    # path('designs/', tile_list, name='tile_list'),
    # path('caliber/', caliber_tile_list, name='caliber_tile_list'),
]
app_name = 'tiles'
