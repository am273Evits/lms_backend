from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([lead_delete_approval, lead_status_record])
