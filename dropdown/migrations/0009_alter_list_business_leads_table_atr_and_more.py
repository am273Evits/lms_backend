# Generated by Django 5.0 on 2023-12-18 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0008_list_business_leads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_business_leads',
            name='table_atr',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='list_business_leads',
            name='table_name',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='list_business_leads',
            name='table_type',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]