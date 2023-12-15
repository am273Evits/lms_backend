from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([ev_branch_location, ev_products, ev_services, ev_bank_details, email_ask_for_details, email_service_proposal])
