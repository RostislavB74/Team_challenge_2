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
