# Generated by Django 5.0 on 2023-12-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0004_alter_user_links_access_department_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ev_department_designation',
        ),
        migrations.DeleteModel(
            name='ev_employee_status',
        ),
        migrations.DeleteModel(
            name='list_business_leads',
        ),
        migrations.DeleteModel(
            name='list_client',
        ),
        migrations.DeleteModel(
            name='list_employee',
        ),
        migrations.RemoveField(
            model_name='ev_branch_location',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ev_products',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='country',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='marketplace',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='percentage_service_fees',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='service_currency',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='services',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='slab',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='ev_services',
            name='static_service_fees',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
