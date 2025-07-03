import pyodbc
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.db import models, connection
from django.contrib.auth.hashers import make_password
from .models import User, Permition, PermitionObject, CGroup


class SuperuserFilter(SimpleListFilter):
    title = 'superuser status'
    parameter_name = 'is_superuser'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Superuser'),
            ('0', 'Not Superuser'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(
                models.Q(userextras__is_superuser=True) |
                models.Q(group_id__group_id=1)
            ).distinct()
        if self.value() == '0':
            return queryset.exclude(
                models.Q(userextras__is_superuser=True) |
                models.Q(group_id__group_id=1)
            ).distinct()
        return queryset

def create_sql_server_login(system_login, password):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    try:
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
            BEGIN
                CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
                USE test_db;
                CREATE USER [{}] FOR LOGIN [{}];
                EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
            END
        """.format(system_login, password, system_login, system_login, system_login), (system_login,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
@admin.register(CGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'group_name')
    search_fields = ('group_name',)
@admin.register(PermitionObject)
class PermitionObjectAdmin(admin.ModelAdmin):
    list_display = ('permition_object_name', 'permition_object_caption')
    search_fields = ('permition_object_name', 'permition_object_caption')
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'system_login', 'user_name', 'group_id', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('system_login', 'user_name')
    list_filter = ('group_id', 'is_active', 'is_staff', 'is_superuser')
    actions = ['make_django_superuser']


    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def make_django_superuser(self, request, queryset):
        queryset.update(is_superuser=True, is_staff=True)
        self.message_user(request, "Вибрані користувачі отримали статус Django superuser.")
    make_django_superuser.short_description = "Зробити Django superuser"

@admin.register(Permition)
class PermitionAdmin(admin.ModelAdmin):
    list_display = ('permition_id', 'object_name', 'group_id', 'add', 'edit', 'delete', 'visible', 'edit_clean_copy')
    list_filter = ('group_id', 'visible', 'add', 'edit', 'delete')
    search_fields = ('object_name',)
    actions = ['grant_full_permissions']

    def grant_full_permissions(self, request, queryset):
        admin_group = Group.objects.get(group_id=16)
        for obj in Permition.objects.filter(group_id=admin_group):
            obj.add = True
            obj.edit = True
            obj.delete = True
            obj.visible = True
            obj.edit_clean_copy = True
            obj.save()
        self.message_user(request, "Повні права надано для групи Администраторы.")
    grant_full_permissions.short_description = "Надати повні права для Администраторы"

# @admin.register(CGroup)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('group_id', 'group_name', 'contractor_id')
#     search_fields = ('group_name',)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('user_id', 'system_login', 'user_name', 'group_id', 'is_active', 'is_staff', 'is_superuser')
#     search_fields = ('system_login', 'user_name')
#     list_filter = ('group_id', 'is_active', 'is_staff', 'is_superuser')
#     actions = ['make_django_superuser']

#     def make_django_superuser(self, request, queryset):
#         queryset.update(is_superuser=True, is_staff=True)
#         self.message_user(request, "Вибрані користувачі отримали статус Django superuser.")
#     make_django_superuser.short_description = "Зробити Django superuser"

# @admin.register(Permition)
# class PermitionAdmin(admin.ModelAdmin):
#     list_display = ('permition_id', 'object_name', 'group_id', 'add', 'edit', 'delete', 'visible', 'edit_clean_copy')
#     list_filter = ('group_id', 'visible', 'add', 'edit', 'delete')
#     search_fields = ('object_name',)
#     actions = ['grant_full_permissions']

#     def grant_full_permissions(self, request, queryset):
#         admin_group = CGroup.objects.get(group_id=16)
#         for obj in Permition.objects.filter(group_id=admin_group):
#             obj.add = True
#             obj.edit = True
#             obj.delete = True
#             obj.visible = True
#             obj.edit_clean_copy = True
#             obj.save()
#         self.message_user(request, "Повні права надано для групи Администраторы.")
#     grant_full_permissions.short_description = "Надати повні права для Администраторы"






# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'get_group_name', 'is_active', 'is_staff', 'get_is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)
#     filter_horizontal = ()

#     def get_is_superuser(self, obj):
#         return obj.get_is_superuser()
#     get_is_superuser.short_description = 'Superuser'
#     get_is_superuser.boolean = True

#     def get_group_name(self, obj):
#         if obj.group_id:
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT group_name FROM c_group WHERE group_id = %s", [obj.group_id.group_id])
#                 result = cursor.fetchone()
#                 return result[0] if result else 'Без групи'
#         return 'Без групи'
#     get_group_name.short_description = 'Назва групи'

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         if not request.user.get_is_superuser():
#             allowed_objects = Permition.objects.filter(
#                 group_id=request.user.group_id,
#                 visible=True
#             ).values_list('object_name__permition_object_name', flat=True)
#             # Add custom menu filtering logic if needed
        # return queryset

# @admin.register(Permition)
# class PermitionAdmin(admin.ModelAdmin):
#     list_display = ('permition_id', 'group_id', 'object_name', 'permition_value', 'visible', 'add', 'edit', 'delete', 'edit_clean_copy')
#     list_filter = ('group_id', 'visible', 'add', 'edit', 'delete')
#     search_fields = ('object_name__permition_object_caption',)
#     actions = ['grant_full_permissions']

#     def grant_full_permissions(self, request, queryset):
#         superuser_group = CGroup.objects.get(group_id=1)  # Або твій group_id для superuser
#         for obj in Permition.objects.filter(group_id=superuser_group):
#             obj.add = True
#             obj.change = True
#             obj.delete = True
#             obj.visible = True
#             obj.save()
#         self.message_user(request, "Повні права надано для групи superuser.")
#     grant_full_permissions.short_description = "Надати повні права для superuser"


# admin.site.register(User, CustomUserAdmin)

# users/admin.py
# from django.contrib import admin
# from .models import Group, User, Permition

# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('group_id', 'group_name', 'contractor_id')
#     search_fields = ('group_name',)


#deploy
# import pyodbc
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin import SimpleListFilter
# from django.db import models, connection
# from .models import User

# class SuperuserFilter(SimpleListFilter):
#     title = 'superuser status'
#     parameter_name = 'is_superuser'

#     def lookups(self, request, model_admin):
#         return (
#             ('1', 'Superuser'),
#             ('0', 'Not Superuser'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == '1':
#             return queryset.filter(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id__group_id=1)
#             ).distinct()
#         if self.value() == '0':
#             return queryset.exclude(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id__group_id=1)
#             ).distinct()
#         return queryset

# def create_sql_server_login(system_login, password):
#     conn = pyodbc.connect(
#         'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
#             BEGIN
#                 CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
#                 USE test_db;
#                 CREATE USER [{}] FOR LOGIN [{}];
#                 EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
#             END
#         """.format(system_login, password, system_login, system_login, system_login), (system_login,))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         raise
#     finally:
#         cursor.close()
#         conn.close()

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'get_group_name', 'is_active', 'is_staff', 'get_is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)
#     filter_horizontal = ()

#     def get_is_superuser(self, obj):
#         return obj.get_is_superuser()
#     get_is_superuser.short_description = 'Superuser'
#     get_is_superuser.boolean = True

#     def get_group_name(self, obj):
#         """Отримує назву групи з таблиці c_group за group_id."""
#         if obj.group_id:
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT group_name FROM c_group WHERE group_id = %s", [obj.group_id.group_id])
#                 result = cursor.fetchone()
#                 return result[0] if result else 'Без групи'
#         return 'Без групи'
#     get_group_name.short_description = 'Назва групи'

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

# admin.site.register(User, CustomUserAdmin)# import pyodbc
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin import SimpleListFilter
# from django.db import models, connection
# from .models import User

# class SuperuserFilter(SimpleListFilter):
#     title = 'superuser status'
#     parameter_name = 'is_superuser'

#     def lookups(self, request, model_admin):
#         return (
#             ('1', 'Superuser'),
#             ('0', 'Not Superuser'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == '1':
#             return queryset.filter(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id__group_id=1)  # Updated to use group_id__group_id
#             ).distinct()
#         if self.value() == '0':
#             return queryset.exclude(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id__group_id=1)  # Updated to use group_id__group_id
#             ).distinct()
#         return queryset

# def create_sql_server_login(system_login, password):
#     conn = pyodbc.connect(
#         'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
#             BEGIN
#                 CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
#                 USE test_db;
#                 CREATE USER [{}] FOR LOGIN [{}];
#                 EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
#             END
#         """.format(system_login, password, system_login, system_login, system_login), (system_login,))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         raise
#     finally:
#         cursor.close()
#         conn.close()

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'get_group_name', 'is_active', 'is_staff', 'get_is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)
#     filter_horizontal = ()

#     def get_is_superuser(self, obj):
#         return obj.get_is_superuser()
#     get_is_superuser.short_description = 'Superuser'
#     get_is_superuser.boolean = True

#     def get_group_name(self, obj):
#         """Отримує назву групи з таблиці c_group за group_id."""
#         if obj.group_id:
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT group_name FROM c_group WHERE group_id = %s", [obj.group_id.group_id])  # Use group_id.group_id
#                 result = cursor.fetchone()
#                 return result[0] if result else 'Без групи'
#         return 'Без групи'
#     get_group_name.short_description = 'Назва групи'

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

# admin.site.register(User, CustomUserAdmin)
# import pyodbc
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin import SimpleListFilter
# from django.db import models
# from .models import User

# class SuperuserFilter(SimpleListFilter):
#     title = 'superuser status'
#     parameter_name = 'is_superuser'

#     def lookups(self, request, model_admin):
#         return (
#             ('1', 'Superuser'),
#             ('0', 'Not Superuser'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == '1':
#             return queryset.filter(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id=1)
#             ).distinct()
#         if self.value() == '0':
#             return queryset.exclude(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id=1)
#             ).distinct()
#         return queryset

# def create_sql_server_login(system_login, password):
#     conn = pyodbc.connect(
#         'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
#             BEGIN
#                 CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
#                 USE test_db;
#                 CREATE USER [{}] FOR LOGIN [{}];
#                 EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
#             END
#         """.format(system_login, password, system_login, system_login, system_login), (system_login,))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         raise
#     finally:
#         cursor.close()
#         conn.close()

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'get_group_name', 'is_active', 'is_staff', 'get_is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)
#     filter_horizontal = ()

#     def get_is_superuser(self, obj):
#         return obj.get_is_superuser()
#     get_is_superuser.short_description = 'Superuser'
#     get_is_superuser.boolean = True

#     def get_group_name(self, obj):
#         """Отримує назву групи з таблиці c_group за group_id."""
#         if obj.group_id:
#             try:
#                 conn = pyodbc.connect(
#                     'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=test_db;Trusted_Connection=yes;'
#                 )
#                 cursor = conn.cursor()
#                 cursor.execute("SELECT group_name FROM c_group WHERE group_id = ?", (obj.group_id,))
#                 result = cursor.fetchone()
#                 cursor.close()
#                 conn.close()
#                 return result[0] if result else 'Без групи'
#             except Exception as e:
#                 print(f"Error fetching group name: {e}")
#                 return 'Помилка'
#         return 'Без групи'
#     get_group_name.short_description = 'Назва групи'

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

# admin.site.register(User, CustomUserAdmin)
# import pyodbc
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin import SimpleListFilter
# from django.db import models
# from .models import User

# class SuperuserFilter(SimpleListFilter):
#     title = 'superuser status'
#     parameter_name = 'is_superuser'

#     def lookups(self, request, model_admin):
#         return (
#             ('1', 'Superuser'),
#             ('0', 'Not Superuser'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == '1':
#             return queryset.filter(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id=1)
#             ).distinct()
#         if self.value() == '0':
#             return queryset.exclude(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id=1)
#             ).distinct()
#         return queryset

# def create_sql_server_login(system_login, password):
#     conn = pyodbc.connect(
#         'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
#             BEGIN
#                 CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
#                 USE test_db;
#                 CREATE USER [{}] FOR LOGIN [{}];
#                 EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
#             END
#         """.format(system_login, password, system_login, system_login, system_login), (system_login,))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         raise
#     finally:
#         cursor.close()
#         conn.close()

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),  # Removed 'groups'
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'is_active', 'is_staff', 'get_is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)
#     filter_horizontal = ()  # Removed 'groups'

#     def get_is_superuser(self, obj):
#         return obj.get_is_superuser()
#     get_is_superuser.short_description = 'Superuser'
#     get_is_superuser.boolean = True

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

# admin.site.register(User, CustomUserAdmin)
# import pyodbc
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin import SimpleListFilter
# from django.db import models
# from .models import User

# class SuperuserFilter(SimpleListFilter):
#     title = 'superuser status'
#     parameter_name = 'is_superuser'

#     def lookups(self, request, model_admin):
#         return (
#             ('1', 'Superuser'),
#             ('0', 'Not Superuser'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == '1':
#             return queryset.filter(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id=1)
#             ).distinct()
#         if self.value() == '0':
#             return queryset.exclude(
#                 models.Q(userextras__is_superuser=True) |
#                 models.Q(group_id=1)
#             ).distinct()
#         return queryset

# def create_sql_server_login(system_login, password):
#     conn = pyodbc.connect(
#         'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
#             BEGIN
#                 CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
#                 USE test_db;
#                 CREATE USER [{}] FOR LOGIN [{}];
#                 EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
#             END
#         """.format(system_login, password, system_login, system_login, system_login), (system_login,))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         raise
#     finally:
#         cursor.close()
#         conn.close()

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'is_active', 'is_staff', 'get_is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)
#     filter_horizontal = ('groups',)

#     def get_is_superuser(self, obj):
#         return obj.get_is_superuser()
#     get_is_superuser.short_description = 'Superuser'
#     get_is_superuser.boolean = True

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

# admin.site.register(User, CustomUserAdmin)
# def create_sql_server_login(system_login, password):
#     conn = pyodbc.connect(
#         'DRIVER={SQL Server Native Client 10.0};'
#         'SERVER=localhost;'
#         'DATABASE=master;'
#         'Trusted_Connection=yes;'
#     )
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = ?)
#             BEGIN
#                 CREATE LOGIN [{}] WITH PASSWORD=N'{}', DEFAULT_DATABASE=[test_db], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON;
#                 USE test_db;
#                 CREATE USER [{}] FOR LOGIN [{}];
#                 EXEC sys.sp_addsrvrolemember @loginame = N'{}', @rolename = N'sysadmin';
#             END
#         """.format(system_login, password, system_login, system_login, system_login), (system_login,))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         raise
#     finally:
#         cursor.close()
#         conn.close()

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id', 'system_login', 'password')}),
#         ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
#     list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'is_active', 'is_staff', 'is_superuser')
#     list_filter = ('is_active', 'is_staff', 'subdivision_id')  # Removed is_superuser
#     search_fields = ('system_login', 'user_name')
#     ordering = ('user_id',)
#     readonly_fields = ('user_id',)

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         if not change and 'password1' in form.cleaned_data:
#             create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

# admin.site.register(User, CustomUserAdmin)