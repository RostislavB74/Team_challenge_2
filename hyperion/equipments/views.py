from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.db.models import Q
from .models import Kilns
# Create your views here.
def EquipmentsKilnsListView(request):
    # Базовий запит
    queryset = Kilns.objects.all()

    # Пошук
    search = request.GET.get("search", "")
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(production_line_id__icontains=search)
        )

    # Сортування
    sort = request.GET.get("sort", "kiln_id")
    direction = request.GET.get("dir", "asc")
    if sort in ["kiln_id", "kiln_name", "production_line_id"]:
        if direction == "desc":
            sort = f"-{sort}"
        queryset = queryset.order_by(sort)

    # Пагінація
    paginator = Paginator(queryset, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Контекст для шаблону
    context = {
        "page_obj": page_obj,
        "sort": sort.lstrip("-"),  # Видаляємо '-' для шаблону
        "dir": direction,
        "search": search,
    }

    return render(request, "equipments/equipments_kilns_list.html", context)
