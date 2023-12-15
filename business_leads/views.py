from django.shortcuts import render
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from django.apps import apps
from django.core.mail import send_mail

import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .serializers import *

import random

import math

from business_leads.models import all_identifiers as all_identifiers, business_identifiers as business_identifiers, comment as comment, contact_preference as contact_preference, followup as followup, seller_address as seller_address, service as service, website_store as website_store

# from evitamin.models import email_ask_for_details, email_service_proposal

from account.models import *
from employees.models import *
from evitamin.models import *

# from lms_backend.models import File

from account.views import getLeadId, getProduct, getUserRole, getTeamLeader, getClientId, get_tokens_for_user, getModelFields
# Create your views here.





class uploadBusLdAmzSPNC(GenericAPIView):
    serializer_class = uploadFileSerializer
    permission_classes = [IsAuthenticated]
    # @api_view(['POST'])
    def post(self, request, format=None, *args, **kwargs):
        if request.method == 'POST':
            file = request.FILES['fileinp']
            obj = File.objects.create(file = file)
            df = pd.read_csv(obj.file, delimiter=',',   header=0)
            head_row = df.columns.values
            h_row = [f.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('__', '_').replace('__', '_').lower() for f in head_row]
            db_head_row_all_rw = all_identifiers._meta.get_fields()
            db_head_row_all = [field.name for field in db_head_row_all_rw]
            db_head_row_all_type = [field.get_internal_type() for field in db_head_row_all_rw]
            db_head_row_serv_rw = service._meta.get_fields()
            db_head_row_serv = [field.name for field in db_head_row_serv_rw]
            list_of_csv = [list(row) for row in df.values]

            ref_id = ''

            for ls in list_of_csv:
                dt = {}
                lead_id = getLeadId()
                all_identifiers_instance = all_identifiers()
                for i in range (len(db_head_row_all)):
                    if not (db_head_row_all[i] == 'id' or db_head_row_all[i] == 'lead_id') and db_head_row_all[i] in h_row:
                            ind = h_row.index(db_head_row_all[i])
                            dt[db_head_row_all[i]] = ls[ind] if db_head_row_all[i] != 'service_category' else ls[ind].lower()
                dt['lead_id'] = str(lead_id)
                for field_name, value in dt.items():
                    setattr(all_identifiers_instance, field_name, value)
                all_identifiers_instance.save()

                ref_id = all_identifiers.objects.filter(lead_id = lead_id).values('id').first()
                ref_id = ref_id['id']
                print(ref_id)

                service_instance = service()
                dt = {}
                for i in range (len(db_head_row_serv)):
                    if not (db_head_row_serv[i] == 'id' or db_head_row_serv[i] == 'lead_id') and db_head_row_serv[i] in h_row:
                        ind = h_row.index(db_head_row_serv[i])
                        dt[db_head_row_serv[i]] = ls[ind].lower().strip()
                dt['lead_id'] = all_identifiers_instance
                for field_name, value in dt.items():
                    setattr(service_instance, field_name, value)
                service_instance.save()

                
                all_instances = [business_identifiers(), comment(), contact_preference(), followup(), seller_address(), website_store()]
                dl = []
                for i in range(len(all_instances)):
                    dl.append({"lead_id": all_identifiers_instance})
                for model_instace, data in zip(all_instances, dl):
                    for field_name, value in data.items():
                        setattr(model_instace, field_name, value)
                    model_instace.save()
            res =  Response()
            res.status_code = status.HTTP_201_CREATED
            # res['Access-Control-Allow-Origin'] = '*'
            # res['Access-Control-Allow-Credentials'] = True
            # res['Allow_'] = status.HTTP_201_CREATED
            res.data = {"status": status.HTTP_201_CREATED,"message": 'all records saved successfully', "data": []}
            return res
        else:
            res = Response()
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                "status" : status.HTTP_400_BAD_REQUEST,
                "message": "unsuccessful",
                "data": []
            }
        
        return res



class viewAllLeads(GenericAPIView):
    serializer_class = lead_managerBlSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, page, format=None, *args, **kwargs):
        user = request.user
        user_role = getUserRole(user.id)
        limit = 10
        offset = int((page - 1) * limit)
        data = []
        pagecount = []
        res =  Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'unauthorized access', 
                'data': [],
            }
        )

        with connection.cursor() as cursor:
            if user_role == 'lead_manager':

                cursor.execute(f"SELECT a.lead_id, a.requester_name, b.service_category, b.lead_status, a.upload_date FROM business_leads_all_identifiers as a JOIN business_leads_service as b WHERE a.lead_id = b.lead_id ORDER BY b.lead_id LIMIT {offset}, {limit}")

                column = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    data.append(dict(zip(column, row)))

                cursor.execute(f"select count(lead_id) from business_leads_all_identifiers")
                for row in cursor.fetchall():
                    pagecount = math.ceil(row[0]/limit)

                serializer = lead_managerBlSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                
                res.status_code = status.HTTP_200_OK
                res.data = {
                    "status": status.HTTP_200_OK,
                    "message": 'successful',
                    "data": {'data': serializer.data, 'pagecount': pagecount}
                    }

            elif user_role == 'bd_tl':
                product = getProduct(user.id)

                cursor.execute(f"SELECT b.lead_id, b.service_category, b.associate, b.lead_status, a.requester_name, a.phone_number, a.email_id  FROM business_leads_all_identifiers as a JOIN business_leads_service as b WHERE a.lead_id = b.lead_id AND b.service_category = '{product}' ORDER BY b.lead_id LIMIT {offset}, {limit}")

                column = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    data.append(dict(zip(column, row)))

                cursor.execute(f"select count(lead_id) from business_leads_all_identifiers where service_category = '{product}'")
                for row in cursor.fetchall():
                    pagecount = math.ceil(row[0]/limit)

                serializer = BusinessDevelopmentLeadSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)

                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': status.HTTP_200_OK,
                    'message': 'successful',
                    'data': {'data': serializer.data, 'pagecount': pagecount}
                    }
                # print({'data': serializer.data, 'pagecount': pagecount})

            return res
        
    




# #Team Leader
# class apiLeadTlView(GenericAPIView):
#     serializer_class = BusinessDevelopmentLeadSerializer
#     def get(self, request, page, format=None, *args, **kwargs):
#         user = cookieAuth(request)
#         employee_id = user['user'].employee_id
#         product = getProduct(employee_id)

#         limit = 10
#         offset = int((page - 1) * limit)

#         data = []
#         pagecount = []
#         with connection.cursor() as cursor:
#             cursor.execute(f"SELECT b.lead_id, b.service_category, b.associate, b.lead_status, a.requester_name, a.phone_number, a.email_id  FROM business_leads_all_identifiers as a JOIN business_leads_service as b WHERE a.lead_id = b.lead_id AND b.service_category = '{product}' ORDER BY b.lead_id LIMIT {offset}, {limit}")

#             column = [col[0] for col in cursor.description]
#             for row in cursor.fetchall():
#                 data.append(dict(zip(column, row)))

#             cursor.execute(f"select count(lead_id) from business_leads_all_identifiers where service_category = '{product}'")
#             for row in cursor.fetchall():
#                 pagecount = math.ceil(row[0]/limit)

#             serializer = BusinessDevelopmentLeadSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)

#             res = Response()
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': data,'pagecount' : pagecount}
            return res
        



class viewLeadsAllIdentifiers(GenericAPIView):
    serializer_class = allIdentifiersSerializer
    permission_classes = [IsAuthenticated]
        # return super().get_serializer_class()

    def get(self, request, table, lead_id, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()

        models = apps.get_model('business_leads', table)
        serializer_class = models

        if table != 'all_identifiers':
            lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
            lead_id = lead_ref.id

        # print(models)
        if user_role == 'lead_manager':
            data = models.objects.filter(lead_id = lead_id).values()
            data = list(data)

            dynamic = dynamic_serializer(models)
            serializer = dynamic(data=data, many=True)
            
            # serializer = allIdentifiersSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': serializer.data
                }
            # return res
        elif user_role == 'bd_tl':
            product = getProduct(request.user.id)
 
            serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
            if serviceData:
                data = models.objects.filter(lead_id = lead_id)
                print(data)
                data = list(data.values())
                serializer = models(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    "status": status.HTTP_200_OK,
                    'message': 'successful',
                    'data': serializer.data
                    }
                # return res
        else:
            res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            res.data = {'error': 'you are not authorized to see this lead'}
        
        return res



        

# class viewLeadsAllIdentifiers(GenericAPIView):
#     serializer_class = allIdentifiersSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, lead_id, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         if user_role == 'lead_manager':
#             data = all_identifiers.objects.filter(lead_id = lead_id).values()
#             # print('data',data)
#             data = list(data)
#             serializer = allIdentifiersSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             # return res
#         elif user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = all_identifiers.objects.filter(lead_id = lead_id)
#                 print(data)
#                 data = list(data.values())
#                 serializer = allIdentifiersSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 # return res
#         else:
#             res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#             res.data = {'error': 'you are not authorized to see this lead'}
        
#         return res


# class viewLeadBusinessIdentifiers(GenericAPIView):
#     serializer_class = businessIdentifiersSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, lead_id, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':

#             data = business_identifiers.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             serializer = businessIdentifiersSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             # print(serializer.data)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = business_identifiers.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = businessIdentifiersSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res


# class viewLeadComment(GenericAPIView):
#     serializer_class=commentSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, lead_id, format=None ,*args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':
#             data = comment.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             # print(data)
#             serializer = commentSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = comment.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = commentSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res


# class viewLeadContactPreference(GenericAPIView):
#     serializer_class=contactPreferenceSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, lead_id, format=None ,*args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':
#             data = contact_preference.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             print('data', data)
#             serializer = contactPreferenceSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = contact_preference.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = contactPreferenceSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res


# class viewLeadFollowup(GenericAPIView):
#     serializer_class=followupSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, lead_id, format=None ,*args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':
#             data = followup.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             serializer = followupSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = followup.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = followupSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res


# class viewLeadSellerAddress(GenericAPIView):
#     serializer_class=sellerAddressSerializer
#     def get(self, request, lead_id, format=None ,*args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':
#             data = seller_address.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             serializer = sellerAddressSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = seller_address.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = sellerAddressSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res


# class viewLeadService(GenericAPIView):
#     serializer_class=serviceSerializer
#     def get(self, request, lead_id, format=None ,*args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':
#             data = service.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             serializer = serviceSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = service.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = serviceSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res


# class viewLeadWebsiteStore(GenericAPIView):
#     serializer_class=websiteStoreSerializer
#     def get(self, request, lead_id, format=None ,*args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()

#         lead_ref = all_identifiers.objects.filter(lead_id = lead_id)[0]
#         lead_ref = lead_ref.id

#         if user_role == 'lead_manager':
#             data = website_store.objects.filter(lead_id = lead_ref).values()
#             data = list(data)
#             serializer = websiteStoreSerializer(data=data, many=True)
#             serializer.is_valid(raise_exception=True)
#             res.status_code = status.HTTP_200_OK
#             res.data = {'data': serializer.data}
#             return res
        
#         if user_role == 'bd_tl':
#             product = getProduct(request.user.id)
#             serviceData = service.objects.filter(lead_id = lead_id, service_category = product)
#             if serviceData:
#                 data = website_store.objects.filter(lead_id = lead_id)
#                 data = list(data.values())
#                 serializer = websiteStoreSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {'data': serializer.data}
#                 return res
#             else:
#                 res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#                 res.data = {'error': 'this lead id not aligned to you'}
#                 return res



class apiFieldEmailProposal(GenericAPIView):
    serializer_class = fieldEmailProposalCountry
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        data = list(ev_services.objects.values('country').distinct())
        serializer = fieldEmailProposalCountry(data=data, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': {'country': serializer.data}
                }
        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }

        return res

class apiFieldEmailProposalCountry(GenericAPIView):
    serializer_class = fieldEmailProposalMarketplace
    permission_classes = [IsAuthenticated]
    def get(self, request, country, format=None, *args, **kwargs):
        data = list(ev_services.objects.filter(country = country).values('marketplace').distinct())
        serializer = fieldEmailProposalMarketplace(data=data, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': {'marketplace': serializer.data}
                }
        else: 
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
                }

        return res

class apiFieldEmailProposalMarkeplace(GenericAPIView):
    serializer_class = fieldEmailProposalService
    permission_classes = [IsAuthenticated]
    def get(self,request, country, marketplace, format=None, *args, **kwargs):
        # user = cookieAuth(request)
        # employee_id = user['user'].employee_id
        product = getProduct(request.user.id)
        dt_list = []
        data = ev_services.objects.filter(country = country, marketplace = marketplace).values('services').distinct()
        for d in data:
            print(d['services'])
            print(product)
            if d['services'] == product:
                dt_list.append(d)

        print(dt_list)
        serializer = fieldEmailProposalService(data=dt_list, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': {'service': serializer.data}
                }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
            }
        return res


class apiFieldEmailProposalService(GenericAPIView):
    serializer_class = fieldEmailProposalSlab
    permission_classes = [IsAuthenticated]
    def get(self, request, country, marketplace, services, format=None, *args, **kwargs):
        data = list(ev_services.objects.filter(country = country, marketplace = marketplace, services = services).values('slab').distinct())
        serializer = fieldEmailProposalSlab(data=data, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data':{'slab': serializer.data}
                }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                'data': []
                }
            
        return res


class apiSubmitEmailProposal(GenericAPIView):
    serializer_class = ev_servicesSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, lead_id, format=None, *args, **kwargs):
        # user = cookieAuth(request)
        # employee_id = user['user'].employee_id
        product = getProduct(request.user.id)
        services_res = ''
        slab_res = ''


        d = request.data
        if d['services'] == product:
            services_res = True
        else:
            raise AuthenticationFailed('service do not exist')

        data = ev_services.objects.filter(country = d['country'], marketplace = d['marketplace'], services = d['services'], slab = d['slab']).exists()

        if data is False:
            country_res = ev_services.objects.filter(country = d['country']).exists()
            marketplace_res = ev_services.objects.filter(marketplace = d['marketplace']).exists()
            services_res = ev_services.objects.filter(services = d['services']).exists()
            slab_res = ev_services.objects.filter(slab = d['slab']).exists()

            if country_res is False:
                raise AuthenticationFailed('country do not exist') 
            if marketplace_res is False:
                raise AuthenticationFailed('marketplace do not exist') 
            if slab_res is False:
                raise AuthenticationFailed('slab do not exist')
            

        message = email_service_proposal.objects.filter(service = d['services']).values('proposal_email').first()
        message = message['proposal_email']

        bank_details = ev_bank_details.objects.all().first()
        account_name = bank_details.account_name
        bank_name = bank_details.bank_name
        account_number = bank_details.account_number
        ifsc = bank_details.ifsc

        message = message.replace('{***account_name***}', account_name)
        message = message.replace('{***bank_name***}', bank_name)
        message = message.replace('{***account_number***}', account_number)
        message = message.replace('{***ifsc_code***}', ifsc)

        message = message.replace('{***service***}', d['services'])
        message = message.replace('{***slab***}', d['slab'])
        message = message.replace('{***sender***}', request.user.name)

        # message = html.escape(message)
        # print(message)

        data_basic = all_identifiers.objects.get(lead_id=lead_id)
        email = data_basic.email_id

        subject = 'service proposal from evitamin'
        # message = '<h1>This email was sent from django</h1>'
        from_email = 'akshatnigamcfl@gmail.com'
        recipient_list = [email]
        text = 'email sent from MyDjango'

        # if send_mail(subject, message, from_email, recipient_list):
        print(recipient_list)

        email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
        email.attach_alternative(message, 'text/html')
        # email.attach_file('files/uploadFile_0dTGU7A.csv', 'text/csv')
        email.send()

        if email:
            status_update = service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = 'proposal email sent')
            print(status_update)
            if status_update:
                res = Response()
                res.status_code = status.HTTP_200_OK
                res.data = {'message': 'email sent' }
                return res
        else:
            raise AuthenticationFailed('email not sent')
        





class getTableFields(GenericAPIView):
    serializer_class = getTableFieldsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, table, format=None, *args, **kwargs):

        model = apps.get_model('business_leads', table)
        model_fields = getModelFields(model)
        serializer = getTableFieldsSerializer(data=model_fields, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                "data": model_fields
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'request failed',
                "data": []
            }
        return res
    


# @api_view(['POST'])
class formsSubmit(GenericAPIView):
    serializer_class = getTableFieldsSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, table, lead_id, format=None, *args, **kwargs):
        main_data = request.data
        OF_data = employee_official.objects.filter(emp = request.user.id).first()
        product = OF_data.product
        user_role = OF_data.user_role

        res = Response()
        # user = cookieAuth(request)

        model = apps.get_model('business_leads', table)
        if model is not None:
            dynamic = dynamic_serializer_submit(model)

            if user_role == 'lead_manager':

                if table == 'followup':
                    main_data['created_by'] = request.user.employee_id

                if table != 'all_identifiers':
                    data = model.objects.filter(lead_id__lead_id=lead_id).first()
                    p_id = data.lead_id.id
                    main_data['lead_id'] = p_id

                else:
                    main_data['lead_id'] = lead_id
                    data = model.objects.filter(lead_id = lead_id).first()

                serializer = dynamic(data, data=main_data, partial=True)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    if table == 'followup':
                        service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = 'follow up')
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        "status":status.HTTP_200_OK,
                        "message": 'updations successful',
                        "data": {'message' : "changes saved successfully"}
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'request failed',
                    'data': []
                    }

                return res

            elif user_role == 'bd_tl':
                if table != 'all_identifiers':
                    lead_service_category = all_identifiers.objects.filter(lead_id = lead_id).first()
                    lead_service_category = lead_service_category.service_category
                    print(lead_service_category)

                    if product == lead_service_category:
                        # model = apps.get_model('business_leads', table)
                        # dynamic = dynamic_serializer_submit(model)

                        if table == 'followup':
                            main_data['created_by'] = request.user.employee_id

                        data = model.objects.filter(lead_id__lead_id=lead_id).first()
                        p_id = data.lead_id.id
                        print(data)

                        if table != 'all_identifiers':
                            main_data['lead_id'] = p_id

                        serializer = dynamic(data, data=main_data, partial=True)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()

                            if table == 'followup':
                                service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = 'follow up')

                            res.status_code = status.HTTP_200_OK
                            res.data = {
                                "status":status.HTTP_200_OK,
                                "data": 'successful',
                                "data": serializer.data
                                }
                        else :
                            res.status_code = status.HTTP_400_BAD_REQUEST
                            res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'request failed',
                            'data': []
                            }

                        return res
                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'unauthorized access to this lead',
                            'data': []
                            }
                        return res
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'you are not authorized to make any changes to all identifiers',
                        'data': []
                        }
                    return res
            return res
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'the table do not exists',
                'data': []
                }
            return res




class assignAssociate(GenericAPIView):
    serializer_class = assignAssociateSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None, *args, **kwargs):
        print('request.data',request.data)

        lead_id = request.data.get('lead_id')
        assoc_employee_id = request.data.get('employee_id')
        team_leader_id = getTeamLeader(assoc_employee_id)
        print(team_leader_id)
        
        req_data = {"team_leader_id": team_leader_id, "associate_id": assoc_employee_id}
        
        # with connection.cursor() as cursor:
        res = Response()
        if isinstance(lead_id, list):
            for ld in lead_id:
                data = service.objects.filter(lead_id__lead_id = ld).first()
                print(data)
                serializer = assignAssociateSerializer(data, data=req_data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res.status_code = status.HTTP_201_CREATED
                    res.data = {
                        'status' : status.HTTP_201_CREATED,
                        'message' : 'associate assigned',
                        'data' : {'message': 'this lead has been updated'}
                        }
                    return res
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status' : status.HTTP_400_BAD_REQUEST,
                        'message' : 'request failed',
                        'data' : []
                        }
                    return res
                # d = cursor.execute(f"UPDATE api_business_leads_service set associate_id = '{assoc_employee_id}', team_leader_id = '{team_leader_id}' WHERE lead_id = '{ld}'")
        else: 
            data = service.objects.filter(lead_id__lead_id = lead_id).first()
            print(data)
            serialize = assignAssociateSerializer(data, data=req_data, partial=True)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                res.status_code = status.HTTP_201_CREATED
                res.data = {
                    'status' : status.HTTP_201_CREATED,
                    'message' : 'associate assigned',
                    'data' : {'message': 'this lead has been updated'}
                }
                return res
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'request failed',
                    'data' : []
                }
                return res
            # d = cursor.execute(f"UPDATE api_business_leads_service set associate_id = '{assoc_employee_id}', team_leader_id = '{team_leader_id}' WHERE lead_id = '{lead_id}'")
        # cursor.close()
        # connection.close()
    
        # return res



# def dbTableAddData(request):
#     email_ask_for_details.objects.create(
#         service = 'account management',
#         email = """<html>
#             Hello Customer,
#             <br>
#             Please help us with the below details to proceed further:
#             <br>
#             <ul>
#             <li>Company Name:</li>
#             <li>Company Address:</li>
#             <li>Contact Person/ Designation:</li>
#             <li>Signing Person/ Designation:</li>
#             <li>Email:</li>
#             <li>Mobile:</li>
#             <li>GST Number:</li>
#             <li>Brand Name:</li>
#             </ul>
#             <br>

#             Best Regards,
#             <br>
#             {***sender***}

#             </html>""",
#     )
#     return render(request, 'upload.html')
#     pass




# @api_view(['POST'])
# def apiLeadManagerIndvView(request, lead_id):
#     user = cookieAuth(request)
#     employee_id = user['user'].employee_id
#     product = getProduct(employee_id)

#     all_identifiers_data_rw = all_identifiers.objects.raw(f"SELECT * FROM business_leads_all_identifiers as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     all_identifiers_data = allIdentifiersSerializer(all_identifiers_data_rw, many=True)

#     business_identifiers_data_rw = business_identifiers.objects.raw(f"SELECT * FROM business_leads_business_identifiers as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     business_identifiers_data = businessIdentifiersSerializer(business_identifiers_data_rw, many=True)

#     comment_data_rw = comment.objects.raw(f"SELECT * FROM business_leads_comment as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     comment_data = commentSerializer(comment_data_rw, many=True)


#     contact_preference_data_rw = contact_preference.objects.raw(f"SELECT * FROM business_leads_contact_preference as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     contact_preference_data = contactPreferenceSerializer(contact_preference_data_rw, many=True)


#     followup_data_rw = followup.objects.raw(f"SELECT * FROM business_leads_followup as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     followup_data = followupSerializer(followup_data_rw, many=True)
    

#     seller_address_data_rw = seller_address.objects.raw(f"SELECT * FROM business_leads_seller_address as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     seller_address_data = sellerAddressSerializer(seller_address_data_rw, many=True)


#     service_data_rw = service.objects.raw(f"SELECT * FROM business_leads_service WHERE lead_id = '{lead_id}'")
#     service_data = serviceSerializer(service_data_rw, many=True)
#     print(service_data.data)


#     website_store_data_rw = website_store.objects.raw(f"SELECT * FROM business_leads_website_store as bls JOIN business_leads_service as ser WHERE ser.lead_id = bls.lead_id AND bls.lead_id = '{lead_id}'")
#     website_store_data = websiteStoreSerializer(website_store_data_rw, many=True)


#     res =  Response()
#     res.status_code = status.HTTP_200_OK
#     res.data = {'all_identifiers' : all_identifiers_data.data , 'business_identifiers' : business_identifiers_data.data , 'comment' : comment_data.data , 'contact_preference': contact_preference_data.data, 'followup' : followup_data.data , 'seller_address' : seller_address_data.data , 'service' : service_data.data , 'website_store': website_store_data.data}    
    
#     return res


