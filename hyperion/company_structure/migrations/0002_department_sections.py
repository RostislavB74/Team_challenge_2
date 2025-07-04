# Generated by Django 4.2 on 2025-06-23 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_structure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department_sections',
            fields=[
                ('id', models.SmallIntegerField(db_column='production_section_id', primary_key=True, serialize=False)),
                ('name', models.SmallIntegerField(db_column='production_section')),
                ('descriptions', models.CharField(blank=True, db_column='descriptions', max_length=255, null=True)),
                ('archived', models.BooleanField(db_column='archived', default=False)),
                ('num', models.SmallIntegerField(blank=True, db_column='num', null=True)),
            ],
            options={
                'verbose_name': 'Виробнича секція',
                'verbose_name_plural': 'Виробнгичі секції',
                'db_table': 'c_production_section',
                'managed': False,
            },
        ),
    ]
