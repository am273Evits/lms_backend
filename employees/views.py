from django.shortcuts import render
from django.apps import apps
from django.db.models import fields
from rest_framework.generics import GenericAPIView, CreateAPIView
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

        associates = getAssociate(user.employee_id)
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
    

# class officialDetailsSubmit(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = employee_officialSerializer
#     def put(self, request, format=None, *args, **kwargs):
#         # print('wrking here')
#         user_role = getUserRole(request.user.id)

#         res = Response()
#         if user_role == 'admin' or 'lead_manager':
#             try:
#                 data = request.data
#                 # print(data)

#                 if not data.get('employee_id'):
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'employee_id field is required',
#                         'data': []
#                     }
#                     return res
#                 if not data.get('department'):
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'department field is required',
#                         'data': []
#                     }
#                     return res
#                 if not data.get('designation'):
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'designation field is required',
#                         'data': []
#                     }
#                     return res
#                 if not data.get('product'):
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'product field is required',
#                         'data': []
#                     }
#                     return res
#                 if not data.get('team_leader'):
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'team_leader field is required',
#                         'data' : []
#                     }
#                     return res
#                 if not data.get('user_role'):
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'team_leader field is required',
#                         'data' : []
#                     }
#                     return res
                
#                 UA_data = UserAccount.objects.filter(employee_id = data.get('employee_id')).first()
#                 UA_data_ID = UA_data.id
#                 print(UA_data)
                
#                 data['emp'] = UA_data_ID
#                 del data['employee_id']
#                 print('data', data)


#                 serializer = employee_officialSerializer(UA_data, data=data, partial=True)
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         "message": 'data saved',
#                         'data': serializer.data,
#                         'status': status.HTTP_200_OK
#                     }
#                     print('working tillhere')




                # AI_data = employee_official.objects.filter(lead_id_emp = lead_id).first()
                # data['lead_id'] = int(AI_data.id)

                # S_data = emp.objects.filter(lead_id__lead_id = lead_id)
                # for d in S_data:
                #     if d.service_category == data.get('service_category'):
                #         res.status_code = status.HTTP_208_ALREADY_REPORTED
                #         res.data = {
                #             'status': status.HTTP_208_ALREADY_REPORTED,
                #             'message': 'service category already registered for this lead_id',
                #             'data':[]
                #         }
                #         return res
                # print(S_data[0].service_category)
                

                # lead_id = getLeadId()
                # data = request.data
                # data['lead_id'] = lead_id
                # serializer = serviceFieldSubSerializer(data=data)
                # if serializer.is_valid(raise_exception=True):
                #     if serializer.save():
                #         res.status_code = status.HTTP_200_OK
                #         res.data = {
                #             'status': status.HTTP_200_OK,
                #             'message': 'new lead created',
                #             'data': []
                #         }
                #         return res
        #         else: 
        #                 res.status_code = status.HTTP_200_OK
        #                 res.data = {
        #                     'status': status.HTTP_200_OK,
        #                     'message': 'request failed',
        #                     'data': serializer.errors
        #                 }
        #                 return res

        #     except ValueError as e:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data = {
        #             'status': status.HTTP_400_BAD_REQUEST,
        #             "message": str(e),
        #             'data': []
        #             }

        # # else :
        # #     res.status_code = status.HTTP_400_BAD_REQUEST
        # #     res.data = {
        # #         'status': status.HTTP_400_BAD_REQUEST,
        # #         'message': 'you are not authorized for this action',
        # #         'data': []
        # #     }

        # return res

    


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