# Generated by Django 5.0.1 on 2024-04-17 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0049_service_category_associate'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_category',
            name='payment_approval',
            field=models.BooleanField(blank=True, default='', null=True),
        ),
    ]