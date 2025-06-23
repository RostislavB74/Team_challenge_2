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
class Department_sections(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='production_section_id')
    name = models.SmallIntegerField(db_column='production_section')
    department_id=models.ForeignKey(Departments, on_delete=models.CASCADE, db_column='department_id', blank=True, null=True)
    descriptions=models.CharField(max_length=255, db_column='descr', blank=True, null=True)
    archived=models.BooleanField(db_column='archived', default=False)
    num=models.SmallIntegerField(db_column='num', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'c_production_section'
        verbose_name = "Виробнича секція"
        verbose_name_plural = "Виробнгичі секції"