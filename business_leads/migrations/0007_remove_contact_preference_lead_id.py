# Generated by Django 5.0 on 2023-12-19 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0006_rename_contact_preference_contact_preference_contact_preferences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact_preference',
            name='lead_id',
        ),
    ]
