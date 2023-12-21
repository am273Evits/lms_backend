# Generated by Django 5.0 on 2023-12-20 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0016_all_identifiers_service_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business_identifiers',
            old_name='designation',
            new_name='designation_in_company',
        ),
        migrations.RenameField(
            model_name='followup',
            old_name='service_category',
            new_name='service',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='service_name',
            new_name='marketplace',
        ),
    ]
