# journals/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import ShiftReports
from .forms import ShiftReportForm


def shift_report_list(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC GetShiftReportList")
        columns = [col[0] for col in cursor.description]
        reports = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, "journals/shift_report_list.html", {"reports": reports})


def shift_report_detail(request, doc_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
        columns = [col[0] for col in cursor.description]
        doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        shift_doc = doc_data[0] if doc_data else {}

        cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(
        request,
        "journals/shift_report_detail.html",
        {
            "shift_doc": shift_doc,
            "shift_rows": rows,
        },
    )


def shift_report_create(request):
    if request.method == "POST":
        form = ShiftReportForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "EXEC AddShiftReport %s, %s, %s",
                    [
                        form.cleaned_data["doc_number"],
                        form.cleaned_data["author"],
                        form.cleaned_data["doc_date"],
                    ],
                )
                cursor.execute("SELECT @@IDENTITY AS id")
                doc_id = cursor.fetchone()[0]
                return redirect("shift_report_detail", doc_id=doc_id)
    else:
        form = ShiftReportForm()
    return render(request, "journals/shift_report_form.html", {"form": form})
# journals/views.py
def shift_report_row_create(request, doc_id):
    if request.method == "POST":
        form = ShiftReportRowForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "EXEC AddShiftReportRow %s, %s, %s",
                    [
                        doc_id,
                        form.cleaned_data["product_id"],
                        form.cleaned_data["quantity"],
                    ],
                )
            return redirect("shift_report_detail", doc_id=doc_id)
    else:
        form = ShiftReportRowForm()
    return render(
        request, "journals/shift_report_row_form.html", {"form": form, "doc_id": doc_id}
    )


def shift_report_edit(request, doc_id):
    report = get_object_or_404(ShiftReports, id=doc_id)
    if request.method == "POST":
        form = ShiftReportForm(request.POST, instance=report)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "EXEC SetShiftReport %s, %s, %s, %s",
                    [
                        doc_id,
                        form.cleaned_data["doc_number"],
                        form.cleaned_data["author"],
                        form.cleaned_data["doc_date"],
                    ],
                )
            return redirect("shift_report_detail", doc_id=doc_id)
    else:
        form = ShiftReportForm(instance=report)
    return render(request, "journals/shift_report_form.html", {"form": form})


def shift_report_delete(request, doc_id):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("EXEC DelShiftReport %s", [doc_id])
        return redirect("shift_report_list")
    return render(
        request, "journals/shift_report_confirm_delete.html", {"doc_id": doc_id}
    )
