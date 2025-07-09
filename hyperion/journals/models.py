from django.db import models
from users.models import User
from equipments.models import Kilns
from productions.models import Production_lines,Production_line_groups
from company_structure.models import *


class ShiftReports(models.Model):
    doc_id = models.SmallIntegerField(primary_key=True, db_column='doc_id')
    doc_number = models.CharField(max_length=255, db_column='doc_num', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="author_id", blank=True, null=True, related_name='author')
    doc_date = models.DateTimeField(db_column='doc_date')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", blank=True, null=True, related_name='user')
    description = models.TextField(db_column='descr', blank=True, null=True)
    draft=models.BooleanField(db_column='draft', default=False)
    parent_doc_id = models.SmallIntegerField(db_column='parent_doc_id', blank=True, null=True)
    deleted=models.BooleanField(db_column='deleted', default=False)
    read_only=models.BooleanField(db_column='read_only', default=False)
    has_child=models.BooleanField(db_column='has_child', default=False)
    imported=models.BooleanField(db_column='imported', default=False)
    production_line_id = models.ForeignKey(
        Production_lines,
        on_delete=models.CASCADE,
        db_column="production_line_id",
        blank=True,
        null=True,
        related_name="production_line" )
    shift_id = models.ForeignKey(
        Shifts,
        on_delete=models.CASCADE,
        db_column="shift_id",
        blank=True,
        null=True,
        related_name="shift",
    )
    stoppage1=models.SmallIntegerField(db_column='stoppage1', blank=True, null=True)
    kiln1 = models.ForeignKey(Kilns, on_delete=models.CASCADE, db_column="kiln1", blank=True, null=True, related_name='kiln1')
    comments1=models.TextField(db_column='comment1', blank=True, null=True)
    stoppage2=models.SmallIntegerField(db_column='stoppage2', blank=True, null=True)
    kiln2 = models.ForeignKey(Kilns, on_delete=models.CASCADE, db_column="kiln2", blank=True, null=True, related_name='kiln2')
    comments2=models.TextField(db_column='comment2', blank=True, null=True)
    total=models.SmallIntegerField(db_column='total', blank=True, null=True)
    begin_time=models.TimeField(db_column='begin_time', blank=True, null=True)
    end_time=models.TimeField(db_column='end_time', blank=True, null=True)
    foreman_name=models.CharField(db_column='foreman_name', max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'd_shift_report'
        verbose_name = "Звіт зміни"
        verbose_name_plural = "Звіт змін"
    def __str__(self):
        return self.doc_number


class ShiftMaterialsDebit(models.Model):
    doc_id = models.SmallIntegerField(primary_key=True, db_column="doc_id")
    doc_number = models.CharField(
        max_length=255, db_column="doc_num", blank=True, null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="author_id",
        blank=True,
        null=True,
        related_name="author_debit",
    )
    doc_date = models.DateTimeField(db_column="doc_date")
    user = models.ForeignKey(
        User,
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
        Shifts,
        on_delete=models.CASCADE,
        db_column="shift_id",
        blank=True,
        null=True,
        related_name="shift_debit",
    )
    department_id = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        db_column="department_id",
        blank=True,
        null=True,
        related_name="department_debit",
    )
    production_section_id = models.ForeignKey(
        Department_sections,
        on_delete=models.CASCADE,
        db_column="production_section_id",
        blank=True,
        null=True,
        related_name="production_section_debit",
    )
    store_id = models.ForeignKey(
        Stores,
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
