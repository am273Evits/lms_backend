# Generated by Django 5.0 on 2023-12-20 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0013_rename_dropdown_fields_dropdown_fields_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='prop_dir_designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
    ]
