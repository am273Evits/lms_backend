# Generated by Django 5.0 on 2024-01-04 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_designation_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='drp_Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
