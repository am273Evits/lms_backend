# Generated by Django 5.0 on 2024-01-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0024_alter_leads_hot_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
