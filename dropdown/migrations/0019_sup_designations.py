# Generated by Django 5.0 on 2023-12-26 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0018_rename_country_country_state_city_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='sup_designations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
    ]
