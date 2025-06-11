
# def tile_list(request):
#     tiles = Tile.objects.all()[:100]  # Обмеження для швидкості
#     print(tiles.query)  # SQL-запит
#     print(tiles.count())  # Кількість записів
#     return render(request, 'tiles/list.html', {'tiles': tiles})
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Tile

def tile_list(request):
    tiles = Tile.objects.all()
    paginator = Paginator(tiles, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tiles/list.html', {'page_obj': page_obj})