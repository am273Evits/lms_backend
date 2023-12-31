# Generated by Django 5.0 on 2023-12-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee_basic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=300, null=True)),
                ('employee_status', models.CharField(max_length=300, null=True)),
                ('name', models.CharField(max_length=300, null=True)),
                ('gender', models.CharField(max_length=300, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('blood_group', models.CharField(max_length=300, null=True)),
                ('age', models.CharField(max_length=300, null=True)),
                ('disability', models.CharField(max_length=300, null=True)),
                ('email_id', models.CharField(max_length=300, null=True)),
                ('marital_status', models.CharField(max_length=300, null=True)),
                ('mobile_number', models.CharField(max_length=300, null=True)),
                ('alternate_mobile_number', models.CharField(max_length=300, null=True)),
                ('nationality', models.CharField(max_length=300, null=True)),
                ('emergency_contact_number', models.CharField(max_length=300, null=True)),
                ('religion', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='employee_official',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=500, null=True)),
                ('department', models.CharField(max_length=500, null=True)),
                ('designation', models.CharField(max_length=500, null=True)),
                ('product', models.CharField(max_length=500, null=True)),
                ('team_leader', models.CharField(max_length=500, null=True)),
                ('team_manager', models.CharField(max_length=500, null=True)),
                ('admin', models.CharField(max_length=500, null=True)),
                ('super_admin', models.CharField(max_length=500, null=True)),
                ('user_role', models.CharField(max_length=500, null=True)),
                ('branch', models.CharField(max_length=500, null=True)),
                ('office_location', models.CharField(max_length=500, null=True)),
                ('email_id_official', models.CharField(max_length=500, null=True)),
                ('tool_login_id', models.CharField(max_length=500, null=True)),
                ('evitamin_portal_login_id', models.CharField(max_length=500, null=True)),
                ('joining_date', models.DateField(null=True)),
                ('signed_bond', models.CharField(max_length=500, null=True)),
                ('work_from_home', models.CharField(max_length=500, null=True)),
                ('employee_status', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
