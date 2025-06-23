from django.contrib import admin
from .models import *

@admin.register(Production_line_groups)
class Production_line_groupsAdmin(admin.ModelAdmin):
    list_display=('id', 'name','decor','base','order')
    search_fields=('id', 'name')

@admin.register(Production_lines)
class Production_lineAdmin(admin.ModelAdmin):
    list_display=('id', 'name','productivity','internal_number','report_group_id','order','production_section_id','summarize_number','department_id')
    search_fields=('id', 'name')

@admin.register(Snap_types_to_lines)
class Snap_types_to_linesAdmin(admin.ModelAdmin):
    list_display=('id', 'name','production_line_id','productivity')
    search_fields=('id', 'name')