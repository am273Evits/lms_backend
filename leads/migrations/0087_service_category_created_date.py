# Generated by Django 5.0.1 on 2024-05-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0086_alter_service_category_payment_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_category',
            name='created_date',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]