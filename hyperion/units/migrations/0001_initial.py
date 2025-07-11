# Generated by Django 4.2 on 2025-06-22 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialUnit',
            fields=[
                ('id', models.SmallIntegerField(db_column='unit_id', primary_key=True, serialize=False)),
                ('name', models.SmallIntegerField(db_column='unit_name')),
                ('unit', models.SmallIntegerField(db_column='unit_alias')),
                ('code', models.SmallIntegerField(db_column='okei')),
                ('id_1c_code', models.SmallIntegerField(db_column='id_1c8')),
            ],
            options={
                'db_table': 'c_unit',
                'managed': False,
            },
        ),
    ]
