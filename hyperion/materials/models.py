from django.db import models
from units.models import Units
from company_structure.models import Subdivision, Departments
class MaterialGroups(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='material_group_id')
    name = models.CharField(max_length=255, db_column='material_group')

    class Meta:
        managed = False
        db_table = 'cu_material_group'
        verbose_name='Група матеріалу'
        verbose_name_plural='Групи матеріалів'

    def __str__(self):
        return self.name

class MaterialUnits(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='material_unit_id')
    name = models.ForeignKey('MaterialTypes', on_delete=models.CASCADE, db_column='material_type_id')#models.SmallIntegerField(db_column='material_type_id')
    unit= models.ForeignKey(Units, on_delete=models.CASCADE, db_column='unit_id')#models.SmallIntegerField(db_column='unit_id')
    basic = models.BooleanField(db_column="basic", default=False)
    course=models.SmallIntegerField(db_column='course')

    class Meta:
        managed = False
        db_table = 'cu_material_unit'
        verbose_name='Одиниця виміру матеріалу'
        verbose_name_plural='Одиниці вимірів матеріалів'

    def __str__(self):
        return self.name


class MaterialTypes(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='material_type_id')
    name = models.CharField(max_length=100, db_column='material_type')

    class Meta:
        managed = False
        db_table = 'cu_material_type'
        verbose_name='Тип матеріалу'
        verbose_name_plural='Типи матеріалів'

    def __str__(self):
        return self.name


class MaterialKinds(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='material_kind_id')
    name = models.CharField(max_length=100, db_column='material_kind')

    class Meta:
        managed = False
        db_table = 'c_material_kind'
        verbose_name='Вид матеріалу'
        verbose_name_plural='Види матеріалів'

    def __str__(self):
        return self.name
class MaterialsTechnnologicalGroups(models.Model):
    id = models.AutoField(primary_key=True, db_column="material_teh_group_id")
    name = models.CharField(max_length=255, db_column="material_teh_group")

    class Meta:
        managed = False
        db_table = 'c_material_teh_group'
        verbose_name='Технологічні група сировини'
        verbose_name_plural='Технологічні групи сировин'

    def __str__(self):
        return self.name

class Materials(models.Model):
    id = models.AutoField(primary_key=True, db_column='material_id')
    material_type_id = models.ForeignKey(MaterialTypes, on_delete=models.CASCADE, db_column='material_type_id', blank=True, null=True) #models.SmallIntegerField(db_column='material_type_id')
    material_kind_id = models.ForeignKey(MaterialKinds, on_delete=models.CASCADE, db_column='material_kind_id', blank=True, null=True)
    name = models.CharField(max_length=255, db_column='material')
    fullname = models.CharField(max_length=500, db_column='fullname', blank=True, null=True)
    is_equipment = models.BooleanField(db_column='is_equipment', default=False)
    material_group_id = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE, db_column='material_group_id', blank=True, null=True,related_name='material_group')
    unit_id = models.ForeignKey(Units, on_delete=models.CASCADE, db_column='unit_id', blank=True, null=True,related_name='material_unit')
    spec = models.CharField(max_length=255, db_column='spec', blank=True, null=True)
    descr = models.TextField(db_column='descr', blank=True, null=True)
    control_param_sample_unit_id = models.ForeignKey(Units, on_delete=models.CASCADE, db_column="control_param_sample_unit_id", blank=True, null=True,related_name='control_param_sample_unit')
    archived = models.BooleanField(db_column='archived', default=False)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, db_column='humidity', blank=True, null=True)
    id_1c8 = models.CharField(max_length=50, db_column='id_1c8', blank=True, null=True)
    min_rest = models.DecimalField(max_digits=10, decimal_places=2, db_column='min_rest', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cu_material'
        verbose_name='Матеріал'
        verbose_name_plural='Матеріали'

    def __str__(self):
        return self.name
class MaterialsByDepartments(models.Model):
    materials=models.ForeignKey(Materials, on_delete=models.CASCADE, db_column='material_id')
    # material_id = models.IntegerField(db_column='material_id', blank=True, null=True)
    id = models.IntegerField( primary_key=True, db_column="section_material_list_id")    
    production_section_id = models.ForeignKey("company_structure.Department_sections", on_delete=models.CASCADE, db_column="production_section_id", blank=True, null=True)
       

    class Meta:
        managed = False
        db_table = "c_section_material_list"
        verbose_name='Матеріали по дільницях'
        verbose_name_plural='Матеріали по дільницях'
