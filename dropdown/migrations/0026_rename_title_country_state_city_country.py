# Generated by Django 5.0 on 2023-12-26 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0025_user_role_list_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country_state_city',
            old_name='title',
            new_name='country',
        ),
    ]
