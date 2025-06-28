# apps/passports_designs/admin.py
from django.contrib import admin
from .models import (
     
    DesignMaterial, DesignPassportCalculation, DesignMaterialCalculation
)



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
