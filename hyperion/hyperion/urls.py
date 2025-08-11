from django.contrib import admin
from journals import views
from django.urls import path, include
from hyperion.admin import my_admin_site

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mysite/", my_admin_site.urls),
    path("navigation/", include("navigation.urls", namespace="navigation")),
    path("tiles/", include("tiles.urls", namespace="tiles")),
    path("units/", include("units.urls", namespace="units")),
    path("journals/", include("journals.urls"), name="journals"),
    # path("shift-reports/", views.shift_report_list, name="shift_report_list"),
    path(
        "shift-reports/<int:doc_id>/",
        views.shift_report_detail,
        name="shift_report_detail",
    ),
    path(
        "shift-reports/<int:doc_id>/add-row/",
        views.add_row,
        name="add_row",
    ),
    path(
        "shift-reports/<int:doc_id>/edit-row/<int:row_id>/",
        views.edit_row,
        name="edit_row",
    ),
    path(
        "shift-reports/<int:doc_id>/delete-row/<int:row_id>/",
        views.delete_row,
        name="delete_row",
    ),
]
