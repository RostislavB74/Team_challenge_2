from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.db import models

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
        verbose_name = 'Група користувача'
        verbose_name_plural = 'Групи користувачів'

    def __str__(self):
        return f"{self.user.system_login} - {self.group.name}"

class CGroup(models.Model):
    group_id = models.SmallIntegerField(primary_key=True, db_column='group_id')
    group_name = models.CharField(max_length=255, db_column='group_name')

    class Meta:
        managed = False
        db_table = 'c_group'
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    def __str__(self):
        return self.group_name

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    group_id = models.ForeignKey(CGroup, on_delete=models.CASCADE, db_column='group_id')
    system_login = models.CharField(max_length=100, unique=True)
    user_name = models.CharField(max_length=100)
    subdivision_id = models.IntegerField(default=1)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'system_login'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        managed = False
        db_table = 'c_user'
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
    def __str__(self):
        return self.user_name

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
                self.group_id.group_id == 1  # Updated to use group_id.group_id
            )
        except UserExtras.DoesNotExist:
            return self.groups.filter(name='superuser').exists() or self.group_id.group_id == 1

    def has_perm(self, perm, obj=None):
        return self.get_is_superuser()

    def has_module_perms(self, app_label):
        return self.get_is_superuser()

class UserExtras(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='user_id')
    is_superuser = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'django_user_extras'
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

# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key=True, db_column='user_id')
#     group_id = models.IntegerField()
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
#         blank=True
#     )

#     def get_is_superuser(self):
#         try:
#             return (
#                 self.userextras.is_superuser or
#                 self.groups.filter(name='superuser').exists() or
#                 self.group_id == 1
#             )
#         except UserExtras.DoesNotExist:
#             return self.groups.filter(name='superuser').exists() or self.group_id == 1

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

# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key=True, db_column='user_id')
#     group_id = models.IntegerField()
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
#         blank=True
#     )

#     def get_is_superuser(self):
#         try:
#             return (
#                 self.userextras.is_superuser or
#                 self.groups.filter(name='superuser').exists() or
#                 self.group_id == 1
#             )
#         except UserExtras.DoesNotExist:
#             return self.groups.filter(name='superuser').exists() or self.group_id == 1

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