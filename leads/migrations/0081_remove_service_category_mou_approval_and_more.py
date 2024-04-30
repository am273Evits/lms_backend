# Generated by Django 5.0.1 on 2024-04-30 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0080_service_category_mou_service_category_payment_proof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service_category',
            name='mou_approval',
        ),
        migrations.AlterField(
            model_name='service_category',
            name='mou',
            field=models.FileField(blank=True, default='', null=True, upload_to='mou'),
        ),
        migrations.AlterField(
            model_name='service_category',
            name='payment_proof',
            field=models.FileField(blank=True, default='', null=True, upload_to='payment_proof'),
        ),
    ]
