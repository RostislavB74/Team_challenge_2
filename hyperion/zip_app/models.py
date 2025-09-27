# BASE_DIR: D:\Team_challenge_2\hyperion
# Шлях до .env: D:\Team_challenge_2\hyperion\.env
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='Cyrillic_General_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class Orders(models.Model):
    id = models.AutoField(db_column='№', primary_key=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    order_id = models.IntegerField(db_column='ЗАКАЗ_№', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    status = models.CharField(db_column='СТАТУС', max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    order_date = models.DateTimeField(db_column='ДАТА_ФОРМ', blank=True, null=True)  # Field name made lowercase.
    confirmation_date = models.DateTimeField(db_column='ДАТА_ПОДТВ', blank=True, null=True)  # Field name made lowercase.
    order_amount = models.DecimalField(db_column='СУММА_ЗАК', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(db_column='ПРИМЕЧАНИЕ', db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    date_receipt_order = models.DateTimeField(db_column='ДАТА_ПРИХОД', blank=True, null=True)  # Field name made lowercase.
    cancellation_date = models.DateTimeField(db_column='ДАТА_АНУЛ', blank=True, null=True)  # Field name made lowercase.
    execution_status = models.CharField(db_column='ВЫПОЛНЕНИЕ', max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scheduled_delivery_date = models.DateTimeField(db_column='ДАТА_ПЛАН_ДОСТ', blank=True, null=True)  # Field name made lowercase.
    ssma_timestamp = models.TextField(db_column='SSMA_TimeStamp')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ВЫП_ЗАКАЗОВ'

    def __str__(self):
        return str(self.order_id)


class Catalogues(models.Model):
    код_кат = models.AutoField(db_column='Код кат', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    каталог = models.CharField(db_column='Каталог', max_length=80, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    код_оборудования = models.ForeignKey(
        "EquipmentsZip",
        on_delete=models.CASCADE,
        db_column="Код оборудования",
        blank=True,
        null=True,
    )  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Каталог'


class Complectation(models.Model):
    номер = models.AutoField(db_column='Номер', primary_key=True)  # Field name made lowercase.
    код = models.CharField(db_column='Код', max_length=32, db_collation='Cyrillic_General_CI_AS', db_comment='код детали по каталогу')  # Field name made lowercase.
    табл = models.CharField(db_column='Табл', max_length=30, db_collation='Cyrillic_General_CI_AS', blank=True, null=True, db_comment='таблица по каталогу')  # Field name made lowercase.
    поз = models.CharField(db_column='Поз', max_length=16, db_collation='Cyrillic_General_CI_AS', blank=True, null=True, db_comment='позиция детали по каталогу')  # Field name made lowercase.
    наименование = models.CharField(db_column='Наименование', max_length=200, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    узел = models.CharField(db_column='Узел', max_length=96, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    усл_заказа = models.BooleanField(db_column='Усл заказа', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    кол = models.FloatField(db_column='Кол', blank=True, null=True)  # Field name made lowercase.
    ед = models.CharField(db_column='Ед', max_length=14, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    код_кат = models.ForeignKey(
        "Catalogues",
        on_delete=models.CASCADE,
        db_column="Код кат",
        blank=True,
        null=True,
    )  # Field name made lowercase. Field renamed to remove unsuitable characters.
    примечение = models.CharField(db_column='Примечение', max_length=100, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    дата = models.DateTimeField(db_column='Дата', blank=True, null=True)  # Field name made lowercase.
    на_складе = models.FloatField(db_column='На складе', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ssma_timestamp = models.TextField(db_column='SSMA_TimeStamp')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Комплектация'


class GeneralOrders(models.Model):
    field_записи = models.AutoField(db_column='№записи', primary_key=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_заказа = models.IntegerField(db_column='№_ЗАКАЗА', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    номер = models.IntegerField(db_column='Номер', blank=True, null=True)  # Field name made lowercase.
    кол = models.FloatField(db_column='Кол', blank=True, null=True)  # Field name made lowercase.
    ед = models.CharField(db_column='Ед', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    усл = models.BooleanField(db_column='Усл', blank=True, null=True)  # Field name made lowercase.
    дата_заказа = models.DateTimeField(db_column='Дата_заказа', blank=True, null=True)  # Field name made lowercase.
    ssma_timestamp = models.TextField(db_column='SSMA_TimeStamp')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Общ_Заказ'


class GeneralIncome(models.Model):
    field_записи = models.AutoField(db_column='№записи', primary_key=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    номер = models.IntegerField(db_column='Номер', blank=True, null=True)  # Field name made lowercase.
    field_заказа = models.IntegerField(db_column='№_ЗАКАЗА', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    кол = models.FloatField(db_column='Кол', blank=True, null=True)  # Field name made lowercase.
    ед = models.CharField(db_column='Ед', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    дата_получения = models.DateTimeField(db_column='Дата_получения', blank=True, null=True)  # Field name made lowercase.
    ssma_timestamp = models.TextField(db_column='SSMA_TimeStamp')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Общ_Приход'


class Sections(models.Model):
    field_раздел = models.AutoField(db_column='№Раздел', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    name = models.CharField(db_column='РАЗДЕЛ', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'РАЗДЕЛ'
    def __str__(self):
        return self.name

class CurrentOrders(models.Model):
    код = models.AutoField(db_column='Код', primary_key=True)  # Field name made lowercase.
    field_текущего_заказа = models.IntegerField(db_column='№ТЕКУЩЕГО_ЗАКАЗА', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    дата = models.DateTimeField(db_column='ДАТА', blank=True, null=True)  # Field name made lowercase.
    примечание = models.TextField(db_column='ПРИМЕЧАНИЕ', db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    field_заказа = models.IntegerField(db_column='№_ЗАКАЗА', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    статус = models.CharField(db_column='СТАТУС', max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    у = models.BooleanField(db_column='У', blank=True, null=True)  # Field name made lowercase.
    ssma_timestamp = models.TextField(db_column='SSMA_TimeStamp')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ТЕКУЩИЙ_ЗАКАЗ'


class EquipmentsZip(models.Model):
    код_оборудования = models.AutoField(db_column='Код оборудования', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    тип = models.CharField(db_column='Тип', max_length=40, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    наименование = models.CharField(db_column='Наименование', max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    код_фирмы = models.ForeignKey(
        "Firms", on_delete=models.CASCADE, db_column="Код фирмы", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'оборудование'


class Firms(models.Model):
    firms_id = models.AutoField(db_column='Код фирмы', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.CharField(
        max_length=50,
        db_column="фирма",
        db_collation="Cyrillic_General_CI_AS",
        blank=True,
        null=True,
    )
    section = models.ForeignKey(
        "Sections", on_delete=models.CASCADE, db_column="№Раздел", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'фирмы'
        app_label = "zip_app"

    def __str__(self):
        return self.name
