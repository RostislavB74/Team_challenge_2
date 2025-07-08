from django.contrib import admin
from .models import ShiftReports

admin.site.register(ShiftReports)
class ShiftReportsAdmin(admin.ModelAdmin):
    list_display = (
        "doc_id",
        "doc_number",
        "doc_date",
        "production_line_id",
        "author",
        "user",
        "draft",
        "deleted",
        # "total",
        # "foreman_name",
    )
    list_filter = ("doc_id","doc_date", "author", "user", "draft", "deleted")
    # search_fields = ("doc_number", "author__username", "user__username")

    # def author_name(self, obj):
    #     return obj.author.get_full_name() or obj.author.username if obj.author else "—"

    # author_name.short_description = "Автор"

    # def last_modified_by(self, obj):
    #     return obj.user.get_full_name() or obj.user.username if obj.user else "—"

    # last_modified_by.short_description = "Останній редактор"


# class ShiftReportAdmin(admin.ModelAdmin):
#     list_display = (
#         "doc_number",
#         "author_name",
#         "doc_date",
#         "total",
#         "last_modified_by",
#     )
#     list_filter = ("doc_date", "author", "user", "draft", "deleted")
#     search_fields = ("doc_number", "author__username", "user__username")

#     def author_name(self, obj):
#         return obj.author.get_full_name() or obj.author.username if obj.author else "—"

#     author_name.short_description = "Автор"

#     def last_modified_by(self, obj):
#         return obj.user.get_full_name() or obj.user.username if obj.user else "—"

#     last_modified_by.short_description = "Останній редактор"
