# Generated by Django 5.0 on 2024-04-23 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0069_alter_leads_lead_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_category',
            name='Status_history_all',
            field=models.ManyToManyField(to='leads.status_history'),
        ),
    ]