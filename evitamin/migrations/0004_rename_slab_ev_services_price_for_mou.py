# Generated by Django 5.0 on 2023-12-27 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evitamin', '0003_email_ask_for_details_email_service_proposal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ev_services',
            old_name='slab',
            new_name='price_for_mou',
        ),
    ]
