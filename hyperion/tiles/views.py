from django.shortcuts import render
from django.core.paginator import Paginator
from .models import (
    Designs,
    CaliberTiles,
    Collections,
    TileTypes,
    ProductTypes,
    ProductGroups,
    Quality,
)
from django.http import JsonResponse
from django.template.loader import render_to_string


def TileListView(request):
    sort = request.GET.get("sort", "design_ean")  # поле для сортування
    order = request.GET.get("order", "asc")  # порядок

    if order == "desc":
        sort = f"-{sort}"

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
    ).order_by(sort)

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
    return render(
        request,
        "tiles/list.html",
        {
            "page_obj": page_obj,
            "current_sort": request.GET.get("sort", "design_ean"),
            "current_order": order,
        },
    )

    # return render(request, "tiles/list.html", context)


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

def filter_products(request):
    query = Designs.objects.all()

    is_archived = request.GET.get("archived")
    if is_archived in ["yes", "no"]:
        query = query.filter(is_archived=(is_archived == "yes"))

    design = request.GET.get("design")
    if design:
        query = query.filter(design=design)

    collection = request.GET.get("collection")
    if collection:
        query = query.filter(collection=collection)

    results = list(query.values("id", "name", "design", "collection", "is_archived"))
    return JsonResponse({"results": results})

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


def CollectionsTileListView(request):
    collections_tiles = Collections.objects.all()
    paginator = Paginator(collections_tiles, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tiles/collections_tiles_list.html", {"page_obj": page_obj})


def TilesTypesListView(request):
    tiles_types = TileTypes.objects.all()
    paginator = Paginator(tiles_types, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tiles/tiles_types_list.html", {"page_obj": page_obj})


def ProductTypesListView(request):
    product_types = ProductTypes.objects.all()
    paginator = Paginator(product_types, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tiles/product_types_list.html", {"page_obj": page_obj})
def ProductGroupsListView(request):
    product_groups = ProductGroups.objects.all()
    paginator = Paginator(product_groups, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tiles/product_groups_list.html", {"page_obj": page_obj})


def ProductQualityListView(request):
    product_groups = Quality.objects.all()
    paginator = Paginator(product_groups, 50)  # 50 записів на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tiles/product_quality_list.html", {"page_obj": page_obj})
