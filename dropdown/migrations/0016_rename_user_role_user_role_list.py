# Generated by Django 5.0 on 2023-12-20 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0015_business_category_list'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_role',
            new_name='user_role_list',
        ),
    ]