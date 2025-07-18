from django.db import models
# from users.models import User
# from equipments.models import Kilns
# from productions.models import Production_lines,Production_line_groups
from company_structure.models import *
# journals/models.py
# from tiles.models import Quality,Designs

class ShiftMaterialsDebit(models.Model):
    doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
    doc_number = models.CharField(
        max_length=255, db_column="doc_num", blank=True, null=True
    )
    author = models.ForeignKey('users.User',
        on_delete=models.CASCADE,
        db_column="author_id",
        blank=True,
        null=True,
        related_name="author_debit",
    )
    doc_date = models.DateTimeField(db_column="doc_date")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="user_id",
        blank=True,
        null=True,
        related_name="user_debit",
    )
    description = models.TextField(db_column="descr", blank=True, null=True)
    draft = models.BooleanField(db_column="draft", default=False)
    parent_doc_id = models.SmallIntegerField(
        db_column="parent_doc_id", blank=True, null=True
    )
    deleted = models.BooleanField(db_column="deleted", default=False)
    read_only = models.BooleanField(db_column="read_only", default=False)
    has_child = models.BooleanField(db_column="has_child", default=False)
    imported = models.BooleanField(db_column="imported", default=False)

    shift_id = models.ForeignKey(
        "company_structure.Shifts",
        on_delete=models.CASCADE,
        db_column="shift_id",
        blank=True,
        null=True,
        related_name="shift_debit",
    )
    department_id = models.ForeignKey(
        "company_structure.Departments",
        on_delete=models.CASCADE,
        db_column="department_id",
        blank=True,
        null=True,
        related_name="department_debit",
    )
    production_section_id = models.ForeignKey(
        "company_structure.Department_sections",
        on_delete=models.CASCADE,
        db_column="production_section_id",
        blank=True,
        null=True,
        related_name="production_section_debit",
    )
    store_id = models.ForeignKey(
        "company_structure.Stores",
        on_delete=models.CASCADE,
        db_column="store_id",
        blank=True,
        null=True,
        related_name="store",
    )

    class Meta:
        managed = False
        db_table = "d_shift_material_debit"
        verbose_name = "Звіт виробництва по сировині"
        verbose_name_plural = "Звіт виробництва по сировині"

    def __str__(self):
        return self.doc_number
from django.db import models


class ShiftReports(models.Model):
    doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
    doc_number = models.CharField(
        max_length=10, db_column="doc_num", blank=True, null=True
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="author_id",
        blank=True,
        null=True,
        related_name="author",
    )
    doc_date = models.DateTimeField(db_column="doc_date")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="user_id",
        blank=True,
        null=True,
        related_name="user",
    )
    description = models.TextField(db_column="descr", blank=True, null=True)
    draft = models.BooleanField(db_column="draft", default=True)
    parent_doc_id = models.SmallIntegerField(
        db_column="parent_doc_id", blank=True, null=True
    )
    deleted = models.BooleanField(db_column="deleted", default=False)
    read_only = models.BooleanField(db_column="read_only", default=False)
    has_child = models.BooleanField(db_column="has_child", default=False)
    imported = models.BooleanField(db_column="imported", default=False)
    production_line_id = models.ForeignKey(
        "productions.Production_lines",
        on_delete=models.CASCADE,
        db_column="production_line_id",
        blank=True,
        null=True,
    )
    shift_id = models.ForeignKey(
        "company_structure.Shifts",
        on_delete=models.CASCADE,
        db_column="shift_id",
        blank=True,
        null=True,
    )
    stoppage1 = models.SmallIntegerField(db_column="stoppage1", blank=True, null=True)
    kiln1 = models.ForeignKey(
        "equipments.Kilns",
        on_delete=models.CASCADE,
        db_column="kiln1",
        blank=True,
        null=True,
        related_name="kiln1",
    )
    comments1 = models.TextField(db_column="comment1", blank=True, null=True)
    stoppage2 = models.SmallIntegerField(db_column="stoppage2", blank=True, null=True)
    kiln2 = models.ForeignKey(
        "equipments.Kilns",
        on_delete=models.CASCADE,
        db_column="kiln2",
        blank=True,
        null=True,
        related_name="kiln2",
    )
    comments2 = models.TextField(db_column="comment2", blank=True, null=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=3, db_column="total", blank=True, null=True
    )
    begin_time = models.TimeField(db_column="begin_time", blank=True, null=True)
    end_time = models.TimeField(db_column="end_time", blank=True, null=True)
    foreman_name = models.CharField(
        db_column="foreman_name", max_length=30, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "d_shift_report"
        verbose_name = "Звіт зміни"
        verbose_name_plural = "Звіти змін"

    def __str__(self):
        return self.doc_number or str(self.doc_id)


class ShiftReportRow(models.Model):
    row_id = models.IntegerField(primary_key=True, db_column="row_id")
    doc_id = models.ForeignKey(
        "journals.ShiftReports", on_delete=models.CASCADE, db_column="doc_id"
    )
    design_ean = models.ForeignKey(
        "tiles.Designs", on_delete=models.CASCADE, db_column="design_ean"
    )
    quality = models.ForeignKey(
        "tiles.Quality",
        on_delete=models.CASCADE,
        db_column="quality",
        related_name="shift_rows",
    )
    is_defect = models.BooleanField(db_column="is_defect", default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=3, db_column="amount")
    unit_id = models.ForeignKey(
        "units.Units", on_delete=models.CASCADE, db_column="unit"
    )
    box_unit_id = models.SmallIntegerField(db_column="box_unit_id")
    box_amount = models.DecimalField(
        max_digits=10, decimal_places=3, db_column="box_amount"
    )
    package_amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        db_column="package_amount",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "dr_shift_report"
        verbose_name = "Рядок звіту"
        verbose_name_plural = "Рядки звіту"

    def __str__(self):
        return f"Row {self.row_id} for Doc {self.doc_id_id}"


# class ShiftReports(models.Model):
#     doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
#     doc_number = models.CharField(
#         max_length=10, db_column="doc_num", blank=True, null=True
#     )
#     author = models.ForeignKey(
#         'users.User',
#         on_delete=models.CASCADE,
#         db_column="author_id",
#         blank=True,
#         null=True,
#         related_name="author",
#     )
#     doc_date = models.DateTimeField(db_column="doc_date")
#     user = models.ForeignKey(
#         "users.User",
#         on_delete=models.CASCADE,
#         db_column="user_id",
#         blank=True,
#         null=True,
#         related_name="user",
#     )
#     description = models.TextField(db_column="descr", blank=True, null=True)
#     draft = models.BooleanField(db_column="draft", default=True)
#     parent_doc_id = models.SmallIntegerField(
#         db_column="parent_doc_id", blank=True, null=True
#     )
#     deleted = models.BooleanField(db_column="deleted", default=False)
#     read_only = models.BooleanField(db_column="read_only", default=False)
#     has_child = models.BooleanField(db_column="has_child", default=False)
#     imported = models.BooleanField(db_column="imported", default=False)
#     production_line_id = models.ForeignKey(
#         "productions.Production_lines",
#         on_delete=models.CASCADE,
#         db_column="production_line_id",
#         blank=True,
#         null=True,
#         related_name="production_line",
#     )
#     shift_id = models.ForeignKey(
#         "company_structure.Shifts",
#         on_delete=models.CASCADE,
#         db_column="shift_id",
#         blank=True,
#         null=True,
#         related_name="shift",
#     )
#     stoppage1 = models.SmallIntegerField(db_column="stoppage1", blank=True, null=True)
#     kiln1 = models.ForeignKey(
#         'equipments.Kilns',
#         on_delete=models.CASCADE,
#         db_column="kiln1",
#         blank=True,
#         null=True,
#         related_name="kiln1",
#     )
#     comments1 = models.TextField(db_column="comment1", blank=True, null=True)
#     stoppage2 = models.SmallIntegerField(db_column="stoppage2", blank=True, null=True)
#     kiln2 = models.ForeignKey(
#         "equipments.Kilns",
#         on_delete=models.CASCADE,
#         db_column="kiln2",
#         blank=True,
#         null=True,
#         related_name="kiln2",
#     )
#     comments2 = models.TextField(db_column="comment2", blank=True, null=True)
#     total = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="total", blank=True, null=True
#     )
#     begin_time = models.TimeField(db_column="begin_time", blank=True, null=True)
#     end_time = models.TimeField(db_column="end_time", blank=True, null=True)
#     foreman_name = models.CharField(
#         db_column="foreman_name", max_length=30, blank=True, null=True
#     )

#     class Meta:
#         managed = False
#         db_table = "d_shift_report"
#         verbose_name = "Звіт зміни"
#         verbose_name_plural = "Звіти змін"

#     def __str__(self):
#         return self.doc_number or str(self.doc_id)


# class ShiftReportRow(models.Model):
#     row_id = models.IntegerField(primary_key=True, db_column="row_id")
#     doc_id = models.ForeignKey(
#         ShiftReports, on_delete=models.CASCADE, db_column="doc_id"
#     )
#     design_ean = models.CharField(max_length=13, db_column="design_ean")
#     quality = models.ForeignKey(
#         'tiles.Quality',
#         on_delete=models.CASCADE,
#         db_column="quality",
#         related_name="shift_rows",
#     )
#     is_defect = models.BooleanField(db_column="is_defect", default=False)
#     amount = models.DecimalField(max_digits=10, decimal_places=3, db_column="amount")
#     unit_id = models.SmallIntegerField(db_column="unit_id")
#     box_unit_id = models.SmallIntegerField(db_column="box_unit_id")
#     box_amount = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="box_amount"
#     )
#     package_amount = models.DecimalField(
#         max_digits=7,
#         decimal_places=2,
#         db_column="package_amount",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         managed = False
#         db_table = "dr_shift_report"
#         verbose_name = "Рядок звіту"
#         verbose_name_plural = "Рядки звіту"

#     def __str__(self):
#         return f"Row {self.row_id} for Doc {self.doc_id_id}"


# # class Design(models.Model):
# #     ean = models.CharField(max_length=13, db_column="ean", primary_key=True)
# #     name = models.CharField(max_length=100, db_column="name")
# #     quality = models.ForeignKey(Quality, on_delete=models.CASCADE, db_column="quality")
# #     is_defect = models.BooleanField(db_column="is_defect", default=False)
# #     pieces_per_box = models.DecimalField(
# #         max_digits=10, decimal_places=3, db_column="pieces_per_box"
# #     )
# #     boxes_per_pallet = models.DecimalField(
# #         max_digits=10, decimal_places=3, db_column="boxes_per_pallet"
# #     )
# #     unit_id = models.SmallIntegerField(db_column="unit_id", default=8)  # Наприклад, м²
# #     box_unit_id = models.SmallIntegerField(
# #         db_column="box_unit_id", default=12
# #     )  # Наприклад, коробки

# #     class Meta:
# #         managed = False
# #         db_table = "c_design"
# #         verbose_name = "Дизайн"
# #         verbose_name_plural = "Дизайни"

# #     def __str__(self):
# #         return self.name


# class ShiftReports(models.Model):
#     doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
#     doc_number = models.CharField(
#         max_length=10, db_column="doc_num", blank=True, null=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         db_column="author_id",
#         blank=True,
#         null=True,
#         related_name="author",
#     )
#     doc_date = models.DateTimeField(db_column="doc_date")
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         db_column="user_id",
#         blank=True,
#         null=True,
#         related_name="user",
#     )
#     description = models.TextField(db_column="descr", blank=True, null=True)
#     draft = models.BooleanField(db_column="draft", default=True)
#     parent_doc_id = models.SmallIntegerField(
#         db_column="parent_doc_id", blank=True, null=True
#     )
#     deleted = models.BooleanField(db_column="deleted", default=False)
#     read_only = models.BooleanField(db_column="read_only", default=False)
#     has_child = models.BooleanField(db_column="has_child", default=False)
#     imported = models.BooleanField(db_column="imported", default=False)
#     production_line_id = models.ForeignKey(
#         Production_lines,
#         on_delete=models.CASCADE,
#         db_column="production_line_id",
#         blank=True,
#         null=True,
#         related_name="production_line",
#     )
#     shift_id = models.ForeignKey(
#         Shifts,
#         on_delete=models.CASCADE,
#         db_column="shift_id",
#         blank=True,
#         null=True,
#         related_name="shift",
#     )
#     stoppage1 = models.SmallIntegerField(db_column="stoppage1", blank=True, null=True)
#     kiln1 = models.ForeignKey(
#         Kilns,
#         on_delete=models.CASCADE,
#         db_column="kiln1",
#         blank=True,
#         null=True,
#         related_name="kiln1",
#     )
#     comments1 = models.TextField(db_column="comment1", blank=True, null=True)
#     stoppage2 = models.SmallIntegerField(db_column="stoppage2", blank=True, null=True)
#     kiln2 = models.ForeignKey(
#         Kilns,
#         on_delete=models.CASCADE,
#         db_column="kiln2",
#         blank=True,
#         null=True,
#         related_name="kiln2",
#     )
#     comments2 = models.TextField(db_column="comment2", blank=True, null=True)
#     total = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="total", blank=True, null=True
#     )
#     begin_time = models.TimeField(db_column="begin_time", blank=True, null=True)
#     end_time = models.TimeField(db_column="end_time", blank=True, null=True)
#     foreman_name = models.CharField(
#         db_column="foreman_name", max_length=30, blank=True, null=True
#     )

#     class Meta:
#         managed = False
#         db_table = "d_shift_report"
#         verbose_name = "Звіт зміни"
#         verbose_name_plural = "Звіти змін"

#     def __str__(self):
#         return self.doc_number or str(self.doc_id)


# class ShiftReportRow(models.Model):
#     row_id = models.IntegerField(primary_key=True, db_column="row_id")
#     doc_id = models.ForeignKey(
#         ShiftReports, on_delete=models.CASCADE, db_column="doc_id"
#     )
#     design_ean = models.ForeignKey(
#         Designs, on_delete=models.CASCADE, db_column="design_ean"
#     )
#     quality = models.ForeignKey(
#         Quality,
#         on_delete=models.CASCADE,
#         db_column="quality",
#         related_name="shift_rows",
#     )
#     is_defect = models.BooleanField(db_column="is_defect", default=False)
#     amount = models.DecimalField(max_digits=10, decimal_places=3, db_column="amount")
#     unit_id = models.SmallIntegerField(db_column="unit_id")
#     box_unit_id = models.SmallIntegerField(db_column="box_unit_id")
#     box_amount = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="box_amount"
#     )
#     package_amount = models.DecimalField(
#         max_digits=7,
#         decimal_places=2,
#         db_column="package_amount",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         managed = False
#         db_table = "dr_shift_report"
#         verbose_name = "Рядок звіту"
#         verbose_name_plural = "Рядки звіту"

#     def __str__(self):
#         return f"Row {self.row_id} for Doc {self.doc_id_id}"


# class ShiftReports(models.Model):
#     doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
#     doc_number = models.CharField(
#         max_length=10, db_column="doc_num", blank=True, null=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         db_column="author_id",
#         blank=True,
#         null=True,
#         related_name="author",
#     )
#     doc_date = models.DateTimeField(db_column="doc_date")
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         db_column="user_id",
#         blank=True,
#         null=True,
#         related_name="user",
#     )
#     description = models.TextField(db_column="descr", blank=True, null=True)
#     draft = models.BooleanField(db_column="draft", default=True)
#     parent_doc_id = models.SmallIntegerField(
#         db_column="parent_doc_id", blank=True, null=True
#     )
#     deleted = models.BooleanField(db_column="deleted", default=False)
#     read_only = models.BooleanField(db_column="read_only", default=False)
#     has_child = models.BooleanField(db_column="has_child", default=False)
#     imported = models.BooleanField(db_column="imported", default=False)
#     production_line_id = models.ForeignKey(
#         Production_lines,
#         on_delete=models.CASCADE,
#         db_column="production_line_id",
#         blank=True,
#         null=True,
#         related_name="production_line",
#     )
#     shift_id = models.ForeignKey(
#         Shifts,
#         on_delete=models.CASCADE,
#         db_column="shift_id",
#         blank=True,
#         null=True,
#         related_name="shift",
#     )
#     stoppage1 = models.SmallIntegerField(db_column="stoppage1", blank=True, null=True)
#     kiln1 = models.ForeignKey(
#         Kilns,
#         on_delete=models.CASCADE,
#         db_column="kiln1",
#         blank=True,
#         null=True,
#         related_name="kiln1",
#     )
#     comments1 = models.TextField(db_column="comment1", blank=True, null=True)
#     stoppage2 = models.SmallIntegerField(db_column="stoppage2", blank=True, null=True)
#     kiln2 = models.ForeignKey(
#         Kilns,
#         on_delete=models.CASCADE,
#         db_column="kiln2",
#         blank=True,
#         null=True,
#         related_name="kiln2",
#     )
#     comments2 = models.TextField(db_column="comment2", blank=True, null=True)
#     total = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="total", blank=True, null=True
#     )
#     begin_time = models.TimeField(db_column="begin_time", blank=True, null=True)
#     end_time = models.TimeField(db_column="end_time", blank=True, null=True)
#     foreman_name = models.CharField(
#         db_column="foreman_name", max_length=30, blank=True, null=True
#     )

#     class Meta:
#         managed = False
#         db_table = "d_shift_report"
#         verbose_name = "Звіт зміни"
#         verbose_name_plural = "Звіти змін"

#     def __str__(self):
#         return self.doc_number or str(self.doc_id)


# class ShiftReportRow(models.Model):
#     row_id = models.IntegerField(primary_key=True, db_column="row_id")
#     doc_id = models.ForeignKey(
#         ShiftReports, on_delete=models.CASCADE, db_column="doc_id"
#     )
#     design_ean = models.CharField(max_length=13, db_column="design_ean")
#     quality = models.ForeignKey(
#         Quality,
#         on_delete=models.CASCADE,
#         db_column="quality",
#         related_name="shift_rows",
#     )
#     is_defect = models.BooleanField(db_column="is_defect", default=False)
#     amount = models.DecimalField(max_digits=10, decimal_places=3, db_column="amount")
#     unit_id = models.SmallIntegerField(db_column="unit_id")
#     box_unit_id = models.SmallIntegerField(db_column="box_unit_id")
#     box_amount = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="box_amount"
#     )
#     package_amount = models.DecimalField(
#         max_digits=7,
#         decimal_places=2,
#         db_column="package_amount",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         managed = False
#         db_table = "dr_shift_report"
#         verbose_name = "Рядок звіту"
#         verbose_name_plural = "Рядки звіту"

#     def __str__(self):
#         return f"Row {self.row_id} for Doc {self.doc_id_id}"


# class ShiftReports(models.Model):
#     doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
#     doc_number = models.CharField(
#         max_length=10, db_column="doc_num", blank=True, null=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         db_column="author_id",
#         blank=True,
#         null=True,
#         related_name="author",
#     )
#     doc_date = models.DateTimeField(db_column="doc_date")
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         db_column="user_id",
#         blank=True,
#         null=True,
#         related_name="user",
#     )
#     description = models.TextField(db_column="descr", blank=True, null=True)
#     draft = models.BooleanField(db_column="draft", default=True)
#     parent_doc_id = models.SmallIntegerField(
#         db_column="parent_doc_id", blank=True, null=True
#     )
#     deleted = models.BooleanField(db_column="deleted", default=False)
#     read_only = models.BooleanField(db_column="read_only", default=False)
#     has_child = models.BooleanField(db_column="has_child", default=False)
#     imported = models.BooleanField(db_column="imported", default=False)
#     production_line_id = models.ForeignKey(
#         Production_lines,
#         on_delete=models.CASCADE,
#         db_column="production_line_id",
#         blank=True,
#         null=True,
#         related_name="production_line",
#     )
#     shift_id = models.ForeignKey(
#         Shifts,
#         on_delete=models.CASCADE,
#         db_column="shift_id",
#         blank=True,
#         null=True,
#         related_name="shift",
#     )
#     stoppage1 = models.SmallIntegerField(db_column="stoppage1", blank=True, null=True)
#     kiln1 = models.ForeignKey(
#         Kilns,
#         on_delete=models.CASCADE,
#         db_column="kiln1",
#         blank=True,
#         null=True,
#         related_name="kiln1",
#     )
#     comments1 = models.TextField(db_column="comment1", blank=True, null=True)
#     stoppage2 = models.SmallIntegerField(db_column="stoppage2", blank=True, null=True)
#     kiln2 = models.ForeignKey(
#         Kilns,
#         on_delete=models.CASCADE,
#         db_column="kiln2",
#         blank=True,
#         null=True,
#         related_name="kiln2",
#     )
#     comments2 = models.TextField(db_column="comment2", blank=True, null=True)
#     total = models.DecimalField(
#         max_digits=10, decimal_places=3, db_column="total", blank=True, null=True
#     )
#     begin_time = models.TimeField(db_column="begin_time", blank=True, null=True)
#     end_time = models.TimeField(db_column="end_time", blank=True, null=True)
#     foreman_name = models.CharField(
#         db_column="foreman_name", max_length=30, blank=True, null=True
#     )

#     class Meta:
#         managed = False
#         db_table = "d_shift_report"
#         verbose_name = "Звіт зміни"
#         verbose_name_plural = "Звіти змін"

#     def __str__(self):
#         return self.doc_number or str(self.doc_id)
