from django.shortcuts import render
from company_structure.models import Departments, Department_sections
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from productions.models import ProductionSections, Production_line_groups, Production_lines, Snap_types_to_lines, StoppageCausesTypes, StoppageCauses
# from company_structure.models import Department_sections


def ProductionLineGroupsListView(request):
    production_line_groups = Production_line_groups.objects.all()
    paginator = Paginator(production_line_groups, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "productions/production_line_groups_list.html", {"page_obj": page_obj})

def ProductionSectionsListView(request):
    # Збираємо всі цехи
    departments = Departments.objects.all()

    # Отримуємо ID цеху з GET або беремо перший як дефолт
    department_id = request.GET.get("department_id")
    try:
        department_id = int(department_id) if department_id else None
    except (ValueError, TypeError):
        department_id = None

    if not department_id and departments.exists():
        department_id = (
            departments.first().department_id
        )  # Змінено з .id на .department_id

    # Вибираємо цех (або None, якщо ID некоректний)
    selected_department = (
        Departments.objects.filter(
            department_id=department_id
        ).first()  # Змінено з id на department_id
        if department_id
        else (departments.first() if departments.exists() else None)
    )

    # Дільниці для вибраного цеху
    if selected_department:
        sections = Department_sections.objects.filter(
            department_id=selected_department, archived=False
        ).select_related("department_id")
    else:
        sections = Department_sections.objects.none()

    context = {
        "departments": departments,
        "selected_department": selected_department,
        "sections": sections,
    }
    return render(request, "productions/production_sections_list.html", context)


def sections_by_department_data(request, department_id):
    items_qs = Department_sections.objects.filter(
        department_id=department_id, archived=False
    ).order_by("name")
    paginator = Paginator(items_qs, 50)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    items = [
        {
            "id": s.id,
            "section_name": s.name,
            "description": s.descriptions or "",
            "num": s.num or "",
        }
        for s in page_obj
    ]
    return JsonResponse(
        {
            "items": items,
            "has_next": page_obj.has_next(),
            "page": page_number,
        }
    )
