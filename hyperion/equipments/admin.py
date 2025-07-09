from django.contrib import admin
from .models import *

@admin.register(EquipmentsTypes)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Kilns)
class KilnsAdmin(admin.ModelAdmin):
    list_display = (
        "kiln_id",
        "name",
        "production_line_id",
        "hardware_id",
        "kiln_number",
    )
    list_display_links = ("kiln_id", "name")
