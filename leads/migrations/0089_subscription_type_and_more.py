# Generated by Django 5.0.1 on 2024-05-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0088_service_category_subscription_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='service_category',
            name='subscription_type',
        ),
    ]
