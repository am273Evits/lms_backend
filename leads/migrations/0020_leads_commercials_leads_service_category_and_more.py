# Generated by Django 5.0 on 2024-01-11 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0019_alter_leads_visibility'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='commercials',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.commercials'),
        ),
        migrations.AddField(
            model_name='leads',
            name='service_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.services'),
        ),
        migrations.AddField(
            model_name='leads',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.drp_lead_status'),
        ),
        migrations.DeleteModel(
            name='Service_category',
        ),
    ]
