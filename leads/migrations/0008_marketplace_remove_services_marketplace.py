# Generated by Django 5.0 on 2024-01-10 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_remove_leads_email_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(blank=True, default='', max_length=100)),
                ('marketplace', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='services',
            name='marketplace',
        ),
    ]
