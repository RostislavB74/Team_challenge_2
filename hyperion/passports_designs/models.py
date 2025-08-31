# apps/passports_designs/models.py
from django.db import models
from django.utils import timezone

class TileType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    box_amount = models.PositiveIntegerField()
    package_amount = models.PositiveIntegerField()
    box_weight = models.DecimalField(max_digits=6, decimal_places=2)
    tolerance = models.DecimalField(max_digits=4, decimal_places=2)
    package_square = models.DecimalField(max_digits=6, decimal_places=2)
    square_weight = models.DecimalField(max_digits=6, decimal_places=2)
    product_type_id = models.IntegerField()
    tile_standart_id = models.IntegerField()
    use_modifier = models.BooleanField(default=False)
    combi_design = models.CharField(max_length=30, blank=True, null=True)
    tech_design = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class Design(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    tile_type = models.ForeignKey(TileType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)  # kg, box, etc.

    def __str__(self):
        return self.name

class DesignMaterial(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount_per_m2 = models.DecimalField(max_digits=8, decimal_places=3)
    calculated_amount_per_m2 = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    last_calculated = models.DateTimeField(null=True, blank=True)
    needs_review = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["design", "material"]),
        ]
        # unique_together = ('design', 'material')

    def __str__(self):
        return f"{self.design} - {self.material}"

class DesignPassportCalculation(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    date_calculated = models.DateTimeField(default=timezone.now)
    total_m2 = models.PositiveIntegerField()

    def __str__(self):
        return f"Calculation for {self.design.name} on {self.date_calculated.date()}"

class DesignMaterialCalculation(models.Model):
    calculation = models.ForeignKey(DesignPassportCalculation, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    calculated_amount = models.DecimalField(max_digits=10, decimal_places=3)
    previous_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    changed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.material.name} - {self.calculated_amount} ({'changed' if self.changed else 'no change'})"
