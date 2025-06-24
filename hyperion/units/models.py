from django.db import models

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
