from django.contrib import admin

from .models import *  

@admin.register(Units)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'code', 'id_1c_code')
    search_fields = ('name', )

@admin.register(ProductUnits)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ('product_unit_id', 'tile_type_id', 'unit_id', 'basic','course', 'box_unit', 'package_unit')
    search_fields = ('product_unit_id','tile_type_id' )
