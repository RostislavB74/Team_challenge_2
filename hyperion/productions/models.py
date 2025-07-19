from django.db import models
# from tiles.models import TileTypes
class Production_line_groups(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='line_group_id')
    name = models.SmallIntegerField(db_column='group_name')
    decor=models.SmallIntegerField(db_column='is_decor')
    base=models.SmallIntegerField(db_column='is_base')
    order=models.SmallIntegerField(db_column='in_order')

    class Meta:
        managed = False
        db_table = 'c_production_line_group'
        verbose_name = "Група виробничої лінії"
        verbose_name_plural = "Групи виробничих ліній"

    def __str__(self):
        return self.name


# productions/models.py (або правильний шлях до файлу)
class Production_lines(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="production_line_id")
    name = models.CharField(
        max_length=20, db_column="production_line"
    )  # Виправлено на CharField
    productivity = models.SmallIntegerField(db_column="productivity")
    internal_number = models.SmallIntegerField(db_column="internal_number")
    report_group_id = models.SmallIntegerField(db_column="report_group_id")
    order = models.SmallIntegerField(db_column="in_order")
    production_section_id = models.SmallIntegerField(db_column="production_section_id")
    summarize_number = models.SmallIntegerField(db_column="summarize_number")
    department_id = models.SmallIntegerField(db_column="department_id")

    class Meta:
        managed = False
        db_table = "c_production_line"
        verbose_name = "Лінія виробництва"
        verbose_name_plural = "Лінії виробництва"

    def __str__(self):
        return self.name


class Snap_types_to_lines(models.Model): #snap_types_to_lines
    id = models.SmallIntegerField(primary_key=True, db_column='product_id')
    name = models.ForeignKey('tiles.TileTypes', on_delete=models.CASCADE, db_column='tile_type_id')
    production_line_id = models.ForeignKey(Production_lines, on_delete=models.CASCADE, db_column='production_line_id')#models.SmallIntegerField(db_column='production_line_id')
    productivity=models.SmallIntegerField(db_column='productivity')
   
    class Meta:
        managed = False
        db_table = 'cu_tile_product'
        verbose_name = "Прив'язка до виробничої лінії"
        verbose_name_plural = "Прив'язка до виробничих ліній"

    def __str__(self):
        return str(self.name)

class ProductionSections(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='production_section_id')
    name = models.CharField(max_length=255, db_column='production_section')
    production_line_group_id = models.ForeignKey(Production_line_groups, on_delete=models.CASCADE, db_column='production_line_group_id')#models.SmallIntegerField(db_column='production_line_group_id')
    order=models.SmallIntegerField(db_column='in_order')
    class Meta:
        managed = False
        db_table = 'c_production_section'
        verbose_name = "Секція виробництва"
        verbose_name_plural = "Секціі виробництва"

    def __str__(self):
        return str(self.name)

class StoppageCauses(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='stoppage_cause_id')
    name = models.CharField(max_length=255, db_column='cause')
    class Meta:
        managed = False
        db_table = 'cu_stoppage_cause'
        verbose_name = "Причина простою"
        verbose_name_plural = "Причини простою"

    def __str__(self):
        return str(self.name)
class StoppageCausesTypes(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='stoppage_cause_type_id')
    name = models.CharField(max_length=255, db_column='cause_name')
    level = models.SmallIntegerField(db_column='level')
    class Meta:
        managed = False
        db_table = 'cu_stoppage_cause_type'
        verbose_name = "Тип простою"
        verbose_name_plural = "Типи простоїв"

    def __str__(self):
        return str(self.name)