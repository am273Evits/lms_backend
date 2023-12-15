from django.db import models

# Create your models here.

class all_identifiers(models.Model):
    lead_id = models.CharField(max_length=100, blank=True, default='')
    marketplace = models.CharField(max_length=100, blank=True, default='')
    request_id = models.CharField(max_length=150, blank=True, default='')
    provider_id = models.CharField(max_length=150, blank=True, default='')
    service_requester_type = models.CharField(max_length=200, blank=True, default='')
    requester_name = models.CharField(max_length=100, blank=True, default='')
    requester_id = models.CharField(max_length=150, blank=True, default='')
    phone_number = models.CharField(max_length=50, blank=True, default='')
    email_id = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    created_date = models.CharField(max_length=200, blank=True, default='')
    service_category = models.CharField(max_length=200, blank=True, default='')
    requester_location = models.CharField(max_length=200, blank=True, default='')
    requester_sell_in_country = models.CharField(max_length=200, blank=True, default='')
    current_status = models.CharField(max_length=200, blank=True, default='')
    change_status_to = models.CharField(max_length=200, blank=True, default='')
    shipment_id = models.CharField(max_length=200, blank=True, default='')
    fulfillment_center = models.CharField(max_length=200, blank=True, default='')
    delivery_date = models.CharField(max_length=200, blank=True, default='')
    total_weight = models.CharField(max_length=200, blank=True, default='')
    shipment_tracking_id_awb = models.CharField(max_length=200, blank=True, default='')
    pickup_pincode = models.CharField(max_length=200, blank=True, default='')
    followup_date = models.CharField(max_length=200, blank=True, default='')
    pitch_in_progress_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
    not_interested_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
    not_reachable_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
    cancelled_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
    sales_manager = models.CharField(max_length=200, blank=True, default='')
    comments = models.CharField(max_length=200, blank=True, default='')
    amazon_comments = models.CharField(max_length=200, blank=True, default='')
    note_from_requester = models.TextField(blank=True, default='')
    account_manager = models.CharField(max_length=200, blank=True, default='')
    start_date_pickup_date = models.CharField(max_length=200, blank=True, default='')
    end_date = models.CharField(max_length=200, blank=True, default='')
    type_of_service_offered = models.CharField(max_length=200, blank=True, default='')
    mode_of_training = models.CharField(max_length=200, blank=True, default='')
    number_of_products_model_shoot = models.CharField(max_length=200, blank=True, default='')
    number_of_products_table_top = models.CharField(max_length=200, blank=True, default='')
    number_of_products_editing = models.CharField(max_length=200, blank=True, default='')
    number_of_products_cataloging_ebc_compliance = models.CharField(max_length=200, blank=True, default='')
    date_of_filing_poa = models.CharField(max_length=200, blank=True, default='')
    test_result = models.CharField(max_length=200, blank=True, default='')
    trademark_type = models.CharField(max_length=200, blank=True, default='')
    trademark_serial_number = models.CharField(max_length=200, blank=True, default='')
    trademark_pto = models.CharField(max_length=200, blank=True, default='')
    actual_date_of_reaching_destination_port = models.CharField(max_length=200, blank=True, default='')
    date_of_shipping_out_of_origin_port = models.CharField(max_length=200, blank=True, default='')
    container_number = models.CharField(max_length=200, blank=True, default='')
    order_date = models.CharField(max_length=200, blank=True, default='')
    estimated_dispatch_date_sample = models.CharField(max_length=200, blank=True, default='')
    assured_delivery_date = models.CharField(max_length=200, blank=True, default='')
    production_start_date = models.CharField(max_length=200, blank=True, default='')
    dispatch_date = models.CharField(max_length=200, blank=True, default='')
    interest_rate = models.CharField(max_length=200, blank=True, default='')
    loan_amount = models.CharField(max_length=200, blank=True, default='')
    loan_tenure_in_months = models.CharField(max_length=200, blank=True, default='')
    processing_fee = models.CharField(max_length=200, blank=True, default='')
    pre_closure_charges = models.CharField(max_length=200, blank=True, default='')
    upload_date = models.DateTimeField(auto_now=True)
    def __str__(self):return str(self.lead_id)
    

class business_identifiers(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    business_name = models.CharField(max_length=500, blank=True,default='')
    business_type = models.CharField(max_length=500, blank=True,default='')
    business_category = models.CharField(max_length=500, blank=True,default='')
    brand_name = models.CharField(max_length=500, blank=True,default='')
    firm_type = models.CharField(max_length=500, blank=True,default='')
    name_for_mou = models.CharField(max_length=500, blank=True,default='')
    designation = models.CharField(max_length=500, blank=True,default='')
    turnover = models.CharField(max_length=500, blank=True,default='')
    monthly_sales = models.CharField(max_length=500, blank=True,default='')
    gst = models.CharField(max_length=500, blank=True,default='')
    def __str__(self): return str(self.lead_id)


class comment(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=500, blank=True, default='') 
    comment_date = models.DateField( auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
    def __str__(self): return str(self.lead_id)


class contact_preference(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    contact_preference = models.CharField(max_length=500, blank=True, default='')
    def __str__(self): return str(self.lead_id)


class followup(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    followup_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
    followup_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    followup_notes = models.TextField(blank=True, default='')
    created_by = models.CharField(max_length=50, blank=True, default='')
    service_category = models.CharField(max_length=50, blank=True, default='')
    def __str__(self): return str(self.lead_id)


class seller_address(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    address_line1 = models.CharField(max_length=50, blank=True, default='')
    address_line2 = models.CharField(max_length=50, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    state = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=50, blank=True, default='')
    pin_code = models.CharField(max_length=50, blank=True, default='')
    def __str__(self): return str(self.lead_id)


class service(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    platform = models.CharField(max_length=50, blank=True, default='')
    service_country = models.CharField(max_length=50, blank=True, default='')
    service_category = models.CharField(max_length=50, blank=True, default='')
    service_name = models.CharField(max_length=50, blank=True, default='')
    team_leader = models.CharField(max_length=50, blank=True, default='')
    team_leader_id = models.CharField(max_length=50, blank=True, default='')
    associate = models.CharField(max_length=50, blank=True, default='')
    associate_id = models.CharField(max_length=50, blank=True, default='')
    lead_status = models.CharField(max_length=50, blank=True, default='')
    lead_status_reason = models.CharField(max_length=50, blank=True, default='')
    fees_slab = models.CharField(max_length=50, blank=True, default='')
    def __str__(self): return str(self.lead_id)


# class source(models.Model):
#     lead_id = models.CharField(max_length=50, null=True)
#     lead_source_channel = models.CharField(max_length=50, null=True)
#     lead_source_poc_name = models.CharField(max_length=50, null=True)
#     lead_source_poc_contact = models.CharField(max_length=50, null=True)
#     def __str__(self):return str(self.lead_id)


# class status(models.Model):
#     lead_id = models.CharField(max_length=50, null=True)
#     lead_status = models.CharField(max_length=50, null=True)
#     lead_status_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
#     def __str__(self):return str(self.lead_id)


class website_store(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    seller_website = models.CharField(max_length=50, blank=True, default='')
    amazon_store_link = models.CharField(max_length=50, blank=True, default='')
    facebook_store_link = models.CharField(max_length=50, blank=True, default='')
    instagram_store_link = models.CharField(max_length=50, blank=True, default='')
    def __str__(self): return str(self.lead_id)