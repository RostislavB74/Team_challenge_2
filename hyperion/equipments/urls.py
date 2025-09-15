from django.urls import path
from . import views



app_name = "equipments"


urlpatterns = [
    path(
        "kilns/",
        views.EquipmentsKilnsListView,
        name="equipments_kilns_list",
    ),
]
