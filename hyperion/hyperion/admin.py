# Наприклад: core/admin_site.py

from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MyAdminSite(AdminSite):
    site_header = "Моя адміністративна панель"
    site_title = "Адмінка"
    index_title = "Навігація"

 

my_admin_site = MyAdminSite(name="myadmin")


# admin.site = my_admin_site
# У тому ж файлі або в core/admin.py


my_admin_site.register(User, UserAdmin)
