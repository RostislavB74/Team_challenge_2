# Generated by Django 4.2 on 2025-06-26 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cgroup',
            options={'managed': False, 'verbose_name': 'Група', 'verbose_name_plural': 'Групи'},
        ),
        migrations.AlterModelOptions(
            name='usergroup',
            options={'managed': False, 'verbose_name': 'Група користувача', 'verbose_name_plural': 'Групи користувачів'},
        ),
    ]
