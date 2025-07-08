from django.contrib import admin
from .models import ShiftReports

@admin.register(ShiftReports)
class ShiftReportsAdmin(admin.ModelAdmin):
    list_display = ('doc_number', 'doc_date', 'author', 'user', 'production_line_id', 'draft', 'deleted')
    search_fields = ('doc_number', 'author__username', 'user__username', 'production_line_id')
