# Generated by Django 5.0 on 2023-12-27 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0027_rename_country_country_state_city_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='list_employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(blank=True, default='', max_length=500)),
                ('table_type', models.CharField(blank=True, default='', max_length=500)),
                ('table_atr', models.CharField(blank=True, default='', max_length=500)),
            ],
        ),
    ]
