# Generated by Django 5.0 on 2023-12-27 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evitamin', '0007_ev_services_service_id'),
        ('records', '0006_service_delete_approval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_delete_approval',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evitamin.ev_services'),
        ),
    ]