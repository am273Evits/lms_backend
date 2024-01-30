# Generated by Django 5.0 on 2024-01-04 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_rename_department_drp_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.drp_designation'),
        ),
        migrations.AlterField(
            model_name='product',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.drp_designation'),
        ),
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='product',
        ),
        migrations.DeleteModel(
            name='Designation',
        ),
    ]
