from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, "materials/dashboard.html")


def products(request):
    return render(request, "pages/products.html")


def orders(request):
    return render(request, "pages/orders.html")
