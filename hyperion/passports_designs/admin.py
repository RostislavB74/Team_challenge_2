# apps/passports_designs/admin.py
from django.contrib import admin
from .models import (
    TileType, Design, 
    DesignMaterial, DesignPassportCalculation, DesignMaterialCalculation
)

@admin.register(TileType)
class TileTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "width", "height", "thickness", "box_amount", "package_amount")
    search_fields = ("name",)

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "tile_type")
    search_fields = ("name", "code")
    list_filter = ("tile_type",)



@admin.register(DesignMaterial)
class DesignMaterialAdmin(admin.ModelAdmin):
    list_display = ("design", "material", "amount_per_m2", "calculated_amount_per_m2", "needs_review")
    search_fields = ("design__name", "material__name")
    list_filter = ("needs_review",)

class DesignMaterialCalculationInline(admin.TabularInline):
    model = DesignMaterialCalculation
    extra = 0

@admin.register(DesignPassportCalculation)
class DesignPassportCalculationAdmin(admin.ModelAdmin):
    list_display = ("design", "date_calculated", "total_m2")
    search_fields = ("design__name",)
    inlines = [DesignMaterialCalculationInline]
