# Generated by Django 5.0 on 2023-12-30 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_useraccount_employee_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='employee_status',
            field=models.IntegerField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.IntegerField(max_length=300, null=True),
        ),
    ]
