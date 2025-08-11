from django.db import models
from tiles.models import TileTypes

# Create your models here.
class Units(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='unit_id')
    name = models.SmallIntegerField(db_column='unit_name')
    unit=models.SmallIntegerField(db_column='unit_alias')
    code=models.SmallIntegerField(db_column='okei')
    id_1c_code=models.SmallIntegerField(db_column='id_1c8')

    class Meta:
        managed = False
        db_table = 'c_unit'
        verbose_name = 'Одиниця виміру'
        verbose_name_plural = 'Одиниці вимірів'

    def __str__(self):
        return self.name
class ProductUnits(models.Model):
    product_unit_id = models.SmallIntegerField(primary_key=True, db_column='product_unit_id')
    tile_type_id = models.ForeignKey(TileTypes, on_delete=models.CASCADE, db_column='tile_type_id', blank=True, null=True)
    unit_id=models.ForeignKey(Units, on_delete=models.CASCADE, db_column='unit_id')
    basic=models.BooleanField(db_column='basic')
    course=models.SmallIntegerField(db_column='course')
    box_unit=models.BooleanField(db_column='box_unit')
    package_unit=models.BooleanField(db_column='package_unit')

    class Meta:
        managed = False
        db_table = 'cu_product_unit'
        verbose_name = 'Одиниця виміру продукту'
        verbose_name_plural = 'Одиниці виміру продуктів'

    def __str__(self):
        return self.name