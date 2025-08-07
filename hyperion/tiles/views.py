from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Designs, CaliberTiles
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from django.http import JsonResponse


def TileListView(request):
    tiles = Designs.objects.select_related(
        "tile_type", "collection", "color", "tile_glaze", "hue", "author"
    ).only(
        "design_ean",
        "ean",
        "design_name",
        "is_base",
        "archived",
        "is_action",
        "is_stock",
        "is_test",
        "tone",
        "quality",
        "width",
        "height",
        "thickness",
        "box_amount",
        "box_weight",
        "package_amount",
        "add_date",
        "parent_ean",
        "on_tile_ean",
        "tile_type__name",
        "collection__name",
        "color__name",
        "tile_glaze__name",
        "hue__name",
        "author__user_name",
    )

    # Бульові фільтри
    for field in ["is_base", "archived", "is_stock", "is_test", "is_action"]:
        val = request.GET.get(field)
        if val == "true":
            tiles = tiles.filter(**{field: True})
        elif val == "false":
            tiles = tiles.filter(**{field: False})

    # Строкові фільтри
    if design_name := request.GET.get("design_name"):
        tiles = tiles.filter(design_name__icontains=design_name)
    if tile_type := request.GET.get("tile_type"):
        tiles = tiles.filter(tile_type__name__icontains=tile_type)
    if collection := request.GET.get("collection"):
        tiles = tiles.filter(collection__name__icontains=collection)

    # Пагінація
    paginator = Paginator(tiles, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Доступні варіанти фільтрів (з урахуванням вже застосованих)
    design_names = (
        tiles.values_list("design_name", flat=True).distinct().order_by("design_name")
    )
    tile_types = (
        tiles.filter(tile_type__isnull=False)
        .values_list("tile_type__name", flat=True)
        .distinct()
        .order_by("tile_type__name")
    )
    collections = (
        tiles.filter(collection__isnull=False)
        .values_list("collection__name", flat=True)
        .distinct()
        .order_by("collection__name")
    )

    context = {
        "page_obj": page_obj,
        "design_names": design_names,
        "tile_types": tile_types,
        "collections": collections,
        "filters": request.GET,  # Щоб зберігати у формі вибране
    }

    # 🔁 Якщо це AJAX-запит — повертаємо тільки частину
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("tiles/tiles_partial.html", context, request=request)
        return JsonResponse({"html": html})

    # Інакше — повна сторінка
    return render(request, "tiles/list.html", context)


def filtered_options(request):
    tiles = Designs.objects.all()

    # застосовуємо ті самі фільтри, що і в TileListView
    bool_fields = ["is_base", "archived", "is_stock", "is_test", "is_action"]
    for field in bool_fields:
        val = request.GET.get(field)
        if val == "true":
            tiles = tiles.filter(**{field: True})
        elif val == "false":
            tiles = tiles.filter(**{field: False})

    design_name = request.GET.get("design_name")
    tile_type = request.GET.get("tile_type")
    collection = request.GET.get("collection")

    if design_name:
        tiles = tiles.filter(design_name__icontains=design_name)
    if tile_type:
        tiles = tiles.filter(tile_type__name__icontains=tile_type)
    if collection:
        tiles = tiles.filter(collection__name__icontains=collection)

    design_names = (
        tiles.values_list("design_name", flat=True).distinct().order_by("design_name")
    )
    tile_types = (
        tiles.filter(tile_type__isnull=False)
        .values_list("tile_type__name", flat=True)
        .distinct()
        .order_by("tile_type__name")
    )
    collections = (
        tiles.filter(collection__isnull=False)
        .values_list("collection__name", flat=True)
        .distinct()
        .order_by("collection__name")
    )

    return JsonResponse(
        {
            "design_names": list(design_names),
            "tile_types": list(tile_types),
            "collections": list(collections),
        }
    )


# def TileListView(request):
#     tiles = Designs.objects.all()
#     tiles = tiles.select_related(
#         'tile_type',
#         'collection',
#         'color',
#         'tile_glaze',
#         'hue',
#         'author',
#             ).only(
#             'design_ean', 'ean', 'design_name', 'is_base', 'archived', 'is_action', 'is_stock', 'is_test',
#         'tone', 'quality', 'width', 'height', 'thickness', 'box_amount', 'box_weight',
#         'package_amount', 'add_date', 'parent_ean', 'on_tile_ean',
#         'tile_type__name', 'collection__name', 'color__name',
#         'tile_glaze__name', 'hue__name', 'author__user_name'
#         )
#     # Фільтрація за GET-параметрами

#     if is_base := request.GET.get('is_base'):
#         if is_base == 'true':
#             tiles = tiles.filter(is_base=True)
#         elif is_base == 'false':
#             tiles = tiles.filter(is_base=False)

#     if archived := request.GET.get('archived'):
#         if archived == 'true':
#             tiles = tiles.filter(archived=True)
#         elif archived == 'false':
#             tiles = tiles.filter(archived=False)
#     if is_stock := request.GET.get('is_stock'):
#         if is_stock == 'true':
#             tiles = tiles.filter(is_stock=True)
#         elif is_stock == 'false':
#             tiles = tiles.filter(is_stock=False)
#     if is_test := request.GET.get('is_test'):
#         if is_test == 'true':
#             tiles = tiles.filter(is_test=True)
#         elif is_test == 'false':
#             tiles = tiles.filter(is_test=False)
#     if is_action := request.GET.get('is_action'):
#         if is_action == 'true':
#             tiles = tiles.filter(is_action=True)
#         elif is_action == 'false':
#             tiles = tiles.filter(is_action=False)
#     # Фільтрація
#     design_name = request.GET.get("design_name")
#     tile_type = request.GET.get("tile_type")
#     collection = request.GET.get("collection")

#     if design_name:
#         tiles = tiles.filter(design_name__icontains=design_name)
#     if tile_type:
#         tiles = tiles.filter(tile_type__name__icontains=tile_type)
#     if collection:
#         tiles = tiles.filter(collection__name__icontains=collection)

#     paginator = Paginator(tiles, 50)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     html = render_to_string("tiles/tiles_partial.html", {"page_obj": page_obj})
#     return HttpResponse(html)


def filter_options(request):
    tiles = Designs.objects.all()
    # фільтруємо як вище, ті ж умови

    design_names = tiles.values_list("design_name", flat=True).distinct().order_by("design_name")

    return JsonResponse({
        "design_names": list(design_names),
    })


def CaliberTileListView(request):
    caliber_tiles = CaliberTiles.objects.all()
    paginator = Paginator(caliber_tiles, 50)  # 50 записів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tiles/caliber_tile_list.html', {'page_obj': page_obj})
# Після пагінації, перед формуванням списку фільтрів:
#     filtered_tiles = tiles  # Уже відфільтровані плитки
#     # Після пагінації, перед формуванням списку фільтрів:
#     filtered_tiles = tiles  # Уже відфільтровані плитки

# # Формування фільтрів з урахуванням вже застосованих фільтрів:
#     design_names = filtered_tiles.values_list("design_name", flat=True).distinct().order_by("design_name")
#     tile_types = filtered_tiles.filter(tile_type__isnull=False).values_list("tile_type__name", flat=True).distinct().order_by("tile_type__name")
#     collections = filtered_tiles.filter(collection__isnull=False).values_list("collection__name", flat=True).distinct().order_by("collection__name")

#     # Формування фільтрів з урахуванням вже застосованих фільтрів:
#     # design_names = filtered_tiles.values_list("design_name", flat=True).distinct().order_by("design_name")
#     # tile_types = filtered_tiles.filter(tile_type__isnull=False).values_list("tile_type__name", flat=True).distinct().order_by("tile_type__name")
#     # collections = filtered_tiles.filter(collection__isnull=False).values_list("collection__name", flat=True).distinct().order_by("collection__name")

#     context = {
#         "page_obj": page_obj,
#         "design_names": design_names,
#         "tile_types": tile_types,
#         "collections": collections,
#     }
#     return render(request, 'tiles/list.html', context)
