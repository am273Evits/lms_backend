# Generated by Django 4.2.6 on 2023-12-08 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dropdown', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='xsup_drp_business_type',
            new_name='business_type',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_contact_preference',
            new_name='contact_preference',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_decision',
            new_name='decision',
        ),
        migrations.RenameModel(
            old_name='xsup_ev_employee_status',
            new_name='dropdown_fields',
        ),
        migrations.RenameModel(
            old_name='xsup_email_ask_for_details',
            new_name='email_ask_for_details',
        ),
        migrations.RenameModel(
            old_name='xsup_email_service_proposal',
            new_name='email_service_proposal',
        ),
        migrations.RenameModel(
            old_name='xsup_ev_bank_details',
            new_name='ev_bank_details',
        ),
        migrations.RenameModel(
            old_name='xsup_ev_branch_location',
            new_name='ev_branch_location',
        ),
        migrations.RenameModel(
            old_name='xsup_ev_products',
            new_name='ev_department_designation',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_dropdown_fields',
            new_name='ev_employee_status',
        ),
        migrations.RenameModel(
            old_name='xsup_ev_department_designation',
            new_name='ev_products',
        ),
        migrations.RenameModel(
            old_name='xsup_ev_services',
            new_name='ev_services',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_firm_type',
            new_name='firm_type',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_service_country',
            new_name='gender',
        ),
        migrations.RenameModel(
            old_name='xsup_image_src',
            new_name='image_src',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_user_role',
            new_name='lead_status',
        ),
        migrations.RenameModel(
            old_name='xsup_list_employee',
            new_name='list_business_leads',
        ),
        migrations.RenameModel(
            old_name='xsup_list_client',
            new_name='list_client',
        ),
        migrations.RenameModel(
            old_name='xsup_list_business_leads',
            new_name='list_employee',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_lead_status',
            new_name='not_interested_reason',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_unresponsive_reason',
            new_name='service_category',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_not_interested_reason',
            new_name='service_country',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_service_category',
            new_name='unresponsive_reason',
        ),
        migrations.RenameModel(
            old_name='xsup_user_links',
            new_name='user_links',
        ),
        migrations.RenameModel(
            old_name='xsup_drp_gender',
            new_name='user_role',
        ),
        migrations.RenameField(
            model_name='dropdown_fields',
            old_name='created_by',
            new_name='dropdown_fields',
        ),
        migrations.RenameField(
            model_name='dropdown_fields',
            old_name='title',
            new_name='ref_tb',
        ),
        migrations.RenameField(
            model_name='ev_department_designation',
            old_name='department',
            new_name='designation',
        ),
        migrations.RenameField(
            model_name='ev_employee_status',
            old_name='dropdown_fields',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='ev_employee_status',
            old_name='ref_tb',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='ev_products',
            old_name='designation',
            new_name='department',
        ),
    ]
