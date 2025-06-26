from django.contrib import admin
from .models import *

@admin.register(EquipmentsTypes)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
