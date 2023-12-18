from django.shortcuts import render
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from django.apps import apps
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import FileResponse

from io import BytesIO

from xhtml2pdf import pisa

import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

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
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = uploadFileSerializer
    permission_classes = [IsAuthenticated]
    # @api_view(['POST'])
    def post(self, request, format=None, *args, **kwargs):
        # print(request)
        if request.method == 'POST':
            if request.FILES:
                file = request.FILES['file']
                # print('file', file)
                obj = File.objects.create(file = file)
                df = pd.read_csv(obj.file, delimiter=',',   header=0)
                df = pd.DataFrame(df)
                df.fillna('', inplace=True)
                # print(df)
                head_row = df.columns.values
                h_row = [f.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('__', '_').replace('__', '_').lower() for f in head_row]
                db_head_row_all_rw = all_identifiers._meta.get_fields()
                db_head_row_all = [field.name for field in db_head_row_all_rw]
                db_head_row_all_type = [field.get_internal_type() for field in db_head_row_all_rw]
                db_head_row_serv_rw = service._meta.get_fields()
                db_head_row_serv = [field.name for field in db_head_row_serv_rw]
                list_of_csv = [list(row) for row in df.values]
                # print(list_of_csv)

                output_data = []

                break_out = True

                ref_id = ''

                for ls in list_of_csv:
                    # print(db_head_row_all)cls
                    # print('isna',pd.DataFrame(ls).isna())
                    dt = {}
                    lead_id = getLeadId()
                    all_identifiers_instance = all_identifiers()
                    for i in range (len(db_head_row_all)):
                        if not (db_head_row_all[i] == 'id' or db_head_row_all[i] == 'lead_id') and db_head_row_all[i] in h_row:
                                ind = h_row.index(db_head_row_all[i])

                                # print(db_head_row_all[i])

                                
                                if db_head_row_all[i] == 'service_category':
                                    dt[db_head_row_all[i]] = ls[ind]
                                

                                elif db_head_row_all[i] == 'request_id':
                                    if ls[ind] != '':
                                        if len(str(ls[ind])) > 0:
                                            dt[db_head_row_all[i]] = ls[ind]
                                    else:
                                        break_out = False
                                        break

                                elif db_head_row_all[i] == 'phone_number':
                                    if ls[ind] != '':
                                        dt[db_head_row_all[i]] = str(int(ls[ind]))
                                        print(str(int(ls[ind])))
                                    else:
                                        dt[db_head_row_all[i]] = ''

                                else:

                                    if isinstance(ls[ind], str):
                                        # if len(ls[ind]) >= 0:
                                           dt[db_head_row_all[i]] = ls[ind].lower()
                                        # else:
                                        #    print(ls[ind].lower())

                                    elif isinstance(ls[ind], float):
                                        if ls[ind] != '':
                                            dt[db_head_row_all[i]] = str(ls[ind])
                                        else:
                                            dt[db_head_row_all[i]] = ''
                                        # print(str(ls[ind]))
                                    elif isinstance(ls[ind], int):
                                        if ls[ind] != '':
                                            dt[db_head_row_all[i]] = str(ls[ind])
                                        else:
                                            dt[db_head_row_all[i]] = ''
                                        # print('int', ls[ind])
                                    
                                    else: 
                                        # len(ls[ind])>0 else
                                        dt[db_head_row_all[i]] = ls[ind]

                                

                    # print('function passed')
                    # print(break_out)
                    if break_out:
                        d = [lead_id]
                        d = d + ls
                        output_data.append(d)

                        dt['lead_id'] = str(lead_id)
                        for field_name, value in dt.items():
                            setattr(all_identifiers_instance, field_name, value)
                        all_identifiers_instance.save()

                        ref_id = all_identifiers.objects.filter(lead_id = lead_id).values('id').first()
                        ref_id = ref_id['id']
                        # print(ref_id)

                        service_instance = service()
                        dt = {}
                        for i in range (len(db_head_row_serv)):
                            if not (db_head_row_serv[i] == 'id' or db_head_row_serv[i] == 'lead_id') and db_head_row_serv[i] in h_row:
                                ind = h_row.index(db_head_row_serv[i])
                                # print('working till here')


                                if isinstance(ls[ind], str):
                                    dt[db_head_row_serv[i]] = ls[ind].lower().strip()
                                elif isinstance(ls[ind], float):
                                    if ls[ind] == '':
                                        dt[db_head_row_all[i]] = ''
                                    else:
                                        dt[db_head_row_all[i]] = str(ls[ind])
                                    # print(str(ls[ind]))
                                elif isinstance(ls[ind], int):
                                    if ls[ind] != '':
                                        dt[db_head_row_all[i]] = ''
                                    else:
                                        dt[db_head_row_all[i]] = str(ls[ind])


                                # if db_head_row_all[i] != 'service_category': 
                                #     dt[db_head_row_serv[i]] = ls[ind]

                                # else:
                                #     if isinstance(ls[ind], str):
                                #         dt[db_head_row_serv[i]] = ls[ind].lower() 
                                #     else: 
                                #         # len(ls[ind])>0 else
                                #         dt[db_head_row_serv[i]] = ls[ind]


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
                    else:
                        d = ['not generated']
                        d = d + ls
                        output_data.append(d)

                        
                    
                res =  Response()
                res.status_code = status.HTTP_201_CREATED
                # res['Access-Control-Allow-Origin'] = '*'
                # res['Access-Control-Allow-Credentials'] = True
                # res['Allow_'] = status.HTTP_201_CREATED
                res.data = {
                    "status": status.HTTP_201_CREATED,
                    "message": 'all records saved successfully', 
                    "data": output_data
                    }
                print('working here')
            else :
                res =  Response()
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'file object not provided with key "file"',
                    'data': []
                }
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
            if user_role == 'lead_manager' or 'admin':

                cursor.execute(f"SELECT a.lead_id, a.requester_name, b.service_category, b.lead_status, a.upload_date FROM business_leads_all_identifiers as a JOIN business_leads_service as b WHERE a.id = b.lead_id_id ORDER BY b.lead_id_id LIMIT {offset}, {limit}")

                column = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    data.append(dict(zip(column, row)))

                cursor.execute(f"select count(lead_id) from business_leads_all_identifiers")
                for row in cursor.fetchall():
                    pagecount = math.ceil(row[0]/limit)

                serializer = lead_managerBlSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                
                if int(page) <= pagecount:
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        "status": status.HTTP_200_OK,
                        "message": 'successful',
                        "data": {'data': serializer.data, 'total_pages': pagecount, "current_page": page}
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'the page is unavailable',
                        "data": {'data': [], 'total_pages': pagecount, "current_page": page}
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

                if int(page) <= pagecount:
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'message': 'successful',
                        'data': {'data': serializer.data, 'pagecount': pagecount}
                        }
                
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'the page is unavailable',
                        "data": {'data': [], 'total_pages': pagecount, "current_page": page}
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
        if user_role == 'lead_manager' or 'admin':
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

            if user_role == 'lead_manager' or 'admin':

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

        obj_user = employee_official.objects.filter(emp__id = request.user.id).first()
        user_role = obj_user.user_role
        print('user_role', user_role)

        res = Response()
        if user_role == 'admin' or 'lead_manager' or 'bd_tl':
            lead_id = request.data.get('lead_id')
            assoc_employee_id = request.data.get('employee_id')
            team_leader_id = getTeamLeader(assoc_employee_id)
            print(team_leader_id)

            req_data = {"team_leader_id": team_leader_id, "associate_id": assoc_employee_id}

            # with connection.cursor() as cursor:
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
        else: 
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : 'you are not authorized to assign leads',
                'data' : []
            }
            return res
        



class apiSubmitEmailAskForDetails(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, lead_id, format=None, *args, **kwargs):
        # user = cookieAuth(request)
        # employee_id = user.employee_id
        product = getProduct(request.user.id)
        user_role = getUserRole(request.user.id)
        res =  Response()
        if user_role == 'bd_tl' or 'bd_t_member': 
    
            message = email_ask_for_details.objects.filter(service = product).first()
            message = message.email
            message = message.replace('{***sender***}', request.user.name)

            data_basic = all_identifiers.objects.get(lead_id=lead_id)
            email = data_basic.email_id

            subject = 'details required to proceed further'
            text = ''
            from_email = 'akshatnigamcfl@gmail.com'
            recipient = [email]

            email = EmailMultiAlternatives(subject, text, from_email, recipient)
            email.attach_alternative(message, 'text/html')
            email = email.send()
            if email:
                status_update = service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = 'asked for details')
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': status.HTTP_200_OK,
                    'message': 'email sent',
                    'data': []}
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'email not sent sent',
                    'data': []
                    }
            return res
        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'you are not authorized for this action',
                'data' : []
            }


class mouFun(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, lead_id, format=None, *args, **kwargs):
        # user = cookieAuth(request)
        # employee_id = user['user'].employee_id
        user_role = getUserRole(request.user.id)
        if user_role == 'bd_tl' or 'bd_t_member':

            data_service = service.objects.get(lead_id__lead_id=lead_id)
            service_name = data_service.service_category
            fees_slab = data_service.fees_slab

            res = Response()
            if not service_name:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'add service name in the lead details',
                    'data': []
                    }
                return res 
            if not fees_slab:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'add fees slab in the lead details',
                    'data': []
                    }
                return res


            data_basic = all_identifiers.objects.get(lead_id = lead_id)
            requester_name = data_basic.requester_name
            email_id = data_basic.email_id
            phone_number = data_basic.phone_number

            # res = Response()
            if not requester_name:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add requester name in the lead details',
                    'data': []
                    }
                return res
            if not email_id:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add email id in the lead details',
                    'data': []
                    }
                return res 
            if not phone_number:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add phone number in the lead details',
                    'data': []
                    }
                return res


            data_business_identifiers = business_identifiers.objects.get(lead_id__lead_id = lead_id)
            business_name = data_business_identifiers.business_name
            brand_name = data_business_identifiers.brand_name
            name_for_mou = data_business_identifiers.name_for_mou
            designation = data_business_identifiers.designation
            gst = data_business_identifiers.gst

            # res = Response()
            if not business_name:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add business name in the lead details',
                    'data': []
                    }
                return res 
            if not brand_name:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add brand name in the lead details',
                    'data': []
                    }
                return res
            if not name_for_mou:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add name for mou in the lead details',
                    'data': []
                    }
                return res
            if not designation:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add designation in the lead details',
                    'data': []
                    }
                return res
            if not gst:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add gst in the lead details',
                    'data': []
                    }
                return res

            data_seller_address = seller_address.objects.get(lead_id__lead_id = lead_id)
            address_line1 = data_seller_address.address_line1
            address_line2 = data_seller_address.address_line2
            city = data_seller_address.city
            state = data_seller_address.state
            country = data_seller_address.country
            pin_code = data_seller_address.pin_code

            if not address_line1:
                res.status_code = status.HTTP_400_BAD_REQUEST,
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add addredd line1 in the lead details',
                    'data': []
                    }
            else:
                address_line = address_line1
                if address_line2:
                    address_line += ' '+address_line2 

            if not city:
                res.data ={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add city in the lead details',
                    'data': []
                    }
                return res 
            if not state:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add state in the lead details',
                    'data': []
                    }
                return res
            if not country:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add country in the lead details',
                    'data': []
                    }
                return res
            if not pin_code:
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'add pin code in the lead details',
                    'data': []
                    }
                return res 

            address = address_line +' '+ city +' '+ state+' '+ country +' '+ pin_code


            if address:
                template = get_template('mou/mou.html')
                date = datetime.datetime.now()
                date = f"{date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}"

                context = {
                    'current_date': date, 
                    'business_name': business_name, 
                    'brand_name': brand_name, 
                    'business_address': address, 
                    "service_name": service_name, 
                    "fees_slab": fees_slab, 
                    "name_for_mou": name_for_mou, 
                    'designation': designation, 
                    'requester_name': requester_name, 
                    "email_id": email_id, 
                    "gst": gst, 
                    "phone_number": phone_number
                    }

                html = template.render(context)

                res = BytesIO()
                result = pisa.CreatePDF(html, dest=res)

                # res = HttpResponse(content_type = 'application/pdf')
                # res['Content_Disposition'] = 'filename = "mou.pdf"'

                if result.err:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'error': 'error generating pdf',
                        'data': []
                        })

                status_update = service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = 'mou generated')
                res.seek(0)
                return FileResponse(res, content_type='application/pdf', as_attachment=True, filename=f'{business_name}.pdf')


        


# class statusUpdate(GenericAPIView):
#     serializer_class = statusUpdateSerializer
#     permission_classes = [IsAuthenticated]
#     def put(self, request, lead_id, format=None, *args, **kwargs):

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


