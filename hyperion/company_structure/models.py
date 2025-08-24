from django.db import models

class Departments(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='department_id')
    name = models.SmallIntegerField(db_column='department')
    use_kiln_press=models.SmallIntegerField(db_column='use_kiln_press')
   

    class Meta:
        managed = False
        db_table = 'c_department'
        verbose_name = "Цех"
        verbose_name_plural = "Цехи"

    def __str__(self):
        return self.name
class Department_sections(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='production_section_id')
    name = models.CharField(max_length=50, unique=True, db_index=True, db_column='production_section')
    department_id=models.ForeignKey(Departments, on_delete=models.CASCADE, db_column='department_id', blank=True, null=True)
    descriptions=models.CharField(max_length=255, db_column='descr', blank=True, null=True)
    archived=models.BooleanField(db_column='archived', default=False)
    num=models.SmallIntegerField(db_column='num', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'c_production_section'
        verbose_name = "Виробнича секція"
        verbose_name_plural = "Виробничі секції"

    def __str__(self):
        return self.name

class Subdivision(models.Model):
    subdivision_id = models.SmallIntegerField(primary_key=True, db_column='subdivision_id')
    name = models.CharField(max_length=255, db_column='subdivision')
    description = models.CharField(max_length=255, db_column='descr', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'c_subdivision' 
        verbose_name = 'Дільниця'
        verbose_name_plural = 'Дільниці' 
    def __str__(self):
        return self.name

class Shifts(models.Model):
    shift_id = models.SmallIntegerField(primary_key=True, db_column='shift_id')
    name = models.CharField(max_length=255, db_column='shift')
    shift_foreman = models.CharField(max_length=255, db_column='shiftforeman', blank=True, null=True)
    alias = models.CharField(max_length=255, db_column='alias', blank=True, null=True)
    begin_time = models.TimeField(db_column='begin_time', blank=True, null=True)
    end_time = models.TimeField(db_column='end_time', blank=True, null=True)
    line_group_id=models.ForeignKey('productions.Production_line_groups', on_delete=models.CASCADE, db_column='line_group_id', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'c_shift'
        verbose_name = 'Зміна'
        verbose_name_plural = 'Зміни'
    def __str__(self):
        return self.name
class Stores(models.Model):
    store_id = models.SmallIntegerField(primary_key=True, db_column='store_id')
    name = models.CharField(max_length=255, db_column='store')
    store_type_id = models.ForeignKey(
        "Store_types",
        on_delete=models.CASCADE,
        db_column="store_type_id",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(db_column='is_active', default=True)

    class Meta:
        managed = False
        db_table = 'c_store'
        verbose_name = 'Склад'
        verbose_name_plural = 'Склади'
    def __str__(self):
        return self.name
class Store_types(models.Model):
    store_type_id = models.SmallIntegerField(primary_key=True, db_column='store_type_id')
    name = models.CharField(max_length=255, db_column='store_type')
    
    class Meta:
        managed = False
        db_table = 'c_store_type'
        verbose_name = 'Тип складу'
        verbose_name_plural = 'Типи складів'
    def __str__(self):
        return self.name
