import pyodbc
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.db import models, connection
from .models import User

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
                models.Q(group_id__group_id=1)  # Updated to use group_id__group_id
            ).distinct()
        if self.value() == '0':
            return queryset.exclude(
                models.Q(userextras__is_superuser=True) |
                models.Q(group_id__group_id=1)  # Updated to use group_id__group_id
            ).distinct()
        return queryset

def create_sql_server_login(system_login, password):
    conn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 10.0};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
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

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('user_id', 'system_login', 'password')}),
        ('Personal info', {'fields': ('user_name', 'group_id', 'subdivision_id', 'phone', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('system_login', 'user_name', 'subdivision_id', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('user_id', 'system_login', 'user_name', 'subdivision_id', 'get_group_name', 'is_active', 'is_staff', 'get_is_superuser')
    list_filter = ('is_active', 'is_staff', 'subdivision_id', SuperuserFilter)
    search_fields = ('system_login', 'user_name')
    ordering = ('user_id',)
    readonly_fields = ('user_id',)
    filter_horizontal = ()

    def get_is_superuser(self, obj):
        return obj.get_is_superuser()
    get_is_superuser.short_description = 'Superuser'
    get_is_superuser.boolean = True

    def get_group_name(self, obj):
        """Отримує назву групи з таблиці c_group за group_id."""
        if obj.group_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT group_name FROM c_group WHERE group_id = %s", [obj.group_id.group_id])  # Use group_id.group_id
                result = cursor.fetchone()
                return result[0] if result else 'Без групи'
        return 'Без групи'
    get_group_name.short_description = 'Назва групи'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and 'password1' in form.cleaned_data:
            create_sql_server_login(obj.system_login, form.cleaned_data['password1'])

admin.site.register(User, CustomUserAdmin)
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