# Generated by Django 5.0 on 2023-12-27 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evitamin', '0005_rename_percentage_service_fees_ev_services_commission_service_fees_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ev_services',
            old_name='commission_price',
            new_name='commission_fees',
        ),
    ]
