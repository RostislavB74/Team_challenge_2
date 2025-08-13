from django.urls import path
from . import views
# from .views import TileListView, CaliberTileListView, CollectionsTileListView
urlpatterns = [
    path("designs/", views.TileListView, name="design_list"),
    path("caliber/", views.CaliberTileListView, name="caliber_list"),
    path("collections/", views.CollectionsTileListView, name="collections_tiles_list"),
    path("types/", views.TilesTypesListView, name="tiles_types_list"),
    path("groups/", views.ProductGroupsListView, name="product_groups_list"),
    path("product-types/", views.ProductTypesListView, name="product_types_list"),
    path("tiles/options/", views.filtered_options, name="filtered_options"),
    # path('designs/', tile_list, name='tile_list'),
    # path('caliber/', caliber_tile_list, name='caliber_tile_list'),
]
app_name = 'tiles'
