# Generated by Django 5.0 on 2023-12-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0015_remove_all_identifiers_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_identifiers',
            name='service_country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]