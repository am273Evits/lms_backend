# Generated by Django 5.0 on 2023-12-30 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_useraccount_employee_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='employee_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.employee_status'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.gender'),
            preserve_default=False,
        ),
    ]
