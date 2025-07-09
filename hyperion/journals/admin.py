# journals/admin.py
from django.contrib import admin
from django.db import connection
from .models import ShiftReports, ShiftMaterialsDebit


@admin.register(ShiftReports)
class ShiftReportAdmin(admin.ModelAdmin):
    list_display = (
        "doc_id",
        "doc_date",
        "doc_number",
        "production_line_id",
        "begin_time",
        "shift_id",
        "foreman_name",
        "total",
        "draft",
        "deleted",
        "description",
        "author",
        "user",
    )
    list_filter = ("doc_date", "author")
    search_fields = ("doc_number",)

    def save_model(self, request, obj, form, change):
        with connection.cursor() as cursor:
            if change:
                # Редагування звіту
                cursor.execute(
                    "EXEC SetShiftReport %s, %s, %s, %s",
                    [obj.doc_number, obj.author, obj.doc_date, obj.total],
                )
            else:
                # Створення звіту
                cursor.execute(
                    "EXEC AddShiftReport %s, %s, %s",
                    [obj.doc_number, obj.author, obj.doc_date],
                )
                # Отримати doc_id нового звіту
                cursor.execute("SELECT @@IDENTITY AS id")
                obj.id = cursor.fetchone()[0]

    def delete_model(self, request, obj):
        with connection.cursor() as cursor:
            cursor.execute("EXEC DelShiftReport %s", [obj.id])

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        doc_id = int(object_id)

        # Дані документа
        with connection.cursor() as cursor:
            cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
            columns = [col[0] for col in cursor.description]
            doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            extra_context["shift_doc"] = doc_data[0] if doc_data else {}

        # Рядки звіту
        with connection.cursor() as cursor:
            cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            extra_context["shift_rows"] = rows

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )


@admin.register(ShiftMaterialsDebit)
class ShiftMaterialsDebitAdmin(admin.ModelAdmin):
    list_display = ('doc_number', 'doc_date', 'author', 'user', 'draft', 'deleted')
    search_fields = ('doc_number', 'author__username', 'user__username')
