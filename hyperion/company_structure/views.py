from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.db.models import Q
from .models import Shifts


def ShiftsListView(request):
    queryset = Shifts.objects.select_related("line_group_id")  # Оптимізація запиту
    search = request.GET.get("search", "")
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(line_group_id__name__icontains=search)
            | Q(shift_foreman__icontains=search)  # Додано пошук за майстром
        )
    sort = request.GET.get("sort", "shift_id")
    direction = request.GET.get("dir", "asc")
    if sort == "line_group_id":
        sort = "line_group_id__name" if direction == "asc" else "-line_group_id__name"
    elif sort in ["shift_id", "name", "shift_foreman", "alias"]:
        if direction == "desc":
            sort = f"-{sort}"
    else:
        sort = "shift_id"
    queryset = queryset.order_by(sort)
    paginator = Paginator(queryset, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "sort": sort.lstrip("-"),
        "dir": direction,
        "search": search,
    }
    return render(request, "company_structure/shifts_list.html", context)



# def ShiftsListView(request):
#     # Базовий запит
#     queryset = Shifts.objects.all()

#     # Пошук
#     search = request.GET.get("search", "")
#     if search:
#         queryset = queryset.filter(
#             Q(name__icontains=search) | Q(line_group_id__name__icontains=search)
#         )

#     # Сортування
#     sort = request.GET.get("sort", "shift_id")
#     direction = request.GET.get("dir", "asc")
#     if sort in ["shift_id", "name", "shift_foreman", "alias", "line_group_id"]:
#         if direction == "desc":
#             sort = f"-{sort}"
#         queryset = queryset.order_by(sort)

#     # Пагінація
#     paginator = Paginator(queryset, 50)  # 50 записів на сторінку
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # Контекст для шаблону
#     context = {
#         "page_obj": page_obj,
#         "sort": sort.lstrip("-"),  # Видаляємо '-' для шаблону
#         "dir": direction,
#         "search": search,
#     }

#     return render(request, "company_structure/shifts_list.html", context)


# Create your views here.
