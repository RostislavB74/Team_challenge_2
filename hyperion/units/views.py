
from .models import ProductUnits, Units
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import ProductUnits, Units


def ProductUnitsView(request):
    product_units_qs = ProductUnits.objects.all()
    paginator = Paginator(product_units_qs, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "units/product_units_list.html", {"page_obj": page_obj})


def UnitsView(request):
    units_qs = Units.objects.all()
    paginator = Paginator(units_qs, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "units/units_list.html", {"page_obj": page_obj})


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
