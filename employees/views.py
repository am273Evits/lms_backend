from django.shortcuts import render
from django.apps import apps
from django.db.models import fields
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from employees.models import *
from dropdown.models import *
# from business_leads.models import *

from account.views import getLeadId, getProduct, getUserRole, getTeamLeader, getClientId, get_tokens_for_user , getAssociates as getAssociate, getModelFields
# from lms.models import employee_basic, employee_official

# Create your views here.

class getAssociates(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = getAssociatesSerializers
    def get(self, request, format=None, *args, **kwargs):
        user = request.user

        # employee_id = user.employee_id
        associates = getAssociate(user.employee_id)
        # print('associates', associates)
        serializer = getAssociatesSerializers(data=associates, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': {"user details": serializer.data}
                }
        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }
        return res
    


# class getTableFields(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = getTableFieldsSerializer
#     def get(self, request, table, format=None, *args, **kwargs):

#         model = apps.get_model('business_leads', table)
#         model_fields = getModelFields(model)
#         serializer = getTableFieldsSerializer(data=model_fields, many=True)
#         res = Response()
#         if serializer.is_valid(raise_exception=True):
#             res.status_code = status.HTTP_200_OK
#             res.data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'request failed',
#                 "data": model_fields
#             }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'request failed',
#                 "data": []
#             }
#         return res
    


# class createAssociateBasic(GenericAPIView):
#     serializer_class = employee_basicSerializer
#     def post(self, request, format=None, *args, **kwargs):
#         serializer = employee_basicSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             data = serializer.data
#             print('data', data)

#             data = employee_basic.objects.create(**serializer.data)
            
#             return Response({'message': 'register'})
#             pass



# class createAssociateOfficial(GenericAPIView):
#     serializer_class = employee_officialSerializer
#     def post(self, request, format=None, *args, **kwargs):
#         pass