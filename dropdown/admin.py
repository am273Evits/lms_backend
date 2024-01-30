from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register([business_type, firm_type, decision, dropdown_fields, user_links, not_interested_reason, unresponsive_reason, service_category, service_country, user_role_list, gender, lead_status, list_business_leads, ev_commercials, prop_dir_designation, business_category_list, country_state_city, sup_designations, ev_department, ev_designation, list_employee])