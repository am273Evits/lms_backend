# Generated by Django 5.0 on 2024-04-24 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0070_service_category_status_history_all'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Drp_business_category',
            new_name='Business_category',
        ),
        migrations.RenameModel(
            old_name='Drp_business_type',
            new_name='Business_type',
        ),
        migrations.RenameModel(
            old_name='Drp_firm_type',
            new_name='Firm_type',
        ),
        migrations.RemoveField(
            model_name='service_category',
            name='Status_history_all',
        ),
    ]
