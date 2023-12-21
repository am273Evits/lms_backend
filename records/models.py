from django.db import models
from business_leads.models import all_identifiers
from dropdown.models import lead_status

# Create your models here.

class lead_delete_approval(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
    approval = models.BooleanField(default=False)


class lead_status_record(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.CASCADE)
    status = models.ForeignKey(lead_status, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True)