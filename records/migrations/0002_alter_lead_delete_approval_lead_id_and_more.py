# Generated by Django 5.0 on 2023-12-20 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0018_alter_business_identifiers_lead_id_and_more'),
        ('dropdown', '0017_country_state_city'),
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead_delete_approval',
            name='lead_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_leads.all_identifiers'),
        ),
        migrations.CreateModel(
            name='lead_status_record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('lead_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_leads.all_identifiers')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dropdown.lead_status')),
            ],
        ),
    ]
