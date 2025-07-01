from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.db import models

class PermitionObject(models.Model):
    permition_object_name = models.CharField(max_length=50, primary_key=True, db_column='permition_object_name')
    permition_object_caption = models.CharField(max_length=255, blank=True, null=True, db_column='permition_object_caption')
    group_name = models.CharField(max_length=255, blank=True, null=True, db_column='group_name')

    class Meta:
        managed = False
        db_table = 's_permition_object'
        verbose_name = 'Об’єкт дозволу'
        verbose_name_plural = 'Об’єкти дозволів'

    def __str__(self):
        return self.permition_object_caption or self.permition_object_name

class Permition(models.Model):
    permition_id = models.AutoField(primary_key=True, db_column='permition_id')
    group_id = models.ForeignKey('CGroup', on_delete=models.CASCADE, db_column='group_id')
    object_name = models.ForeignKey(PermitionObject, on_delete=models.CASCADE, db_column='object_name')
    permition_value = models.BooleanField(default=False, db_column='permition_value')
    visible = models.BooleanField(default=False, db_column='visible')
    add = models.BooleanField(default=False, db_column='add')
    edit = models.BooleanField(default=False, db_column='edit')
    delete = models.BooleanField(default=False, db_column='del')
    edit_clean_copy = models.BooleanField(default=False, db_column='edit_clean_copy')

    class Meta:
        managed = False
        db_table = 'c_permition'
        verbose_name = 'Дозвіл'
        verbose_name_plural = 'Дозволи'

    def __str__(self):
        return f"{self.group_id.group_name} - {self.object_name.permition_object_caption or self.object_name.permition_object_name}"

class UserManager(BaseUserManager):
    def create_user(self, system_login, password=None, **extra_fields):
        user = self.model(system_login=system_login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, system_login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(system_login, password, **extra_fields)

class UserGroup(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, db_column='group_id')

    class Meta:
        db_table = 'auth_user_groups'
        unique_together = ('user', 'group')
        managed = False

class CGroup(models.Model):
    group_id = models.SmallIntegerField(primary_key=True, db_column='group_id')
    group_name = models.CharField(max_length=255, db_column='group_name')
    contractor_id = models.IntegerField(null=True, db_column='contractor_id')

    class Meta:
        managed = False
        db_table = 'c_group'

    def __str__(self):
        return self.group_name

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    # group_id = models.ForeignKey(CGroup, on_delete=models.CASCADE, db_column='group_id')
    system_login = models.CharField(max_length=100, unique=True)
    # user_name = models.CharField(max_length=100)
    # subdivision_id = models.IntegerField(default=1)
    # phone = models.CharField(max_length=20, blank=True)
    # birth_date = models.DateField(null=True, blank=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # password = models.CharField(max_length=128)
    # last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False, db_column='is_superuser')
    # user_id = models.SmallIntegerField(primary_key=True, db_column='user_id')
    # system_login = models.CharField(max_length=50, db_column='system_login')
    group_id = models.ForeignKey('CGroup', on_delete=models.CASCADE, db_column='group_id', related_name='users')
    user_name = models.CharField(max_length=255, db_column='user_name')
    subdivision_id = models.IntegerField(db_column='subdivision_id')
    phone = models.CharField(max_length=255, null=True, blank=True, db_column='phone')
    birth_date = models.DateTimeField(null=True, blank=True, db_column='birth_date')
    is_active = models.BooleanField(db_column='is_active', default=True)
    is_staff = models.BooleanField(db_column='is_staff', default=False)
    password = models.CharField(max_length=128, db_column='password')
    last_login = models.DateTimeField(null=True, db_column='last_login', blank=True)
    is_superuser = models.BooleanField(default=False, db_column='is_superuser')
    objects = UserManager()
    USERNAME_FIELD = 'system_login'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        managed = False
        db_table = 'c_user'

    groups = models.ManyToManyField(
        Group,
        related_name='user_set',
        related_query_name='user',
        blank=True,
        through='UserGroup',
        through_fields=('user', 'group')
    )

    def get_is_superuser(self):
        try:
            return (
                self.userextras.is_superuser or
                self.groups.filter(name='superuser').exists() or
                self.group_id.group_id == 1
            )
        except UserExtras.DoesNotExist:
            return self.groups.filter(name='superuser').exists() or self.group_id.group_id == 1

    def has_perm(self, perm, obj=None):
        if self.get_is_superuser():
            return True
        try:
            app_label, action_object = perm.split('.', 1)
            action, object_name = action_object.split('_', 1) if '_' in action_object else (action_object, '')
            if action not in ['add', 'edit', 'delete', 'edit_clean_copy', 'visible']:
                return False
            return Permition.objects.filter(
                group_id=self.group_id,
                object_name__permition_object_name=object_name,
                **{action: True}
            ).exists()
        except ValueError:
            return False

    def has_module_perms(self, app_label):
        if self.get_is_superuser():
            return True
        return Permition.objects.filter(
            group_id=self.group_id,
            object_name__permition_object_name__startswith=f'{app_label}_'
        ).exists()

class UserExtras(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='user_id')
    is_superuser = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'django_user_extras'
        verbose_name = 'Додаткові дані користувача'
        verbose_name_plural = 'Додаткові дані користувачів'
#deploy ok
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
# from django.db import models

# class UserManager(BaseUserManager):
#     def create_user(self, system_login, password=None, **extra_fields):
#         user = self.model(system_login=system_login, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, system_login, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(system_login, password, **extra_fields)

# class UserGroup(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
#     group = models.ForeignKey(Group, on_delete=models.CASCADE, db_column='group_id')

#     class Meta:
#         db_table = 'auth_user_groups'
#         unique_together = ('user', 'group')
#         managed = False

# class CGroup(models.Model):
#     group_id = models.SmallIntegerField(primary_key=True, db_column='group_id')
#     group_name = models.CharField(max_length=255, db_column='group_name')
#     contractor_id = models.IntegerField(null=True, db_column='contractor_id')

#     class Meta:
#         managed = False
#         db_table = 'c_group'

#     def __str__(self):
#         return self.group_name

# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key=True, db_column='user_id')
#     group_id = models.ForeignKey(CGroup, on_delete=models.CASCADE, db_column='group_id')
#     system_login = models.CharField(max_length=100, unique=True)
#     user_name = models.CharField(max_length=100)
#     subdivision_id = models.IntegerField(default=1)
#     phone = models.CharField(max_length=20, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(null=True, blank=True)

#     objects = UserManager()
#     USERNAME_FIELD = 'system_login'
#     REQUIRED_FIELDS = ['user_name']

#     class Meta:
#         managed = False
#         db_table = 'c_user'

#     groups = models.ManyToManyField(
#         Group,
#         related_name='user_set',
#         related_query_name='user',
#         blank=True,
#         through='UserGroup',
#         through_fields=('user', 'group')
#     )

#     def get_is_superuser(self):
#         try:
#             return (
#                 self.userextras.is_superuser or
#                 self.groups.filter(name='superuser').exists() or
#                 self.group_id.group_id == 1
#             )
#         except UserExtras.DoesNotExist:
#             return self.groups.filter(name='superuser').exists() or self.group_id.group_id == 1

#     def has_perm(self, perm, obj=None):
#         return self.get_is_superuser()

#     def has_module_perms(self, app_label):
#         return self.get_is_superuser()

# class UserExtras(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='user_id')
#     is_superuser = models.BooleanField(default=False)

#     class Meta:
#         managed = True
#         db_table = 'django_user_extras'
#         verbose_name = 'Додаткові дані користувача'
#         verbose_name_plural = 'Додаткові дані користувачів' 