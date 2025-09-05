from django.urls import path
from . import views


app_name = "productions"


urlpatterns = [
    path(
        "production-sections/",
        views.ProductionSectionsListView,
        name="production_sections_list",
    ),
    path(
        "production-sections/department/<int:department_id>/data/",
        views.sections_by_department_data,
        name="sections_by_department_data",
    ),
    path(
        "production-line-groups/",
        views.ProductionLineGroupsListView,
        name="production_line_groups_list",
    ),
]
