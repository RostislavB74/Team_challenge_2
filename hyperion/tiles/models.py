from django.db import models
from users.models import User

# Пов’язані моделі
class TileType(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='tile_type_id')
    name = models.CharField(max_length=255, db_column='tile_type')
    class Meta:
        managed = False
        db_table = 'c_tile_type'  

class Color(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='color_id')  
    name = models.CharField(max_length=255, db_column='color')
    class Meta:
        managed = False
        db_table = 'c_color'  

class Collection(models.Model):
    id = models.IntegerField(primary_key=True, db_column='collection_id')
    name = models.CharField(max_length=255, db_column='collection')
    class Meta:
        managed = False
        db_table = 'cu_collection' 

class Author(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='user_id')
    name = models.CharField(max_length=255, db_column='user_name')
    class Meta:
        managed = False
        db_table = 'c_user'  

class DecorType(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='decor_type_id')
    name = models.CharField(max_length=255, db_column='decor_type')
    class Meta:
        managed = False
        db_table = 'cu_decor_type'  

class Coat(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='coat_type_id')  # Змінено з TinyIntegerField
    name = models.CharField(max_length=255, db_column='coat_type')
    class Meta:
        managed = False
        db_table = 'cu_coat_type'  

class Hue(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='hue_id')
    name = models.CharField(max_length=255, db_column='hue')
    class Meta:
        managed = False
        db_table = 'c_hue'  

class TileGeometry(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='tile_geometry_id')  # Змінено з TinyIntegerField
    name = models.CharField(max_length=255, db_column='tile_geometry')
    class Meta:
        managed = False
        db_table = 'c_tile_geometry'  # Замініть, якщо назва інша

class TileGlaze(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column='tile_glaze_id')  # Змінено з TinyIntegerField
    name = models.CharField(max_length=255, db_column='tile_glaze')
    class Meta:
        managed = False
        db_table = 'c_tile_glaze'  # Замініть, якщо назва інша

class Tile(models.Model):
    design_ean = models.CharField(max_length=50, primary_key=True, db_column='design_ean')
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id', blank=True, null=True)
    original_author = models.ForeignKey(User, on_delete=models.CASCADE, db_column='original_author_id', blank=True, null=True, related_name='original_tiles')
    design_name = models.CharField(max_length=255, db_column='design_name', blank=True, null=True)
    tile_type = models.ForeignKey(TileType, on_delete=models.CASCADE, db_column='tile_type_id', blank=True, null=True)
    color = models.ForeignKey(Color, related_name='tiles_color', on_delete=models.CASCADE, db_column='color_id', blank=True, null=True)
    is_test = models.BooleanField(db_column='is_test', default=False)
    tone = models.CharField(max_length=50, db_column='tone', blank=True, null=True)
    hue = models.ForeignKey(Hue, on_delete=models.CASCADE, db_column='hue_id', blank=True, null=True)
    quality = models.CharField(max_length=50, db_column='quality', blank=True, null=True)
    height = models.SmallIntegerField(db_column='height', blank=True, null=True)
    width = models.SmallIntegerField(db_column='width', blank=True, null=True)
    thickness = models.DecimalField(max_digits=10, decimal_places=2, db_column='thickness', blank=True, null=True)
    box_amount = models.SmallIntegerField(db_column='box_amount', blank=True, null=True)
    package_amount = models.SmallIntegerField(db_column='package_amount', blank=True, null=True)
    box_weight = models.DecimalField(max_digits=10, decimal_places=2, db_column='box_weight', blank=True, null=True)
    photo = models.BinaryField(db_column='photo', blank=True, null=True)
    tolerance = models.DecimalField(max_digits=10, decimal_places=2, db_column='tolerance', blank=True, null=True)
    package_square = models.DecimalField(max_digits=10, decimal_places=2, db_column='package_square', blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, db_column='collection_id', blank=True, null=True)
    is_base = models.BooleanField(db_column='is_base', default=False)
    tile_1c_id = models.IntegerField(db_column='tile_1c_id', blank=True, null=True)
    parent_ean = models.CharField(max_length=50, db_column='parent_ean', blank=True, null=True)
    print_name = models.CharField(max_length=255, db_column='print_name', blank=True, null=True)
    add_date = models.DateTimeField(db_column='add_date', blank=True, null=True)
    ean = models.CharField(max_length=50, db_column='ean', blank=True, null=True)
    design_code = models.IntegerField(db_column='design_code')
    archived = models.BooleanField(db_column='archived', default=False)
    is_action = models.BooleanField(db_column='is_action', default=False)
    caliber = models.SmallIntegerField(db_column='caliber')
    modifier = models.CharField(max_length=255, db_column='modifier', blank=True, null=True)
    is_stock = models.BooleanField(db_column='is_stock', default=False)
    use_second_color = models.BooleanField(db_column='use_second_color', default=False)
    second_color = models.ForeignKey(Color, related_name='tiles_second_color', on_delete=models.CASCADE, db_column='second_color_id', blank=True, null=True)
    decor_base_ean = models.CharField(max_length=50, db_column='decor_base_ean', blank=True, null=True)
    decor_type = models.ForeignKey(DecorType, on_delete=models.CASCADE, db_column='decor_type_id', blank=True, null=True)
    set_amount = models.SmallIntegerField(db_column='set_amount', blank=True, null=True)
    amount_in_row = models.SmallIntegerField(db_column='amount_in_row', blank=True, null=True)  # Змінено з TinyIntegerField
    amount_in_column = models.SmallIntegerField(db_column='amount_in_column', blank=True, null=True)  # Змінено з TinyIntegerField
    additional_name = models.CharField(max_length=255, db_column='additional_name', blank=True, null=True)
    coat = models.ForeignKey(Coat, on_delete=models.CASCADE, db_column='coat_id', blank=True, null=True)
    laying_type = models.CharField(max_length=50, db_column='laying_type', blank=True, null=True)
    laying = models.CharField(max_length=255, db_column='laying', blank=True, null=True)
    serial_number_in_set = models.SmallIntegerField(db_column='serial_number_in_set', blank=True, null=True)  # Змінено з TinyIntegerField
    amount_panno_in_box = models.SmallIntegerField(db_column='amount_panno_in_box', blank=True, null=True)  # Змінено з TinyIntegerField
    tile_glaze = models.ForeignKey(TileGlaze, on_delete=models.CASCADE, db_column='tile_glaze_id')
    caliber2 = models.SmallIntegerField(db_column='caliber2')
    tile_geometry = models.ForeignKey(TileGeometry, on_delete=models.CASCADE, db_column='tile_geometry_id')
    on_tile_ean = models.CharField(max_length=50, db_column='on_tile_ean', blank=True, null=True)

    @property
    def tile_size(self):
        if self.width and self.height:
            return f"{self.width}x{self.height}"
        return None

    class Meta:
        managed = False
        db_table = 'c_design'