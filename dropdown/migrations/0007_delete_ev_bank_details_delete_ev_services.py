# Generated by Django 5.0 on 2023-12-14 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0006_delete_ev_branch_location_delete_ev_products'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ev_bank_details',
        ),
        migrations.DeleteModel(
            name='ev_services',
        ),
    ]
