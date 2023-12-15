# Generated by Django 5.0 on 2023-12-13 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_leads', '0002_alter_business_identifiers_lead_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_identifiers',
            name='account_manager',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='actual_date_of_reaching_destination_port',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='amazon_comments',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='assured_delivery_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='cancelled_request_status_reason_code',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='change_status_to',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='comments',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='container_number',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='created_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='current_status',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='date_of_filing_poa',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='date_of_shipping_out_of_origin_port',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='delivery_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='dispatch_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='email_id',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='end_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='estimated_dispatch_date_sample',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='followup_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='fulfillment_center',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='interest_rate',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='lead_id',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='loan_amount',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='loan_tenure_in_months',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='marketplace',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='mode_of_training',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='not_interested_request_status_reason_code',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='not_reachable_request_status_reason_code',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='note_from_requester',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='number_of_products_cataloging_ebc_compliance',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='number_of_products_editing',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='number_of_products_model_shoot',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='number_of_products_table_top',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='order_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='pickup_pincode',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='pitch_in_progress_request_status_reason_code',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='pre_closure_charges',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='processing_fee',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='production_start_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='provider_id',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='request_id',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='requester_id',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='requester_location',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='requester_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='requester_sell_in_country',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='sales_manager',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='service_category',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='service_requester_type',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='shipment_id',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='shipment_tracking_id_awb',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='start_date_pickup_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='test_result',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='total_weight',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='trademark_pto',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='trademark_serial_number',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='trademark_type',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='all_identifiers',
            name='type_of_service_offered',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
