# from django.urls import path
# from . import views

# urlpatterns = [
#     path("<int:doc_id>/", views.shift_report_detail, name="shift_report_detail"),
#     path("get-designs/", views.get_designs, name="get_designs"),
#     path("<int:doc_id>/print/", views.shift_report_print, name="shift_report_print"),
# ]

# app_name = "journals"
from django.urls import path
from . import views

urlpatterns = [
    path("<int:doc_id>/", views.shift_report_detail, name="shift_report_detail"),
    path("<int:doc_id>/add-row/", views.add_row, name="add_row"),
    path("<int:doc_id>/edit-row/<int:row_id>/", views.edit_row, name="edit_row"),
    path("<int:doc_id>/delete-row/<int:row_id>/", views.delete_row, name="delete_row"),
]

app_name = "journals"