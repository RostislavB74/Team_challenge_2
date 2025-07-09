from django.db import models
class EquipmentsTypes(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='equipment_type_id')
    name = models.CharField(max_length=255, db_column='equipment_type')

    class Meta:
        managed = False
        db_table = 'c_equipment_type'
        verbose_name = "Тип обладнання"
        verbose_name_plural = "Типи обладнання"

    def __str__(self):
        return self.name


class Kilns(models.Model):
    kiln_id = models.SmallIntegerField(primary_key=True, db_column="kiln_id")
    name = models.CharField(max_length=255, db_column="kiln")
    production_line_id = models.CharField(
        max_length=255, db_column="production_line_id", blank=True, null=True
    )
    hardware_id = models.CharField(
        max_length=255, db_column="hardware_id", blank=True, null=True
    )
    kiln_number = models.CharField(
        max_length=255, db_column="kiln_num", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "cu_kiln"
        verbose_name = "Піч"
        verbose_name_plural = "Печі"

    def __str__(self):
        return self.name

    def get_kiln_number(self):
        return self.kiln_number