from django.contrib import admin
from .models import *
# Register your models here.


class CommercialsAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'price', 'commission', 'price_for_mou')


class LeadsAdmin(admin.ModelAdmin):
    list_display = ('lead_id', 'client_name' )

# admin.site.register(Commercials, CommercialsAdmin)  
admin.site.register(Leads, LeadsAdmin)
admin.site.register([Drp_country,Drp_state ,Drp_city, Marketplace, Client_turnover, Turn_Arround_Time])
