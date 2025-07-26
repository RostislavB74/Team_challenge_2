
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Designs, CaliberTiles, TileTypes

def tile_list(request):
    tiles = Designs.objects.all()
    paginator = Paginator(tiles, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tiles/list.html', {'page_obj': page_obj})

def caliber_tile_list(request):
    caliber_tiles = CaliberTiles.objects.all()
    paginator = Paginator(caliber_tiles, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tiles/caliber_tile_list.html', {'page_obj': page_obj})