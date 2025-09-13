from django.db import models
from users.models import User
from django.db import connection
from django.core.exceptions import ValidationError
from users.models import User
from company_structure.models import Subdivision


class CaliberTiles(models.Model):
    # id = models.AutoField(primary_key=True)
    caliber = models.SmallIntegerField(primary_key=True, unique=True, db_column="caliber")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "c_caliber"
        verbose_name = "Калібр плитки"
        verbose_name_plural = "Калібри плитки"

    def __str__(self):
        return str(self.caliber)

class Collections(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="collection_id")
    name = models.CharField(max_length=255, db_column="collection")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )
    collection_group_id = models.ForeignKey(
        "CollectionGroups",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="collection_group_id",
    )

    class Meta:
        managed = False
        db_table = "cu_collection"
        verbose_name = "Колекція"
        verbose_name_plural = "Колекції"

    def __str__(self):
        return str(self.name)


class CollectionGroups(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="collection_group_id")
    name = models.CharField(max_length=255, db_column="collection_group")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "c_collection_group"
        verbose_name = "Група колекції"
        verbose_name_plural = "Групи колекцій"

    def __str__(self):
        return self.name
# Пов’язані моделі
class TileTypes(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="tile_type_id")
    name = models.CharField(max_length=255, db_column="tile_type")
    height = models.SmallIntegerField(db_column="height", blank=True, null=True)
    width = models.SmallIntegerField(db_column="width", blank=True, null=True)
    thickness = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="thickness", blank=True, null=True
    )
    box_amount = models.SmallIntegerField(db_column="box_amount", blank=True, null=True)
    package_amount = models.SmallIntegerField(
        db_column="package_amount", blank=True, null=True
    )
    box_weight = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="box_weight", blank=True, null=True
    )
    tolerance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, db_column="tolerance"
    )
    package_square = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, db_column="package_square"
    )
    product_type_id = models.ForeignKey(
        "ProductTypes",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="product_type_id",
    )
    tile_standart = models.ForeignKey(
        "Tilestandarts",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="tile_standart_id",
    )  # (null=True, db_column='tile_standart_id')
    use_modifier = models.BooleanField(default=False, db_column="use_modifier")
    combi_design = models.CharField(max_length=13, null=True, db_column="combi_design")
    tech_design = models.CharField(max_length=13, null=True, db_column="tech_design")
    square_weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, db_column="square_weight"
    )

    # suffix_product_type = models.ForeignKey('Suffix_For_ProductType', on_delete=models.CASCADE, blank=True, null=True, db_column='suffix_for_product_type_id')
    class Meta:
        managed = False
        db_table = "c_tile_type"
        verbose_name = "Тип продукції"
        verbose_name_plural = "Типи продукції"

    def __str__(self):
        return self.name


class TilePassportGroups(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="tile_passport_group_id")
    name = models.CharField(max_length=255, db_column="tile_passport_group")

    class Meta:
        managed = False
        db_table = "c_tile_passport_group"
        verbose_name = "Група плитки для паспорту"
        verbose_name_plural = "Групи плиток для паспортів"

    def __str__(self):
        return self.name


class Suffix_For_ProductTypes(models.Model):
    id = models.AutoField(primary_key=True, db_column="suffix_for_product_type_id")
    product_type_id = models.ForeignKey(
        "ProductTypes",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="product_type_id",
    )
    suffix = models.CharField(max_length=255, db_column="suffix")

    class Meta:
        managed = False
        db_table = "c_suffix_for_product_type"
        verbose_name = "Суфікс для типу продукту"
        verbose_name_plural = "Суфікси для типу продукту"

    def __str__(self):
        return self.suffix


class ProductTypes(models.Model):
    product_type_id = models.SmallIntegerField(
        primary_key=True, db_column="product_type_id"
    )
    name = models.CharField(max_length=255, db_column="product_type")
    subdivision_id = models.ForeignKey(
        Subdivision,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="subdivision_id",
    )
    short_name = models.CharField(
        max_length=255, db_column="short_name", blank=True, null=True
    )
    product_group_id = models.ForeignKey(
        "ProductGroups",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="product_group_id",
    )
    export_name = models.CharField(
        max_length=255, db_column="export_name", blank=True, null=True
    )
    label_name = models.CharField(
        max_length=255, db_column="label_name", blank=True, null=True
    )
    tile_passport_group_id = models.ForeignKey(
        "TilePassportGroups",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="tile_passport_group_id",
    )
    use_claiber = models.BooleanField(default=False, db_column="use_caliber")

    class Meta:
        managed = False
        db_table = "c_product_type"
        verbose_name = "Тип продукту"
        verbose_name_plural = "Типи продуктів"

    def __str__(self):
        return self.name


class ProductGroups(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="product_group_id")
    name = models.CharField(max_length=255, db_column="product_group")
    in_order = models.SmallIntegerField(db_column="in_order")
    is_base = models.BooleanField(default=False, db_column="is_base")

    class Meta:
        managed = False
        db_table = "c_product_group"
        verbose_name = "Група продукту"
        verbose_name_plural = "Групи продуктів"

    def __str__(self):
        return self.name


class Tilestandarts(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="tile_standart_id")
    name = models.CharField(max_length=255, db_column="standart")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )
    full_name = models.CharField(
        max_length=255, db_column="full_name", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "cu_tile_standart"
        verbose_name = "Стандарт ппродукції"
        verbose_name_plural = "Стандарти продукції"

    def __str__(self):
        return self.name


class Colors(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="color_id")
    name = models.CharField(max_length=255, db_column="color")

    class Meta:
        managed = False
        db_table = "c_color"
        verbose_name = "Колір"
        verbose_name_plural = "Кольори"

    def __str__(self):
        return self.name


class Authors(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="user_id")
    name = models.CharField(max_length=255, db_column="user_name")

    class Meta:
        managed = False
        db_table = "c_user"

    def __str__(self):
        return self.name


class DecorTypes(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="decor_type_id")
    name = models.CharField(max_length=255, db_column="decor_type")

    class Meta:
        managed = False
        db_table = "cu_decor_type"

    def __str__(self):
        return self.name


class Coats(models.Model):
    id = models.SmallIntegerField(
        primary_key=True, db_column="coat_type_id"
    )  # Змінено з TinyIntegerField
    name = models.CharField(max_length=255, db_column="coat_type")

    class Meta:
        managed = False
        db_table = "cu_coat_type"
        verbose_name = "Тип покриття"
        verbose_name_plural = "Типи покриття"

    def __str__(self):
        return self.name


class Hues(models.Model):
    id = models.SmallIntegerField(primary_key=True, db_column="hue_id")
    name = models.CharField(max_length=255, db_column="hue")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "c_hue"
        verbose_name = "Тон"
        verbose_name_plural = "Тони"

    def __str__(self):
        return self.name


class TileGeometry(models.Model):
    id = models.SmallIntegerField(
        primary_key=True, db_column="tile_geometry_id"
    )  # Змінено з TinyIntegerField
    name = models.CharField(max_length=255, db_column="tile_geometry")

    class Meta:
        managed = False
        db_table = "c_tile_geometry"
        verbose_name = "Геометрія продукту"
        verbose_name_plural = "Геометрія продуктів"

    def __str__(self):
        return self.name


class TileGlazes(models.Model):
    id = models.SmallIntegerField(
        primary_key=True, db_column="tile_glaze_id"
    )  # Змінено з TinyIntegerField
    name = models.CharField(max_length=255, db_column="tile_glaze")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "c_tile_glaze"  # Замініть, якщо назва інша

    def __str__(self):
        return self.name


class Quality(models.Model):
    quality = models.CharField(max_length=50, primary_key=True, db_column="quality")
    description = models.CharField(
        max_length=255, db_column="descr", blank=True, null=True
    )
    is_defect = models.BooleanField(db_column="is_defect", default=False)
    sort_order = models.SmallIntegerField(db_column="sort_order", blank=True, null=True)
    mark = models.DecimalField(
        max_digits=1, decimal_places=0, db_column="mark", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "c_quality"
        verbose_name = "Сорт продукції"
        verbose_name_plural = "Сорти продукції"

    def __str__(self):
        return self.quality


class Designs(models.Model):
    design_ean = models.CharField(
        max_length=50, primary_key=True, db_column="design_ean"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="author_id", blank=True, null=True
    )
    design_name = models.CharField(
        max_length=255, db_column="design_name", blank=True, null=True
    )
    tile_type = models.ForeignKey(
        TileTypes,
        on_delete=models.CASCADE,
        db_column="tile_type_id",
        blank=True,
        null=True,
    )
    color = models.ForeignKey(
        Colors,
        related_name="tiles_color",
        on_delete=models.CASCADE,
        db_column="color_id",
        blank=True,
        null=True,
    )
    is_test = models.BooleanField(db_column="is_test", default=False)
    tone = models.CharField(max_length=50, db_column="tone", blank=True, null=True)
    hue = models.ForeignKey(
        Hues, on_delete=models.CASCADE, db_column="hue_id", blank=True, null=True
    )
    quality = models.CharField(
        max_length=50, db_column="quality", blank=True, null=True
    )
    height = models.SmallIntegerField(db_column="height", blank=True, null=True)
    width = models.SmallIntegerField(db_column="width", blank=True, null=True)
    thickness = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="thickness", blank=True, null=True
    )
    box_amount = models.SmallIntegerField(db_column="box_amount", blank=True, null=True)
    package_amount = models.SmallIntegerField(
        db_column="package_amount", blank=True, null=True
    )
    box_weight = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="box_weight", blank=True, null=True
    )
    photo = models.BinaryField(db_column="photo", blank=True, null=True)
    tolerance = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="tolerance", blank=True, null=True
    )
    package_square = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="package_square",
        blank=True,
        null=True,
    )
    collection = models.ForeignKey(
        Collections,
        on_delete=models.CASCADE,
        db_column="collection_id",
        blank=True,
        null=True,
    )
    is_base = models.BooleanField(db_column="is_base", default=False)
    tile_1c_id = models.IntegerField(db_column="tile_1c_id", blank=True, null=True)
    parent_ean = models.CharField(
        max_length=50, db_column="parent_ean", blank=True, null=True
    )
    print_name = models.CharField(
        max_length=255, db_column="print_name", blank=True, null=True
    )
    add_date = models.DateTimeField(db_column="add_date", blank=True, null=True)
    ean = models.CharField(max_length=50, db_column="ean", blank=True, null=True)
    design_code = models.IntegerField(db_column="design_code")
    archived = models.BooleanField(db_column="archived", default=False)
    is_action = models.BooleanField(db_column="is_action", default=False)
    caliber = models.SmallIntegerField(db_column="caliber")
    modifier = models.CharField(
        max_length=255, db_column="modifier", blank=True, null=True
    )
    is_stock = models.BooleanField(db_column="is_stock", default=False)
    use_second_color = models.BooleanField(db_column="use_second_color", default=False)
    second_color = models.ForeignKey(
        Colors,
        related_name="tiles_second_color",
        on_delete=models.CASCADE,
        db_column="second_color_id",
        blank=True,
        null=True,
    )
    decor_base_ean = models.CharField(
        max_length=50, db_column="decor_base_ean", blank=True, null=True
    )
    decor_type = models.ForeignKey(
        DecorTypes,
        on_delete=models.CASCADE,
        db_column="decor_type_id",
        blank=True,
        null=True,
    )
    set_amount = models.SmallIntegerField(db_column="set_amount", blank=True, null=True)
    amount_in_row = models.SmallIntegerField(
        db_column="amount_in_row", blank=True, null=True
    )
    amount_in_column = models.SmallIntegerField(
        db_column="amount_in_column", blank=True, null=True
    )
    additional_name = models.CharField(
        max_length=255, db_column="additional_name", blank=True, null=True
    )
    coat = models.ForeignKey(
        Coats, on_delete=models.CASCADE, db_column="coat_id", blank=True, null=True
    )
    laying_type = models.CharField(
        max_length=50, db_column="laying_type", blank=True, null=True
    )
    laying = models.CharField(max_length=255, db_column="laying", blank=True, null=True)
    serial_number_in_set = models.SmallIntegerField(
        db_column="serial_number_in_set", blank=True, null=True
    )
    amount_panno_in_box = models.SmallIntegerField(
        db_column="amount_panno_in_box", blank=True, null=True
    )
    tile_glaze = models.ForeignKey(
        TileGlazes, on_delete=models.CASCADE, db_column="tile_glaze_id"
    )
    caliber2 = models.SmallIntegerField(db_column="caliber2")
    tile_geometry = models.ForeignKey(
        TileGeometry, on_delete=models.CASCADE, db_column="tile_geometry_id"
    )
    on_tile_ean = models.CharField(
        max_length=50, db_column="on_tile_ean", blank=True, null=True
    )

    @property
    def tile_size(self):
        if self.width and self.height:
            return f"{self.width}x{self.height}"
        elif self.tile_type and self.tile_type.width and self.tile_type.height:
            return f"{self.tile_type.width}x{self.tile_type.height}"
        return None

    class Meta:
        managed = False
        db_table = "c_design"
        verbose_name = "Дизайн"
        verbose_name_plural = "Дизайни"

    def __str__(self):
        return self.design_name or "Без назви"

    def delete(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM reports WHERE design_ean = %s", [self.design_ean]
            )
            count = cursor.fetchone()[0]
            if count > 0:
                raise ValidationError(
                    "Неможливо видалити дизайн, який присутній у звітах."
                )
        super().delete(*args, **kwargs)
