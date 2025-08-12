from .models import ProductUnits, Units
from django.shortcuts import render
from django.core.paginator import Paginator
# from .models import PrUnitsoductUnits, 


def ProductUnitsView(request):
    sort = request.GET.get("sort", "product_unit_id")  # поле для сортування
    direction = request.GET.get("dir", "asc")  # asc / desc

    product_units = ProductUnits.objects.all()

    if direction == "desc":
        sort = f"-{sort}"

    product_units = product_units.order_by(sort)

    paginator = Paginator(product_units, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "units/product_units_list.html",
        {
            "page_obj": page_obj,
            "sort": request.GET.get("sort"),
            "dir": request.GET.get("dir"),
        },
    )


# def ProductUnitsView(request):
#     product_units_qs = ProductUnits.objects.all()
#     paginator = Paginator(product_units_qs, 50)  # 50 записів на сторінку
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     return render(request, "units/product_units_list.html", {"page_obj": page_obj})


# def UnitsView(request):
#     units_qs = Units.objects.all()
#     paginator = Paginator(units_qs, 50)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     return render(request, "units/units_list.html", {"page_obj": page_obj})
# views.py
def UnitsView(request):
    query = request.GET.get("q", "")
    units = Units.objects.all()
    if query:
        units = units.filter(name__icontains=query)
    paginator = Paginator(units, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "units/units_list.html", {"page_obj": page_obj, "query": query}
    )


# Create your views here.
# def ProductUnitsView(request):
#     product_units = ProductUnits.objects.select_related(
#         "product_type", "tile_type", "unit"
#     ).all()

#     # product_units = ProductUnits.objects.all()
#     paginator = Paginator(product_units, 50)  # 50 записів на сторінку
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     return render(request, "units/product_units_list.html", {"page_obj": page_obj})


# def UnitsView(request):
#     units = Units.objects.all()
#     paginator = Paginator(units, 50)  # 50 записів на сторінку
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     return render(request, "uits/units_list.html", {"page_obj": page_obj})
