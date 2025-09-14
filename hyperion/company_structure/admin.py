from django.contrib import admin
from .models import *
@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'name', 'use_kiln_press') 
    list_display_links = ('department_id', 'name')
    search_fields = ('department_id', 'name')

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

@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'name', 'store_type_id', 'is_active') 
    list_display_links = ('store_id', 'name')
    search_fields = ('store_id', 'name')

@admin.register(Store_types)
class Store_typesAdmin(admin.ModelAdmin):
    list_display = ('store_type_id', 'name') 
    list_display_links = ('store_type_id', 'name')
    search_fields = ('store_type_id', 'name')
@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('subdivision_id', 'name', 'description') 
    list_display_links = ('subdivision_id', 'name')
    search_fields = ('subdivision_id', 'name')