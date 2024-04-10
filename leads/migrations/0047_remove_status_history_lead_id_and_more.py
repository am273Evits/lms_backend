# Generated by Django 5.0.1 on 2024-04-10 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0046_remove_remark_history_lead_id_leads_remark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status_history',
            name='lead_id',
        ),
        migrations.AddField(
            model_name='leads',
            name='status_history_all',
            field=models.ManyToManyField(to='leads.status_history'),
        ),
    ]
