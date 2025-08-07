from django.shortcuts import render
from .models import MenuItem
# from django.http import HttpResponse

def menu_view(request):
    menu_items = MenuItem.objects.filter(parent__isnull=True, visible=True).order_by('order')
    return render(request, 'navigation/base.html', {'menu_items': menu_items})


