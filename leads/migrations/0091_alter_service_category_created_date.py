# Generated by Django 5.0.1 on 2024-05-03 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0090_service_category_subscription_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_category',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]