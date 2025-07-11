"""
URL configuration for hyperion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('tiles/', include('tiles.urls')),
# ]
# hyperion/urls.py
from django.contrib import admin
from django.urls import path
from journals import views

    
urlpatterns = [
    path('shift-reports/<int:doc_id>/row/create/', views.shift_report_row_create, name='shift_report_row_create'),
    path("admin/", admin.site.urls),
    path("shift-reports/", views.shift_report_list, name="shift_report_list"),
    path(
        "shift-reports/<int:doc_id>/",
        views.shift_report_detail,
        name="shift_report_detail",
    ),
    path(
        "shift-reports/create/", views.shift_report_create, name="shift_report_create"
    ),
    path(
        "shift-reports/<int:doc_id>/edit/",
        views.shift_report_edit,
        name="shift_report_edit",
    ),
    path(
        "shift-reports/<int:doc_id>/delete/",
        views.shift_report_delete,
        name="shift_report_delete",
    ),
]
