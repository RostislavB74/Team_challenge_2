from django.shortcuts import render
from .models import Firms, Orders


def zip_firms_list(request):
    firms = Firms.objects.using("zip_db").all()
    return render(request, "zip_app/firms_list.html", {"firms": firms})


def zip_orders_list(request):
    orders = Orders.objects.using("zip_db").all()
    return render(request, "zip_app/orders_list.html", {"orders": orders})
