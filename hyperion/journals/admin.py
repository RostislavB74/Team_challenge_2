# journals/admin.py
from django.contrib import admin
from django.db import connection
from django.utils import timezone
from datetime import time
from .models import ShiftReports, ShiftReportRow
from tiles.models import Quality



# @admin.register(ShiftReports)
# class ShiftReportAdmin(admin.ModelAdmin):
#     list_display = (
#         "doc_number",
#         "author",
#         "user",
#         "doc_date",
#         "begin_time",
#         "end_time",
#         "foreman_name",
#         "total",
#         "draft",
#     )
#     list_filter = ("doc_date", "shift_id")
#     search_fields = ("doc_number", "foreman_name")
#     readonly_fields = (
#         "doc_number",
#         "author",
#         "user",
#         "doc_date",
#         "begin_time",
#         "end_time",
#         "foreman_name",
#         "total",
#     )
#     fields = (
#         "doc_number",
#         "author",
#         "user",
#         "doc_date",
#         "description",
#         "draft",
#         "production_line_id",
#         "shift_id",
#         "stoppage1",
#         "kiln1",
#         "comments1",
#         "stoppage2",
#         "kiln2",
#         "comments2",
#         "total",
#         "begin_time",
#         "end_time",
#         "foreman_name",
#     )

#     def save_model(self, request, obj, form, change):
#         with connection.cursor() as cursor:
#             now = timezone.now()
#             hour = now.hour
#             is_day_shift = 9 <= hour < 21
#             shift_id = 1 if is_day_shift else 2
#             begin_time = time(8, 0) if is_day_shift else time(20, 0)
#             end_time = time(20, 0) if is_day_shift else time(8, 0)
#             foreman_name = request.user.user_name

#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [obj.doc_id],
#             )
#             total = cursor.fetchone()[0] or 0

#             if change:
#                 cursor.execute(
#                     "SELECT draft FROM d_shift_report WHERE doc_id = %s", [obj.doc_id]
#                 )
#                 draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#                 if not draft and not request.user.is_superuser:
#                     self.message_user(
#                         request, "Тільки ОТК може редагувати нечернетку!", level="error"
#                     )
#                     return
#                 cursor.execute(
#                     "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                     [
#                         obj.doc_id,
#                         obj.doc_number,
#                         obj.description,
#                         obj.doc_date,
#                         obj.draft,
#                         obj.imported,
#                         obj.parent_doc_id,
#                         obj.production_line_id_id,
#                         shift_id,
#                         obj.stoppage1,
#                         obj.kiln1_id,
#                         obj.comments1,
#                         obj.stoppage2,
#                         obj.kiln2_id,
#                         obj.comments2,
#                         total,
#                         begin_time,
#                         end_time,
#                         foreman_name,
#                     ],
#                 )
#             else:
#                 cursor.execute(
#                     "EXEC AddShiftReport @doc_id OUTPUT, @doc_num OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                     [
#                         obj.description,
#                         now,
#                         True,
#                         obj.imported,
#                         obj.parent_doc_id,
#                         obj.production_line_id_id,
#                         shift_id,
#                         obj.stoppage1,
#                         obj.kiln1_id,
#                         obj.comments1,
#                         obj.stoppage2,
#                         obj.kiln2_id,
#                         obj.comments2,
#                         total,
#                         begin_time,
#                         end_time,
#                         foreman_name,
#                     ],
#                 )
#                 cursor.execute("SELECT @@IDENTITY AS id")
#                 obj.doc_id = cursor.fetchone()[0]

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [form.instance.doc_id],
#             )
#             total = cursor.fetchone()[0] or 0
#             cursor.execute(
#                 "SELECT draft FROM d_shift_report WHERE doc_id = %s",
#                 [form.instance.doc_id],
#             )
#             draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#             cursor.execute(
#                 "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     form.instance.doc_id,
#                     form.instance.doc_number,
#                     form.instance.description,
#                     form.instance.doc_date,
#                     draft,
#                     form.instance.imported,
#                     form.instance.parent_doc_id,
#                     form.instance.production_line_id_id,
#                     form.instance.shift_id_id,
#                     form.instance.stoppage1,
#                     form.instance.kiln1_id,
#                     form.instance.comments1,
#                     form.instance.stoppage2,
#                     form.instance.kiln2_id,
#                     form.instance.comments2,
#                     total,
#                     form.instance.begin_time,
#                     form.instance.end_time,
#                     form.instance.foreman_name,
#                 ],
#             )

#     def delete_model(self, request, obj):
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT draft FROM d_shift_report WHERE doc_id = %s", [obj.doc_id]
#             )
#             draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#             if not draft and not request.user.is_superuser:
#                 self.message_user(
#                     request, "Тільки ОТК може видалити нечернетку!", level="error"
#                 )
#                 return
#             cursor.execute("EXEC DelShiftReport %s", [obj.doc_id])

#     def change_view(self, request, object_id, form_url="", extra_context=None):
#         extra_context = extra_context or {}
#         doc_id = int(object_id)
#         can_edit = True

#         with connection.cursor() as cursor:
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             shift_doc = doc_data[0] if doc_data else {}
#             cursor.execute(
#                 "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
#             )
#             draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#             can_edit = draft or request.user.is_superuser
#             extra_context["shift_doc"] = shift_doc

#             cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             extra_context["shift_rows"] = rows

#         extra_context["can_edit"] = can_edit
#         return super().change_view(
#             request, object_id, form_url, extra_context=extra_context
#         )

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if "delete_selected" in actions:
#             del actions["delete_selected"]
#         return actions
# class ShiftReportRowInline(admin.TabularInline):
#     model = ShiftReportRow
#     extra = 1
#     fields = (
#         "design_ean",
#         "quality",
#         "is_defect",
#         "amount",
#         "unit_id",
#         "box_unit_id",
#         "box_amount",
#         "package_amount",
#     )

#     def get_readonly_fields(self, request, obj=None):
#         # Якщо obj=None або draft не існує, дозволяємо редагування лише суперкористувачам
#         if obj and not request.user.is_superuser:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT draft FROM d_shift_report WHERE doc_id = %s", [obj.doc_id]
#                 )
#                 draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#                 if not draft:
#                     return (
#                         "design_ean",
#                         "quality",
#                         "is_defect",
#                         "amount",
#                         "unit_id",
#                         "box_unit_id",
#                         "box_amount",
#                         "package_amount",
#                     )
#         return ()

#     def has_change_permission(self, request, obj=None):
#         if obj:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT draft FROM d_shift_report WHERE doc_id = %s", [obj.doc_id]
#                 )
#                 draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#                 return draft or request.user.is_superuser
#         return True

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "quality":
#             kwargs["queryset"] = Quality.objects.all()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ShiftReports)
class ShiftReportAdmin(admin.ModelAdmin):
    list_display = (
        "doc_number",
        "author",
        "user",
        "doc_date",
        "begin_time",
        "end_time",
        "foreman_name",
        "total",
        "draft",
    )
    list_filter = ("doc_date", "shift_id")
    search_fields = ("doc_number", "foreman_name")
    readonly_fields = (
        "doc_number",
        "author",
        "user",
        "doc_date",
        "begin_time",
        "end_time",
        "foreman_name",
        "total",
    )
    fields = (
        "doc_number",
        "author",
        "user",
        "doc_date",
        "description",
        "draft",
        "production_line_id",
        "shift_id",
        "stoppage1",
        "kiln1",
        "comments1",
        "stoppage2",
        "kiln2",
        "comments2",
        "total",
        "begin_time",
        "end_time",
        "foreman_name",
    )
    # inlines = [ShiftReportRowInline]

    def save_model(self, request, obj, form, change):
        with connection.cursor() as cursor:
            now = timezone.now()
            hour = now.hour
            is_day_shift = 9 <= hour < 21
            shift_id = 1 if is_day_shift else 2
            begin_time = time(8, 0) if is_day_shift else time(20, 0)
            end_time = time(20, 0) if is_day_shift else time(8, 0)
            foreman_name = request.user.user_name  # Потрібна логіка для майстра

            cursor.execute(
                "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
                [obj.doc_id],
            )
            total = cursor.fetchone()[0] or 0

            if change:
                cursor.execute(
                    "SELECT draft FROM d_shift_report WHERE doc_id = %s", [obj.doc_id]
                )
                draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
                if not draft and not request.user.is_superuser:
                    self.message_user(
                        request, "Тільки ОТК може редагувати нечернетку!", level="error"
                    )
                    return
                cursor.execute(
                    "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                    [
                        obj.doc_id,
                        obj.doc_number,
                        obj.description,
                        obj.doc_date,
                        obj.draft,
                        obj.imported,
                        obj.parent_doc_id,
                        obj.production_line_id_id,
                        shift_id,
                        obj.stoppage1,
                        obj.kiln1_id,
                        obj.comments1,
                        obj.stoppage2,
                        obj.kiln2_id,
                        obj.comments2,
                        total,
                        begin_time,
                        end_time,
                        foreman_name,
                    ],
                )
            else:
                cursor.execute(
                    "EXEC AddShiftReport @doc_id OUTPUT, @doc_num OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                    [
                        obj.description,
                        now,
                        True,
                        obj.imported,
                        obj.parent_doc_id,
                        obj.production_line_id_id,
                        shift_id,
                        obj.stoppage1,
                        obj.kiln1_id,
                        obj.comments1,
                        obj.stoppage2,
                        obj.kiln2_id,
                        obj.comments2,
                        total,
                        begin_time,
                        end_time,
                        foreman_name,
                    ],
                )
                cursor.execute("SELECT @@IDENTITY AS id")
                obj.doc_id = cursor.fetchone()[0]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
                [form.instance.doc_id],
            )
            total = cursor.fetchone()[0] or 0
            cursor.execute(
                "SELECT draft FROM d_shift_report WHERE doc_id = %s",
                [form.instance.doc_id],
            )
            draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
            cursor.execute(
                "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    form.instance.doc_id,
                    form.instance.doc_number,
                    form.instance.description,
                    form.instance.doc_date,
                    draft,
                    form.instance.imported,
                    form.instance.parent_doc_id,
                    form.instance.production_line_id_id,
                    form.instance.shift_id_id,
                    form.instance.stoppage1,
                    form.instance.kiln1_id,
                    form.instance.comments1,
                    form.instance.stoppage2,
                    form.instance.kiln2_id,
                    form.instance.comments2,
                    total,
                    form.instance.begin_time,
                    form.instance.end_time,
                    form.instance.foreman_name,
                ],
            )

    def delete_model(self, request, obj):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT draft FROM d_shift_report WHERE doc_id = %s", [obj.doc_id]
            )
            draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
            if not draft and not request.user.is_superuser:
                self.message_user(
                    request, "Тільки ОТК може видалити нечернетку!", level="error"
                )
                return
            cursor.execute("EXEC DelShiftReport %s", [obj.doc_id])

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        doc_id = int(object_id)
        can_edit = True

        with connection.cursor() as cursor:
            cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
            columns = [col[0] for col in cursor.description]
            doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            shift_doc = doc_data[0] if doc_data else {}
            cursor.execute(
                "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
            )
            draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
            can_edit = draft or request.user.is_superuser
            extra_context["shift_doc"] = shift_doc

            cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            extra_context["shift_rows"] = rows

        extra_context["can_edit"] = can_edit
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions










# class ShiftReportRowInline(admin.TabularInline):
#     model = ShiftReportRow
#     extra = 1
#     fields = (
#         "design_ean",
#         "quality",
#         "is_defect",
#         "amount",
#         "unit_id",
#         "box_unit_id",
#         "box_amount",
#         "package_amount",
#     )

#     def get_readonly_fields(self, request, obj=None):
#         if obj and not obj.draft and not request.user.is_superuser:
#             return (
#                 "design_ean",
#                 "quality",
#                 "is_defect",
#                 "amount",
#                 "unit_id",
#                 "box_unit_id",
#                 "box_amount",
#                 "package_amount",
#             )
#         return ()

#     def has_change_permission(self, request, obj=None):
#         return obj.draft if obj else True or request.user.is_superuser

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "quality":
#             kwargs["queryset"] = Quality.objects.all()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# @admin.register(ShiftReports)
# class ShiftReportAdmin(admin.ModelAdmin):
#     list_display = (
#         "doc_number",
#         "author",
#         "user",
#         "doc_date",
#         "begin_time",
#         "end_time",
#         "foreman_name",
#         "total",
#         "draft",
#     )
#     list_filter = ("doc_date", "draft", "shift_id")
#     search_fields = ("doc_number", "foreman_name")
#     readonly_fields = (
#         "doc_number",
#         "author",
#         "user",
#         "doc_date",
#         "begin_time",
#         "end_time",
#         "foreman_name",
#         "total",
#     )
#     fields = (
#         "doc_number",
#         "author",
#         "user",
#         "doc_date",
#         "description",
#         "draft",
#         "production_line_id",
#         "shift_id",
#         "total",
#         "begin_time",
#         "end_time",
#         "foreman_name",
#         "stoppage1",
#         "kiln1",
#         "comments1",
#         "stoppage2",
#         "kiln2",
#         "comments2",
#     )
#     inlines = [ShiftReportRowInline]

#     def save_model(self, request, obj, form, change):
#         with connection.cursor() as cursor:
#             now = timezone.now()
#             hour = now.hour
#             is_day_shift = 9 <= hour < 21
#             shift_id = 1 if is_day_shift else 2
#             begin_time = time(8, 0) if is_day_shift else time(20, 0)
#             end_time = time(20, 0) if is_day_shift else time(8, 0)
#             foreman_name = request.user.user_name  # Потрібна логіка для майстра

#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [obj.doc_id],
#             )
#             total = cursor.fetchone()[0] or 0

#             if change:
#                 if not obj.draft and not request.user.is_superuser:
#                     self.message_user(
#                         request, "Тільки ОТК може редагувати нечернетку!", level="error"
#                     )
#                     return
#                 cursor.execute(
#                     "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                     [
#                         obj.doc_id,
#                         obj.doc_number,
#                         obj.description,
#                         obj.doc_date,
#                         obj.draft,
#                         obj.imported,
#                         obj.parent_doc_id,
#                         obj.production_line_id_id,
#                         shift_id,
#                         obj.stoppage1,
#                         obj.kiln1_id,
#                         obj.comments1,
#                         obj.stoppage2,
#                         obj.kiln2_id,
#                         obj.comments2,
#                         total,
#                         begin_time,
#                         end_time,
#                         foreman_name,
#                     ],
#                 )
#             else:
#                 cursor.execute(
#                     "EXEC AddShiftReport @doc_id OUTPUT, @doc_num OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                     [
#                         obj.description,
#                         now,
#                         True,
#                         obj.imported,
#                         obj.parent_doc_id,
#                         obj.production_line_id_id,
#                         shift_id,
#                         obj.stoppage1,
#                         obj.kiln1_id,
#                         obj.comments1,
#                         obj.stoppage2,
#                         obj.kiln2_id,
#                         obj.comments2,
#                         total,
#                         begin_time,
#                         end_time,
#                         foreman_name,
#                     ],
#                 )
#                 cursor.execute("SELECT @@IDENTITY AS id")
#                 obj.doc_id = cursor.fetchone()[0]

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [form.instance.doc_id],
#             )
#             total = cursor.fetchone()[0] or 0
#             cursor.execute(
#                 "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     form.instance.doc_id,
#                     form.instance.doc_number,
#                     form.instance.description,
#                     form.instance.doc_date,
#                     form.instance.draft,
#                     form.instance.imported,
#                     form.instance.parent_doc_id,
#                     form.instance.production_line_id_id,
#                     form.instance.shift_id_id,
#                     form.instance.stoppage1,
#                     form.instance.kiln1_id,
#                     form.instance.comments1,
#                     form.instance.stoppage2,
#                     form.instance.kiln2_id,
#                     form.instance.comments2,
#                     total,
#                     form.instance.begin_time,
#                     form.instance.end_time,
#                     form.instance.foreman_name,
#                 ],
#             )

#     def delete_model(self, request, obj):
#         if not obj.draft and not request.user.is_superuser:
#             self.message_user(
#                 request, "Тільки ОТК може видалити нечернетку!", level="error"
#             )
#             return
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC DelShiftReport %s", [obj.doc_id])

#     def change_view(self, request, object_id, form_url="", extra_context=None):
#         extra_context = extra_context or {}
#         doc_id = int(object_id)
#         can_edit = True

#         with connection.cursor() as cursor:
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             shift_doc = doc_data[0] if doc_data else {}
#             can_edit = shift_doc.get("draft", True) or request.user.is_superuser
#             extra_context["shift_doc"] = shift_doc

#             cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             extra_context["shift_rows"] = rows

#         extra_context["can_edit"] = can_edit
#         return super().change_view(
#             request, object_id, form_url, extra_context=extra_context
#         )

#     def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
#         extra_context = extra_context or {}
#         doc_id = int(object_id) if object_id else 0
#         can_edit = True

#         with connection.cursor() as cursor:
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             shift_doc = doc_data[0] if doc_data else {}
#             can_edit = shift_doc.get("draft", True) or request.user.is_superuser
#             extra_context["shift_doc"] = shift_doc

#             cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             extra_context["shift_rows"] = rows

#         extra_context["can_edit"] = can_edit
#         return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

# @admin.register(ShiftMaterialsDebit)
# class ShiftMaterialsDebitAdmin(admin.ModelAdmin):
#     list_display = ("doc_number", "doc_date", "author", "user", "draft", "deleted")
#     search_fields = ("doc_number", "author__username", "user__username")
