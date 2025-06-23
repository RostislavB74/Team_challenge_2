# apps/passports_designs/admin.py
from django.contrib import admin
from .models import Material, MaterialGroup, MaterialUnit, MaterialType, MaterialKind
from units.models import Units


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "material_group_id", "unit_id")
    search_fields = ("name", "material_group__name")
    list_filter = ("archived", "is_equipment")

@admin.register(MaterialGroup)
class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(MaterialUnit)
class MaterialUnitAdmin(admin.ModelAdmin):
    list_display = ("id","name","unit","basic","course")
    search_fields = ("name",)

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(MaterialKind)
class MaterialKindAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

