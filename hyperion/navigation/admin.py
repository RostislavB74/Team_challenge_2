from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_name', 'parent', 'order')
    list_filter = ('parent',)
    search_fields = ('title', 'url_name')
    prepopulated_fields = {'url_name': ('title',)}