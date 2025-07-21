from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from tiles.models import Designs
from units.models import ProductUnits#, Units
from productions.models import Snap_types_to_lines
from productions.models import Production_lines, StoppageCausesTypes
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
                SELECT dr2.row_id, ck.kiln AS kiln_name, dr2.amount, dr2.stoppage_cause_type_id AS stoppage_type,
                    dr2.stoppage_cause AS stoppage_cause, ISNULL(dr2.comment,'') AS comment
                FROM dr2_shift_report dr2
                INNER JOIN cu_kiln ck ON dr2.kiln_id = ck.kiln_id
                WHERE dr2.doc_id = %s AND ck.production_line_id = %s
                """,
                [doc_id, production_line_id],
            )
            downtime_columns = [col[0] for col in cursor.description]
            downtimes = [dict(zip(downtime_columns, row)) for row in cursor.fetchall()]
            logger.debug(f"Downtimes returned: {len(downtimes)}")

            # Мапінг id → назва типу простою
            stoppage_type_map = {
                t.id: t.name for t in StoppageCausesTypes.objects.all()
            }
            for dt in downtimes:
                dt["stoppage_type_name"] = stoppage_type_map.get(dt["stoppage_type"], "Невідомо")

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
        # tile_type_id = design['tile_type_id'] if design else None
        package_square = design['package_square'] if design and design['package_square'] else 1.0

        # product_unit = ProductUnits.objects.filter(
        #     tile_type_id=tile_type_id,
        #     basic=True
        # ).select_related('unit_id').first()
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

