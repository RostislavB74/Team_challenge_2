from django.contrib import admin
from .models import *

@admin.register(Tilestandart)
class TilestandartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'full_name')
@admin.register(TileType)
class TileTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'width', 'height', 'thickness', 'box_amount', 'package_amount', 'box_weight', 'product_type_id', 'tile_standart', 'use_modifier', 'combi_design', 'tech_design')

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('design_ean', 'design_name', 'tile_type', 'width', 'height', 'thickness', 'box_amount', 'package_amount', 'is_base')
@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ('quality','description', 'is_defect', 'sort_order', 'mark')