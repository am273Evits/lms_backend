# Generated by Django 5.0.1 on 2024-04-30 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0081_remove_service_category_mou_approval_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercial_approval',
            name='approval_type',
            field=models.BooleanField(default=False),
        ),
    ]
