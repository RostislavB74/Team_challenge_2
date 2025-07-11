from django.contrib import admin
from journals import views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tiles/", include("tiles.urls")),
    path("shift-reports/", views.shift_report_list, name="shift_report_list"),
    path(
        "shift-reports/<int:doc_id>/",
        views.shift_report_detail,
        name="shift_report_detail",
    ),
    path(
        "shift-reports/create/", views.shift_report_create, name="shift_report_create"
    ),
    # path(
    #     "shift-reports/<int:doc_id>/edit/",
    #     views.shift_report_edit,
    #     name="shift_report_edit",
    # ),
    # path(
    #     "shift-reports/<int:doc_id>/delete/",
    #     views.shift_report_delete,
    #     name="shift_report_delete",
    # ),
    path(
        "shift-reports/<int:doc_id>/row/create/",
        views.shift_report_row_create,
        name="shift_report_row_create",
    ),
    # path(
    #     "shift-reports/<int:doc_id>/row/<int:row_id>/edit/",
    #     views.shift_report_row_edit,
    #     name="shift_report_row_edit",
    # ),
    # path(
    #     "shift-reports/<int:doc_id>/row/<int:row_id>/delete/",
    #     views.shift_report_row_delete,
    #     name="shift_report_row_delete",
    # ),
]
# urlpatterns = [
#     path('shift-reports/<int:doc_id>/row/create/', views.shift_report_row_create, name='shift_report_row_create'),
#     path("admin/", admin.site.urls),
#     path("shift-reports/", views.shift_report_list, name="shift_report_list"),
#     path(
#         "shift-reports/<int:doc_id>/",
#         views.shift_report_detail,
#         name="shift_report_detail",
#     ),
#     path(
#         "shift-reports/create/", views.shift_report_create, name="shift_report_create"
#     ),
#     path(
#         "shift-reports/<int:doc_id>/edit/",
#         views.shift_report_edit,
#         name="shift_report_edit",
#     ),
#     path(
#         "shift-reports/<int:doc_id>/delete/",
#         views.shift_report_delete,
#         name="shift_report_delete",
#     ),
# ]
