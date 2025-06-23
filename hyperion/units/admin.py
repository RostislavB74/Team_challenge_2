from django.contrib import admin

from .models import *  

@admin.register(Units)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'code', 'id_1c_code')
    search_fields = ('name', )

