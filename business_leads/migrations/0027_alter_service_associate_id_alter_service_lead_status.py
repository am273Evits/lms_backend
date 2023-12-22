# Generated by Django 5.0 on 2023-12-22 05:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0026_alter_service_associate_id'),
        ('dropdown', '0018_rename_country_country_state_city_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='associate_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='lead_status',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dropdown.lead_status'),
        ),
    ]
