# Generated by Django 5.0 on 2024-03-17 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0037_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='marketplace',
            new_name='program',
        ),
    ]
