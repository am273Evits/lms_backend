# Generated by Django 5.0 on 2024-04-25 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0075_delete_ask_for_detail_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_category',
            name='lead_id',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
