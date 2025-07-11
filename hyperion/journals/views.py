# journals/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShiftReportForm

# journals/views.py
from django.http import JsonResponse
from django.db import connection
from django.utils import timezone
from datetime import time
from tiles.models import Quality
from productions.models import Production_lines
from .models import ShiftReports, ShiftReportRow
from django.contrib.auth.decorators import login_required


@login_required
def shift_report_list(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC GetShiftReportList")
        columns = [col[0] for col in cursor.description]
        reports = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, "journals/shift_report_list.html", {"reports": reports})


@login_required
def shift_report_detail(request, doc_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
        columns = [col[0] for col in cursor.description]
        doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        shift_doc = doc_data[0] if doc_data else {}
        cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
        draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
        shift_doc["draft"] = draft

        cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    can_edit = draft or request.user.is_superuser
    return render(
        request,
        "journals/shift_report_detail.html",
        {
            "shift_doc": shift_doc,
            "shift_rows": rows,
            "can_edit": can_edit,
            "qualities": Quality.objects.all(),
        },
    )


@login_required
def shift_report_create(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            now = timezone.now()
            hour = now.hour
            is_day_shift = 9 <= hour < 21
            shift_id = 1 if is_day_shift else 2
            begin_time = time(8, 0) if is_day_shift else time(20, 0)
            end_time = time(20, 0) if is_day_shift else time(8, 0)
            foreman_name = request.user.user_name
            description = request.POST.get("description", "")

            cursor.execute(
                "EXEC AddShiftReport @doc_id OUTPUT, @doc_num OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    description,
                    now,
                    True,
                    False,
                    0,
                    request.POST.get("production_line_id", 1),
                    shift_id,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    0,
                    begin_time,
                    end_time,
                    foreman_name,
                ],
            )
            cursor.execute("SELECT @@IDENTITY AS id")
            doc_id = cursor.fetchone()[0]
            return redirect("shift_report_detail", doc_id=doc_id)
    return render(
        request,
        "journals/shift_report_form.html",
        {
            "qualities": Quality.objects.all(),
            "production_lines": Production_lines.objects.all(),
        },
    )


@login_required
def shift_report_edit(request, doc_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
        columns = [col[0] for col in cursor.description]
        doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        shift_doc = doc_data[0] if doc_data else {}
        cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
        draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
        shift_doc["draft"] = draft

    if not draft and not request.user.is_superuser:
        return render(
            request,
            "journals/shift_report_detail.html",
            {
                "shift_doc": shift_doc,
                "error": "Тільки ОТК може редагувати нечернетку!",
                "can_edit": False,
            },
        )

    if request.method == "POST":
        with connection.cursor() as cursor:
            now = timezone.now()
            hour = now.hour
            is_day_shift = 9 <= hour < 21
            shift_id = 1 if is_day_shift else 2
            begin_time = time(8, 0) if is_day_shift else time(20, 0)
            end_time = time(20, 0) if is_day_shift else time(8, 0)
            foreman_name = request.user.user_name
            description = request.POST.get("description", shift_doc.get("descr", ""))

            cursor.execute(
                "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
                [doc_id],
            )
            total = cursor.fetchone()[0] or 0

            cursor.execute(
                "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    doc_id,
                    shift_doc.get("doc_num"),
                    description,
                    shift_doc.get("doc_date", now),
                    draft,
                    shift_doc.get("imported", False),
                    shift_doc.get("parent_doc_id", 0),
                    request.POST.get(
                        "production_line_id", shift_doc.get("production_line_id", 1)
                    ),
                    shift_id,
                    request.POST.get("stoppage1", shift_doc.get("stoppage1")),
                    shift_doc.get("kiln1"),
                    request.POST.get("comments1", shift_doc.get("comment1")),
                    request.POST.get("stoppage2", shift_doc.get("stoppage2")),
                    shift_doc.get("kiln2"),
                    request.POST.get("comments2", shift_doc.get("comment2")),
                    total,
                    begin_time,
                    end_time,
                    foreman_name,
                ],
            )
            return redirect("shift_report_detail", doc_id=doc_id)

    return render(
        request,
        "journals/shift_report_form.html",
        {
            "shift_doc": shift_doc,
            "qualities": Quality.objects.all(),
            "production_lines": Production_lines.objects.all(),
            "is_edit": True,
        },
    )


@login_required
def shift_report_delete(request, doc_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
        draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
        if not draft and not request.user.is_superuser:
            return JsonResponse(
                {"error": "Тільки ОТК може видалити нечернетку!"}, status=403
            )

        if request.method == "POST":
            cursor.execute("EXEC DelShiftReport %s", [doc_id])
            return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def shift_report_row_create(request, doc_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
        draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
        if not draft and not request.user.is_superuser:
            return JsonResponse(
                {"error": "Тільки ОТК може редагувати нечернетку!"}, status=403
            )

    if request.method == "POST":
        with connection.cursor() as cursor:
            quality_id = request.POST.get("quality")
            is_defect = (
                Quality.objects.get(quality=quality_id).is_defect
                if quality_id
                else False
            )
            cursor.execute(
                "EXEC AddShiftReportRow @row_id OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    doc_id,
                    True,
                    request.POST.get("design_ean"),
                    quality_id,
                    is_defect,
                    request.POST.get("amount", 0),
                    request.POST.get("unit_id", 8),
                    request.POST.get("box_unit_id", 12),
                    request.POST.get("box_amount", 0),
                    request.POST.get("package_amount", 0),
                ],
            )
            cursor.execute("SELECT @@IDENTITY AS id")
            row_id = cursor.fetchone()[0]

            cursor.execute(
                "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
                [doc_id],
            )
            total = cursor.fetchone()[0] or 0
            cursor.execute(
                "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    doc_id,
                    shift_doc.get("doc_num"),
                    shift_doc.get("descr", ""),
                    shift_doc.get("doc_date", now),
                    draft,
                    shift_doc.get("imported", False),
                    shift_doc.get("parent_doc_id", 0),
                    shift_doc.get("production_line_id", 1),
                    shift_doc.get("shift_id", 1),
                    shift_doc.get("stoppage1"),
                    shift_doc.get("kiln1"),
                    shift_doc.get("comment1"),
                    shift_doc.get("stoppage2"),
                    shift_doc.get("kiln2"),
                    shift_doc.get("comment2"),
                    total,
                    shift_doc.get("begin_time", begin_time),
                    shift_doc.get("end_time", end_time),
                    shift_doc.get("foreman_name", foreman_name),
                ],
            )
            return JsonResponse({"row_id": row_id, "total": total})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def shift_report_row_edit(request, doc_id, row_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
        draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
        if not draft and not request.user.is_superuser:
            return JsonResponse(
                {"error": "Тільки ОТК може редагувати нечернетку!"}, status=403
            )

    if request.method == "POST":
        with connection.cursor() as cursor:
            quality_id = request.POST.get("quality")
            is_defect = (
                Quality.objects.get(quality=quality_id).is_defect
                if quality_id
                else False
            )
            cursor.execute(
                "EXEC SetShiftReportRow %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    row_id,
                    doc_id,
                    True,
                    request.POST.get("design_ean"),
                    quality_id,
                    is_defect,
                    request.POST.get("amount", 0),
                    request.POST.get("unit_id", 8),
                    request.POST.get("box_unit_id", 12),
                    request.POST.get("box_amount", 0),
                    request.POST.get("package_amount", 0),
                ],
            )
            cursor.execute(
                "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
                [doc_id],
            )
            total = cursor.fetchone()[0] or 0
            cursor.execute(
                "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    doc_id,
                    shift_doc.get("doc_num"),
                    shift_doc.get("descr", ""),
                    shift_doc.get("doc_date", now),
                    draft,
                    shift_doc.get("imported", False),
                    shift_doc.get("parent_doc_id", 0),
                    shift_doc.get("production_line_id", 1),
                    shift_doc.get("shift_id", 1),
                    shift_doc.get("stoppage1"),
                    shift_doc.get("kiln1"),
                    shift_doc.get("comment1"),
                    shift_doc.get("stoppage2"),
                    shift_doc.get("kiln2"),
                    shift_doc.get("comment2"),
                    total,
                    shift_doc.get("begin_time", begin_time),
                    shift_doc.get("end_time", end_time),
                    shift_doc.get("foreman_name", foreman_name),
                ],
            )
            return JsonResponse({"row_id": row_id, "total": total})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def shift_report_row_delete(request, doc_id, row_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
        draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
        if not draft and not request.user.is_superuser:
            return JsonResponse(
                {"error": "Тільки ОТК може видалити нечернетку!"}, status=403
            )

    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("EXEC DelShiftReportRow %s", [row_id])
            cursor.execute(
                "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
                [doc_id],
            )
            total = cursor.fetchone()[0] or 0
            cursor.execute(
                "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
                [
                    doc_id,
                    shift_doc.get("doc_num"),
                    shift_doc.get("descr", ""),
                    shift_doc.get("doc_date", now),
                    draft,
                    shift_doc.get("imported", False),
                    shift_doc.get("parent_doc_id", 0),
                    shift_doc.get("production_line_id", 1),
                    shift_doc.get("shift_id", 1),
                    shift_doc.get("stoppage1"),
                    shift_doc.get("kiln1"),
                    shift_doc.get("comment1"),
                    shift_doc.get("stoppage2"),
                    shift_doc.get("kiln2"),
                    shift_doc.get("comment2"),
                    total,
                    shift_doc.get("begin_time", begin_time),
                    shift_doc.get("end_time", end_time),
                    shift_doc.get("foreman_name", foreman_name),
                ],
            )
            return JsonResponse({"success": True, "total": total})
    return JsonResponse({"error": "Invalid request"}, status=400)
