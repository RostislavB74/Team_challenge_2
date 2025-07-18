from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from tiles.models import Designs
from units.models import ProductUnits, Units
from productions.models import Snap_types_to_lines
from productions.models import Production_lines
import logging


logger = logging.getLogger(__name__)


@login_required
def shift_report_detail(request, doc_id):
    logger.debug(f"Accessing shift_report_detail with doc_id={doc_id}")
    try:
        with connection.cursor() as cursor:
            # Отримання даних звіту
            logger.debug("Executing GetShiftReportDoc")
            cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
            columns = [col[0] for col in cursor.description]
            doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            if not doc_data:
                logger.warning(f"No data for doc_id={doc_id}")
                return render(
                    request,
                    "journals/shift_report_detail.html",
                    {"error": f"Звіт з doc_id={doc_id} не знайдено", "can_edit": False},
                )
            shift_doc = doc_data[0]
            production_line_id = shift_doc.get("production_line_id", 0)

            # Отримання назви лінії
            if Production_lines:
                try:
                    production_line = Production_lines.objects.get(
                        id=production_line_id
                    )
                    shift_doc["line_name"] = production_line.name
                except Production_lines.DoesNotExist:
                    shift_doc["line_name"] = str(production_line_id)
            else:
                # Запасний варіант: SQL-запит
                logger.warning(
                    "Production_lines model not available, using SQL fallback"
                )
                cursor.execute(
                    "SELECT production_line FROM c_production_line WHERE production_line_id = %s",
                    [production_line_id],
                )
                result = cursor.fetchone()
                shift_doc["line_name"] = (
                    result[0] if result else str(production_line_id)
                )

            # Перевірка draft
            logger.debug("Checking draft")
            cursor.execute(
                "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
            )
            draft_result = cursor.fetchone()
            if not draft_result:
                logger.warning(f"No draft data for doc_id={doc_id}")
                return render(
                    request,
                    "journals/shift_report_detail.html",
                    {"error": f"Звіт з doc_id={doc_id} не існує", "can_edit": False},
                )
            shift_doc["draft"] = draft_result[0]

            # Отримання рядків звіту
            logger.debug("Executing GetShiftReportRowsForDjango")
            cursor.execute("EXEC GetShiftReportRowsForDjango %s", [doc_id])
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            logger.debug(f"Rows returned: {len(rows)}")
            for row in rows:
                logger.debug(
                    f"Row {row['row_id']}: amount={row['amount']}, type={type(row['amount'])}, "
                    f"box_amount={row['box_amount']}, type={type(row['box_amount'])}, "
                    f"package_amount={row['package_amount']}, type={type(row['package_amount'])}, "
                    f"package_square={row.get('package_square', 'N/A')}"
                )

            # Отримання назв дизайнів
            if rows:
                design_eans = list(
                    set(row["design_ean"] for row in rows if row.get("design_ean"))
                )
                cache_key = f"designs_{doc_id}_{production_line_id}"
                design_data = cache.get(cache_key)
                if not design_data:
                    logger.debug(f"Fetching designs for design_eans={design_eans}")
                    designs = (
                        Designs.objects.filter(
                            design_ean__in=design_eans,
                            tile_type_id__in=Snap_types_to_lines.objects.filter(
                                production_line_id=production_line_id
                            )
                            .values_list("name_id", flat=True)
                            .distinct(),
                        )
                        .values(
                            "design_ean",
                            "design_name",
                            "tile_type_id",
                            "package_square",
                        )
                        .distinct()
                    )
                    design_data = {d["design_ean"]: d for d in designs}
                    cache.set(cache_key, design_data, 3600)
                for row in rows:
                    row["design_name"] = design_data.get(row["design_ean"], {}).get(
                        "design_name", "Немає назви"
                    )

            # Отримання простоїв
            logger.debug("Fetching downtimes")
            cursor.execute(
                """
                SELECT dr2.row_id, ck.kiln AS kiln_name, dr2.amount, dr2.stoppage_cause_type_id, dr2.stoppage_cause, dr2.comment,
                       CONCAT('Тип: ', dr2.stoppage_cause_type_id, ', Причина: ', dr2.stoppage_cause, ', Опис: ', ISNULL(dr2.comment, '')) AS downtime_summary
                FROM dr2_shift_report dr2
                INNER JOIN cu_kiln ck ON dr2.kiln_id = ck.kiln_id
                WHERE dr2.doc_id = %s AND ck.production_line_id = %s
            """,
                [doc_id, production_line_id],
            )
            downtime_columns = [col[0] for col in cursor.description]
            downtimes = [dict(zip(downtime_columns, row)) for row in cursor.fetchall()]
            logger.debug(f"Downtimes returned: {len(downtimes)}")

            # Отримання першого дизайну
            default_design = (
                Designs.objects.filter(
                    tile_type_id__in=Snap_types_to_lines.objects.filter(
                        production_line_id=production_line_id
                    )
                    .values("name_id")
                    .distinct()
                )
                .order_by("design_ean")
                .first()
            )

        can_edit = shift_doc["draft"] or request.user.is_superuser
        logger.debug(f"Can edit: {can_edit}")
        return render(
            request,
            "journals/shift_report_detail.html",
            {
                "shift_doc": shift_doc,
                "shift_rows": rows,
                "downtimes": downtimes,
                "can_edit": can_edit,
                "default_design": default_design,
            },
        )
    except Exception as e:
        logger.error(f"Error in shift_report_detail: {str(e)}")
        return render(
            request,
            "journals/shift_report_detail.html",
            {"error": f"Помилка: {str(e)}", "can_edit": False},
        )


# ... (add_row, edit_row, delete_row без змін) ...

@login_required
def add_row(request, doc_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        box_amount = request.POST.get('box_amount')
        design_ean = request.POST.get('design_ean')
        quality = request.POST.get('quality', 'S')
        is_defect = request.POST.get('is_defect', '0')

        design = Designs.objects.filter(design_ean=design_ean).values('tile_type_id', 'package_square').first()
        tile_type_id = design['tile_type_id'] if design else None
        package_square = design['package_square'] if design and design['package_square'] else 1.0

        product_unit = ProductUnits.objects.filter(
            tile_type_id=tile_type_id,
            basic=True
        ).select_related('unit_id').first()
        unit_id = product_unit.unit_id.unit_id if product_unit else None
        package_amount = float(amount) / package_square if design and amount and package_square else 0

        logger.debug(f"Adding row: doc_id={doc_id}, design_ean={design_ean}, amount={amount}, "
                    f"package_square={package_square}, package_amount={package_amount}")

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dr_shift_report (doc_id, design_ean, quality, is_defect, amount, unit_id, box_amount, package_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [doc_id, design_ean, quality, is_defect, amount, unit_id, box_amount, package_amount])
        return redirect(f'/shift-reports/{doc_id}/')

    with connection.cursor() as cursor:
        cursor.execute("SELECT production_line_id FROM d_shift_report WHERE doc_id = %s", [doc_id])
        production_line_id = cursor.fetchone()[0]
    default_design = Designs.objects.filter(
        tile_type_id__in=Snap_types_to_lines.objects.filter(
            production_line_id=production_line_id
        ).values('name_id').distinct()
    ).order_by('design_ean').first()

    return render(request, 'journals/add_row.html', {
        'doc_id': doc_id,
        'default_design': default_design,
    })

@login_required
def edit_row(request, doc_id, row_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        box_amount = request.POST.get('box_amount')

        with connection.cursor() as cursor:
            cursor.execute("SELECT design_ean FROM dr_shift_report WHERE row_id = %s", [row_id])
            design_ean = cursor.fetchone()[0]
        design = Designs.objects.filter(design_ean=design_ean).values('tile_type_id', 'package_square').first()
        tile_type_id = design['tile_type_id'] if design else None
        package_square = design['package_square'] if design and design['package_square'] else 1.0

        product_unit = ProductUnits.objects.filter(
            tile_type_id=tile_type_id,
            basic=True
        ).select_related('unit_id').first()
        package_amount = float(amount) / package_square if design and amount and package_square else 0

        logger.debug(f"Editing row: row_id={row_id}, doc_id={doc_id}, design_ean={design_ean}, amount={amount}, "
                    f"package_square={package_square}, package_amount={package_amount}")

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE dr_shift_report
                SET amount = %s, box_amount = %s, package_amount = %s
                WHERE row_id = %s
            """, [amount, box_amount, package_amount, row_id])
        return redirect(f'/shift-reports/{doc_id}/')

    with connection.cursor() as cursor:
        cursor.execute("SELECT row_id, design_ean, quality, is_defect, amount, box_amount FROM dr_shift_report WHERE row_id = %s", [row_id])
        columns = [col[0] for col in cursor.description]
        row = dict(zip(columns, cursor.fetchone()))
    return render(request, 'journals/edit_row.html', {
        'doc_id': doc_id,
        'row': row,
    })

@login_required
def delete_row(request, doc_id, row_id):
    logger.debug(f"Deleting row: row_id={row_id}, doc_id={doc_id}")
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM dr_shift_report WHERE row_id = %s", [row_id])
    return redirect(f'/shift-reports/{doc_id}/')

# @login_required
# def shift_report_detail(request, doc_id):
#     logger.debug(f"Accessing shift_report_detail with doc_id={doc_id}")
#     try:
#         with connection.cursor() as cursor:
#             # Отримання даних звіту
#             logger.debug("Executing GetShiftReportDoc")
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             if not doc_data:
#                 logger.warning(f"No data for doc_id={doc_id}")
#                 return render(request, 'journals/shift_report_detail.html', {
#                     'error': f'Звіт з doc_id={doc_id} не знайдено',
#                     'can_edit': False
#                 })
#             shift_doc = doc_data[0]
#             production_line_id = shift_doc.get('production_line_id')

#             # Перевірка draft
#             logger.debug("Checking draft")
#             cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
#             draft_result = cursor.fetchone()
#             if not draft_result:
#                 logger.warning(f"No draft data for doc_id={doc_id}")
#                 return render(request, 'journals/shift_report_detail.html', {
#                     'error': f'Звіт з doc_id={doc_id} не існує',
#                     'can_edit': False
#                 })
#             shift_doc['draft'] = draft_result[0]

#             # Отримання рядків звіту
#             logger.debug("Executing GetShiftReportRowsForDjango")
#             cursor.execute("EXEC GetShiftReportRowsForDjango %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             logger.debug(f"Rows returned: {len(rows)}")
#             for row in rows:
#                 logger.debug(f"Row {row['row_id']}: amount={row['amount']}, type={type(row['amount'])}, "
#                              f"package_amount={row['package_amount']}, type={type(row['package_amount'])}, "
#                              f"box_amount={row['box_amount']}, type={type(row['box_amount'])}")
# # @login_required
# # def shift_report_detail(request, doc_id):
# #     logger.debug(f"Accessing shift_report_detail with doc_id={doc_id}")
# #     try:
# #         with connection.cursor() as cursor:
# #             # Отримання даних звіту
# #             logger.debug("Executing GetShiftReportDoc")
# #             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
# #             columns = [col[0] for col in cursor.description]
# #             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
# #             if not doc_data:
# #                 logger.warning(f"No data for doc_id={doc_id}")
# #                 return render(
# #                     request,
# #                     "journals/shift_report_detail.html",
# #                     {"error": f"Звіт з doc_id={doc_id} не знайдено", "can_edit": False},
# #                 )
# #             shift_doc = doc_data[0]
# #             production_line_id = shift_doc.get("production_line_id")

# #             # Перевірка draft
# #             logger.debug("Checking draft")
# #             cursor.execute(
# #                 "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
# #             )
# #             draft_result = cursor.fetchone()
# #             if not draft_result:
# #                 logger.warning(f"No draft data for doc_id={doc_id}")
# #                 return render(
# #                     request,
# #                     "journals/shift_report_detail.html",
# #                     {"error": f"Звіт з doc_id={doc_id} не існує", "can_edit": False},
# #                 )
# #             shift_doc["draft"] = draft_result[0]

# #             # Отримання рядків звіту
# #             logger.debug("Executing GetShiftReportRowsForDjango")
# #             cursor.execute("EXEC GetShiftReportRowsForDjango %s", [doc_id])
# #             columns = [col[0] for col in cursor.description]
# #             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
# #             logger.debug(f"Rows returned: {len(rows)}")

#             # Отримання назв дизайнів
#             if rows:
#                 design_eans = list(
#                     set(row["design_ean"] for row in rows if row.get("design_ean"))
#                 )  # Уникнення дублювання
#                 tile_type_ids = (
#                     Snap_types_to_lines.objects.filter(
#                         production_line_id=production_line_id
#                     )
#                     .values_list("name_id", flat=True)
#                     .distinct()
#                 )
#                 if design_eans and tile_type_ids:
#                     cache_key = f"designs_{doc_id}_{production_line_id}"
#                     design_data = cache.get(cache_key)
#                     if not design_data:
#                         logger.debug(
#                             f"Fetching designs for tile_type_ids={tile_type_ids}"
#                         )
#                         designs = (
#                             Designs.objects.filter(
#                                 design_ean__in=design_eans,
#                                 tile_type_id__in=tile_type_ids,
#                             )
#                             .values("design_ean", "design_name", "tile_type_id")
#                             .distinct()
#                         )
#                         design_data = {d["design_ean"]: d for d in designs}
#                         cache.set(cache_key, design_data, 3600)
#                     for row in rows:
#                         row["design_name"] = design_data.get(row["design_ean"], {}).get(
#                             "design_name", "Немає назви"
#                         )

#             # Отримання простоїв
#             logger.debug("Fetching downtimes")
#             cursor.execute(
#                 "SELECT row_id, kiln_id, amount, stoppage_cause_type_id, stoppage_cause, comment FROM dr2_shift_report WHERE doc_id = %s",
#                 [doc_id],
#             )
#             downtime_columns = [col[0] for col in cursor.description]
#             downtimes = [dict(zip(downtime_columns, row)) for row in cursor.fetchall()]

#             # Отримання першого дизайну
#             default_design = (
#                 Designs.objects.filter(
#                     tile_type_id__in=Snap_types_to_lines.objects.filter(
#                         production_line_id=production_line_id
#                     )
#                     .values("name_id")
#                     .distinct()
#                 )
#                 .order_by("design_ean")
#                 .first()
#             )

#         can_edit = shift_doc["draft"] or request.user.is_superuser
#         logger.debug(f"Can edit: {can_edit}")
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {
#                 "shift_doc": shift_doc,
#                 "shift_rows": rows,
#                 "downtimes": downtimes,
#                 "can_edit": can_edit,
#                 "default_design": default_design,
#             },
#         )
#     except Exception as e:
#         logger.error(f"Error in shift_report_detail: {str(e)}")
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {"error": f"Помилка: {str(e)}", "can_edit": False},
#         )


# @login_required
# def add_row(request, doc_id):
#     if request.method == "POST":
#         amount = request.POST.get("amount")
#         box_amount = request.POST.get("box_amount")
#         design_ean = request.POST.get("design_ean")
#         quality = request.POST.get("quality", "S")
#         is_defect = request.POST.get("is_defect", "0")

#         # Отримання tile_type_id для дизайну
#         design = (
#             Designs.objects.filter(design_ean=design_ean).values("tile_type_id").first()
#         )
#         tile_type_id = design["tile_type_id"] if design else None

#         # Отримання базової одиниці виміру
#         product_unit = (
#             ProductUnits.objects.filter(tile_type_id=tile_type_id, basic=True)
#             .select_related("unit_id")
#             .first()
#         )
#         unit_id = (
#             product_unit.unit_id.unit_id if product_unit else None
#         )  # Без fallback до 8
#         package_amount = (
#             float(amount) / product_unit.course if product_unit and amount else 0
#         )

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 INSERT INTO dr_shift_report (doc_id, design_ean, quality, is_defect, amount, unit_id, box_amount, package_amount)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """,
#                 [
#                     doc_id,
#                     design_ean,
#                     quality,
#                     is_defect,
#                     amount,
#                     unit_id,
#                     box_amount,
#                     package_amount,
#                 ],
#             )
#         return redirect(f"/shift-reports/{doc_id}/")

#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT production_line_id FROM d_shift_report WHERE doc_id = %s", [doc_id]
#         )
#         production_line_id = cursor.fetchone()[0]
#     default_design = (
#         Designs.objects.filter(
#             tile_type_id__in=Snap_types_to_lines.objects.filter(
#                 production_line_id=production_line_id
#             )
#             .values("name_id")
#             .distinct()
#         )
#         .order_by("design_ean")
#         .first()
#     )

#     return render(
#         request,
#         "journals/add_row.html",
#         {
#             "doc_id": doc_id,
#             "default_design": default_design,
#         },
#     )


# @login_required
# def edit_row(request, doc_id, row_id):
#     if request.method == "POST":
#         amount = request.POST.get("amount")
#         box_amount = request.POST.get("box_amount")

#         # Отримання design_ean і tile_type_id для рядка
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT design_ean FROM dr_shift_report WHERE row_id = %s", [row_id]
#             )
#             design_ean = cursor.fetchone()[0]
#         design = (
#             Designs.objects.filter(design_ean=design_ean).values("tile_type_id").first()
#         )
#         tile_type_id = design["tile_type_id"] if design else None

#         # Обчислення package_amount
#         product_unit = (
#             ProductUnits.objects.filter(tile_type_id=tile_type_id, basic=True)
#             .select_related("unit_id")
#             .first()
#         )
#         package_amount = (
#             float(amount) / product_unit.course if product_unit and amount else 0
#         )

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 UPDATE dr_shift_report
#                 SET amount = %s, box_amount = %s, package_amount = %s
#                 WHERE row_id = %s
#             """,
#                 [amount, box_amount, package_amount, row_id],
#             )
#         return redirect(f"/shift-reports/{doc_id}/")

#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT row_id, design_ean, quality, is_defect, amount, box_amount FROM dr_shift_report WHERE row_id = %s",
#             [row_id],
#         )
#         columns = [col[0] for col in cursor.description]
#         row = dict(zip(columns, cursor.fetchone()))
#     return render(
#         request,
#         "journals/edit_row.html",
#         {
#             "doc_id": doc_id,
#             "row": row,
#         },
#     )


# @login_required
# def delete_row(request, doc_id, row_id):
#     with connection.cursor() as cursor:
#         cursor.execute("DELETE FROM dr_shift_report WHERE row_id = %s", [row_id])
#     return redirect(f"/shift-reports/{doc_id}/")


# @login_required
# def shift_report_detail(request, doc_id):
#     logger.debug(f"Accessing shift_report_detail with doc_id={doc_id}")
#     try:
#         with connection.cursor() as cursor:
#             # Отримання даних звіту
#             logger.debug("Executing GetShiftReportDoc")
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             if not doc_data:
#                 logger.warning(f"No data for doc_id={doc_id}")
#                 return render(
#                     request,
#                     "journals/shift_report_detail.html",
#                     {"error": f"Звіт з doc_id={doc_id} не знайдено", "can_edit": False},
#                 )
#             shift_doc = doc_data[0]
#             production_line_id = shift_doc.get("production_line_id")

#             # Перевірка draft
#             logger.debug("Checking draft")
#             cursor.execute(
#                 "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
#             )
#             draft_result = cursor.fetchone()
#             if not draft_result:
#                 logger.warning(f"No draft data for doc_id={doc_id}")
#                 return render(
#                     request,
#                     "journals/shift_report_detail.html",
#                     {"error": f"Звіт з doc_id={doc_id} не існує", "can_edit": False},
#                 )
#             shift_doc["draft"] = draft_result[0]

#             # Отримання рядків звіту
#             logger.debug("Executing GetShiftReportRowsForDjango")
#             cursor.execute("EXEC GetShiftReportRowsForDjango %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             logger.debug(f"Rows returned: {len(rows)}")

#             # Отримання назв дизайнів
#             if rows:
#                 design_eans = list(
#                     set(row["design_ean"] for row in rows if row.get("design_ean"))
#                 )  # Уникнення дублювання
#                 tile_type_ids = (
#                     Snap_types_to_lines.objects.filter(
#                         production_line_id=production_line_id
#                     )
#                     .values_list("name_id", flat=True)
#                     .distinct()
#                 )
#                 if design_eans and tile_type_ids:
#                     cache_key = f"designs_{doc_id}_{production_line_id}"
#                     design_data = cache.get(cache_key)
#                     if not design_data:
#                         logger.debug(
#                             f"Fetching designs for tile_type_ids={tile_type_ids}"
#                         )
#                         designs = (
#                             Designs.objects.filter(
#                                 design_ean__in=design_eans,
#                                 tile_type_id__in=tile_type_ids,
#                             )
#                             .values("design_ean", "design_name", "tile_type_id")
#                             .distinct()
#                         )
#                         design_data = {d["design_ean"]: d for d in designs}
#                         cache.set(cache_key, design_data, 3600)
#                     for row in rows:
#                         row["design_name"] = design_data.get(row["design_ean"], {}).get(
#                             "design_name", "Немає назви"
#                         )

#             # Отримання простоїв
#             logger.debug("Fetching downtimes")
#             cursor.execute(
#                 "SELECT row_id, kiln_id, amount, stoppage_cause_type_id, stoppage_cause, comment FROM dr2_shift_report WHERE doc_id = %s",
#                 [doc_id],
#             )
#             downtime_columns = [col[0] for col in cursor.description]
#             downtimes = [dict(zip(downtime_columns, row)) for row in cursor.fetchall()]

#             # Отримання першого дизайну
#             default_design = (
#                 Designs.objects.filter(
#                     tile_type_id__in=Snap_types_to_lines.objects.filter(
#                         production_line_id=production_line_id
#                     )
#                     .values("name_id")
#                     .distinct()
#                 )
#                 .order_by("design_ean")
#                 .first()
#             )

#         can_edit = shift_doc["draft"] or request.user.is_superuser
#         logger.debug(f"Can edit: {can_edit}")
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {
#                 "shift_doc": shift_doc,
#                 "shift_rows": rows,
#                 "downtimes": downtimes,
#                 "can_edit": can_edit,
#                 "default_design": default_design,
#             },
#         )
#     except Exception as e:
#         logger.error(f"Error in shift_report_detail: {str(e)}")
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {"error": f"Помилка: {str(e)}", "can_edit": False},
#         )


# @login_required
# def add_row(request, doc_id):
#     if request.method == "POST":
#         amount = request.POST.get("amount")
#         box_amount = request.POST.get("box_amount")
#         design_ean = request.POST.get("design_ean")
#         quality = request.POST.get("quality", "S")
#         is_defect = request.POST.get("is_defect", "0")

#         # Отримання tile_type_id для дизайну
#         design = (
#             Designs.objects.filter(design_ean=design_ean).values("tile_type_id").first()
#         )
#         tile_type_id = design["tile_type_id"] if design else None

#         # Отримання базової одиниці виміру
#         product_unit = (
#             ProductUnits.objects.filter(tile_type_id=tile_type_id, basic=True)
#             .select_related("unit_id")
#             .first()
#         )
#         unit_id = (
#             product_unit.unit_id.unit_id if product_unit else None
#         )  # Без fallback до 8
#         package_amount = (
#             float(amount) / product_unit.course if product_unit and amount else 0
#         )

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 INSERT INTO dr_shift_report (doc_id, design_ean, quality, is_defect, amount, unit_id, box_amount, package_amount)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """,
#                 [
#                     doc_id,
#                     design_ean,
#                     quality,
#                     is_defect,
#                     amount,
#                     unit_id,
#                     box_amount,
#                     package_amount,
#                 ],
#             )
#         return redirect(f"/shift-reports/{doc_id}/")

#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT production_line_id FROM d_shift_report WHERE doc_id = %s", [doc_id]
#         )
#         production_line_id = cursor.fetchone()[0]
#     default_design = (
#         Designs.objects.filter(
#             tile_type_id__in=Snap_types_to_lines.objects.filter(
#                 production_line_id=production_line_id
#             )
#             .values("name_id")
#             .distinct()
#         )
#         .order_by("design_ean")
#         .first()
#     )

#     return render(
#         request,
#         "journals/add_row.html",
#         {
#             "doc_id": doc_id,
#             "default_design": default_design,
#         },
#     )


# @login_required
# def edit_row(request, doc_id, row_id):
#     if request.method == "POST":
#         amount = request.POST.get("amount")
#         box_amount = request.POST.get("box_amount")

#         # Отримання design_ean і tile_type_id для рядка
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT design_ean FROM dr_shift_report WHERE row_id = %s", [row_id]
#             )
#             design_ean = cursor.fetchone()[0]
#         design = (
#             Designs.objects.filter(design_ean=design_ean).values("tile_type_id").first()
#         )
#         tile_type_id = design["tile_type_id"] if design else None

#         # Обчислення package_amount
#         product_unit = (
#             ProductUnits.objects.filter(tile_type_id=tile_type_id, basic=True)
#             .select_related("unit_id")
#             .first()
#         )
#         package_amount = (
#             float(amount) / product_unit.course if product_unit and amount else 0
#         )

#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 UPDATE dr_shift_report
#                 SET amount = %s, box_amount = %s, package_amount = %s
#                 WHERE row_id = %s
#             """,
#                 [amount, box_amount, package_amount, row_id],
#             )
#         return redirect(f"/shift-reports/{doc_id}/")

#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT row_id, design_ean, quality, is_defect, amount, box_amount FROM dr_shift_report WHERE row_id = %s",
#             [row_id],
#         )
#         columns = [col[0] for col in cursor.description]
#         row = dict(zip(columns, cursor.fetchone()))
#     return render(
#         request,
#         "journals/edit_row.html",
#         {
#             "doc_id": doc_id,
#             "row": row,
#         },
#     )


# @login_required
# def delete_row(request, doc_id, row_id):
#     with connection.cursor() as cursor:
#         cursor.execute("DELETE FROM dr_shift_report WHERE row_id = %s", [row_id])
#     return redirect(f"/shift-reports/{doc_id}/")


# from django.shortcuts import render, redirect
# from django.db import connection
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse, HttpResponse
# from tiles.models import Designs
# import logging
# import openpyxl
# from openpyxl.utils import get_column_letter
# from datetime import datetime

# logger = logging.getLogger(__name__)


# @login_required
# def shift_report_detail(request, doc_id):
#     logger.debug(f"Accessing shift_report_detail with doc_id={doc_id}")
#     try:
#         with connection.cursor() as cursor:
#             # Отримання даних звіту
#             logger.debug("Executing GetShiftReportDoc")
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             if not doc_data:
#                 logger.warning(f"No data for doc_id={doc_id}")
#                 return render(
#                     request,
#                     "journals/shift_report_detail.html",
#                     {"error": f"Звіт з doc_id={doc_id} не знайдено", "can_edit": False},
#                 )
#             shift_doc = doc_data[0]

#             # Перевірка draft
#             logger.debug("Checking draft")
#             cursor.execute(
#                 "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
#             )
#             draft_result = cursor.fetchone()
#             if not draft_result:
#                 logger.warning(f"No draft data for doc_id={doc_id}")
#                 return render(
#                     request,
#                     "journals/shift_report_detail.html",
#                     {"error": f"Звіт з doc_id={doc_id} не існує", "can_edit": False},
#                 )
#             shift_doc["draft"] = draft_result[0]

#             # Отримання рядків звіту
#             logger.debug("Executing GetShiftReportRows")
#             cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             logger.debug(f"Rows returned: {rows}")

#             # Отримання назв дизайнів через ORM
#             if rows:
#                 design_eans = [
#                     row["design_ean"] for row in rows if row.get("design_ean")
#                 ]
#                 if design_eans:
#                     designs = Designs.objects.filter(design_ean__in=design_eans).values(
#                         "design_ean", "design_name"
#                     )
#                     design_data = {d["design_ean"]: d["design_name"] for d in designs}
#                     for row in rows:
#                         row["design_name"] = design_data.get(
#                             row["design_ean"], "Немає назви"
#                         )

#             # Отримання простоїв
#             logger.debug("Fetching downtimes")
#             cursor.execute(
#                 "SELECT row_id, kiln_id, amount, stoppage_cause_type_id, stoppage_cause, comment FROM dr2_shift_report WHERE doc_id = %s",
#                 [doc_id],
#             )
#             downtime_columns = [col[0] for col in cursor.description]
#             downtimes = [dict(zip(downtime_columns, row)) for row in cursor.fetchall()]

#         can_edit = shift_doc["draft"] or request.user.is_superuser
#         logger.debug(f"Can edit: {can_edit}")
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {
#                 "shift_doc": shift_doc,
#                 "shift_rows": rows,
#                 "downtimes": downtimes,
#                 "can_edit": can_edit,
#             },
#         )
#     except Exception as e:
#         logger.error(f"Error in shift_report_detail: {str(e)}")
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {"error": f"Помилка: {str(e)}", "can_edit": False},
#         )


# @login_required
# def get_designs(request):
#     try:
#         designs = Designs.objects.values("design_ean", "design_name")
#         return JsonResponse({"designs": list(designs)})
#     except Exception as e:
#         logger.error(f"Error in get_designs: {str(e)}")
#         return JsonResponse({"error": str(e)}, status=500)


# @login_required
# def shift_report_print(request, doc_id):
#     try:
#         with connection.cursor() as cursor:
#             # Отримання даних звіту
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             if not doc_data:
#                 return HttpResponse("Звіт не знайдено", status=404)
#             shift_doc = doc_data[0]

#             # Отримання рядків
#             cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             design_eans = [row["design_ean"] for row in rows if row.get("design_ean")]
#             designs = Designs.objects.filter(design_ean__in=design_eans).select_related('tile_type', 'color').values('design_ean', 'design_name')
#             # designs = Designs.objects.filter(design_ean__in=design_eans).values(
#             #     "design_ean", "design_name"

#             design_data = {d["design_ean"]: d["design_name"] for d in designs}
#             for row in rows:
#                 row["design_name"] = design_data.get(row["design_ean"], "Немає назви")

#             # Отримання простоїв
#             cursor.execute(
#                 "SELECT row_id, kiln_id, amount, stoppage_cause_type_id, stoppage_cause, comment FROM dr2_shift_report WHERE doc_id = %s",
#                 [doc_id],
#             )
#             downtime_columns = [col[0] for col in cursor.description]
#             downtimes = [dict(zip(downtime_columns, row)) for row in cursor.fetchall()]

#         # Створення XLS
#         workbook = openpyxl.Workbook()
#         sheet = workbook.active
#         sheet.title = "Звіт зміни"

#         # Заголовок
#         sheet["A1"] = "Отчет смены"
#         sheet["A3"] = f"Звіт № {shift_doc.get('doc_num', '')}"
#         sheet["A4"] = f"від {shift_doc.get('doc_date', '')}"
#         sheet["A5"] = f"Зміна: {shift_doc.get('shift_id', '')}"
#         sheet["A6"] = f"Лінія: {shift_doc.get('production_line_id', '')}"
#         shift_time = (
#             f"{shift_doc.get('begin_time', '')} - {shift_doc.get('end_time', '')}"
#         )
#         sheet["A7"] = f"Час роботи: {shift_time}"

#         # Таблиця рядків
#         headers = [
#             "№",
#             "Продукція",
#             "Сорт",
#             "Брак",
#             "Кількість",
#             "Од. вим.",
#             "Примітка",
#         ]
#         for col, header in enumerate(headers, 1):
#             sheet[f"{get_column_letter(col)}9"] = header
#         for row_idx, row in enumerate(rows, 10):
#             sheet[f"A{row_idx}"] = row_idx - 9
#             sheet[f"B{row_idx}"] = row.get("design_name", "Немає назви")
#             sheet[f"C{row_idx}"] = row.get("quality", "")
#             sheet[f"D{row_idx}"] = "Так" if row.get("is_defect") else "Ні"
#             sheet[f"E{row_idx}"] = row.get("amount", 0)
#             sheet[f"F{row_idx}"] = row.get("unit_id", "")
#             sheet[f"G{row_idx}"] = ""

#         # Підсумки
#         total_row = len(rows) + 11
#         sheet[f"A{total_row}"] = "Всього:"
#         sheet[f"E{total_row}"] = shift_doc.get("total", 0)
#         sheet[f"A{total_row + 1}"] = "Всього без браку:"
#         sheet[f"E{total_row + 1}"] = sum(
#             row["amount"] for row in rows if not row.get("is_defect")
#         )
#         sheet[f"A{total_row + 2}"] = "Всього найменувань:"
#         sheet[f"E{total_row + 2}"] = len(rows)

#         # Простої
#         downtime_start = total_row + 4
#         sheet[f"A{downtime_start}"] = "Зауваження:"
#         sheet[f"A{downtime_start + 1}"] = "Піч"
#         sheet[f"B{downtime_start + 1}"] = "Простій, хв"
#         sheet[f"C{downtime_start + 1}"] = "Вид причини"
#         sheet[f"D{downtime_start + 1}"] = "Причина"
#         for idx, downtime in enumerate(downtimes, downtime_start + 2):
#             sheet[f"A{idx}"] = downtime.get("kiln_id", "")
#             sheet[f"B{idx}"] = downtime.get("amount", 0)
#             sheet[f"C{idx}"] = downtime.get("stoppage_cause_type_id", "")
#             sheet[f"D{idx}"] = downtime.get("stoppage_cause", "")

#         # Майстер
#         sheet[f"A{downtime_start + len(downtimes) + 3}"] = (
#             f"Майстер ____________________ {shift_doc.get('foreman_name', '')}"
#         )

#         # Вихід XLS
#         response = HttpResponse(
#             content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
#         response["Content-Disposition"] = (
#             f"attachment; filename=shift_report_{doc_id}.xlsx"
#         )
#         workbook.save(response)
#         return response
#     except Exception as e:
#         logger.error(f"Error in shift_report_print: {str(e)}")
#         return HttpResponse(f"Помилка: {str(e)}", status=500)


# # journals/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import ShiftReportForm

# # journals/views.py
# from django.http import JsonResponse
# from django.db import connection
# from django.utils import timezone
# from datetime import time
# from tiles.models import Quality
# from productions.models import Production_lines
# from .models import ShiftReports, ShiftReportRow
# from django.contrib.auth.decorators import login_required


# @login_required
# def shift_report_list(request):
#     with connection.cursor() as cursor:
#         cursor.execute("EXEC GetShiftReportList")
#         columns = [col[0] for col in cursor.description]
#         reports = [dict(zip(columns, row)) for row in cursor.fetchall()]
#     return render(request, "journals/shift_report_list.html", {"reports": reports})


# @login_required
# def shift_report_detail(request, doc_id):
#     try:
#         with connection.cursor() as cursor:
#             # Перевірка GetShiftReportDoc
#             cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#             if not doc_data:
#                 return render(
#                     request,
#                     "journals/shift_report_detail.html",
#                     {"error": f"Звіт з doc_id={doc_id} не знайдено", "can_edit": False},
#                 )
#             shift_doc = doc_data[0]

#             # Перевірка draft
#             cursor.execute(
#                 "SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id]
#             )
#             draft_result = cursor.fetchone()
#             if not draft_result:
#                 return render(
#                     request,
#                     "journals/shift_report_detail.html",
#                     {
#                         "error": f"Звіт з doc_id={doc_id} не існує в d_shift_report",
#                         "can_edit": False,
#                     },
#                 )
#             shift_doc["draft"] = draft_result[0]

#             # Перевірка GetShiftReportRows
#             cursor.execute("EXEC GetShiftReportRows %s", [doc_id])
#             columns = [col[0] for col in cursor.description]
#             rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         can_edit = shift_doc["draft"] or request.user.is_superuser
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {
#                 "shift_doc": shift_doc,
#                 "shift_rows": rows,
#                 "can_edit": can_edit,
#                 "designs": [],  # Тимчасово порожній список, якщо цикли імпорту не виправлені
#             },
#         )
#     except Exception as e:
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {"error": f"Помилка: {str(e)}", "can_edit": False},
#         )


# @login_required
# def shift_report_create(request):
#     if request.method == "POST":
#         with connection.cursor() as cursor:
#             now = timezone.now()
#             hour = now.hour
#             is_day_shift = 9 <= hour < 21
#             shift_id = 1 if is_day_shift else 2
#             begin_time = time(8, 0) if is_day_shift else time(20, 0)
#             end_time = time(20, 0) if is_day_shift else time(8, 0)
#             foreman_name = request.user.user_name
#             description = request.POST.get("description", "")

#             cursor.execute(
#                 "EXEC AddShiftReport @doc_id OUTPUT, @doc_num OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     description,
#                     now,
#                     True,
#                     False,
#                     0,
#                     request.POST.get("production_line_id", 1),
#                     shift_id,
#                     None,
#                     None,
#                     None,
#                     None,
#                     None,
#                     None,
#                     0,
#                     begin_time,
#                     end_time,
#                     foreman_name,
#                 ],
#             )
#             cursor.execute("SELECT @@IDENTITY AS id")
#             doc_id = cursor.fetchone()[0]
#             return redirect("shift_report_detail", doc_id=doc_id)
#     return render(
#         request,
#         "journals/shift_report_form.html",
#         {
#             "qualities": Quality.objects.all(),
#             "production_lines": Production_lines.objects.all(),
#         },
#     )


# @login_required
# def shift_report_edit(request, doc_id):
#     with connection.cursor() as cursor:
#         cursor.execute("EXEC GetShiftReportDoc %s", [doc_id])
#         columns = [col[0] for col in cursor.description]
#         doc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
#         shift_doc = doc_data[0] if doc_data else {}
#         cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
#         draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#         shift_doc["draft"] = draft

#     if not draft and not request.user.is_superuser:
#         return render(
#             request,
#             "journals/shift_report_detail.html",
#             {
#                 "shift_doc": shift_doc,
#                 "error": "Тільки ОТК може редагувати нечернетку!",
#                 "can_edit": False,
#             },
#         )

#     if request.method == "POST":
#         with connection.cursor() as cursor:
#             now = timezone.now()
#             hour = now.hour
#             is_day_shift = 9 <= hour < 21
#             shift_id = 1 if is_day_shift else 2
#             begin_time = time(8, 0) if is_day_shift else time(20, 0)
#             end_time = time(20, 0) if is_day_shift else time(8, 0)
#             foreman_name = request.user.user_name
#             description = request.POST.get("description", shift_doc.get("descr", ""))

#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [doc_id],
#             )
#             total = cursor.fetchone()[0] or 0

#             cursor.execute(
#                 "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     doc_id,
#                     shift_doc.get("doc_num"),
#                     description,
#                     shift_doc.get("doc_date", now),
#                     draft,
#                     shift_doc.get("imported", False),
#                     shift_doc.get("parent_doc_id", 0),
#                     request.POST.get(
#                         "production_line_id", shift_doc.get("production_line_id", 1)
#                     ),
#                     shift_id,
#                     request.POST.get("stoppage1", shift_doc.get("stoppage1")),
#                     shift_doc.get("kiln1"),
#                     request.POST.get("comments1", shift_doc.get("comment1")),
#                     request.POST.get("stoppage2", shift_doc.get("stoppage2")),
#                     shift_doc.get("kiln2"),
#                     request.POST.get("comments2", shift_doc.get("comment2")),
#                     total,
#                     begin_time,
#                     end_time,
#                     foreman_name,
#                 ],
#             )
#             return redirect("shift_report_detail", doc_id=doc_id)

#     return render(
#         request,
#         "journals/shift_report_form.html",
#         {
#             "shift_doc": shift_doc,
#             "qualities": Quality.objects.all(),
#             "production_lines": Production_lines.objects.all(),
#             "is_edit": True,
#         },
#     )


# @login_required
# def shift_report_delete(request, doc_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
#         draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#         if not draft and not request.user.is_superuser:
#             return JsonResponse(
#                 {"error": "Тільки ОТК може видалити нечернетку!"}, status=403
#             )

#         if request.method == "POST":
#             cursor.execute("EXEC DelShiftReport %s", [doc_id])
#             return JsonResponse({"success": True})
#     return JsonResponse({"error": "Invalid request"}, status=400)


# @login_required
# def shift_report_row_create(request, doc_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
#         draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#         if not draft and not request.user.is_superuser:
#             return JsonResponse(
#                 {"error": "Тільки ОТК може редагувати нечернетку!"}, status=403
#             )

#     if request.method == "POST":
#         with connection.cursor() as cursor:
#             quality_id = request.POST.get("quality")
#             is_defect = (
#                 Quality.objects.get(quality=quality_id).is_defect
#                 if quality_id
#                 else False
#             )
#             cursor.execute(
#                 "EXEC AddShiftReportRow @row_id OUTPUT, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     doc_id,
#                     True,
#                     request.POST.get("design_ean"),
#                     quality_id,
#                     is_defect,
#                     request.POST.get("amount", 0),
#                     request.POST.get("unit_id", 8),
#                     request.POST.get("box_unit_id", 12),
#                     request.POST.get("box_amount", 0),
#                     request.POST.get("package_amount", 0),
#                 ],
#             )
#             cursor.execute("SELECT @@IDENTITY AS id")
#             row_id = cursor.fetchone()[0]

#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [doc_id],
#             )
#             total = cursor.fetchone()[0] or 0
#             cursor.execute(
#                 "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     doc_id,
#                     shift_doc.get("doc_num"),
#                     shift_doc.get("descr", ""),
#                     shift_doc.get("doc_date", now),
#                     draft,
#                     shift_doc.get("imported", False),
#                     shift_doc.get("parent_doc_id", 0),
#                     shift_doc.get("production_line_id", 1),
#                     shift_doc.get("shift_id", 1),
#                     shift_doc.get("stoppage1"),
#                     shift_doc.get("kiln1"),
#                     shift_doc.get("comment1"),
#                     shift_doc.get("stoppage2"),
#                     shift_doc.get("kiln2"),
#                     shift_doc.get("comment2"),
#                     total,
#                     shift_doc.get("begin_time", begin_time),
#                     shift_doc.get("end_time", end_time),
#                     shift_doc.get("foreman_name", foreman_name),
#                 ],
#             )
#             return JsonResponse({"row_id": row_id, "total": total})
#     return JsonResponse({"error": "Invalid request"}, status=400)


# @login_required
# def shift_report_row_edit(request, doc_id, row_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
#         draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#         if not draft and not request.user.is_superuser:
#             return JsonResponse(
#                 {"error": "Тільки ОТК може редагувати нечернетку!"}, status=403
#             )

#     if request.method == "POST":
#         with connection.cursor() as cursor:
#             quality_id = request.POST.get("quality")
#             is_defect = (
#                 Quality.objects.get(quality=quality_id).is_defect
#                 if quality_id
#                 else False
#             )
#             cursor.execute(
#                 "EXEC SetShiftReportRow %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     row_id,
#                     doc_id,
#                     True,
#                     request.POST.get("design_ean"),
#                     quality_id,
#                     is_defect,
#                     request.POST.get("amount", 0),
#                     request.POST.get("unit_id", 8),
#                     request.POST.get("box_unit_id", 12),
#                     request.POST.get("box_amount", 0),
#                     request.POST.get("package_amount", 0),
#                 ],
#             )
#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [doc_id],
#             )
#             total = cursor.fetchone()[0] or 0
#             cursor.execute(
#                 "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     doc_id,
#                     shift_doc.get("doc_num"),
#                     shift_doc.get("descr", ""),
#                     shift_doc.get("doc_date", now),
#                     draft,
#                     shift_doc.get("imported", False),
#                     shift_doc.get("parent_doc_id", 0),
#                     shift_doc.get("production_line_id", 1),
#                     shift_doc.get("shift_id", 1),
#                     shift_doc.get("stoppage1"),
#                     shift_doc.get("kiln1"),
#                     shift_doc.get("comment1"),
#                     shift_doc.get("stoppage2"),
#                     shift_doc.get("kiln2"),
#                     shift_doc.get("comment2"),
#                     total,
#                     shift_doc.get("begin_time", begin_time),
#                     shift_doc.get("end_time", end_time),
#                     shift_doc.get("foreman_name", foreman_name),
#                 ],
#             )
#             return JsonResponse({"row_id": row_id, "total": total})
#     return JsonResponse({"error": "Invalid request"}, status=400)


# @login_required
# def shift_report_row_delete(request, doc_id, row_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT draft FROM d_shift_report WHERE doc_id = %s", [doc_id])
#         draft = cursor.fetchone()[0] if cursor.rowcount > 0 else True
#         if not draft and not request.user.is_superuser:
#             return JsonResponse(
#                 {"error": "Тільки ОТК може видалити нечернетку!"}, status=403
#             )

#     if request.method == "POST":
#         with connection.cursor() as cursor:
#             cursor.execute("EXEC DelShiftReportRow %s", [row_id])
#             cursor.execute(
#                 "SELECT SUM(amount) FROM dr_shift_report WHERE doc_id=%s AND is_defect=0",
#                 [doc_id],
#             )
#             total = cursor.fetchone()[0] or 0
#             cursor.execute(
#                 "EXEC SetShiftReport %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s",
#                 [
#                     doc_id,
#                     shift_doc.get("doc_num"),
#                     shift_doc.get("descr", ""),
#                     shift_doc.get("doc_date", now),
#                     draft,
#                     shift_doc.get("imported", False),
#                     shift_doc.get("parent_doc_id", 0),
#                     shift_doc.get("production_line_id", 1),
#                     shift_doc.get("shift_id", 1),
#                     shift_doc.get("stoppage1"),
#                     shift_doc.get("kiln1"),
#                     shift_doc.get("comment1"),
#                     shift_doc.get("stoppage2"),
#                     shift_doc.get("kiln2"),
#                     shift_doc.get("comment2"),
#                     total,
#                     shift_doc.get("begin_time", begin_time),
#                     shift_doc.get("end_time", end_time),
#                     shift_doc.get("foreman_name", foreman_name),
#                 ],
#             )
#             return JsonResponse({"success": True, "total": total})
#     return JsonResponse({"error": "Invalid request"}, status=400)
