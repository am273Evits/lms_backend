# Generated by Django 5.0 on 2024-01-05 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_remove_useraccount_user_links_delete_user_links'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=500)),
                ('link_type', models.CharField(blank=True, default='', max_length=500)),
                ('user_link', models.CharField(blank=True, default='', max_length=500)),
                ('access_department', models.CharField(blank=True, default='', max_length=500)),
                ('table_ref', models.CharField(blank=True, default='', max_length=500)),
                ('visibility', models.BooleanField(default=False)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.department')),
                ('designation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.designation')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.product')),
            ],
        ),
    ]
