# from django.db import models

# # Create your models here.


# class ev_branch_location(models.Model):
#     title = models.CharField(max_length=500, null=True)
#     location = models.CharField(max_length=200, null=True)
#     def __str__ (self): return self.title


# class ev_products(models.Model):
#     title = models.CharField(max_length=500, null=True)
#     department = models.CharField(max_length=200, null=True)
#     def __str__ (self): return self.title


# class ev_services(models.Model):
#     service_id = models.CharField(max_length=300, blank=True, default='')
#     country = models.CharField(max_length=300, blank=True, default='')
#     marketplace = models.CharField(max_length=300, blank=True, default='')
#     services = models.CharField(max_length=300, blank=True, default='')
#     price_for_mou = models.CharField(max_length=300, blank=True, default='')
#     static_service_fees = models.CharField(max_length=300, blank=True, default='')
#     commission_fees = models.BooleanField(default=False)
#     commission_service_fees = models.CharField(max_length=300, blank=True, default='')
#     service_currency = models.CharField(max_length=300, blank=True, default='')
#     visibility = models.BooleanField(default=True)
#     def __str__ (self): return self.price_for_mou
#     # def __str__ (self): return self.country


# class ev_bank_details(models.Model):
#     account_name = models.CharField(max_length=200, null=True)
#     bank_name = models.CharField(max_length=500, null=True)
#     account_number = models.CharField(max_length=200, null=True)
#     ifsc = models.CharField(max_length=500, null=True)
#     def __str__ (self): return self.account_name


# class email_ask_for_details(models.Model):
#     service = models.CharField(max_length=200, null=True)
#     email = models.TextField(null=True)
#     def __str__ (self): return self.service


# class email_service_proposal(models.Model):
#     country = models.CharField(max_length=200, null=True)
#     marketplace = models.CharField(max_length=500, null=True)
#     service = models.CharField(max_length=200, null=True)
#     proposal_email = models.TextField(null=True)
#     def __str__ (self): return self.service

