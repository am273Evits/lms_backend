# Generated by Django 5.0 on 2024-01-10 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0017_service_category_pricing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='service_category',
        ),
        migrations.AddField(
            model_name='service_category',
            name='lead_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.leads'),
        ),
    ]
