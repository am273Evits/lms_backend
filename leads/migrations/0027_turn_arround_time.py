# Generated by Django 5.0 on 2024-01-17 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0026_rename_created_at_leads_upload_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turn_Arround_Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_in_hrs', models.IntegerField()),
            ],
        ),
    ]
