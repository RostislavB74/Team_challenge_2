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