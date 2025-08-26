from django.urls import path
from . import views

# from .views import TileListView, CaliberTileListView, CollectionsTileListView
urlpatterns = [
    path("materials/", views.MaterialsListView, name="materials_list"),
    path("material-groups/", views.MaterialGroupsListView, name="material_groups_list"),
    path("material-kinds/", views.MaterialKindsListView, name="material_kinds_list"),
    path("material-types/", views.MaterialTypesListView, name="material_types_list"),
    path("material-units/", views.MaterialUnitsListView, name="material_units_list"),
    path(
        "material-by-departments/",
        views.MaterialsBySectionView,
        name="materials_master_detail",
    ),
    path(
        "material-by-departments/<int:section_id>/data/",
        views.materials_by_section_data,
        name="materials_by_section_data",
    ),
]
app_name = "materials"
