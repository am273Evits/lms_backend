# Generated by Django 5.0 on 2024-02-13 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0031_remove_commercials_service_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercials',
            name='visibility',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='marketplace',
            name='visibility',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='services',
            name='visibility',
            field=models.BooleanField(default=True),
        ),
    ]
