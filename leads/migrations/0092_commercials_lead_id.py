# Generated by Django 5.0.1 on 2024-05-09 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0091_alter_service_category_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercials',
            name='lead_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.service_category'),
        ),
    ]