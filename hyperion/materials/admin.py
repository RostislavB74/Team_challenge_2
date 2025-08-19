# apps/passports_designs/admin.py
from django.contrib import admin
from .models import Materials, MaterialGroups, MaterialUnits, MaterialTypes, MaterialKinds


@admin.register(Materials)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "material_group_id", "unit_id", "material_type_id", "material_kind_id", "spec", "is_equipment", "archived")
    search_fields = ("name", "material_group__name")
    list_filter = ("archived", "is_equipment")

@admin.register(MaterialGroups)
class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(MaterialUnits)
class MaterialUnitAdmin(admin.ModelAdmin):
    list_display = ("id","name","unit","basic","course")
    search_fields = ("name",)

@admin.register(MaterialTypes)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(MaterialKinds)
class MaterialKindAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

