# Generated by Django 5.0 on 2024-01-15 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0023_leads_alternate_email_id_leads_email_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leads',
            name='hot_lead',
            field=models.BooleanField(default=False),
        ),
    ]
