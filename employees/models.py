from django.db import models
from account.models import * 

# Create your models here.

# class employee_basic(models.Model):
    # employee_id = models.CharField(max_length=300, blank=True, default='')
    # employee_status = models.CharField(max_length=300, blank=True, default='')
    # # first_name = models.CharField(max_length=300, blank=True, default='')
    # name = models.CharField(max_length=300, blank=True, default='')
    # gender = models.CharField(max_length=300, blank=True, default='')
    # date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
    # blood_group = models.CharField(max_length=300, blank=True, default='')
    # age = models.CharField(max_length=300, blank=True, default='')
    # disability = models.CharField(max_length=300, blank=True, default='')
    # email_id = models.CharField(max_length=300, blank=True, default='')
    # marital_status = models.CharField(max_length=300, blank=True, default='')
    # mobile_number = models.CharField(max_length=300, blank=True, default='')
    # alternate_mobile_number = models.CharField(max_length=300, blank=True, default='')
    # nationality = models.CharField(max_length=300, blank=True, default='')
    # emergency_contact_number = models.CharField(max_length=300, blank=True, default='')
    # religion = models.CharField(max_length=300, blank=True, default='')

    # def __str__(self):
    #     return self.employee_id
    
    
class employee_official(models.Model):
    # employee_id = models.CharField(max_length=500, default='', blank=True)
    emp = models.ForeignKey(UserAccount,on_delete=models.DO_NOTHING)
    department = models.CharField(max_length=500, default='', blank=True)
    designation = models.CharField(max_length=500, default='', blank=True)
    product = models.CharField(max_length=500, default='', blank=True)
    team_leader = models.CharField(max_length=500, default='', blank=True)
    team_manager = models.CharField(max_length=500, default='', blank=True)
    admin = models.CharField(max_length=500, default='', blank=True)
    super_admin = models.CharField(max_length=500, default='', blank=True)
    user_role = models.CharField(max_length=500, default='', blank=True)
    branch = models.CharField(max_length=500, default='', blank=True)
    office_location = models.CharField(max_length=500, default='', blank=True)
    email_id_official = models.CharField(max_length=500, default='', blank=True)
    tool_login_id = models.CharField(max_length=500, default='', blank=True)
    evitamin_portal_login_id = models.CharField(max_length=500, default='', blank=True)
    joining_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    signed_bond = models.CharField(max_length=500, default='', blank=True)
    work_from_home = models.CharField(max_length=500, default='', blank=True)
    employee_status = models.CharField(max_length=500, default='', blank=True)

    def __str__ (self):
        return str(self.emp)