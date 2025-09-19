from django.urls import path
from . import views



app_name = "company_structure"


urlpatterns = [
    path(
        "shifts/",
        views.ShiftsListView,
        name="shifts_list",
    ),
]
