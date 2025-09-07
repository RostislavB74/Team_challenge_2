from django.urls import path
from . import views

# from .views import TileListView, CaliberTileListView, CollectionsTileListView
urlpatterns = [
    path("product-units/", views.ProductUnitsView, name="product_units_list"),
    path("units/", views.UnitsView, name="units_list"),
    
]
app_name = "units"
