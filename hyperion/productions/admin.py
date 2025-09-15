from django.contrib import admin
from .models import Production_line_groups, Production_lines, Snap_types_to_lines, StoppageCausesTypes, StoppageCauses

@admin.register(Production_line_groups)
class Production_line_groupsAdmin(admin.ModelAdmin):
    list_display=('id', 'name','decor','base','order')
    search_fields=('id', 'name')

@admin.register(Production_lines)
class Production_lineAdmin(admin.ModelAdmin):
    list_display=('id', 'name','productivity','cert_group','internal_number','report_group_id','order','production_section_id','summarize_number','department_id')
    search_fields=('id', 'name')

@admin.register(Snap_types_to_lines)
class Snap_types_to_linesAdmin(admin.ModelAdmin):
    list_display=('id', 'name','production_line_id','productivity')
    search_fields=('id', 'name')

@admin.register(StoppageCausesTypes)
class StoppageCausesTypesAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'level')
    search_fields=('id', 'name')

@admin.register(StoppageCauses)
class StoppageCausesAdmin(admin.ModelAdmin):
    list_display=('id', 'name')
    search_fields=('id', 'name')
