# Generated by Django 5.0 on 2023-12-20 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_alter_lead_delete_approval_lead_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='lead_status_record',
        ),
    ]
