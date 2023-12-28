from django.db import models
# Create your models here.



#xsup

# class banking_account_type(models.Model):
#     title = models.CharField(max_length=200, blank=True, default='')

class business_type(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    def __str__ (self): return self.title

class firm_type(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    def __str__ (self): return self.title

# class prop_dir(models.Model): 
#     title = models.CharField(max_length=200, blank=True, default='')

class prop_dir_designation(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    def __str__ (self): return self.title

# class cities(models.Model):
#     city = models.CharField(max_length=300, blank=True, default='')
#     state = models.CharField(max_length=300, blank=True, default='')
#     coutry = models.CharField(max_length=300, blank=True, default='')

class decision(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    def __str__ (self): return self.title



# class ev_departments(models.Model):
#     title = models.CharField(max_length=200, blank=True, default='')
#     sub_department = models.CharField(max_length=200, blank=True, default='')
#     created_by = models.CharField(max_length=500, blank=True, default='')


class ev_department(models.Model):
    title = models.CharField(max_length=50, blank=True, default='')
    def __str__ (self): return self.title

class sup_designations(models.Model):
    title = models.CharField(max_length=50, blank=True, default='')
    def __str__ (self): return self.title


class ev_designation(models.Model):
    title  = models.ForeignKey(sup_designations, on_delete=models.CASCADE)
    department  = models.ForeignKey(ev_department, on_delete=models.CASCADE)
    def __str__ (self): return str(self.title)










class dropdown_fields(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    ref_tb = models.CharField(max_length=500, blank=True, default='')
    def __str__(self): return str(self.title)


class country_state_city(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    state = models.CharField(max_length=500, blank=True, default='')
    city = models.CharField(max_length=500, blank=True, default='')
    def __str__(self): return str(self.city)





class contact_preference_list(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    def __str__ (self): return self.title


class business_category_list(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    def __str__ (self): return self.title


    
    # CharField(max_length=500, blank=True, default='')

# class ev_admin(models.Model):
#     title = models.CharField(max_length=200, blank=True, default='')
#     created_by = models.CharField(max_length=500, blank=True, default='')
    





class ev_commercials(models.Model):
    platform = models.CharField(max_length=500, blank=True, default='')
    service_country = models.CharField(max_length=200, blank=True, default='')
    service_category = models.CharField(max_length=500, blank=True, default='')

# class ev_department_designation(models.Model):
#     title = models.CharField(max_length=500, blank=True, default='')
#     designation = models.CharField(max_length=200, blank=True, default='')
#     def __str__ (self): return self.title


# class ev_employee_status(models.Model):
#     title = models.CharField(max_length=500, blank=True, default='')
#     created_by = models.CharField(max_length=500, blank=True, default='')
#     def __str__ (self): return self.title


# class ev_super_admin(models.Model):
#     title = models.CharField(max_length=500, blank=True, default='')
#     created_by = models.CharField(max_length=500, blank=True, default='')


# class ev_team_leader(models.Model):
#     title = models.CharField(max_length=500, blank=True, default='')
#     marketplace = models.CharField(max_length=500, blank=True, default='')
#     segment = models.CharField(max_length=500, blank=True, default='')
#     created_by = models.CharField(max_length=500, blank=True, default='')

# class ev_team_manager(models.Model):
#     title = models.CharField(max_length=500, blank=True, default='')
#     created_by = models.CharField(max_length=500, blank=True, default='')

class user_links(models.Model):
    title = models.CharField(max_length=500, default='', blank=True)
    link_type = models.CharField(max_length=500, default='', blank=True)
    user_link = models.CharField(max_length=500, default='', blank=True)
    access_department = models.CharField(max_length=500, default='', blank=True)
    table_ref = models.CharField(max_length=500, default='', blank=True)
    link_status = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
# class user_page_link(models.Model):
#     title = models.CharField(max_length=500, default='', blank=True)



class service_category(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.title


class service_country(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.title


class user_role_list(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    designation = models.ForeignKey(ev_designation, on_delete=models.CASCADE)
    department = models.ForeignKey(ev_department, on_delete=models.CASCADE)
    def __str__ (self): return self.title


class gender(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.title


class lead_status(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.title


# class marital_status(models.Model):
#     title = models.CharField(max_length=500, blank=True, default='')

class not_interested_reason(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.title


class unresponsive_reason(models.Model):
    title = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.title


class list_business_leads(models.Model):
    table_name = models.CharField(max_length=500, blank=True, default='')
    table_type = models.CharField(max_length=500, blank=True, default='')
    table_atr = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.table_name

# class list_client(models.Model):
#     table_name = models.CharField(max_length=500, blank=True, default='')
#     table_type = models.CharField(max_length=500, blank=True, default='')
#     table_atr = models.CharField(max_length=500, blank=True, default='')

class list_employee(models.Model):
    table_name = models.CharField(max_length=500, blank=True, default='')
    table_type = models.CharField(max_length=500, blank=True, default='')
    table_atr = models.CharField(max_length=500, blank=True, default='')
    def __str__ (self): return self.table_name



class image_src(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    src = models.TextField(blank=True, default='')
    status = models.BooleanField(default=True)


# class ref_service_country(models.Model):
#     title = models.CharField(max_length=150, blank=True, default='')