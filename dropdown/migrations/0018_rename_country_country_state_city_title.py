# Generated by Django 5.0 on 2023-12-21 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0017_country_state_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country_state_city',
            old_name='country',
            new_name='title',
        ),
    ]