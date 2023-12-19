from django.db import models
from business_leads.models import all_identifiers

# Create your models here.

class lead_delete_approval(models.Model):
    lead_id = models.ForeignKey(all_identifiers, on_delete=models.DO_NOTHING)
    approval = models.BooleanField(default=False)
