# from django.db import models
# from business_leads.models import all_identifiers
# from dropdown.models import lead_status
# from account.models import UserAccount
# from evitamin.models import ev_services

# # Create your models here.

# class lead_delete_approval(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     approval = models.BooleanField(default=False)


# class lead_status_record(models.Model):
#     lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
#     status = models.ForeignKey(lead_status, on_delete=models.CASCADE)
#     updated_date = models.DateTimeField(auto_now=True)


# class user_delete_approval(models.Model):
#     employee_id = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     approval = models.BooleanField(default=False)


# class service_delete_approval(models.Model):
#     service_id = models.ForeignKey(ev_services, on_delete=models.CASCADE)
#     approval = models.BooleanField(default=False)