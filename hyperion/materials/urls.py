from django.urls import path
from . import views

# from .views import TileListView, CaliberTileListView, CollectionsTileListView
urlpatterns = [
    path("materials/", views.MaterialsListView, name="materials_list"),
    path("material-groups/", views.MaterialGroupsListView, name="material_groups_list"),
    path("material-kinds/", views.MaterialKindsListView, name="material_kinds_list"),
    path("material-types/", views.MaterialTypesListView, name="material_types_list"),
    path("material-units/", views.MaterialUnitsListView, name="material_units_list"),
]
app_name = "materials"
