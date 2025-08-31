from utils.utils import list_view
from django.shortcuts import render
from materials.models import (
    Materials,
    MaterialGroups,
    MaterialKinds,
    MaterialTypes,
    MaterialUnits,
    MaterialsByDepartments
)  
from company_structure.models import  Department_sections
from django.http import JsonResponse
from django.core.paginator import Paginator

# materials/views.py
from django.core.cache import cache


def MaterialsBySectionView(request):
    cache_key = "all_department_sections"
    sections = cache.get(cache_key)
    if not sections:
        sections = Department_sections.objects.select_related("department_id").all()
        cache.set(cache_key, sections, timeout=3600)

    # def MaterialsBySectionView(request):
    #     sections = Department_sections.objects.select_related("department_id").all()
    section_id = request.GET.get("section_id")

    # Валідація section_id
    try:
        section_id = int(section_id) if section_id else None
    except (ValueError, TypeError):
        section_id = None

    if not section_id and sections.exists():
        section_id = sections.first().id

    selected_section = (
        Department_sections.objects.filter(id=section_id).first()
        if section_id
        else (sections.first() if sections.exists() else None)
    )

    if selected_section:
        materials = MaterialsByDepartments.objects.filter(
            production_section=selected_section
        ).select_related("material")
    else:
        materials = MaterialsByDepartments.objects.none()

    context = {
        "sections": sections,
        "selected_section": selected_section,
        "materials": materials,
    }
    return render(request, "materials/materials_master_detail.html", context)


def materials_by_section_data(request, section_id):
    items_qs = (
        MaterialsByDepartments.objects.filter(production_section_id=section_id)
        .select_related("material")
        .order_by("material__name")
    )
    paginator = Paginator(items_qs, 50)  # 50 матеріалів на сторінку
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    items = [
        {
            "id": m.id,
            "material_id": m.material.id,
            "material_name": m.material.name,
        }
        for m in page_obj
    ]
    return JsonResponse(
        {
            "items": items,
            "has_next": page_obj.has_next(),
            "page": page_number,
        }
    )



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



def MaterialsByDepartmentsListView(request):
    return list_view(
        request,
        MaterialsByDepartments,
        "materials/materials_by_departments_list.html",
        ["materials", "id", "production_section_id"],

    )


def materials_by_department(request, pk):
    qs = Materials.objects.filter(section_id=pk)
    data = [{"material_id": m.id, "material_name": m.name} for m in qs]
    return JsonResponse({"items": data})
