# Generated by Django 5.0.1 on 2024-04-17 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0055_alter_followup_history_followup_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service_category',
            name='lead_id',
        ),
    ]
