# Generated by Django 5.0 on 2024-01-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_useraccount_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='title',
            field=models.IntegerField(),
        ),
    ]
