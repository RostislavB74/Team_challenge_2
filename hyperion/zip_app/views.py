from django.shortcuts import render
from .models import Firms, Orders, Catalogues
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.db.models import Q
from utils.utils import list_view
# def zip_firms_list(request):
#     firms = Firms.objects.using("zip_db").all()
#     return render(request, "zip_app/firms_list.html", {"firms": firms})
def zip_catalogue_list(request):
    queryset = Catalogues.objects.select_related("equipments_id").using(
        "zip_db"
    )  # Оптимізація для зовнішнього ключа
    search = request.GET.get("search", "")
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(section__name__icontains=search)
        )
    sort = request.GET.get("sort", "catalogue_id")
    direction = request.GET.get("dir", "asc")
    if sort in ["catalogue_id", "name", "equipments_id"]:
        if direction == "desc":
            sort = f"-{sort}"
    else:
        sort = "catalogue_id"
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
    return render(request, "zip_app/catalogues_list.html", context)


def zip_orders_list(request):
    orders = Orders.objects.using("zip_db").all()
    return render(request, "zip_app/orders_list.html", {"orders": orders})


def zip_firms_list(request):
    queryset = Firms.objects.select_related('section').using('zip_db')  # Оптимізація для зовнішнього ключа
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(section__name__icontains=search)
        )
    sort = request.GET.get('sort', 'firms_id')
    direction = request.GET.get('dir', 'asc')
    if sort in ['firms_id', 'name', 'section__name']:
        if direction == 'desc':
            sort = f'-{sort}'
    else:
        sort = 'firms_id'
    queryset = queryset.order_by(sort)
    paginator = Paginator(queryset, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'sort': sort.lstrip('-'),
        'dir': direction,
        'search': search,
    }
    return render(request, 'zip_app/firms_list.html', context)
