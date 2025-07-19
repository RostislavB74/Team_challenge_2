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
        "kiln_name",
        "production_line_id",
        "hardware_id",
        "kiln_number",
    )
    list_display_links = ("kiln_id", "kiln_name")
@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = (
        "hardware_id",
        "name",
        "production_section_id",
        "hardware_group_id",
    )
    list_display_links = ("hardware_id", "name")

@admin.register(Hardware_groups)
class Hardware_groupsAdmin(admin.ModelAdmin):
    list_display = (
        "hardware_group_id",
        "name",
    )
    list_display_links = ("hardware_group_id", "name")