from django.contrib import admin
from.models import *
# Register your models here.


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'employee_id', 'name')
admin.site.register(UserAccount, UserAccountAdmin)

# class DesignationAdmin(admin.ModelAdmin):
#     list_display = ('designation', 'department')
# admin.site.register(Designation, DesignationAdmin)

class Drp_ProductAdmin(admin.ModelAdmin):
    list_display = ('department','designation', 'product')
admin.site.register(Drp_Product, Drp_ProductAdmin)  



admin.site.register([Department, Designation, Product, Employee_status])