from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import *
# Create your views here.


class deleteLeadApprovalWrite(CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, lead_id, format=None, *args, **kwargs):
        pass

