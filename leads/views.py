from django.db.models import Q
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


import pandas as pd

from .serializers import *
from account.models import UserAccount, Drp_Program, Department, Designation, Employee_status
from .models import Leads, Remark_history
# from account.views import getLeadId

import math
from datetime import date, datetime, timezone, timedelta



def loginpage(request):
    context = {'text':'something'}
    res = HttpResponse(render(request, 'login.html', context))
    return res





def resFun(status,message,data):
    res = Response()
    res.status_code = status
    res.data = {
        'status': status,
        'message': message,
        'data': data,
    }
    return res




class dashboard(GenericAPIView):
    serializer_class = dashboardSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if str(user.department) == 'director':

            status_history = Status_history.objects.filter(status_date = datetime.now()).distinct()
            print(status_history)

            res.status_code = status.HTTP_200_OK
            res.data = {
                "status": status.HTTP_200_OK,
                "message": 'request successful',
                "data": list(status_history.values())
                }

        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": 'you are not authorized to view this data',
                "data": { 'data': [] }
                }
        return res










# class uploadBusinessLeads(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]
#     serializer_class = uploadFileSerializer
#     def post(self, request, format=None, *args, **kwargs):
#         user = request.FILES
#         if (str(user.department) == 'lead_management' and str(user.designation) == 'lead_manager'):
#             if request.method == 'POST':
#                 if request.FILES:
#                     file = request.FILES['file']
#                     df = pd.read_csv(file, delimiter=',',   header=0)
#                     df = pd.DataFrame(df)
#                     df.fillna('', inplace=True)
#                     head_row = df.columns.values
#                     h_row = [f.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('__', '_').replace('__', '_').lower() for f in head_row]
#                     h_row[h_row.index('requester_name')] = 'client_name'
#                     h_row[h_row.index('phone_number')] = 'contact_number'

#                     db_head_row_all_rw = Leads._meta.get_fields()
#                     db_head_row_all = [field.name for field in db_head_row_all_rw]

#                     # db_head_row_all_type = [field.get_internal_type() for field in db_head_row_all_rw]

#                     # db_head_row_phNum_rw = Contact_number._meta.get_fields()
#                     # db_head_row_phNum = [field.name for field in db_head_row_phNum_rw]

#                     # db_head_row_emlId_rw = email_ids._meta.get_fields()
#                     # db_head_row_emlId = [field.name for field in db_head_row_emlId_rw]

#                     list_of_csv = [list(row) for row in df.values]
#                     output_data = []

#                     ref_id = ''

#                     for ls in list_of_csv:
#                         dup = False
#                         break_out = True
#                         dup_data = None

#                         ind_contact_number = h_row.index('contact_number')
#                         ind_email_id = h_row.index('email_id')


#                         dup_contact = str(int(ls[ind_contact_number]) if ls[ind_contact_number] != '' else '')
#                         dup_email = str(ls[ind_email_id] if ls[ind_email_id] != '' else '')


#                         dup_contact_number = Leads.objects.filter(Q(contact_number = dup_contact) | Q(alternate_contact_number = dup_contact))
#                         duplicate_contacts = []
#                         if dup_contact_number.exists():
#                             for d in dup_contact_number:
#                                 duplicate_remarks = Remark_history.objects.filter(lead_id = d.id)
#                                 duplicate_remarks = [str(d.remark) for d in duplicate_remarks]
#                                 duplicate_contacts.append({'lead_id': str(d.lead_id), 'remarks': duplicate_remarks})

#                         dup_email_id = Leads.objects.filter(Q(email_id = dup_email) | Q(alternate_email_id = dup_email))
#                         duplicate_email = []
#                         if dup_email_id:
#                             for d in dup_email_id:
#                                 if len(duplicate_contacts) > 0:
#                                     for dt in duplicate_contacts:
#                                         if dt['lead_id'] == d.lead_id:
#                                             break
#                                 else:
#                                     duplicate_remarks = Remark_history.objects.filter(lead_id = d.id)
#                                     duplicate_remarks = [str(d.remark) for d in duplicate_remarks]
#                                     duplicate_email.append({'lead_id': str(d.lead_id) , 'remarks': duplicate_remarks})

#                         if len(duplicate_contacts) > 0 or len(duplicate_email) > 0:
#                             dup = True
#                             break_out = False
#                             dup_data =  duplicate_contacts + duplicate_email

#                         if dup == False:
#                             dt = {}
#                             lead_id = getLeadId()
#                             leads_instance = Leads()
#                             for i in range (len(db_head_row_all)):
#                                 # service_category = ''
#                                 if not (db_head_row_all[i] == 'id' or db_head_row_all[i] == 'lead_id') and db_head_row_all[i] in h_row:
#                                     ind = h_row.index(db_head_row_all[i])

#                                     if db_head_row_all[i] == 'service_category':
#                                         dt[db_head_row_all[i]] = Services.objects.filter(service_name = ls[ind].lower()).first()

#                                     elif db_head_row_all[i] == 'request_id':
#                                         if ls[ind] != '':
#                                             if len(str(ls[ind])) > 0:
#                                                 dt[db_head_row_all[i]] = ls[ind]
#                                         else:
#                                             break_out = False
#                                             break

#                                     elif db_head_row_all[i] == 'status':
#                                         dt[db_head_row_all[i]] = 'yet to contact'

#                                     else:
#                                         if isinstance(ls[ind], str):
#                                                dt[db_head_row_all[i]] = ls[ind].lower()
#                                         elif isinstance(ls[ind], float):
#                                             if ls[ind] != '':
#                                                 dt[db_head_row_all[i]] = str(ls[ind])
#                                             else:
#                                                 dt[db_head_row_all[i]] = ''
#                                         elif isinstance(ls[ind], int):
#                                             if ls[ind] != '':
#                                                 dt[db_head_row_all[i]] = str(ls[ind])
#                                             else:
#                                                 dt[db_head_row_all[i]] = ''
#                                         else: 
#                                             dt[db_head_row_all[i]] = ls[ind]

#                         if break_out:
#                             # Status_history.objects.create({'service'})
#                             d = [lead_id]
#                             head_rows = [h for h in h_row]
#                             head_rows.insert(0, 'lead_id')
#                             d = d + ls
#                             head_rows.insert(0, 'status')
#                             d = [str(drp_lead_status.objects.filter(title = 'yet to contact').first().title)] + d
#                             output_data.append(dict(zip(head_rows ,d)))

#                             dt['lead_id'] = str(lead_id)
#                             dt['status'] = drp_lead_status.objects.filter(title = 'yet to contact').first()
#                             for field_name, value in dt.items():
#                                 if field_name != 'city':
#                                     setattr(leads_instance, field_name, value)
#                             leads_instance.save()

#                             # ref_id = Leads.objects.filter(lead_id = lead_id).values('id').first()
#                             # ref_id = ref_id['id']

#                             # contact_instance = Contact_number()
#                             # dt = {}
#                             # for i in range (len(db_head_row_phNum)):
#                             #     if not (db_head_row_phNum[i] == 'id' or db_head_row_phNum[i] == 'lead_id'):
#                             #         ind = h_row.index(db_head_row_phNum[i])
#                             #         dt[db_head_row_phNum[i]] = str(int(ls[ind]))

#                             # dt['lead_id'] = leads_instance
#                             # for field_name, value in dt.items():
#                             #     setattr(contact_instance, field_name, value)
#                             # contact_instance.save()

#                             # email_instance = email_ids()
#                             # dt = {}
#                             # for i in range (len(db_head_row_emlId)):
#                             #     if not (db_head_row_emlId[i] == 'id' or db_head_row_emlId[i] == 'lead_id'):
#                             #         ind = h_row.index(db_head_row_emlId[i])
#                             #         dt[db_head_row_emlId[i]] = str(ls[ind])

#                             # dt['lead_id'] = leads_instance
#                             # for field_name, value in dt.items():
#                             #     setattr(email_instance, field_name, value)
#                             # email_instance.save()

#                             Status_history.objects.create(**{'status': drp_lead_status.objects.filter(title = 'yet to contact').first(), "lead_id": leads_instance, 'status_date': date.today() ,'updated_by': request.user })

#                             # service_instance = Service_category() 
#                             # dt = {'service': service_category if service_category else None  ,'lead_id': leads_instance, 'status': drp_lead_status.objects.filter(title = 'yet to contact').first() }
#                             # for i in range (len(db_head_row_emlId)):
#                             #     if not (db_head_row_emlId[i] == 'id' or db_head_row_emlId[i] == 'lead_id'):
#                             #         ind = h_row.index(db_head_row_emlId[i])
#                             #         dt[db_head_row_emlId[i]] = str(ls[ind])

#                             # dt['lead_id'] = leads_instance
#                             # for field_name, value in dt.items():
#                             #     setattr(service_instance, field_name, value)
#                             # service_instance.save()

#                         else:
#                             d = ['not generated']
#                             head_rows = [h for h in h_row]
#                             if dup_data:
#                                 head_rows.insert(0, 'duplicate_leads')
#                                 data = [dup_data] + ls
#                             else:
#                                 data = ls
#                             head_rows.insert(0, 'lead_id')
#                             d = d + data
#                             output_data.append(dict(zip(head_rows ,d)))

#                     res =  Response()
#                     res.status_code = status.HTTP_201_CREATED
#                     # res['Access-Control-Allow-Origin'] = '*'
#                     # res['Access-Control-Allow-Credentials'] = True
#                     res.data = {
#                         "status": status.HTTP_201_CREATED,
#                         "message": 'all records saved successfully', 
#                         "data": output_data
#                         }
#                 else :
#                     res =  Response()
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'file object not provided with key "file"',
#                         'data': []
#                     }
#                 return res
#             else:
#                 res = Response()
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     "status" : status.HTTP_400_BAD_REQUEST,
#                     "message": "unsuccessful",
#                     "data": []
#                 }
        
#         else:
#                 res = Response()
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     "status" : status.HTTP_400_BAD_REQUEST,
#                     "message": "you are not authorized for this action",
#                     "data": []
#                 }

#         return res
    



# class createLeadManual(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = createLeadManualSerializer
#     def post(self, request, format=None, *args, **kwargs):
#         # user_role = getUserRole(request.user.id)
#         res = Response()
#         serializer = createLeadManualSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             # pass
#             if serializer.save():
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     "status": status.HTTP_200_OK,
#                     "message" : 'lead registered successfully',
#                     "data": []
#                 }
#                 return res
#             else :
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "message" : 'request failed',
#                     "data": []
#                 }
#         return res
    


class viewAllLeads(GenericAPIView):
    serializer_class = lead_managerBlSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, page, format=None, *args, **kwargs):
        user = request.user
        limit = 10
        offset = int((page - 1) * limit)
        data = []
        pagecount = 1
        res =  Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'unauthorized access', 
                'data': [],
            })

        if str(user.department) == 'director' or (str(user.department) == 'admin' and str(user.designation) == 'administrator'):
            data = []
            leadsData = Leads.objects.select_related().filter(visibility = True).all()[offset : offset + limit]

            for sd in leadsData:
                tat = Turn_Arround_Time.objects.all().first()
                today = datetime.now()
                upload_date = datetime.strptime(str(sd.upload_date),"%Y-%m-%d %H:%M:%S.%f%z")
                upload_date = upload_date.replace(tzinfo=None)
                # upload_date = upload_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                deadline = (today - upload_date).total_seconds()
                deadline = (math.ceil((int(tat.duration_in_hrs) - math.floor(int(deadline // (3600)))) / 24) -1 )
                # print('deadline', deadline)

                data.append({
                    'lead_id' : sd.lead_id , 
                    'client_name': sd.client_name, 
                    # 'service_category': sd.service_category.service_name, 
                    'assigned_to': sd.associate.name if sd.associate else '-', 
                    # 'status': sd.status.title if sd.status else '-', 
                    'upload_date': upload_date , 
                    'deadline': deadline,
                    "associate" : sd.associate.name if sd.associate else '-',
                    "service_category" : sd.service_category.service_name if sd.service_category else '-',
                    "commercials" : sd.commercials.price_for_mou if sd.commercials else '-',
                    "status" : sd.status.title if sd.status else '-',
                    "client_turnover" : sd.client_turnover.title if sd.client_turnover else '-',
                    "business_type" : sd.business_type.title if sd.business_type else '-',
                    "business_category" : sd.business_category.title if sd.business_category else '-',
                    "firm_type" : sd.firm_type.title if sd.firm_type else '-',
                    "contact_preferences" : sd.contact_preferences.title if sd.contact_preferences else '-',
                    "followup" : sd.followup.followup_date if sd.followup else '-',
                    "country" : sd.country.title if sd.country else '-',
                    "state" : sd.state.title if sd.state else '-',
                    "city" : sd.city.title if sd.city else '-'
                    
                    })
            
            if len(data) > 0:
                pagecount = math.ceil(Leads.objects.filter(visibility = True).count()/limit)
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
            else:   
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": 'no data found',
                    "data": {'data': [], 'total_pages': [], "current_page": page}
                    }
            return res

        elif user_role == 'bd_tl':
            product = getProduct(user.id)
            # print(product)
            data = []
            serviceData = service.objects.select_related().filter(service_category = product, lead_id__visibility = True)[offset : limit]
            for sd in serviceData:
                associate = sd.associate_id.name if sd.associate_id != None else 'not assigned'
                data.append({'lead_id': sd.lead_id.lead_id, 'requester_name': sd.lead_id.requester_name, 'phone_number':  sd.lead_id.phone_number, 'email_id': sd.lead_id.email_id, 'service_category': sd.service_category, 'associate': associate, 'lead_status': sd.lead_status.title})

            if len(data) > 0:
                pagecount = math.ceil(service.objects.filter(service_category = product ,lead_id__visibility = True).count()/limit)
                print('pagecount',pagecount)
                serializer = bd_teamLeaderSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                if int(page) <= pagecount:
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'message': 'successful',
                        'data': {'data': serializer.data, 'total_pages': pagecount, "current_page": page}
                        }

                else :
                    pagecount = math.ceil(service.objects.filter(service_category = product ,lead_id__visibility = True).count()/limit)

                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'the page is unavailable',
                        "data": {'data': [], 'total_pages': pagecount, "current_page": page}
                        }
                    
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": 'no data found',
                    "data": {'data': [], 'total_pages': pagecount, "current_page": page}
                    }
        
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": 'you are not authorized to view this data',
                "data": {'data': [], 'total_pages': pagecount, "current_page": page}
                }
        return res

        




class viewLeadsAllIdentifiers(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = View_All_Leads
    def post(self, request, lead_id ,format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if (str(user.department) == 'director'):

            leads = Leads.objects.select_related().filter(lead_id=lead_id, visibility =True)
            if leads.exists():
                # print('leads', leads)
                leads_val = leads.values().first()
                leads = leads.first()

                leads_val["associate"] = leads.associate.name if leads.associate else '-'
                leads_val["service_category"] = leads.service_category.service_name if leads.service_category else '-'
                leads_val["commercials"] = leads.commercials.price_for_mou if leads.commercials else '-'
                leads_val["status"] = leads.status.title if leads.status else '-'
                leads_val["client_turnover"] = leads.client_turnover.title if leads.client_turnover else '-'
                leads_val["business_type"] = leads.business_type.title if leads.business_type else '-'
                leads_val["business_category"] = leads.business_category.title if leads.business_category else '-'
                leads_val["firm_type"] = leads.firm_type.title if leads.firm_type else '-'
                leads_val["contact_preferences"] = leads.contact_preferences.title if leads.contact_preferences else '-'
                leads_val["followup"] = leads.followup.followup_date if leads.followup else '-'
                leads_val["country"] = leads.country.title if leads.country else '-'
                leads_val["state"] = leads.state.title if leads.state else '-'
                leads_val["city"] = leads.city.title if leads.city else '-'

                print(leads_val)

                serializer = View_All_Leads(data=leads_val)

                if serializer.is_valid(raise_exception=True):

                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        "status": status.HTTP_200_OK,
                        'data': serializer.data,
                        'message': 'request successful'
                    }
                else:
                    res.status_code = status.HTTP_404_NOT_FOUND
                    res.data = {
                        "status": status.HTTP_404_NOT_FOUND,
                        'data': [],
                        'message': 'request failed'
                    }
            else:
                res.status_code = status.HTTP_404_NOT_FOUND
                res.data = {
                    "status": status.HTTP_404_NOT_FOUND,
                    'data': [],
                    'message': 'invalid lead_id'
                }

        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                "status": status.HTTP_404_NOT_FOUND,
                'data': [],
                'message': 'you are not authorized for this actions'
            }
        return res
    



class viewAllLeadsSearch(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = lead_managerBlSerializer
    def get(self, request, lead_id, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):

            # user_role = getUserRole(user.id)
            # data = []

            # if user_role == 'lead_manager' or user_role == 'admin':
            data = []
            leads = Leads.objects.select_related().filter(lead_id = lead_id, visibility = True)
            if leads.exists():
                data = []
                for sd in leads:
                    tat = Turn_Arround_Time.objects.all().first()
                    today = datetime.now()
                    upload_date = datetime.strptime(str(sd.upload_date),"%Y-%m-%d %H:%M:%S.%f%z")
                    upload_date = upload_date.replace(tzinfo=None)
                    # upload_date = upload_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    deadline = (today - upload_date).total_seconds()
                    deadline = (math.ceil((int(tat.duration_in_hrs) - math.floor(int(deadline // (3600)))) / 24) -1 )
                    print('deadline', deadline)

                    data.append({'lead_id' : sd.lead_id , 'client_name': sd.client_name, 'service_category': sd.service_category.service_name, 'assigned_to': sd.associate.name if sd.associate else '-', 'status': sd.status.title if sd.status else '-', 'upload_date': upload_date , 'deadline': deadline })
                    # for sd in serviceData:
                #     data.append({'lead_id' : sd.lead_id.lead_id , 'requester_name': sd.lead_id.requester_name, 'service_category': sd.service_category, 'upload_date': sd.lead_id.upload_date, 'lead_status': getLeadStatusInst(sd.lead_status) }) 
                #     print('data', data)
                serializer = lead_managerBlSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    "status": status.HTTP_200_OK,
                    "message": 'successful',
                    "data": serializer.data
                    }
            else:
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid lead id',
                    'data' : []
                }

        elif user_role == 'bd_tl':
            product = getProduct(user.id)
            data = []
            serviceData = service.objects.select_related().filter(lead_id__lead_id = lead_id, service_category = product, lead_id__visibility=True)
            if serviceData:
                for sd in serviceData:
                    associate = sd.associate_id.name if sd.associate_id != None else '-'
                    data.append({'lead_id': sd.lead_id.lead_id, 'requester_name': sd.lead_id.requester_name, 'phone_number':  sd.lead_id.phone_number, 'email_id': sd.lead_id.email_id, 'service_category': sd.service_category, 'associate': associate, 'lead_status': sd.lead_status.title})

                serializer = BusinessDevelopmentLeadSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': status.HTTP_200_OK,
                    'message': 'successful',
                    'data': serializer.data
                    }
            else: 
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid lead id',
                    'data' : []
                }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": 'you are not authorized to view this data',
                "data": []
                }
        return res
    













#services:

class Createcountry(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCountrySerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):
            country = Country.objects.filter(country = request.data.get('country').lower()).values()
            if not country.exists():
                serializer = CreateCountrySerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK,'added successfully',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'country already exists, kindly check archives',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res
   
class Updatecountry(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCountrySerializer
    def put(self, request, id, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):
            country = Country.objects.get(id=id, visibility=True)
            if country:
                if not Country.objects.filter(country=request.data.get('country').lower()).exists():
                    serializer = CreateCountrySerializer(country, data=request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        res = resFun(status.HTTP_400_BAD_REQUEST,'updated successfully',[])
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'marketplace already exists',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no data found, kindly check archives',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res
    
class Deletecountry(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCountrySerializer
    def delete(self, request, id, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):
            try:
                country = Country.objects.filter(id=id, visibility=True).first()
            except:
                country = Country.objects.filter(pk__in=[]).first()
            # print(marketplace)
            if country:
                country.visibility = False
                for m in country.service.all():
                    for c in m.commercials.all():
                        if c.visibility == True:
                            c.visibility = False
                            c.save()
                    if m.visibility == True:
                        m.visibility = False
                        m.save()
                country.save()
                res = resFun(status.HTTP_200_OK,'deleted successfully',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'invalid marketplace id',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res
    
class Viewcountry(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewCountrySerializer
    def get(self, request ,format=None, *args, **kwargs):
        # limit = 10
        # offset = int((page - 1) * limit)
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):
            country = Country.objects.filter(visibility=True)
            # print(list(marketplace.values_list()))
            if country.exists():
                serializer = ViewCountrySerializer(data={'country': country.values()})
                # pagecount = math.ceil(Marketplace.objects.filter().count()/limit)
                if serializer.is_valid(raise_exception=True):
                    res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
            else:
                res = resFun(status.HTTP_200_OK,'no data found',[])
        else:
            res = resFun(status.HTTP_401_UNAUTHORIZED,'you are not authorized for this action',[])
        return res
   
class Searchcountry(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchCountrySerializer
    def get(self, request, id, format=None, *args, **kwargs):
        user = request.user
        # res =  Response()
        if (str(user.department) == 'director'):
            name = id.replace('_',' ')
            try:
                country = Country.objects.filter(country__contains = name, visibility=True)
            except:
                country = Country.objects.filter(pk__in=[])
            if country.exists():
                serializer = SearchCountrySerializer(data=[{'id': country.first().id, 'country': country.first().country}], many=True)
                if serializer.is_valid(raise_exception=True):
                    res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no data found, kindly check archives',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res
      




class CreateSegment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSegmentSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):
            try:
                segment = Segment.objects.filter(segment = request.data.get('segment').lower()).values()
            except:
                segment = Segment.objects.filter(pk__in = []).values()
            
            if not segment.exists():
                serializer = CreateSegmentSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    res = resFun(status.HTTP_200_OK, 'added successfully',serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'segment already exists, kindly check archives',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action',[])
        return res
    


class ViewSegment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSegmentSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                segment = Segment.objects.filter(visibility=True)
            except:
                segment = Segment.objects.filter(pk__in=[])

            if segment.exists():
                serializer = ViewSegmentSerializer(data=list(segment.values()),many=True)
                if serializer.is_valid():
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class EditSegment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSegmentSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                segment = Segment.objects.filter(id=id)
            except:
                segment = Segment.objects.filter(pk__in=[])

            if segment.exists():
                serializer = ViewSegmentSerializer(segment.first(), data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_200_OK, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
            


class ArchiveSegment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSegmentSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                segment = Segment.objects.filter(id=id)
            except:
                segment = Segment.objects.filter(pk__in=[])

            if segment.exists():
                segment = segment.first()
                segment.visibility = False
                segment.save()
                res = resFun(status.HTTP_200_OK, 'segment archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class ViewArchiveSegment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSegmentSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                segment = Segment.objects.filter(visibility=False)
            except:
                segment = Segment.objects.filter(pk__in=[])

            if segment.exists():
                serializer = ViewSegmentSerializer(data=list(segment.values()),many=True)
                if serializer.is_valid():
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class UnarchiveSegment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSegmentSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                segment = Segment.objects.filter(id=id)
            except:
                segment = Segment.objects.filter(pk__in=[])

            if segment.exists():
                segment = segment.first()
                segment.visibility = True
                segment.save()
                res = resFun(status.HTTP_200_OK, 'segment unarchived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res    



class CreateService(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateServiceSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                segment = Service.objects.filter(service = request.data.get('service').lower()).values()
            except:
                segment = Service.objects.filter(pk__in = []).values()
            
            if not segment.exists():
                serializer = CreateServiceSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    res = resFun(status.HTTP_200_OK, 'added successfully',serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'service already exists, kindly check archives',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action',[])
        return res    



class ViewService(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                service = Service.objects.filter(visibility=True)
            except:
                service = Service.objects.filter(pk__in=[])

            if service.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(service.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])

        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class EditService(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                service = Service.objects.filter(id=id)
            except:
                service = Service.objects.filter(pk__in=[])

            if service.exists():
                serializer = ViewServiceSerializer(service.first(), data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_200_OK, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res




class ArchiveService(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                service = Service.objects.filter(id=id)
            except:
                service = Service.objects.filter(pk__in=[])

            if service.exists():
                service = service.first()
                service.visibility = False
                service.save()
                res = resFun(status.HTTP_200_OK, 'service archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class ViewArchiveService(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                service = Service.objects.filter(visibility=False)
            except:
                service = Service.objects.filter(pk__in=[])

            if service.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(service.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])

        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res



class UnarchiveService(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                service = Service.objects.filter(id=id)
            except:
                service = Service.objects.filter(pk__in=[])

            if service.exists():
                service = service.first()
                service.visibility = True
                service.save()
                res = resFun(status.HTTP_200_OK, 'service archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res




class CreateMarketplace(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMarketplaceSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):
            marketplace = Marketplace.objects.filter(marketplace = request.data.get('marketplace').lower()).values()
            if not marketplace.exists():
                serializer = CreateMarketplaceSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'added successfully', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'marketplace already exists, kindly check archives', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class ViewMarketplace(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MarketplaceSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Marketplace.objects.filter(visibility=True)
            except:
                marketplace = Marketplace.objects.filter(pk__in=[])

            if marketplace.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(marketplace.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class EditMarketplace(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewMarketplaceSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Marketplace.objects.filter(id=id)
            except:
                marketplace = Marketplace.objects.filter(pk__in=[])

            print('marketplace',marketplace)

            if marketplace.exists():
                serializer = ViewMarketplaceSerializer(marketplace.first(), data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_200_OK, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

class ArchiveMarketplace(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewMarketplaceSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Marketplace.objects.filter(id=id)
            except:
                marketplace = Marketplace.objects.filter(pk__in=[])

            if marketplace.exists():
                marketplace = marketplace.first()
                marketplace.visibility = False
                marketplace.save()
                res = resFun(status.HTTP_200_OK, 'marketplace archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class ViewArchiveMarketplace(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MarketplaceSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Marketplace.objects.filter(visibility=False)
            except:
                marketplace = Marketplace.objects.filter(pk__in=[])

            if marketplace.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(marketplace.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res


class UnarchiveMarketplace(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewMarketplaceSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Marketplace.objects.filter(id=id)
            except:
                marketplace = Marketplace.objects.filter(pk__in=[])

            if marketplace.exists():
                marketplace = marketplace.first()
                marketplace.visibility = True
                marketplace.save()
                res = resFun(status.HTTP_200_OK, 'marketplace archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    

    

class CreateProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateProgramSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        # res =  Response()
        if (str(user.department) == 'director'):
            segment = Program.objects.filter(program = request.data.get('program').lower()).values()
            if not segment.exists():
                serializer = CreateProgramSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'added successfully', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'program already exists, kindly check archives', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    




class ViewProgram(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Program.objects.filter(visibility=True)
            except:
                marketplace = Program.objects.filter(pk__in=[])

            print('marketplace',marketplace)

            if marketplace.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(marketplace.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    



# class EditProgram(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProgramSerializer
#     def get(self,)

class EditProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                program = Program.objects.filter(id=id)
            except:
                program = Program.objects.filter(pk__in=[])

            if program.exists():
                serializer = ProgramSerializer(program.first(), data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_200_OK, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class ArchiveProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                program = Program.objects.filter(id=id)
            except:
                program = Program.objects.filter(pk__in=[])

            
            if program.exists():
                program = program.first()
                program.visibility = False
                program.save()
                
                print('program',program.visibility)
                res = resFun(status.HTTP_200_OK, 'program archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res



class ViewArchiveProgram(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                marketplace = Program.objects.filter(visibility=False)
            except:
                marketplace = Program.objects.filter(pk__in=[])

            if marketplace.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(marketplace.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class UnarchiveProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                program = Program.objects.filter(id=id)
            except:
                program = Program.objects.filter(pk__in=[])

            
            if program.exists():
                program = program.first()
                program.visibility = True
                program.save()
                
                print('program',program.visibility)
                res = resFun(status.HTTP_200_OK, 'program archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res




class CreateSubProgram(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSubProgramSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        # res =  Response()
        print('request.data', request.data)
        if (str(user.department) == 'director'):
            segment = Sub_Program.objects.filter(sub_program = request.data.get('sub_program').lower()).values()
            if not segment.exists():
                # print('request.data', request.data)
                serializer = CreateSubProgramSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'added successfully', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'program already exists, kindly check archives', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class ViewSubProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubProgramSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                sub_program = Sub_Program.objects.filter(visibility=True)
            except:
                sub_program = Sub_Program.objects.filter(pk__in=[])
            if sub_program.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(sub_program.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class EditSubProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubProgramSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                sub_program = Sub_Program.objects.filter(id=id)
            except:
                sub_program = Sub_Program.objects.filter(pk__in=[])
            if sub_program.exists():
                serializer = SubProgramSerializer(sub_program.first(), data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', serializer.errors)
            else:
                res = resFun(status.HTTP_200_OK, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class ArchiveSubProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                sub_program = Sub_Program.objects.filter(id=id)
            except:
                sub_program = Sub_Program.objects.filter(pk__in=[])
            
            if sub_program.exists():
                sub_program = sub_program.first()
                sub_program.visibility = False
                sub_program.save()
                res = resFun(status.HTTP_200_OK, 'sub program archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res


class ViewArchiveSubProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubProgramSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                sub_program = Sub_Program.objects.filter(visibility=False)
            except:
                sub_program = Sub_Program.objects.filter(pk__in=[])
            
            if sub_program.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(sub_program.values()))
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res
    


class UnarchiveSubProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director'):
            try:
                sub_program = Sub_Program.objects.filter(id=id)
            except:
                sub_program = Sub_Program.objects.filter(pk__in=[])

            
            if sub_program.exists():
                sub_program = sub_program.first()
                sub_program.visibility = True
                sub_program.save()
                
                res = resFun(status.HTTP_200_OK, 'sub program archived', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'data not found', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res


# class CreateCommercials(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = 




    

# class UpdateMarketplace(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CreateMarketplaceSerializer
#     def put(self, request, id, format=None, *args, **kwargs):
#         user = request.user
#         res =  Response()
#         if (str(user.department) == 'director'):
#             marketplace = Marketplace.objects.get(id=id, visibility=True)
#             if marketplace:
#                 if not Marketplace.objects.filter(marketplace=request.data.get('marketplace').lower()).exists():
#                     serializer = CreateMarketplaceSerializer(marketplace, data=request.data, partial=True)
#                     if serializer.is_valid(raise_exception=True):
#                         serializer.save()
#                         res.status_code = status.HTTP_200_OK
#                         res.data = {
#                             'data': serializer.data,
#                             'status': status.HTTP_200_OK,
#                             'message': 'updated successfully',
#                         }
#                     else:
#                         res.status_code = status.HTTP_400_BAD_REQUEST
#                         res.data = {
#                             'data': [],
#                             'status': status.HTTP_400_BAD_REQUEST,
#                             'message': 'request failed',
#                         }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': [],
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'marketplace already exists',
#                     }

#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'no data found, kindly check archives',
#                 }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
    
# class SearchMarketplace(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = SearchMarketplaceSerializer
#     def get(self, request, id, format=None, *args, **kwargs):
#         user = request.user
#         res =  Response()
#         if (str(user.department) == 'director'):

#             name = id.replace('_',' ')
#             try:
#                 marketplace = Marketplace.objects.filter(marketplace__contains = name, visibility=True)
#             except:
#                 marketplace = Marketplace.objects.filter(pk__in=[])

#             # try: 
#             #     marketplace = Marketplace.objects.get(id=id, visibility=True)
#             # except:
#             #     marketplace = Marketplace.objects.filter(pk__in=[])
#             # print('marketplace',marketplace)
#             if marketplace.exists():
#                 serializer = SearchMarketplaceSerializer(data=[{'id': marketplace.first().id, 'marketplace': marketplace.first().marketplace}], many=True)
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'data': serializer.data,
#                         'status': status.HTTP_200_OK,
#                         'message': 'request successful',
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': [],
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                     }
#                 # else:
#                 #     res.status_code = status.HTTP_400_BAD_REQUEST
#                 #     res.data = {
#                 #         'data': [],
#                 #         'status': status.HTTP_400_BAD_REQUEST,
#                 #         'message': 'marketplace already exists',
#                 #     }

#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'no data found, kindly check archives',
#                 }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
        
# class DeleteMarketplace(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CreateMarketplaceSerializer
#     def delete(self, request, id, format=None, *args, **kwargs):
#         user = request.user
#         res =  Response()
#         if (str(user.department) == 'director'):
#             try:
#                 marketplace = Marketplace.objects.filter(id=id, visibility=True).first()
#             except:
#                 marketplace = Marketplace.objects.filter(pk__in=[]).first()
#             # print(marketplace)
#             if marketplace:
#                 marketplace.visibility = False
#                 for m in marketplace.service.all():
#                     for c in m.commercials.all():
#                         if c.visibility == True:
#                             c.visibility = False
#                             c.save()
#                     if m.visibility == True:
#                         m.visibility = False
#                         m.save()
#                 marketplace.save()
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_200_OK,
#                     'message': 'deleted successfully',
#                 }
#                 # else:
#                 #     res.status_code = status.HTTP_400_BAD_REQUEST
#                 #     res.data = {
#                 #         'data': [],
#                 #         'status': status.HTTP_400_BAD_REQUEST,
#                 #         'message': 'request failed',
#                 #     }
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'invalid marketplace id',
#                 }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
    
# class ViewMarketplace(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ViewMarketplaceSerializer
#     def get(self, request ,format=None, *args, **kwargs):
#         # limit = 10
#         # offset = int((page - 1) * limit)
#         user = request.user
#         res =  Response()
#         if (str(user.department) == 'director'):
#             marketplace = Marketplace.objects.filter(visibility=True)
#             # print(list(marketplace.values_list()))
#             if marketplace.exists():
#                 pass
#                 serializer = ViewMarketplaceSerializer(data={'marketplace': marketplace.values()})
#                 # pagecount = math.ceil(Marketplace.objects.filter().count()/limit)

#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'data': serializer.data,
#                         'status': status.HTTP_200_OK,
#                         'message': 'request successful',
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': [],
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                     }
#             else:
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_200_OK,
#                     'message': 'no data found',
#                 }
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_401_UNAUTHORIZED,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
    






    
# class UpdateServices(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UpdateServicesSerializer
#     def put(self, request,format=None, *args, **kwargs):
#         user = request.user
#         res =  Response()

#         if (str(user.department) == 'director'):
#             try:
#                 services = Services.objects.filter(id=request.data.get('service_id'), visibility=True)
#             except:
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_200_OK,
#                     'message': 'no data found, kindly check archives',
#                 }
#                 return res
            
#             # print('services',services)
#             if services.exists():
#                 serializer = UpdateServicesSerializer(services.first(), data=request.data, partial=True)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save()
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'data': serializer.data,
#                         'status': status.HTTP_200_OK,
#                         'message': 'updated successfully',
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': [],
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                     }
#             else:
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_200_OK,
#                     'message': 'no data found',
#                 }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
        
# class DeleteServices(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CreateServicesSerializer
#     def delete(self, request, id, format=None, *args, **kwargs):
#         user = request.user
#         res =  Response()
#         if (str(user.department) == 'director'):
#             services = Services.objects.get(id=id, visibility=True)
#             if services:
#                 for s in services.commercials.all():
#                     if s.visibility == True:
#                         s.visibility = False
#                         s.save()
#                     # commercials = Commercials.objects.get(id = s.id, visibility=True)
#                     # commercials.delete()
#                 services.visibility = False
#                 services.save()
           
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_200_OK,
#                     'message': 'deleted successfully',
#                 }
#                 # else:
#                 #     res.status_code = status.HTTP_400_BAD_REQUEST
#                 #     res.data = {
#                 #         'data': [],
#                 #         'status': status.HTTP_400_BAD_REQUEST,
#                 #         'message': 'request failed',
#                 #     }
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'invalid services id',
#                 }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
    
# class ViewServices(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ViewServicesSerializer
#     def get(self, request, page, format=None, *args, **kwargs):
#         user = request.user
#         limit = 10
#         offset = int((page - 1) * limit)
#         res =  Response()
#         if (str(user.department) == 'director'):
#             try:
#                 # marketplace = Marketplace.objects.select_related().filter(visibility=True).values('id','marketplace','service').filter(visibility=True)[offset : offset + limit]
#                 marketplace = Marketplace.objects.select_related().filter(visibility=True, service__isnull=False).values('id','marketplace','service')[offset : offset + limit]
#                 print('marketplace',marketplace)
#             except:
#                 # marketplace = Marketplace.objects.filter(pk__in=[])
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data':  {'data': [], 'total_pages': 1, "current_page": page},
#                     'status': status.HTTP_200_OK,
#                     'message': 'no data found',
#                 }
#                 return res

#             if marketplace.exists():
#                 ser = []

#                 # print(marketplace)

#                 for m in marketplace:
#                     # print(m)
#                     try:
#                         service = Services.objects.get(id = m['service'], visibility=True)
#                         print(service)
#                     except:
#                         service = Services.objects.filter(pk__in=[])
#                         # res.status_code = status.HTTP_200_OK
#                         # res.data = {
#                             # 'data':  {'data': [], 'total_pages': 1, "current_page": page},
#                             # 'status': status.HTTP_200_OK,
#                             # 'message': 'no data found',
#                         # }
#                         # return res

#                     if service:
#                         ser.append({'service_id': m['service'], 'service_name': service.service_name, 'marketplace_id': m['id'], 'marketplace': m['marketplace']})
                
#                 page_count = []
#                 pagecount = Marketplace.objects.all()
#                 for p in pagecount:
#                     page_count.append(p.service.all())

#                 # pagecount = math.ceil(Marketplace.objects.select_related().filter(visibility=True).values('id','marketplace','service', 'visibility').filter(visibility=True).count()/limit)
#                 pagecount = math.ceil(Marketplace.objects.select_related().filter(visibility=True, service__isnull=False).values('id','marketplace','service', 'visibility').count()/limit)

#                 # print(Marketplace.objects.select_related().filter(visibility=True, service__isnull=False).values('id','marketplace','service', 'visibility'))

#                 serializer = ViewServicesSerializer(data=ser, many=True)
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'data':  {'data': serializer.data, 'total_pages': pagecount, "current_page": page},
#                         'status': status.HTTP_200_OK,
#                         'message': 'request successful',
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': {'data': [], 'total_pages': 1, "current_page": page},
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                     }
#             else:
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': {'data': [], 'total_pages': 1, "current_page": page},
#                     'status': status.HTTP_200_OK,
#                     'message': 'no data found',
#                 }
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_401_UNAUTHORIZED,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
    
# class SearchService(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ViewServicesSerializer
#     def get(self, request, searchAtr, id, format=None, *args, **kwargs):
#         user = request.user
#         res =  Response()
#         if (str(user.department) == 'director'):

#             if searchAtr == 'service':
#                 name = id.replace('_',' ')
#                 marketplace = Marketplace.objects.select_related().filter(service__service_name__contains = name, visibility=True).values('id','marketplace','service').filter(visibility=True)
#             elif searchAtr == 'marketplace':
#                 name = id.replace('_',' ')
#                 marketplace = Marketplace.objects.select_related().filter(marketplace__contains = name, visibility=True).values('id','marketplace','service').filter(visibility=True)
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'message': 'invalid search term',
#                     'status': status.HTTP_400_BAD_REQUEST
#                 }
#                 return res



#             # try:
#             #     marketplace = Marketplace.objects.select_related().filter(visibility=True).values('id','marketplace','service').filter(visibility=True)
#             # except:
#             #     # marketplace = Marketplace.objects.filter(pk__in=[])
#             #     res.status_code = status.HTTP_200_OK
#             #     res.data = {
#             #         'data':  [],
#             #         'status': status.HTTP_200_OK,
#             #         'message': 'no data found',
#             #     }
#             #     return res

#             if marketplace.exists():
#                 ser = []

#                 for m in marketplace:
#                     # print(m['service'])
#                     try:
#                         service = Services.objects.get(id = m['service'], visibility=True)
#                     except:
#                         service = Services.objects.filter(pk__in=[])
#                         # res.status_code = status.HTTP_200_OK
#                         # res.data = {
#                             # 'data':  {'data': [], 'total_pages': 1, "current_page": page},
#                             # 'status': status.HTTP_200_OK,
#                             # 'message': 'no data found',
#                         # }
#                         # return res

#                     if service:
#                         ser.append({'service_id': m['service'], 'service_name': service.service_name, 'marketplace_id': m['id'], 'marketplace': m['marketplace']})
                
#                 # page_count = []
#                 # pagecount = Marketplace.objects.all()
#                 # for p in pagecount:
#                 #     page_count.append(p.service.all())

#                 # pagecount = math.ceil(Marketplace.objects.select_related().filter(visibility=True).values('id','marketplace','service', 'visibility').filter(visibility=True).count()/limit)

#                 # print(Marketplace.objects.select_related().filter(visibility=True).values('id','marketplace','service', 'visibility'))

#                 serializer = ViewServicesSerializer(data=ser, many=True)
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'data':  serializer.data,
#                         'status': status.HTTP_200_OK,
#                         'message': 'request successful',
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': [],
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                     }
#             else:
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_200_OK,
#                     'message': 'no data found',
#                 }
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_401_UNAUTHORIZED,
#                 'message': 'you are not authorized for this action',
#             }
#         return res




# class ViewCommercials(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CommercialsSerializer
#     def get(self, request, id ,format=None, *args, **kwargs):
#         user = request.user
#         res = Response()
#         if (str(user.department) == 'director'):
#             comm = [[{'commercial_id': c.id, 'price': c.price, 'commission': c.commission, 'price_for_mou': c.price_for_mou} for c in s.commercials.all()] for s in Services.objects.filter(id = id)]
#             # for c in comm:
#             #     print(c)
#             if comm:
#                 serializer = CommercialsSerializer(data=comm[0], many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'data': serializer.data,
#                     'status': status.HTTP_200_OK,
#                     'message': 'request successful',
#                 }                
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'no data found',
#                 }

#             # print(comm)


#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res
    
# class DeleteCommercials(GenericAPIView):
#     serializer_class = CommercialsSerializer
#     permission_classes = [IsAuthenticated]
#     def delete(self, request, service_id ,commercial_id, format=None, *args, **kwargs):
#         res = Response()
#         user = request.user
#         if (str(user.department) == 'director'):
#             try:
#                 serv = Services.objects.get(id = service_id ,commercials__id = commercial_id)
#             except:
#                 serv = False
#             # print('serv',serv.commercials.all())
#             if serv:
#                 for s in serv.commercials.all():
#                     if s.id == commercial_id:
#                         # print(s,'this wokring')
#                         s.delete()
#                         res.status_code = status.HTTP_200_OK
#                         res.data = {
#                             'data': [],
#                             'status': status.HTTP_200_OK,
#                             'message': 'commercial deleted',
#                         }
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'no data found',
#             }
        
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized for this action',
#             }
#         return res


        
#         # serv = Services.objects.get()
#         # for s in serv.commercials.all():
#         #     print(s.id, s)
            
#                 # print(s, id, s.id)


class dropdown_employee_status(GenericAPIView):
    serializer_class = dropdown_employee_statusSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        # res = Response()
        if (str(user.department) == 'director'):

            employee_status = Employee_status.objects.values('title','id').distinct()
            # print('employee_status',employee_status)
            if employee_status.exists():
                data =[]
                for d in employee_status:
                    data.append({'employee_status_id': d.get('id'), 'employee_status_name': d.get('title')})

                serializer = dropdown_employee_statusSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no employee_status list found',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res
    

class dropdown_department(GenericAPIView):
    serializer_class = dropdown_departmentSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if (str(user.department) == 'director'):

            department = Drp_Program.objects.values('department').distinct()
            print('department',department)
            if department.exists():
                data =[]
                for d in department:
                    data.append({'department_id': d.get('department'), 'department_name': Department.objects.get(id=d.get('department')).title})

                serializer = dropdown_departmentSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'data': serializer.data,
                    'status': status.HTTP_200_OK,
                    'message': 'request successful',
                }                    
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'no department list found',
                }


        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'data': [],
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'you are not authorized for this action',
            }
        return res








class dropdown_designation(GenericAPIView):
    serializer_class = dropdown_designationSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if (str(user.department) == 'director'):
            # print(user.designation)

            designation = Drp_Program.objects.filter(department = id).values('designation').distinct()
            # print(designation)
            if designation.exists():
                data = []
                for d in designation:
                    data.append({'designation_id': d.get('designation'), 'designation_name': Designation.objects.get(id=d.get('designation')).title})

                serializer = dropdown_designationSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'data': serializer.data,
                    'status': status.HTTP_200_OK,
                    'message': 'request successful',
                }                    
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'no designation list found',
                }


        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'data': [],
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'you are not authorized for this action',
            }
        return res
    



class dropdown_program(GenericAPIView):
    serializer_class = dropdown_programSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if (str(user.department) == 'director'):
            program = Drp_Program.objects.filter(designation = id).values('program').distinct()
            print(program)
            if program.exists():
                data = []
                for d in program:
                    if d.get('program') == None:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'data': [],
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'invalid designation id',
                        }
                        res = resFun(status.HTTP_200_OK,'invalid designation id',[])

                        return res                           
                    else:
                        data.append({'program_id': d.get('program'), 'program_name': Program.objects.get(id = d.get('program')).title})


                serializer = dropdown_programSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)

                res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no program list found',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res

# class ()