from django.db import models
from account.models import UserAccount, Product
# from dropdown.models import lead_status

# Create your models here.



class Client_turnover(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')
  def __str__(self): return str(self.title)

class Drp_business_type(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')

class Drp_business_category(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')
  def __str__(self): return (self.title)

class Drp_firm_type(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')

# class Turnover_slab(models.Model):
#   title = models.CharField(max_length=100, blank=True, default='')


class Contact_preference(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')

class Followup_history(models.Model):
  followup_date = models.DateTimeField(auto_now=False, auto_now_add=False, default='0001/01/01')
  # followup_time = models.TimeField(auto_now=False, auto_now_add=False)
  followup_notes = models.TextField()
  created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)

class Drp_country(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')
  def __str__(self): return str(self.title)

class Drp_state(models.Model):
  country = models.ForeignKey(Drp_country, on_delete=models.CASCADE, null=True, blank=None)
  title = models.CharField(max_length=100, blank=True, default='')
  def __str__(self): return str(self.title)

class Drp_city(models.Model):
  state = models.ForeignKey(Drp_state, on_delete=models.CASCADE, null=True, blank=None)
  title = models.CharField(max_length=100, blank=True, default='')
  def __str__(self): return str(self.title)

# class Contact_number(models.Model):
#   lead_id = models.ForeignKey("leads.Leads", on_delete=models.CASCADE, null=True, blank=None)
#   contact_number = models.CharField(max_length=100, blank=True, default='')

class Email(models.Model):
  lead_id = models.ForeignKey("leads.Leads", on_delete=models.CASCADE, null=True, blank=None)
  email_id = models.CharField(max_length=100, blank=True, default='')



# Table contact_number_connector {
#   id integer [primary key]
#   leads_id integer
#   emails_id integer
# }


# Table contact_number_type {
#   id integer [primary key]
#   title varchar
# }
  
class Commercials(models.Model):
  # service_id = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)
  price = models.CharField(max_length=100, blank=True, default='')
  commission = models.CharField(max_length=100, blank=True, default='')
  price_for_mou = models.CharField(max_length=100, blank=True, default='')
  def __str__(self): return str(self.price_for_mou)

class Services(models.Model):
  # marketplace = models.ForeignKey("leads.Marketplace", on_delete=models.CASCADE, null=True, blank=True)
  service_name = models.CharField(max_length=100, blank=True, default='')
  commercials = models.ManyToManyField(Commercials)
  def __str__(self): return str(self.service_name)

  
class Marketplace(models.Model):
  marketplace = models.CharField(max_length=100, blank=True, default='')
  service = models.ManyToManyField(Services)
  def __str__(self): return str(self.marketplace)

  






  # create_by = mode




# class Commercials(models.Model):
#   service_id = models.ForeignKey(Service_category, on_delete=models.CASCADE)
#   price = models.IntegerField(max_length=100, blank=True, default='')


# Table email_record_connector {
#   id integer [primary key]
#   lead_id integer
#   email_record_id integer
# }

# Table email_record {
#   id integer [primary key]
#   email varchar
#   date timestamp
# }


# Table email_connector {
#   id integer [primary key]
#   leads_id integer
#   emails_id integer
# }



# Table record_status{
#   id integer [primary key]
#   lead_id integer
#   status varchar
#   status_date varchar
# }
class drp_lead_status(models.Model):
  title = models.CharField(max_length=100, blank=True, default='')

class Status_history(models.Model):
  lead_id = models.ForeignKey("leads.Leads", on_delete=models.CASCADE, null=True, blank=None)
  status = models.ForeignKey(drp_lead_status, on_delete=models.CASCADE)
  status_date = models.DateField(auto_now=False, auto_now_add=False)
  updated_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)




class Leads(models.Model):
    lead_id = models.CharField(max_length=100, blank=True, default='')
    associate = models.ForeignKey(UserAccount , on_delete=models.CASCADE, null=True, blank=True)
    # service_country = models.CharField(max_length=100, blank=True, default='') 
    marketplace = models.CharField(max_length=100, blank=True, default='') 
    request_id = models.CharField(max_length=100, blank=True, default='') 
    provider_id = models.CharField(max_length=100, blank=True, default='') 
    service_requester_type = models.CharField(max_length=100, blank=True, default='') 
    client_name = models.CharField(max_length=100, blank=True, default='') 
    requester_id = models.CharField(max_length=100, blank=True, default='') 
    contact_number = models.CharField(max_length=100, blank=True, default='') 
    alternate_contact_number = models.CharField(max_length=100, blank=True, default='')
    email_id = models.EmailField(max_length=254, blank=True, default='')
    alternate_email_id = models.EmailField(max_length=254, blank=True, default='')
    created_date = models.CharField(max_length=100, blank=True, default='') 
    service_category = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)
    # service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)
    commercials = models.ForeignKey(Commercials, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(drp_lead_status, on_delete=models.CASCADE, null=True, blank=True)

    requester_location = models.CharField(max_length=100, blank=True, default='') 
    requester_sell_in_country = models.CharField(max_length=100, blank=True, default='') 
    current_status = models.CharField(max_length=100, blank=True, default='') 
    client_turnover = models.ForeignKey(Client_turnover, on_delete=models.CASCADE, null=True, blank=True)
    hot_lead = models.BooleanField(default=False)
    business_name = models.CharField(max_length=100, blank=True, default='') 
    business_type = models.ForeignKey(Drp_business_type, on_delete=models.CASCADE, null=True, blank=True) 
    business_category = models.ForeignKey(Drp_business_category, on_delete=models.CASCADE, null=True, blank=True) 
    brand_name = models.CharField(max_length=100, blank=True, default='') 
    firm_type = models.ForeignKey(Drp_firm_type, on_delete=models.CASCADE, null=True, blank=True) 
    name_for_mou = models.CharField(max_length=100, blank=True, default='') 
    designation_in_company = models.CharField(max_length=100, blank=True, default='') 
    # turnover = models.ForeignKey(Turnover_slab, on_delete=models.CASCADE, null=True, blank=True) 
    # monthly_sales = models.CharField(max_length=100, blank=True, default='') 
    gst = models.CharField(max_length=100, blank=True, default='') 
    # remark = models.ForeignKey(Remark_history, on_delete=models.CASCADE, null=True, blank=True)
    contact_preferences = models.ForeignKey(Contact_preference, on_delete=models.CASCADE, null=True, blank=True)
    followup = models.ForeignKey(Followup_history, on_delete=models.CASCADE, null=True, blank=True)
    address_line1 = models.CharField(max_length=100, blank=True, default='') 
    address_line2 = models.CharField(max_length=100, blank=True, default='') 
    country = models.ForeignKey(Drp_country, on_delete=models.CASCADE, null=True, blank=True) 
    state = models.ForeignKey(Drp_state, on_delete=models.CASCADE, null=True, blank=True) 
    city = models.ForeignKey(Drp_city, on_delete=models.CASCADE, null=True, blank=True) 
    pin_code = models.CharField(max_length=100, blank=True, default='') 
    email_record = models.CharField(max_length=100, blank=True, default='')
    # deadline = models.CharField(max_length=100, blank=True, default='')
    seller_website = models.CharField(max_length=100, blank=True, default='') 
    amazon_store_link = models.CharField(max_length=100, blank=True, default='') 
    facebook_store_link = models.CharField(max_length=100, blank=True, default='') 
    instagram_store_link = models.CharField(max_length=100, blank=True, default='')
    upload_date = models.DateTimeField(auto_now_add=True, null=True)
    visibility = models.BooleanField(default=True)

    def __str__(self):return str(self.lead_id)


class Turn_Arround_Time(models.Model):
  duration_in_hrs = models.IntegerField()
  def __str__(self): return str(self.duration_in_hrs)



# class contact_numbers(models.Model):
#   lead_id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True, blank=None)
#   contact_number = models.CharField(max_length=100, blank=True, default='')
#   contact_number_type = models.CharField(max_length=100, blank=True, default='')
    
class Remark_history(models.Model):
  remark = models.CharField(max_length=100, blank=True, default='')
  lead_id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True, blank=True)
  # remark_date = models.DateField(auto_now=False, auto_now_add=False)



# class email_ids(models.Model):
#   lead_id =  models.ForeignKey(Leads, on_delete=models.CASCADE, null=True, blank=None)
#   email_id = models.CharField(max_length=100, blank=True, default='')



# class Service_category(models.Model):
#   lead_id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True, blank=True)
#   service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)
#   pricing = models.ForeignKey(Commercials, on_delete=models.CASCADE, null=True, blank=True)
#   followup = models.ForeignKey(Followup_history, on_delete=models.CASCADE, null=True, blank=True)
#   status = models.ForeignKey(drp_lead_status, on_delete=models.CASCADE, null=True, blank=True)



class Email_history(models.Model):
  lead_id = models.ForeignKey(Leads, on_delete=models.CASCADE, null=True, blank=None)
  email = models.TextField()
  date = models.DateField(auto_now=False, auto_now_add=False)
  sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)










# class all_identifiers(models.Model):
#     lead_id = models.CharField(max_length=100, blank=True, default='')
#     service_country = models.CharField(max_length=100, blank=True, default='')
#     marketplace = models.CharField(max_length=100, blank=True, default='')
#     request_id = models.CharField(max_length=150, blank=True, default='')
#     provider_id = models.CharField(max_length=150, blank=True, default='')
#     service_requester_type = models.CharField(max_length=200, blank=True, default='')
#     requester_name = models.CharField(max_length=100, blank=True, default='')
#     requester_id = models.CharField(max_length=150, blank=True, default='')
#     phone_number = models.CharField(max_length=50, blank=True, default='')
#     email_id = models.CharField(max_length=100, blank=True, default='')
#     city = models.CharField(max_length=100, blank=True, default='')
#     created_date = models.CharField(max_length=200, blank=True, default='')
#     service_category = models.CharField(max_length=200, blank=True, default='')
#     requester_location = models.CharField(max_length=200, blank=True, default='')
#     requester_sell_in_country = models.CharField(max_length=200, blank=True, default='')
#     current_status = models.CharField(max_length=200, blank=True, default='')
#     change_status_to = models.CharField(max_length=200, blank=True, default='')
#     shipment_id = models.CharField(max_length=200, blank=True, default='')
#     fulfillment_center = models.CharField(max_length=200, blank=True, default='')
#     delivery_date = models.CharField(max_length=200, blank=True, default='')
#     total_weight = models.CharField(max_length=200, blank=True, default='')
#     shipment_tracking_id_awb = models.CharField(max_length=200, blank=True, default='')
#     pickup_pincode = models.CharField(max_length=200, blank=True, default='')
#     followup_date = models.CharField(max_length=200, blank=True, default='')
#     pitch_in_progress_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
#     not_interested_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
#     not_reachable_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
#     cancelled_request_status_reason_code = models.CharField(max_length=200, blank=True, default='')
#     sales_manager = models.CharField(max_length=200, blank=True, default='')
#     comments = models.CharField(max_length=200, blank=True, default='')
#     amazon_comments = models.CharField(max_length=200, blank=True, default='')
#     note_from_requester = models.TextField(blank=True, default='')
#     account_manager = models.CharField(max_length=200, blank=True, default='')
#     start_date_pickup_date = models.CharField(max_length=200, blank=True, default='')
#     end_date = models.CharField(max_length=200, blank=True, default='')
#     type_of_service_offered = models.CharField(max_length=200, blank=True, default='')
#     mode_of_training = models.CharField(max_length=200, blank=True, default='')
#     number_of_products_model_shoot = models.CharField(max_length=200, blank=True, default='')
#     number_of_products_table_top = models.CharField(max_length=200, blank=True, default='')
#     number_of_products_editing = models.CharField(max_length=200, blank=True, default='')
#     number_of_products_cataloging_ebc_compliance = models.CharField(max_length=200, blank=True, default='')
#     date_of_filing_poa = models.CharField(max_length=200, blank=True, default='')
#     test_result = models.CharField(max_length=200, blank=True, default='')
#     trademark_type = models.CharField(max_length=200, blank=True, default='')
#     trademark_serial_number = models.CharField(max_length=200, blank=True, default='')
#     trademark_pto = models.CharField(max_length=200, blank=True, default='')
#     actual_date_of_reaching_destination_port = models.CharField(max_length=200, blank=True, default='')
#     date_of_shipping_out_of_origin_port = models.CharField(max_length=200, blank=True, default='')
#     container_number = models.CharField(max_length=200, blank=True, default='')
#     order_date = models.CharField(max_length=200, blank=True, default='')
#     estimated_dispatch_date_sample = models.CharField(max_length=200, blank=True, default='')
#     assured_delivery_date = models.CharField(max_length=200, blank=True, default='')
#     production_start_date = models.CharField(max_length=200, blank=True, default='')
#     dispatch_date = models.CharField(max_length=200, blank=True, default='')
#     interest_rate = models.CharField(max_length=200, blank=True, default='')
#     loan_amount = models.CharField(max_length=200, blank=True, default='')
#     loan_tenure_in_months = models.CharField(max_length=200, blank=True, default='')
#     processing_fee = models.CharField(max_length=200, blank=True, default='')
#     pre_closure_charges = models.CharField(max_length=200, blank=True, default='')
#     upload_date = models.DateTimeField(auto_now=True)
#     visibility = models.BooleanField(default=True)
#     def __str__(self):return str(self.lead_id)
    

# class business_identifiers(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     business_name = models.CharField(max_length=500, blank=True,default='')
#     business_type = models.CharField(max_length=500, blank=True,default='')
#     business_category = models.CharField(max_length=500, blank=True,default='')
#     brand_name = models.CharField(max_length=500, blank=True,default='')
#     firm_type = models.CharField(max_length=500, blank=True,default='')
#     name_for_mou = models.CharField(max_length=500, blank=True,default='')
#     designation_in_company= models.CharField(max_length=500, blank=True,default='')
#     turnover = models.CharField(max_length=500, blank=True,default='')
#     monthly_sales = models.CharField(max_length=500, blank=True,default='')
#     gst = models.CharField(max_length=500, blank=True,default='')
#     def __str__(self): return str(self.lead_id)


# class comment(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=500, blank=True, default='') 
#     comment_date = models.DateField( auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
#     def __str__(self): return str(self.lead_id)


# class contact_preference(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     contact_preferences = models.CharField(max_length=500, blank=True, default='')
    
#     # class Meta:
#     #     db_table = "contac_preference"
    
#     def __str__(self): return str(self.lead_id)



# class followup(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     followup_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
#     followup_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
#     followup_notes = models.TextField(blank=True, default='')
#     created_by = models.CharField(max_length=50, blank=True, default='')
#     service = models.CharField(max_length=50, blank=True, default='')
#     def __str__(self): return str(self.lead_id)


# class seller_address(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     address_line1 = models.CharField(max_length=50, blank=True, default='')
#     address_line2 = models.CharField(max_length=50, blank=True, default='')
#     country = models.CharField(max_length=50, blank=True, default='')
#     state = models.CharField(max_length=50, blank=True, default='')
#     city = models.CharField(max_length=50, blank=True, default='')
#     pin_code = models.CharField(max_length=50, blank=True, default='')
#     def __str__(self): return str(self.lead_id)


# class service(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     platform = models.CharField(max_length=50, blank=True, default='')
#     service_country = models.CharField(max_length=50, blank=True, default='')
#     service_category = models.CharField(max_length=50, blank=True, default='')
#     marketplace = models.CharField(max_length=50, blank=True, default='')
#     team_leader = models.CharField(max_length=50, blank=True, default='')
#     team_leader_id = models.CharField(max_length=50, blank=True, default='')
#     associate = models.CharField(max_length=50, blank=True, default='')
#     associate_id = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)
#     lead_status = models.ForeignKey(lead_status , default=8, on_delete=models.CASCADE)
#     lead_status_reason = models.CharField(max_length=50, blank=True, default='')
#     fees_slab = models.CharField(max_length=50, blank=True, default='')
#     def __str__(self): return str(self.lead_id)


# # class source(models.Model):
# #     lead_id = models.CharField(max_length=50, null=True)
# #     lead_source_channel = models.CharField(max_length=50, null=True)
# #     lead_source_poc_name = models.CharField(max_length=50, null=True)
# #     lead_source_poc_contact = models.CharField(max_length=50, null=True)
# #     def __str__(self):return str(self.lead_id)


# # class status(models.Model):
# #     lead_id = models.CharField(max_length=50, null=True)
# #     lead_status = models.CharField(max_length=50, null=True)
# #     lead_status_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
# #     def __str__(self):return str(self.lead_id)


# class website_store(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     seller_website = models.CharField(max_length=50, blank=True, default='')
#     amazon_store_link = models.CharField(max_length=50, blank=True, default='')
#     facebook_store_link = models.CharField(max_length=50, blank=True, default='')
#     instagram_store_link = models.CharField(max_length=50, blank=True, default='')
#     def __str__(self): return str(self.lead_id)