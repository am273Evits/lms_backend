# Generated by Django 5.0 on 2024-01-04 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_useraccount_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='username',
        ),
    ]
