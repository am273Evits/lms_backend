# Generated by Django 5.0 on 2023-12-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0003_delete_email_ask_for_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_links',
            name='access_department',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='user_links',
            name='link_type',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='user_links',
            name='table_ref',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='user_links',
            name='title',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='user_links',
            name='user_link',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
