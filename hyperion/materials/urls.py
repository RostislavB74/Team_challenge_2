from django.urls import path
from . import views

# from .views import TileListView, CaliberTileListView, CollectionsTileListView
urlpatterns = [
    path("materials/", views.MaterialsListView, name="materials_list"),
   
]
app_name = "materials"
