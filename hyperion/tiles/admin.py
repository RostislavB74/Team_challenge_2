from django.contrib import admin
from .models import *


@admin.register(Collections)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(ProductTypes)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("product_type_id", "name")


@admin.register(Tilestandarts)
class TilestandartAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "full_name")


@admin.register(TileTypes)
class TileTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "width",
        "height",
        "thickness",
        "box_amount",
        "package_amount",
        "box_weight",
        "product_type_id",
        "tile_standart",
        "use_modifier",
        "combi_design",
        "tech_design",
        "square_weight",
    )


@admin.register(Designs)
class DesignAdmin(admin.ModelAdmin):
    list_display = (
        "design_ean",
        "design_name",
        "tile_type",
        "width",
        "height",
        "thickness",
        "box_amount",
        "package_amount",
        "is_base",
    )


@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ("quality", "description", "is_defect", "sort_order", "mark")


@admin.register(Suffix_For_ProductTypes)
class Suffix_For_ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("product_type_id", "suffix")


@admin.register(Hues)
class HuesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(TileGeometry)
class TileGeometryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
