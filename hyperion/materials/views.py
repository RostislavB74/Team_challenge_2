from utils.utils import list_view
from materials.models import (
    Materials,
    MaterialGroups,
    MaterialKinds,
    MaterialTypes,
    MaterialUnits,
    MaterialsByDepartments
)  # винеси хелпер у окремий файл utils.py


def MaterialsListView(request):
    return list_view(
        request, Materials, "materials/materials_list.html", ["id", " material_type_id"]
    )


def MaterialGroupsListView(request):
    return list_view(
        request, MaterialGroups, "materials/material_groups_list.html", ["name"]
    )


def MaterialKindsListView(request):
    return list_view(
        request, MaterialKinds, "materials/material_kinds_list.html", ["name"]
    )


def MaterialTypesListView(request):
    return list_view(
        request, MaterialTypes, "materials/material_types_list.html", ["name"]
    )


def MaterialUnitsListView(request):
    return list_view(
        request, MaterialUnits, "materials/material_units_list.html", ["name"]
    )
def MaterialsByDepartmentsList_view(request):
    return list_view(
        request,
        MaterialsByDepartments,
        "materials/materials_by_departments_list.html",
        ["materials", "id", "production_section_id"],
    )
