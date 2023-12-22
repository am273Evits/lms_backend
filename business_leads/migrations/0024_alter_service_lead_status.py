# Generated by Django 5.0 on 2023-12-22 04:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0023_alter_service_lead_status'),
        ('dropdown', '0018_rename_country_country_state_city_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='lead_status',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='dropdown.lead_status'),
            preserve_default=False,
        ),
    ]
