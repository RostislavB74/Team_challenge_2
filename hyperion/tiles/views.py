
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Designs, CaliberTiles, TileTypes

# def TileListView(request):
#     tiles = Designs.objects.all()
#     paginator = Paginator(tiles, 50)  # 50 записів на сторінку
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'tiles/list.html', {'page_obj': page_obj})
def TileListView(request):
    tiles = Designs.objects.all()

    # Фільтрація за GET-параметрами
    if design_name := request.GET.get('design_name'):
        tiles = tiles.filter(design_name__icontains=design_name)

    if tile_type := request.GET.get('tile_type'):
        tiles = tiles.filter(tile_type__name__icontains=tile_type)

    if collection := request.GET.get('collection'):
        tiles = tiles.filter(collection__name__icontains=collection)

    if is_base := request.GET.get('is_base'):
        if is_base == 'true':
            tiles = tiles.filter(is_base=True)
        elif is_base == 'false':
            tiles = tiles.filter(is_base=False)

    if archived := request.GET.get('archived'):
        if archived == 'true':
            tiles = tiles.filter(archived=True)
        elif archived == 'false':
            tiles = tiles.filter(archived=False)
    
    
    # Пагінація
    paginator = Paginator(tiles, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tiles/list.html', {
        'page_obj': page_obj,
    })
def CaliberTileListView(request):
    caliber_tiles = CaliberTiles.objects.all()
    paginator = Paginator(caliber_tiles, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tiles/caliber_tile_list.html', {'page_obj': page_obj})