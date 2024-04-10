# Generated by Django 5.0.1 on 2024-04-09 09:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0041_useraccount_marketplace_useraccount_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='director_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='lead_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_manager_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='user_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_manager_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
