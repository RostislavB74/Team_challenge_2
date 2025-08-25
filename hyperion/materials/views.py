from utils.utils import list_view
from django.shortcuts import render, get_object_or_404
from materials.models import (
    Materials,
    MaterialGroups,
    MaterialKinds,
    MaterialTypes,
    MaterialUnits,
    MaterialsByDepartments
)  
from company_structure.models import *# винеси хелпер у окремий файл utils.py
from django.http import JsonResponse

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


def MaterialsBySectionView(request, section_id=None):
    # всі секції
    sections = Department_sections.objects.all()

    # якщо нічого не вибрано – беремо першу секцію
    if section_id is None and sections.exists():
        section_id = sections.first().pk  # бо primary_key = department_id

    # вибираємо секцію
    selected_section = get_object_or_404(Department_sections, pk=section_id)

    # матеріали цієї секції (через проміжну таблицю)
    materials = MaterialsByDepartments.objects.filter(
        production_section=selected_section
    ).select_related("material", "production_section")

    return render(
        request,
        "materials/materials_master_detail.html",
        {
            "sections": sections,
            "selected_section": selected_section,
            "materials": materials,
        },
    )


def MaterialsByDepartmentsListView(request):
    return list_view(
        request,
        MaterialsByDepartments,
        "materials/materials_by_departments_list.html",
        ["materials", "id", "production_section_id"],

    )


def materials_by_section_data(request, section_id):
    items = (
        MaterialsByDepartments.objects.filter(production_section_id=section_id)
        .select_related("material")
        .order_by("material__name")
    )
    data = [
        {
            "link_id": i.id,
            "material_id": i.material.id,
            "material_name": i.material.name,
        }
        for i in items
    ]
    return JsonResponse({"items": data})
