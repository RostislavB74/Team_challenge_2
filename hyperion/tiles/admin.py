from django.contrib import admin
from .models import *
@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('design_ean', 'design_name', 'tile_type', 'width', 'height', 'thickness', 'box_amount', 'package_amount', 'is_base')
@admin.register(Quality)
class QualityAdmin(admin.ModelAdmin):
    list_display = ('quality','description', 'is_defect', 'sort_order', 'mark')