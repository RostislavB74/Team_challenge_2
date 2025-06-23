from django.db import models
class Departments(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='department_id')
    name = models.SmallIntegerField(db_column='department')
    use_kiln_press=models.SmallIntegerField(db_column='use_kiln_press')
   

    class Meta:
        managed = False
        db_table = 'c_department'
        verbose_name = "Підрозділ"
        verbose_name_plural = "Підрозділи"

    def __str__(self):
        return self.name