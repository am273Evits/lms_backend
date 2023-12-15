from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([all_identifiers,business_identifiers, contact_preference ,comment, followup, seller_address, service, website_store])
