# Generated by Django 5.0 on 2023-12-19 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0013_contact_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_identifiers',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
