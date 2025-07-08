from django.contrib import admin
from .models import *
@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'use_kiln_press') 
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')

@admin.register(Department_sections)
class Department_sectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department_id', 'descriptions', 'archived', 'num') 
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Shifts)
class ShiftsAdmin(admin.ModelAdmin):
    list_display = ('shift_id', 'name', 'shift_foreman', 'alias', 'begin_time', 'end_time', 'line_group_id') 
    list_display_links = ('shift_id', 'name')
    search_fields = ('shift_id', 'name')