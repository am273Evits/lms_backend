from django.shortcuts import render
from django.apps import apps
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from .serializers import *

from account.views import getLeadId, getProduct, getUserRole, getTeamLeader, getClientId, get_tokens_for_user , getAssociates as getAssociate, getModelFields


# Create your views here.

class dropdownOption(GenericAPIView):
    serializer_class = dropdownOptionSerializers
    permissions_classes = [IsAuthenticated]
    def get(self, request, table, format=None, *args, **kwargs):

        model = apps.get_model('dropdown', table)
        data = list(model.objects.values_list('title', flat=True).order_by('title'))
        
        serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                "message": 'successful',
                "data": serializer.data
                }
        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                "message": 'request failed',
                "data": []
                }
        return res
    


class dropdownAjaxOption(GenericAPIView):
    serializer_class = dropdownOptionSerializers
    permissions_classes = [IsAuthenticated]
    def get(self, request, table ,format=None, *args, **kwargs):

        model = apps.get_model('dropdown', table)
        if table == 'country_state_city':
            data = list(model.objects.values_list('country', flat=True).distinct().order_by('country'))
            if data:
                serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
                res = Response()
                if serializer.is_valid(raise_exception=True):
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        "message": 'successful',
                        "data": serializer.data
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        "message": 'request failed',
                        "data": []
                        }
                return res
    


class dropdownAjaxD1Option(GenericAPIView):
    serializer_class = dropdownOptionSerializers
    permissions_classes = [IsAuthenticated]
    def get(self, request, table, country ,format=None, *args, **kwargs):

        model = apps.get_model('dropdown', table)
        if table == 'country_state_city':
            data = list(model.objects.filter(country = country).values_list('state', flat=True).distinct().order_by('state'))
            if data:
                serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
                res = Response()
                if serializer.is_valid(raise_exception=True):
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        "message": 'successful',
                        "data": serializer.data
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        "message": 'request failed',
                        "data": []
                        }
                return res
            


class dropdownAjaxD2Option(GenericAPIView):
    serializer_class = dropdownOptionSerializers
    permissions_classes = [IsAuthenticated]
    def get(self, request, table, country, state ,format=None, *args, **kwargs):

        model = apps.get_model('dropdown', table)
        if table == 'country_state_city':
            data = list(model.objects.filter(country = country, state = state).values_list('city', flat=True).distinct().order_by('city'))
            if data:
                serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
                res = Response()
                if serializer.is_valid(raise_exception=True):
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        "message": 'successful',
                        "data": serializer.data
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        "message": 'request failed',
                        "data": []
                        }
                return res