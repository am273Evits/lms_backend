# Generated by Django 5.0 on 2024-03-05 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_alter_useraccount_employee_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='employee_status',
        ),
    ]