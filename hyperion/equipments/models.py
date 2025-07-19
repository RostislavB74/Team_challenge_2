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
    kiln_name = models.CharField(max_length=255, db_column="kiln")
    production_line_id = models.ForeignKey(
        "productions.Production_lines",
        on_delete=models.CASCADE,
        db_column="production_line_id",
        blank=True,
        null=True,
    )
    hardware_id = models.ForeignKey(
        "equipments.Hardware",
        on_delete=models.CASCADE,
        db_column="hardware_id",
        blank=True,
        null=True,
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
        return self.kiln_name

    def get_kiln_number(self):
        return self.kiln_number
class Hardware(models.Model):
    hardware_id = models.SmallIntegerField(primary_key=True, db_column="hardware_id")
    name = models.CharField(max_length=255, db_column="hardware")
    production_section_id=models.ForeignKey("company_structure.Department_sections", on_delete=models.CASCADE, db_column="production_section_id", blank=True, null=True)
    hardware_group_id=models.ForeignKey("Hardware_groups", on_delete=models.CASCADE, db_column="hardware_group_id", blank=True, null=True)
    is_active = models.BooleanField(db_column="is_active", default=True)
    description = models.TextField(db_column="descr", blank=True, null=True)
    class Meta:
        managed = False
        db_table = "c_hardware"
        verbose_name = "Обладнання"
        verbose_name_plural = "Обладнання"

    def __str__(self):
        return self.name

class Hardware_groups(models.Model):
    hardware_group_id = models.SmallIntegerField(primary_key=True, db_column="hardware_group_id")
    name = models.CharField(max_length=255, db_column="hardware_group")

    class Meta:
        managed = False
        db_table = "c_hardware_group"
        verbose_name = "Група обладнання"
        verbose_name_plural = "Групи обладнання"

    def __str__(self):
        return self.name
