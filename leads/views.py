from django.db.models import Q
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


import pandas as pd
import numpy as np
import random

from .serializers import *
from account.models import UserAccount, Drp_Program, Department, Designation, Employee_status, canned_email
from .models import Leads, Remark_history
from dropdown.models import *
from evitamin.models import ev_bank_details
# from account.views import getLeadId
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.http import FileResponse




from .main_functions import getLeadId, getClientId

import math
from datetime import date, datetime, timezone, timedelta



def loginpage(request):
    context = {'text':'something'}
    res = HttpResponse(render(request, 'login.html', context))
    return res


# def getLeadId():
#     date = datetime.now()
#     date = date.strftime('%Y%m%d%H%M%S%f')
#     random_int = random.randint(100,499) + random.randint(100,499)
#     client_id = f'L{str(date) + str(random_int)}'
#     return client_id


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










class uploadBusinessLeads(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = uploadFileSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        if (user.department.title == 'admin' and user.designation.title == 'lead_manager'):
            if request.method == 'POST':
                if request.FILES:
                    file = request.FILES['file']
                    df = pd.read_csv(file, delimiter=',',   header=0)
                    df = pd.DataFrame(df)
                    df = df.astype(object)
                    df.fillna('', inplace=True)
                    # print(df)
                    head_row = df.columns.values
                    h_row = [f.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('__', '_').replace('__', '_').lower() for f in head_row]
                    h_row[h_row.index('requester_name')] = 'client_name'
                    h_row[h_row.index('phone_number')] = 'contact_number'
                    h_row[h_row.index('service_category')] = 'service_category_all'

                    # print('h_row',h_row)

                    db_head_row_all_rw = Leads._meta.get_fields()
                    db_head_row_all = [field.name for field in db_head_row_all_rw]

                    # db_head_row_all_type = [field.get_internal_type() for field in db_head_row_all_rw]

                    # db_head_row_phNum_rw = Contact_number._meta.get_fields()
                    # db_head_row_phNum = [field.name for field in db_head_row_phNum_rw]

                    # db_head_row_emlId_rw = email_ids._meta.get_fields()
                    # db_head_row_emlId = [field.name for field in db_head_row_emlId_rw]

                    list_of_csv = [list(row) for row in df.values]
                    output_data = []

                    ref_id = ''

                    for ls in list_of_csv:
                        dup = False
                        break_out = True
                        dup_data = None

                        ind_contact_number = h_row.index('contact_number')
                        ind_email_id = h_row.index('email_id')


                        dup_contact = str(int(ls[ind_contact_number]) if ls[ind_contact_number] != '' else '')
                        dup_email = str(ls[ind_email_id] if ls[ind_email_id] != '' else '')


                        dup_contact_number = Leads.objects.filter(Q(contact_number = dup_contact) | Q(alternate_contact_number = dup_contact))
                        duplicate_contacts = []
                        if dup_contact_number.exists():
                            for d in dup_contact_number:
                                # duplicate_remarks = Remark_history.objects.filter(client_id = d.id)
                                # duplicate_remarks = [str(d.remark) for d in duplicate_remarks]
                                # duplicate_contacts.append({'client_id': str(d.client_id), 'remarks': duplicate_remarks})
                                
                                duplicate_contacts.append({'client_id': str(d.client_id), 'remarks': [r.remark for r in d.remark.all()]})

                        dup_email_id = Leads.objects.filter(Q(email_id = dup_email) | Q(alternate_email_id = dup_email))
                        duplicate_email = []
                        if dup_email_id:
                            for d in dup_email_id:
                                if len(duplicate_contacts) > 0:
                                    for dt in duplicate_contacts:
                                        if dt['client_id'] == d.client_id:
                                            break
                                else:
                                    print(d.remark.all())
                                    # duplicate_remarks = Remark_history.objects.filter(client_id = d.id)
                                    # duplicate_remarks = [str(d.remark) for d in duplicate_remarks]
                                    # duplicate_email.append({'client_id': str(d.client_id) , 'remarks': duplicate_remarks})

                                    duplicate_contacts.append({'client_id': str(d.client_id), 'remarks': [r.remark for r in d.remark.all()]})


                        if len(duplicate_contacts) > 0 or len(duplicate_email) > 0:
                            dup = True
                            break_out = False
                            error_message = ['already exists']
                            dup_data =  duplicate_contacts + duplicate_email

                        if dup == False:
                            dt = {}
                            client_id = getClientId()
                            leads_instance = Leads()
                            for i in range (len(db_head_row_all)):
                                # service_category = ''
                                if not (db_head_row_all[i] == 'id' or db_head_row_all[i] == 'Client_id') and db_head_row_all[i] in h_row:
                                    ind = h_row.index(db_head_row_all[i])

                                    # print('lsdsd',ls)
                                    # print('lsdsd',h_row)

                                    # if db_head_row_all[i] == 'marketplace':
                                    #     dt[db_head_row_all[i]] = Services_and_Commercials.objects.filter(marketplace__marketplace = ls[ind].lower()).first()

                                    if db_head_row_all[i] == 'service_category_all':
                                        # if ls[h_row.index('sub_program')] == '':
                                        #     print('ls[h_row.index(sub_program)]',ls[h_row.index('sub_program')])

                                        if ls[h_row.index('service_category_all')] == '':
                                            # print(ls[h_row.index('service_category')])
                                            break_out = False
                                            error_message = ['service category can not be blank']
                                            break
                                        elif ls[h_row.index('marketplace')] == '':
                                            break_out = False
                                            error_message = ['marketplace can not be blank']
                                            break
                                        elif ls[h_row.index('program')] == '':
                                            break_out = False
                                            error_message = ['program can not be blank']
                                            break
                                        else:

                                        # dt[db_head_row_all[i]] = 

                                            if ls[h_row.index('sub_program')] != '':
                                                service_commercial = Services_and_Commercials.objects.filter( segment__segment=ls[h_row.index('segment')].lower(), service__service = ls[ind].lower(), marketplace__marketplace=ls[h_row.index('marketplace')].lower(), program__program = ls[h_row.index('program')].lower(), sub_program__sub_program = ls[h_row.index('sub_program')].lower() )
                                                print('service_commercial',service_commercial)
                                            else:
                                                service_commercial = Services_and_Commercials.objects.filter( segment__segment=ls[h_row.index('segment')].lower(), service__service = ls[ind].lower(), marketplace__marketplace=ls[h_row.index('marketplace')].lower(), program__program = ls[h_row.index('program')].lower())
                                                pass

                                            print('service_commercial',service_commercial)


                                            if not service_commercial.exists():
                                                break_out=False
                                                error_message = ['service & commercials not found']
                                                break


                                    elif db_head_row_all[i] == 'request_id':
                                        if ls[ind] != '':
                                            if len(str(ls[ind])) > 0:
                                                dt[db_head_row_all[i]] = ls[ind]
                                        else:
                                            break_out = False
                                            error_message = ['request id can not be blank']
                                            break

                                    elif db_head_row_all[i] == 'status':
                                        dt[db_head_row_all[i]] = 'yet to contact'

                                    else:
                                        if isinstance(ls[ind], str):
                                               dt[db_head_row_all[i]] = ls[ind].lower()
                                        elif isinstance(ls[ind], float):
                                            if ls[ind] != '':
                                                dt[db_head_row_all[i]] = str(ls[ind])
                                            else:
                                                dt[db_head_row_all[i]] = ''
                                        elif isinstance(ls[ind], int):
                                            if ls[ind] != '':
                                                dt[db_head_row_all[i]] = str(ls[ind])
                                            else:
                                                dt[db_head_row_all[i]] = ''
                                        else: 
                                            dt[db_head_row_all[i]] = ls[ind]

                        if break_out:
                            # Status_history.objects.create({'service'})
                            d = [client_id]
                            head_rows = [h for h in h_row]
                            head_rows.insert(0, 'client_id')
                            d = d + ls
                            # head_rows.insert(0, 'status')
                            # d = [str(drp_lead_status.objects.filter(title = 'yet to contact').first().title)] + d
                            output_data.append(dict(zip(head_rows ,d)))

                            dt['client_id'] = str(client_id)
                            # dt['status'] = drp_lead_status.objects.filter(title = 'yet to contact').first()
                            dt['lead_owner'] = request.user
                            
                            Status_history_instance = Status_history.objects.create(**{'status': drp_lead_status.objects.filter(title = 'yet to contact').first(), 'status_date': date.today() ,'updated_by': request.user })

                            # dt['status_history'] = Status_history_instance.id
                            for field_name, value in dt.items():
                                if field_name != 'city':
                                    setattr(leads_instance, field_name, value)
                            leads_instance.save()

                            # print('service_commercial',service_commercial)

                            service_category_instance = Service_category.objects.create(**{'lead_id': getLeadId() ,'service':service_commercial.first()})
                            

                            service_category_instance.status_history_all.add(Status_history_instance)
                            leads_instance.service_category_all.add(service_category_instance.id)

                            # ref_id = Leads.objects.filter(client_id = client_id).values('id').first()
                            # ref_id = ref_id['id']

                            # contact_instance = Contact_number()
                            # dt = {}
                            # for i in range (len(db_head_row_phNum)):
                            #     if not (db_head_row_phNum[i] == 'id' or db_head_row_phNum[i] == 'client_id'):
                            #         ind = h_row.index(db_head_row_phNum[i])
                            #         dt[db_head_row_phNum[i]] = str(int(ls[ind]))

                            # dt['client_id'] = leads_instance
                            # for field_name, value in dt.items():
                            #     setattr(contact_instance, field_name, value)
                            # contact_instance.save()

                            # email_instance = email_ids()
                            # dt = {}
                            # for i in range (len(db_head_row_emlId)):
                            #     if not (db_head_row_emlId[i] == 'id' or db_head_row_emlId[i] == 'client_id'):
                            #         ind = h_row.index(db_head_row_emlId[i])
                            #         dt[db_head_row_emlId[i]] = str(ls[ind])

                            # dt['client_id'] = leads_instance
                            # for field_name, value in dt.items():
                            #     setattr(email_instance, field_name, value)
                            # email_instance.save()

                            

                            # service_instance = Service_category() 
                            # dt = {'service': service_category if service_category else None  ,'client_id': leads_instance, 'status': drp_lead_status.objects.filter(title = 'yet to contact').first() }
                            # for i in range (len(db_head_row_emlId)):
                            #     if not (db_head_row_emlId[i] == 'id' or db_head_row_emlId[i] == 'client_id'):
                            #         ind = h_row.index(db_head_row_emlId[i])
                            #         dt[db_head_row_emlId[i]] = str(ls[ind])

                            # dt['client_id'] = leads_instance
                            # for field_name, value in dt.items():
                            #     setattr(service_instance, field_name, value)
                            # service_instance.save()

                        else:
                            d = ['not generated']
                            head_rows = [h for h in h_row]
                            if dup_data:
                                head_rows.insert(0, 'duplicate_leads')
                                data = [dup_data] + ls
                            else:
                                data = ls
                            head_rows.insert(0, 'client_id')
                            d = d + data
                            head_rows.insert(0, 'error message')
                            d = error_message + d
                            
                            output_data.append(dict(zip(head_rows ,d)))

                    res =  Response()
                    res.status_code = status.HTTP_201_CREATED
                    # res['Access-Control-Allow-Origin'] = '*'
                    # res['Access-Control-Allow-Credentials'] = True
                    res.data = {
                        "status": status.HTTP_201_CREATED,
                        "message": 'all records saved successfully', 
                        "data": output_data
                        }
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
        
        else:
                res = Response()
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    "status" : status.HTTP_400_BAD_REQUEST,
                    "message": "you are not authorized for this action",
                    "data": []
                }

        return res





class createLeadManual(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = createLeadManualSerializer
    def post(self, request, format=None, *args, **kwargs):
    
        serializer = createLeadManualSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            try:
                if serializer.save():
                    serializer.instance.lead_owner = request.user
                    serializer.instance.save()

                    for s in serializer.validated_data['service']:
                        for m in serializer.validated_data['marketplace']:
                            services_and_commercials = Services_and_Commercials.objects.filter(segment__id=serializer.validated_data['segment'], service__id=s, marketplace__id=m, visibility=True, program__program='regular')
                            # print(s,m, services_and_commercials)
                            service_instance = Service_category.objects.create(**{'lead_id': getLeadId(),'service': services_and_commercials.first() })
                            status_history_all = Status_history.objects.create(**{'status': drp_lead_status.objects.get(title='yet to contact'), 'updated_by': request.user })
                            service_instance.status_history_all.add(status_history_all)
                            serializer.instance.service_category_all.add(service_instance)
                
                    res = resFun(status.HTTP_200_OK, 'lead registered successfully', [])
                    return res
            except:
                return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])





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




def viewLeadFun(leadsData, department):
    data = []
    for sd in leadsData:
        tat = Turn_Arround_Time.objects.all().first()
        today = datetime.now()
        upload_date = datetime.strptime(str(sd.upload_date),"%Y-%m-%d %H:%M:%S.%f%z")
        upload_date = upload_date.replace(tzinfo=None)
        # upload_date = upload_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        deadline = (today - upload_date).total_seconds()
        deadline = (math.ceil((int(tat.duration_in_hrs) - math.floor(int(deadline // (3600)))) / 24) -1 )
        # print('deadline', deadline)

        if department == 'admin':
            data.append({
                'id' : sd.id , 
                'client_id' : sd.client_id , 
                'client_name': sd.client_name, 
                'contact_number': sd.contact_number,
                'alternate_contact_number': sd.alternate_contact_number if sd.alternate_contact_number else '-',
                'email_id': sd.email_id,
                'alternate_email_id': sd.alternate_email_id if sd.alternate_email_id else '-',
                # 'service_category': sd.service_category.service_name, 
                # 'assigned_to': sd.service_category_all(), 
                # 'status': sd.status.title if sd.status else '-', 
                'upload_date': upload_date , 
                'deadline': deadline,
                'gst': sd.gst if sd.gst else '-',
                # 'lead_manager': sd.lead_manager.name if sd.lead_manager else '-',
                'seller_address': sd.seller_address if sd.seller_address else '-',
                'services': [s.service.service.service for s in sd.service_category_all.all() if s.service ],
                # "assigned_status": ,
                # "associate" : sd.associate.name if sd.associate else '-',
                "service_category" : [
                    { 
                        "lead_id": s.lead_id,
                        'service': s.service.service.service if s.service else '-',
                        'marketplace': s.service.marketplace.marketplace if s.service else '-',
                        'program': s.service.program.program if s.service else '-',
                        'sub_program': s.service.sub_program.sub_program if s.service.sub_program else '-' if s.service else '-',
                        "associate": {"id": s.associate.id if s.associate else None , "name": s.associate.name if s.associate else "-" }, 
                        "assigned_status": 'assigned' if s.associate != None else "not assigned", 
                        "payment_approval": s.payment_approval if s.payment_approval != None else "-", 
                        "mou_approval": s.mou_approval if s.mou_approval != None else "-",
                        "commercial_approval": {"status": s.commercial_approval.status, "commercial": s.commercial_approval.commercial} if s.commercial_approval != None else {"status": '-', "commercial": '-'},
                        "commercial": s.pricing.commercials if s.pricing else "-",
                        "status": s.status_history_all.all().order_by('-id').first().status.title if s.status_history_all.all().exists() else "-",
                        "follow_up": [ {
                            'date':f.date if f.date else '-', 
                            'time': f.time if f.time else '-', 
                            'notes': f.notes if f.notes else '-', 
                            'created_by': f.created_by.name if f.created_by else '-' } for f in s.followup.all()],
                        } for s in sd.service_category_all.all()] if sd.service_category_all else [],
                # "commercials" : sd.commercials.price_for_mou if sd.commercials else '-',
                # "status" : sd.status.title if sd.status else '-',
                "client_turnover" : sd.client_turnover.id if sd.client_turnover else None,
                "business_name" : sd.business_name if sd.business_name else '-',
                "business_type" : sd.business_type.title if sd.business_type else '-',
                "business_category" : sd.business_category.id if sd.business_category else None,
                "firm_type" : sd.firm_type.title if sd.firm_type else '-',
                "contact_preferences" : sd.contact_preferences.title if sd.contact_preferences else '-',
                "request_id": sd.request_id if sd.request_id else '-',
                "provider_id": sd.provider_id if sd.provider_id else '-',
                "requester_id": sd.requester_id if sd.requester_id else '-',
                "requester_location": sd.requester_location if sd.requester_location else '-',
                "requester_sell_in_country": sd.requester_sell_in_country if sd.requester_sell_in_country else '-',
                "service_requester_type": sd.service_requester_type if sd.service_requester_type else '-',
                "lead_owner": sd.lead_owner.name if sd.lead_owner else '-',
                # "followup" : sd.followup.followup_date if sd.followup else '-',
                # "country" : sd.country.title if sd.country else '-',
                # "state" : sd.state.title if sd.state else '-',
                # "city" : sd.city.title if sd.city else '-'
                "hot_lead" : sd.hot_lead
                })

        elif department == 'business_development':
            for s in sd.service_category_all.all():
                data.append({
                    'id' : sd.id , 
                    'client_id' : sd.client_id , 
                    'client_name': sd.client_name, 
                    'contact_number': sd.contact_number,
                    'alternate_contact_number': sd.alternate_contact_number if sd.alternate_contact_number else '-',
                    'email_id': sd.email_id,
                    'alternate_email_id': sd.alternate_email_id if sd.alternate_email_id else '-',
                    'gst': sd.gst if sd.gst else '-',
                    'seller_address': sd.seller_address if sd.seller_address else '-',
                    # 'service_category': sd.service_category.service_name, 
                    # 'assigned_to': sd.service_category_all(), 
                    # 'status': sd.status.title if sd.status else '-', 
                    'upload_date': upload_date , 
                    'deadline': deadline,
                    # "assigned_status": ,
                    # "associate" : sd.associate.name if sd.associate else '-',
                    # "service_category" : [
                        # { 
                            "lead_id": s.lead_id,
                            'service': s.service.service.service if s.service else '-', 
                            "associate": {"id": s.associate.id if s.associate else None , "name": s.associate.name if s.associate else "-" }, 
                            "assigned_status": 'assigned' if s.associate != None else "not assigned", 
                            "payment_approval": s.payment_approval if s.payment_approval != None else "-", 
                            # "mou_approval": s.mou_approval if s.mou_approval != None else "-",
                            "commercial_approval": {"status": s.commercial_approval.status, "commercial": s.commercial_approval.commercial} if s.commercial_approval != None else {"status": '-', "commercial": '-'},
                            "commercial": s.pricing.commercials if s.pricing else "-",
                            "status": s.status_history_all.all().order_by('-id').first().status.title if s.status_history_all.all().exists() else "-",
                            "follow_up": [ {
                                'date':f.date if f.date else '-', 
                                'time': f.time if f.time else '-', 
                                'notes': f.notes if f.notes else '-', 
                                'created_by': f.created_by.name if f.created_by else '-' } for f in s.followup.all()],
                            # } for s in sd.service_category_all.all()] if sd.service_category_all else [],
                    # "commercials" : sd.commercials.price_for_mou if sd.commercials else '-',
                    # "status" : sd.status.title if sd.status else '-',
                    # "client_turnover" : sd.client_turnover.title if sd.client_turnover else '-',
                    "client_turnover" : sd.client_turnover.id if sd.client_turnover else None,
                    "business_name" : sd.business_name if sd.business_name else '-',
                    "business_type" : sd.business_type.title if sd.business_type else '-',
                    "business_category" : sd.business_category.id if sd.business_category else None,
                    # "business_category" : sd.business_category.title if sd.business_category else '-',
                    "firm_type" : sd.firm_type.title if sd.firm_type else '-',
                    "contact_preferences" : sd.contact_preferences.title if sd.contact_preferences else '-',
                    "request_id": sd.request_id if sd.request_id else '-',
                    "provider_id": sd.provider_id if sd.provider_id else '-',
                    "requester_id": sd.requester_id if sd.requester_id else '-',
                    "requester_location": sd.requester_location if sd.requester_location else '-',
                    "requester_sell_in_country": sd.requester_sell_in_country if sd.requester_sell_in_country else '-',
                    "service_requester_type": sd.service_requester_type if sd.service_requester_type else '-',
                    "lead_manager": { 'id': sd.lead_owner.name, 'name': sd.lead_owner.name} if sd.lead_owner else { 'id': None , 'name': '-' },
                    # "followup" : sd.followup.followup_date if sd.followup else '-',
                    # "country" : sd.country.title if sd.country else '-',
                    # "state" : sd.state.title if sd.state else '-',
                    # "city" : sd.city.title if sd.city else '-'
                    "hot_lead" : sd.hot_lead
                    })
        
        # print([[f.followup_time for f in s.followup.all()] for s in sd.service_category_all.all()][0])

    return data


def viewLeadBd_tl(user, offset, limit, page, client_id, department):
    if user.segment == None:
        return resFun(status.HTTP_400_BAD_REQUEST, 'contact user manager to assign you a segment', [])
    
    if len(user.service.all()) == 0:
        return resFun(status.HTTP_400_BAD_REQUEST, 'contact user manager to assign you atleast one services', [])
    
    if len(user.marketplace.all()) == 0:
        return resFun(status.HTTP_400_BAD_REQUEST, 'contact user manager to assign you atleast one marketplace', [])
    
    if len(user.program.all()) == 0:
        return resFun(status.HTTP_400_BAD_REQUEST, 'contact user manager to assign you atleast one program', [])
    
    if offset!=None:
        if len(user.sub_program.all()) == 0:

            leadsData = Leads.objects.select_related().filter(
                service_category_all__service__segment__segment= user.segment, 
                service_category_all__service__service__in= user.service.all(), 
                service_category_all__service__marketplace__in= user.marketplace.all(),  
                service_category_all__service__program__in= user.program.all(),
                visibility = True
                ).all()[offset : offset + limit]
        elif len(user.sub_program.all()) > 0:
            leadsData = Leads.objects.select_related().filter(
                service_category_all__service__segment__segment= user.segment, 
                service_category_all__service__service__in= user.service.all(), 
                service_category_all__service__marketplace__in= user.marketplace.all(),
                service_category_all__service__program__in= user.program.all(),
                service_category_all__service__sub_program__in= user.sub_program.all(),  
                visibility = True
                ).all()[offset : offset + limit]
        
        print(leadsData)
        print('leadsData',leadsData)

    else:
        if len(user.sub_program.all()) == 0:
            leadsData = Leads.objects.select_related().filter(client_id=client_id,
                service_category_all__service__segment__segment= user.segment, 
                service_category_all__service__service__in= user.service.all(), 
                service_category_all__service__marketplace__in= user.marketplace.all(),  
                service_category_all__service__program__in= user.program.all(),
                visibility = True
                ).all()
        elif len(user.sub_program.all()) > 0:
            leadsData = Leads.objects.select_related().filter(client_id=client_id,
                service_category_all__service__segment__segment= user.segment, 
                service_category_all__service__service__in= user.service.all(), 
                service_category_all__service__marketplace__in= user.marketplace.all(),
                service_category_all__service__program__in= user.program.all(),
                service_category_all__service__sub_program__in= user.sub_program.all(),  
                visibility = True
                ).all()
    
    print('leadsData',leadsData)
    data = viewLeadFun(leadsData, department)
    # print('data')
    
    if len(data) > 0:

        if offset!=None:
            if len(user.sub_program.all()) == 0:
                pagecount = math.ceil(Leads.objects.filter(
                    service_category_all__service__segment__segment= user.segment, 
                    service_category_all__service__service__in= user.service.all(), 
                    service_category_all__service__marketplace__in= user.marketplace.all(),  
                    service_category_all__service__program__in= user.program.all(),
                    visibility = True).count()/limit)
            elif len(user.sub_program.all()) > 0:
                pagecount = math.ceil(Leads.objects.filter(
                    service_category_all__service__segment__segment= user.segment, 
                    service_category_all__service__service__in= user.service.all(), 
                    service_category_all__service__marketplace__in= user.marketplace.all(),  
                    service_category_all__service__program__in= user.program.all(),
                    service_category_all__service__sub_program__in= user.sub_program.all(),
                    visibility = True).count()/limit)
                
        # FLATTEN_DATA = []
        

        # for d in data:
        #     ser_len = len(d['service_category'])
        #     if ser_len == 0:
        #         ser_len = 1
        #     for i in range(ser_len):
        #         FLATTEN_DATA.append({

        #             'id' : d['id'],
        #             'client_id' : d['client_id'] , 
        #             'client_name': d['client_name'], 
        #             'contact_number': d['contact_number'],
        #             'alternate_contact_number': d['alternate_contact_number'] if d["alternate_contact_number else '-'"],
        #             'email_id': d['email_id'],
        #             'alternate_email_id': d['alternate_email_id if d['alternate_email_id else '-',
        #             # 'service_category': d['service_category.service_name, 
        #             # 'assigned_to': d['service_category_all(), 
        #             # 'status': d['status.title if d['status else '-', 
        #             'upload_date': upload_date , 
        #             'deadline': deadline,
        #             # "assigned_status": ,
        #             # "associate" : d['associate.name if d['associate else '-',
        #             "service_category" : [
        #                 { 
        #                     'service': s.service.service.service, 
        #                     "associate": {"id": s.associate.id if s.associate else None , "name": s.associate.name if s.associate else "-" }, 
        #                     "assigned_status": 'assigned' if s.associate != None else "not assigned", 
        #                     "payment_approval": s.payment_approval if s.payment_approval != None else "-", 
        #                     "mou_approval": s.mou_approval if s.mou_approval != None else "-",
        #                     "commercial_approval": s.commercial_approval if s.commercial_approval != None else "-",
        #                     "commercial": s.pricing if s.pricing else "-",
        #                     "status": s.status.title if s.status else "-",
        #                     "follow_up": [ {
        #                         'date':f.followup_date if f.followup_date else '-', 
        #                         'time': f.followup_time if f.followup_time else '-', 
        #                         'notes': f.followup_notes if f.followup_notes else '-', 
        #                         'created_by': f.created_by.name if f.created_by else '-' } for f in s.followup.all()],
        #                     } for s in d['service_category_all.all()] if d['service_category_all else [],
        #             # "commercials" : d['commercials.price_for_mou if d['commercials else '-',
        #             # "status" : d['status.title if d['status else '-',
        #             "client_turnover" : d['client_turnover.title if d['client_turnover else '-',
        #             "business_name" : d['business_name if d['business_name else '-',
        #             "business_type" : d['business_type.title if d['business_type else '-',
        #             "business_category" : d['business_category.title if d['business_category else '-',
        #             "firm_type" : d['firm_type.title if d['firm_type else '-',
        #             "contact_preferences" : d['contact_preferences.title if d['contact_preferences else '-',
        #             "followup" : d['followup.followup_date if d['followup else '-',
        #             # "country" : d['country.title if d['country else '-',
        #             # "state" : d['state.title if d['state else '-',
        #             # "city" : d['city.title if d['city else '-'
        #             "hot_lead" : d['hot_lead

        #         })

                
        if department == 'admin':
            serializer = lead_managerBlSerializer_admin(data=data, many=True)
        elif department == 'business_development':
            serializer = lead_managerBlSerializer_bd(data=data, many=True)
    
        serializer.is_valid(raise_exception=True)

        if offset!=None:

            if int(page) <= pagecount:
                res = resFun(status.HTTP_200_OK, 'successful', {'data': serializer.data, 'total_pages': pagecount, "current_page": page})
            else :
                res = resFun(status.HTTP_400_BAD_REQUEST, 'the page is unavailable', {'data': [], 'total_pages': pagecount, "current_page": page} )
        else:
            res = resFun(status.HTTP_200_OK,'successful',serializer.data)

    else:
        if offset!=None:
            res = resFun(status.HTTP_204_NO_CONTENT, 'no data found', {'data': [], 'total_pages': [], "current_page": page} )
        else:
            res = resFun(status.HTTP_204_NO_CONTENT, 'no data found', [] )
    return res



class viewAllLeads(GenericAPIView):
    serializer_class = lead_managerBlSerializer_admin
    permission_classes = [IsAuthenticated]
    def get(self, request, page, format=None, *args, **kwargs):
        user = request.user
        limit = 10
        offset = int((page - 1) * limit)
        data = []
        pagecount = 1

        print(user.department, user.designation)

        if str(user.department) == 'director' or (str(user.department) == 'admin' and str(user.designation) == 'lead_manager'):
            leadsData = Leads.objects.select_related().filter(visibility = True).all()[offset : offset + limit]

            data = viewLeadFun(leadsData, user.department.title)
            
            if len(data) > 0:
                pagecount = math.ceil(Leads.objects.filter(visibility = True).count()/limit)
                serializer = lead_managerBlSerializer_admin(data=data, many=True)
                serializer.is_valid(raise_exception=True)

                if int(page) <= pagecount:
                    res = resFun(status.HTTP_200_OK, 'successful', {'data': serializer.data, 'total_pages': pagecount, "current_page": page})
                else :
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'the page is unavailable', {'data': [], 'total_pages': pagecount, "current_page": page} )
            else:   
                res = resFun(status.HTTP_400_BAD_REQUEST, 'no data found', {'data': [], 'total_pages': [], "current_page": page} )
            return res

        elif user.department.title == 'business_development':

            if user.designation.title == 'team_leader':
            # services_flatten = .values_list('service', flat=True)
                res = viewLeadBd_tl(user,offset,limit,page, None,user.department.title)

            elif user.designation.title == 'team_member':
                res = resFun(status.HTTP_204_NO_CONTENT, 'no data', [])
        
        elif user.department.title == 'accounts' and user.designation.title == 'payment_followup' :
            res = resFun(status.HTTP_204_NO_CONTENT, 'payment followup working', [])

            
        #     product = getProduct(user.id)
        #     # print(product)
        #     data = []
        #     serviceData = service.objects.select_related().filter(service_category = product, client_id__visibility = True)[offset : limit]
        #     for sd in serviceData:
        #         associate = sd.associate_id.name if sd.associate_id != None else 'not assigned'
        #         data.append({'client_id': sd.client_id.client_id, 'requester_name': sd.client_id.requester_name, 'phone_number':  sd.client_id.phone_number, 'email_id': sd.client_id.email_id, 'service_category': sd.service_category, 'associate': associate, 'lead_status': sd.lead_status.title})

        #     if len(data) > 0:
        #         pagecount = math.ceil(service.objects.filter(service_category = product ,client_id__visibility = True).count()/limit)
        #         print('pagecount',pagecount)
        #         serializer = bd_teamLeaderSerializer(data=data, many=True)
        #         serializer.is_valid(raise_exception=True)
        #         if int(page) <= pagecount:
        #             res.status_code = status.HTTP_200_OK
        #             res.data = {
        #                 'status': status.HTTP_200_OK,
        #                 'message': 'successful',
        #                 'data': {'data': serializer.data, 'total_pages': pagecount, "current_page": page}
        #                 }

        #         else :
        #             pagecount = math.ceil(service.objects.filter(service_category = product ,client_id__visibility = True).count()/limit)

        #             res.status_code = status.HTTP_400_BAD_REQUEST
        #             res.data = {
        #                 "status": status.HTTP_400_BAD_REQUEST,
        #                 "message": 'the page is unavailable',
        #                 "data": {'data': [], 'total_pages': pagecount, "current_page": page}
        #                 }
                    
        #     else:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data = {
        #             "status": status.HTTP_400_BAD_REQUEST,
        #             "message": 'no data found',
        #             "data": {'data': [], 'total_pages': pagecount, "current_page": page}
        #             }
        
            # res = resFun(status.HTTP_200_OK, 'request successful', {'data': [], 'total_pages': pagecount, "current_page": page} )
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized to view this data', {'data': [], 'total_pages': pagecount, "current_page": page} )
        return res
    

class viewAllLeadsArchive(GenericAPIView):
    serializer_class = lead_managerBlSerializer_admin
    permission_classes = [IsAuthenticated]
    def get(self, request, page, format=None, *args, **kwargs):
        user = request.user
        limit = 10
        offset = int((page - 1) * limit)
        data = []
        pagecount = 1

        if str(user.department) == 'director' or (str(user.department) == 'admin' and str(user.designation) == 'lead_manager'):
            leadsData = Leads.objects.select_related().filter(visibility = False).all()[offset : offset + limit]

            data = viewLeadFun(leadsData, user.department.title)
            
            if len(data) > 0:
                pagecount = math.ceil(Leads.objects.filter(visibility = False).count()/limit)
                serializer = lead_managerBlSerializer_admin(data=data, many=True)
                serializer.is_valid(raise_exception=True)

                if int(page) <= pagecount:
                    res = resFun(status.HTTP_200_OK, 'successful', {'data': serializer.data, 'total_pages': pagecount, "current_page": page})
                else :
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'the page is unavailable', {'data': [], 'total_pages': pagecount, "current_page": page} )
            else:   
                res = resFun(status.HTTP_204_NO_CONTENT, 'no data found', {'data': [], 'total_pages': [], "current_page": page} )
            return res

        # elif user_role == 'bd_tl':
        #     product = getProduct(user.id)
        #     # print(product)
        #     data = []
        #     serviceData = service.objects.select_related().filter(service_category = product, client_id__visibility = True)[offset : limit]
        #     for sd in serviceData:
        #         associate = sd.associate_id.name if sd.associate_id != None else 'not assigned'
        #         data.append({'client_id': sd.client_id.client_id, 'requester_name': sd.client_id.requester_name, 'phone_number':  sd.client_id.phone_number, 'email_id': sd.client_id.email_id, 'service_category': sd.service_category, 'associate': associate, 'lead_status': sd.lead_status.title})

        #     if len(data) > 0:
        #         pagecount = math.ceil(service.objects.filter(service_category = product ,client_id__visibility = True).count()/limit)
        #         print('pagecount',pagecount)
        #         serializer = bd_teamLeaderSerializer(data=data, many=True)
        #         serializer.is_valid(raise_exception=True)
        #         if int(page) <= pagecount:
        #             res.status_code = status.HTTP_200_OK
        #             res.data = {
        #                 'status': status.HTTP_200_OK,
        #                 'message': 'successful',
        #                 'data': {'data': serializer.data, 'total_pages': pagecount, "current_page": page}
        #                 }

        #         else :
        #             pagecount = math.ceil(service.objects.filter(service_category = product ,client_id__visibility = True).count()/limit)

        #             res.status_code = status.HTTP_400_BAD_REQUEST
        #             res.data = {
        #                 "status": status.HTTP_400_BAD_REQUEST,
        #                 "message": 'the page is unavailable',
        #                 "data": {'data': [], 'total_pages': pagecount, "current_page": page}
        #                 }
                    
        #     else:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data = {
        #             "status": status.HTTP_400_BAD_REQUEST,
        #             "message": 'no data found',
        #             "data": {'data': [], 'total_pages': pagecount, "current_page": page}
        #             }
        
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized to view this data', {'data': [], 'total_pages': pagecount, "current_page": page} )
        return res


class viewAllLeadsSearchArchive(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = lead_managerBlSerializer_admin
    def get(self, request, client_id, format=None, *args, **kwargs):
        res = viewLeadSeachFun(request, client_id, False)
        return res
    

def archiveRestoreFun(request, id, visibility, message):
        user = request.user
        data = []
        try:
            if str(user.department) == 'director' or (str(user.department) == 'admin' and str(user.designation) == 'lead_manager'):
                lead = Leads.objects.get(id=id,visibility=visibility)
                lead.visibility = False if visibility == True else True
                lead.save()
                res = resFun(status.HTTP_200_OK, message, [])
                # pass
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action',[])
        except:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])
        return res
        

class archive_lead(GenericAPIView):
    serializer_class = lead_managerBlSerializer_admin
    permission_classes = [IsAuthenticated]
    def delete(self, request, id, format=None, *args, **kwargs):
        res = archiveRestoreFun(request, id, True, 'lead archived successfully')
        return res


class restore_lead(GenericAPIView):
    serializer_class = lead_managerBlSerializer_admin
    permission_classes = [IsAuthenticated]
    def put(self, request, id, format=None, *args, **kwargs):
        res = archiveRestoreFun(request, id, False, 'lead restored successfully')
        return res
    

class UpdateLeads(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateLeadsSerializer_TL
    def put(self, request, client_id, format=None, *args, **kwargs):

        try:
            lead_instance = Leads.objects.get(client_id=client_id)
        except:
            lead_instance = None

        if lead_instance != None:
            if request.user.department.title == 'admin' and request.user.designation.title == 'lead_manager':

                serializer = UpdateLeadsSerializer_ADMIN(lead_instance, data=request.data, partial=True)
                # pass
            elif request.user.department.title == 'business_development':

                if request.user.designation.title == 'team_leader':
                    serializer = UpdateLeadsSerializer_TL(lead_instance, data=request.data, partial=True)
                elif request.user.designation.title == 'team_member':
                    serializer = UpdateLeadsSerializer_TM(lead_instance, data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            print('serializer.data', serializer.validated_data)

            if(request.user.department.title == 'business_development' and request.user.designation.title) == 'team_leader':
                service_category_instance = serializer.instance.service_category_all.get(lead_id=serializer.validated_data['lead_id'])
                if serializer.validated_data.get('associate'):
                    service_category_instance.associate = serializer.validated_data['associate']
                if serializer.validated_data.get('status'):
                    service_category_instance.status = serializer.validated_data['status']
                if serializer.validated_data.get('commercial_id'):
                    service_category_instance.pricing = serializer.validated_data['commercial_id']
                service_category_instance.save()
            
            res = resFun(status.HTTP_200_OK, 'request successful', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'invalid client id', [])

        return res
            

                



# class viewLeadsAllIdentifiers(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = View_All_Leads
#     def get(self, request, client_id ,format=None, *args, **kwargs):
#         user = request.user
#         res = Response()
#         if (str(user.department) == 'director'):

#             leads = Leads.objects.select_related().filter(client_id=client_id, visibility =True)
#             if leads.exists():
#                 # print('leads', leads)
#                 leads_val = leads.values().first()
#                 leads = leads.first()

#                 leads_val["associate"] = leads.associate.name if leads.associate else '-'
#                 leads_val["service_category"] = leads.service_category.service_name if leads.service_category else '-'
#                 leads_val["commercials"] = leads.commercials.price_for_mou if leads.commercials else '-'
#                 leads_val["status"] = leads.status.title if leads.status else '-'
#                 leads_val["client_turnover"] = leads.client_turnover.title if leads.client_turnover else '-'
#                 leads_val["business_type"] = leads.business_type.title if leads.business_type else '-'
#                 leads_val["business_category"] = leads.business_category.title if leads.business_category else '-'
#                 leads_val["firm_type"] = leads.firm_type.title if leads.firm_type else '-'
#                 leads_val["contact_preferences"] = leads.contact_preferences.title if leads.contact_preferences else '-'
#                 leads_val["followup"] = leads.followup.followup_date if leads.followup else '-'
#                 leads_val["country"] = leads.country.title if leads.country else '-'
#                 leads_val["state"] = leads.state.title if leads.state else '-'
#                 leads_val["city"] = leads.city.title if leads.city else '-'

#                 # print(leads_val)

#                 serializer = View_All_Leads(data=leads_val)

#                 if serializer.is_valid(raise_exception=True):

#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         "status": status.HTTP_200_OK,
#                         'data': serializer.data,
#                         'message': 'request successful'
#                     }
#                 else:
#                     res.status_code = status.HTTP_404_NOT_FOUND
#                     res.data = {
#                         "status": status.HTTP_404_NOT_FOUND,
#                         'data': [],
#                         'message': 'request failed'
#                     }
#             else:
#                 res.status_code = status.HTTP_404_NOT_FOUND
#                 res.data = {
#                     "status": status.HTTP_404_NOT_FOUND,
#                     'data': [],
#                     'message': 'invalid client_id'
#                 }

#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 "status": status.HTTP_404_NOT_FOUND,
#                 'data': [],
#                 'message': 'you are not authorized for this actions'
#             }
#         return res
    


def viewLeadSeachFun(request, client_id, visibility):
        user = request.user
        if (str(user.department) == 'director') or (str(user.department) == 'admin' and str(user.designation) == 'lead_manager'):
            data = []
            leads = Leads.objects.select_related().filter(client_id = client_id, visibility = visibility)
            if leads.exists():

                data = viewLeadFun(leads, user.department.title)

                serializer = lead_managerBlSerializer_admin(data=data, many=True)
                serializer.is_valid(raise_exception=True)

                res = resFun(status.HTTP_200_OK,'successful',serializer.data)
            else:
                res = resFun(status.HTTP_403_FORBIDDEN,'invalid client id',[])

        elif user.department.title == 'business_development' and user.designation.title == 'team_leader':
            print('user',user)
            leads = Leads.objects.select_related().filter(client_id = client_id, visibility = visibility)
            
            if leads.exists():
                res = viewLeadBd_tl(user,None,None,None, client_id, user.department.title)
            
        #     product = getProduct(user.id)
        #     data = []
        #     serviceData = service.objects.select_related().filter(client_id__client_id = client_id, service_category = product, client_id__visibility=True)
        #     if serviceData:
        #         for sd in serviceData:
        #             associate = sd.associate_id.name if sd.associate_id != None else '-'
        #             data.append({'client_id': sd.client_id.client_id, 'requester_name': sd.client_id.requester_name, 'phone_number':  sd.client_id.phone_number, 'email_id': sd.client_id.email_id, 'service_category': sd.service_category, 'associate': associate, 'lead_status': sd.lead_status.title})

        #         serializer = BusinessDevelopmentLeadSerializer(data=data, many=True)
        #         serializer.is_valid(raise_exception=True)
                    # res = resFun(status.HTTP_200_OK, 'successful', serializer.data)
        #     else: 
                # res = resFun(status.HTTP_403_FORBIDDEN, 'invalid lead id', [])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized to view this data',[])
        return res




class viewAllLeadsSearch(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = lead_managerBlSerializer_admin
    def get(self, request, client_id, format=None, *args, **kwargs):
        res = viewLeadSeachFun(request, client_id, True)
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
    


class ViewSegment(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSegmentSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director') or (str(user.department) == 'admin') or user.department.title == 'business_development':
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
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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
    def delete(self, request,id, format=None, *args, **kwargs):
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
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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



class ViewService(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director') or (str(user.department) == 'admin') or user.department.title == 'business_development':
            try:
                service = Service.objects.filter(visibility=True)
            except:
                service = Service.objects.filter(pk__in=[])

            if service.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(service.values()))
            else:
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])

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
    def delete(self, request,id, format=None, *args, **kwargs):
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
    


class ViewArchiveService(GenericAPIView):
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
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])

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
    

class ViewMarketplace(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MarketplaceSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director') or (str(user.department) == 'admin') or user.department.title == 'business_development':
            try:
                marketplace = Marketplace.objects.filter(visibility=True)
            except:
                marketplace = Marketplace.objects.filter(pk__in=[])

            if marketplace.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(marketplace.values()))
            else:
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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
    def delete(self, request,id, format=None, *args, **kwargs):
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
    


class ViewArchiveMarketplace(GenericAPIView):
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
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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
    




class ViewProgram(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        if (str(user.department) == 'director') or (str(user.department) == 'admin') or user.department.title == 'business_development':
            try:
                marketplace = Program.objects.filter(visibility=True)
            except:
                marketplace = Program.objects.filter(pk__in=[])

            print('marketplace',marketplace)

            if marketplace.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(marketplace.values()))
            else:
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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
    def delete(self, request,id, format=None, *args, **kwargs):
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



class ViewArchiveProgram(GenericAPIView):
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
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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
        if (str(user.department) == 'director') or (str(user.department) == 'admin')or user.department.title == 'business_development':
            try:
                sub_program = Sub_Program.objects.filter(visibility=True)
            except:
                sub_program = Sub_Program.objects.filter(pk__in=[])
            if sub_program.exists():
                res = resFun(status.HTTP_200_OK, 'request successful', list(sub_program.values()))
            else:
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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
    def delete(self, request,id, format=None, *args, **kwargs):
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
                res = resFun(status.HTTP_204_NO_CONTENT, 'data not found', [])
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


class assignAssociate(GenericAPIView):
    serializer_class = assignAssociateSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None, *args, **kwargs):
        print('request.data',request.data)

        # obj_user = Leads.objects.filter(emp__id = request.user.id, visibility=True).first()
        # user_role = obj_user.user_role
        # print('user_role', user_role)
        user = request.user

        res = Response()
        if user.department.title == 'director' or (user.department.title == 'admin' and user.designation.title == 'lead_manager') or (user.department.title == 'business_development' and user.designation.title == 'team_leader'):

            user_id = request.data.get('user_id')
            lead_id = request.data.get('lead_id')

            userData = UserAccount.objects.get(id = user_id, visibility=True)
            print('userData',userData)

            if isinstance(lead_id, list):
                for ld in lead_id:

                    data = Service_category.objects.get(lead_id= ld)
                    if data: 
                        serializer = assignAssociateSerializer(data, data={'associate': user_id}, partial=True)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            lead_status_instance = drp_lead_status.objects.get(title = 'pitch in progress')
                            status_history_instance = Status_history.objects.create(**{'status': lead_status_instance, 'updated_by': request.user})
                            # lead_instance = Leads.objects.get(service_category_all__id=ld)
                            data.status_history_all.add(status_history_instance)
                            res = resFun(status.HTTP_201_CREATED,'associate assigned', [])
                        else:
                            res = resFun(status.HTTP_400_BAD_REQUEST,'request failed', [])
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST,'invalid lead id', [])
                    
                    # return res
                    # d = cursor.execute(f"UPDATE api_business_leads_service set associate_id = '{assoc_employee_id}', team_leader_id = '{team_leader_id}' WHERE client_id = '{ld}'")
            else: 

                data = Service_category.objects.get(lead_id= lead_id)
                if data: 
                    serializer = assignAssociateSerializer(data, data={'associate': user_id}, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        lead_status_instance = drp_lead_status.objects.get(title = 'pitch in progress')
                        status_history_instance = Status_history.objects.create(**{'status': lead_status_instance, 'updated_by': request.user})
                        # lead_instance = Leads.objects.get(service_category_all__id=lead_id)
                        data.status_history_all.add(status_history_instance)
                        res = resFun(status.HTTP_201_CREATED,'associate assigned', [])
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST,'request failed', [])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'invalid lead id', [])




                # data = service.objects.filter(client_id__client_id = client_id, client_id__visibility=True).first()
                # if data:
                    # serialize = assignAssociateSerializer(data, data=req_data, partial=True)
                    # serialize.is_valid(raise_exception=True)
                    # serialize.save()
                    # lead_status_instance = lead_status.objects.get(title = 'pitch in progress')
                    # lead_status_record.objects.create(**{'client_id': data.client_id, 'status': lead_status_instance})

                    # res = resFun(status.HTTP_200_OK,'associate assigned',[])                    
                # else:
                    # res = resFun(status.HTTP_204_NO_CONTENT,'invalid lead id',[])
        else: 
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized to assign leads',[])
        
        return res
        


class reasonSubmit(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = reasonSubmitSerializer
    def put(self, request, table, format=None, *args, **kwargs):
        
        try:
            model = apps.get_model('dropdown', table)

            if not request.data.get('id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'id field is mandatory', [])
            
            if not request.data.get('client_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'client id field is mandatory', [])
            
            if not request.data.get('lead_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'lead id field is mandatory', [])


            id = request.data.get('id')
            client_id = request.data.get('client_id')
            lead_id = request.data.get('lead_id')

            lead_instance = Leads.objects.get(client_id=client_id, service_category_all__lead_id=lead_id)

            if table == 'not_interested':
                for ld in lead_instance.service_category_all.all():
                    if ld.lead_id == lead_id:
                        status_instance = drp_lead_status.objects.get(title='not interested')
                        # ld.status = status_instance
                        ld.not_interested_reason = not_interested.objects.get(id=id)
                        # print(drp_lead_status.objects.get(title=''))
                        ld.save()
                        Status_history_instance = Status_history.objects.create(**{"status": status_instance, "updated_by": request.user })
                        ld.status_history_all.add(Status_history_instance)
                        status_update = True

                if status_update:
                    res = resFun(status.HTTP_200_OK, 'saved successfully',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'status not updated',[])

            elif table == 'unresponsive':
                for ld in lead_instance.service_category_all.all():
                    if ld.lead_id == lead_id:
                        status_instance = drp_lead_status.objects.get(title='unresponsive')
                        # ld.status = status_instance
                        ld.unresponsive_reason = unresponsive.objects.get(id=id)
                        # print(drp_lead_status.objects.get(title=''))
                        ld.save()
                        Status_history_instance = Status_history.objects.create(**{"status": status_instance, "updated_by": request.user })
                        ld.status_history_all.add(Status_history_instance)
                        status_update = True

                if status_update:
                    res = resFun(status.HTTP_200_OK, 'saved successfully',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'status not updated',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'table out of range',[])
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])



class LeadStatusUpdate(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = LeadStatusUpdateSerializer
    def put(self, request, format=None, *args, **kwargs):
        try:
            if not request.data.get('client_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'client id is required',[])
            if not request.data.get('lead_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'lead id is required',[])
            if not request.data.get('lead_status_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'lead status id is required',[])
            
            lead_instance = Leads.objects.get(client_id=request.data.get('client_id'))
            for ld in lead_instance.service_category_all.all():
                if ld.lead_id == request.data.get('lead_id'):
                    status_instance = drp_lead_status.objects.get(id = request.data.get('lead_status_id'))
                    # ld.status  = status_instance
                    ld.save()
                    # print('request.data',ld)
                    status_history_instance = Status_history.objects.create(**{'status': status_instance, 'updated_by': request.user })
                    service_category = lead_instance.service_category_all.filter(lead_id=request.data.get('lead_id')).first()
                    service_category.status_history_all.add(status_history_instance)
                    status_update = True

            if status_update:
                res = resFun(status.HTTP_200_OK, 'successful',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'status not updated',[])
            return res 
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])




class AddNewServiceCategory(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddNewServiceCategorySerializer
    def post(self, request, format=None, *args, **kwargs):
        # print(request.data)
        # try:

            if not request.data.get('client_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'client id is a required field', [])
                
            if not request.data.get('segment'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'segment is a required field', [])
            elif not Segment.objects.filter(id = request.data.get('segment')).exists():
                return resFun(status.HTTP_400_BAD_REQUEST, 'invalid segment id', [])

            if not request.data.get('marketplace'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'marketplace is a required field', [])
            elif not Marketplace.objects.filter(id = request.data.get('marketplace')).exists() :
                return resFun(status.HTTP_400_BAD_REQUEST, 'invalid marketplace id', [])
            
            if not request.data.get('program'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'program is a required field', [])
            else:
                program = Program.objects.filter(id = request.data.get('program'))
                if program.exists():
                    if program.first().program == 'funded':
                        if not request.data.get('sub_program'):
                            return resFun(status.HTTP_400_BAD_REQUEST, 'sub program is a required field', [])
                        elif not Sub_Program.objects.filter(id = request.data.get('sub_program')).exists() :
                            return resFun(status.HTTP_400_BAD_REQUEST, 'invalid sub program id', [])
                    else:
                        pass
                else:
                    return resFun(status.HTTP_400_BAD_REQUEST, 'invalid program id', [])
            
            if not request.data.get('service'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'service is a required field', [])
            else:
                if isinstance(request.data.get('service'), list):
                    for s in request.data.get('service'):
                        if not Service.objects.filter(id = s).exists():
                            return resFun(status.HTTP_400_BAD_REQUEST, 'invalid service id', [])
                else:
                    return resFun(status.HTTP_400_BAD_REQUEST, 'service should be a list of integer values', [])


            try:
                lead_instance = Leads.objects.get(client_id = request.data.get('client_id'))
            except:
                lead_instance = None

            if lead_instance != None:

                if program.first().program == 'funded':
                    service_commercials = Services_and_Commercials.objects.filter(segment__id=request.data.get('segment'),service__id__in=request.data.get('service'), marketplace__id=request.data.get('marketplace'), program__id=request.data.get('program'),sub_program__id=request.data.get('sub_program') , visibility=True)
                else:
                    service_commercials = Services_and_Commercials.objects.filter(segment__id=request.data.get('segment'),service__id__in=request.data.get('service'), marketplace__id=request.data.get('marketplace'), program__id=request.data.get('program'), visibility=True)


                if service_commercials.exists():
                    service_check = lead_instance.service_category_all.filter(service__id=service_commercials.first().id).exists()

                    if service_check:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'service already created previously',[])
                    else:
                        data = {'lead_id': getLeadId(),'service': service_commercials.first().id}
                        serializer = AddNewServiceCategorySerializer(data=data, many=False)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()

                        status_history_instance = Status_history.objects.create(**{'status': drp_lead_status.objects.filter(title='yet to contact').first(), 'updated_by': request.user})
                        print(serializer.instance)
                        serializer.instance.status_history_all.add(status_history_instance)

                        lead_instance.service_category_all.add(serializer.instance)
                        lead_instance.save()
                        res = resFun(status.HTTP_200_OK, 'new service created, it will be assigned to the concerned department',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'service commercial not available, please contact admin to create a service with commercials',[])    
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'invalid client id',[])
            return res
        # except:
        #     return resFun(status.HTTP_400_BAD_REQUEST, 'request failed',[])



class CreateFollowUp(GenericAPIView):
    serializer_class = CreateFollowUpSerializer
    permission_classes =[IsAuthenticated]
    def post(self, request):

        try:
            try:
                service_category_instance = Service_category.objects.get(lead_id=request.data.get('lead_id'))
            except:
                service_category_instance = None

            if not request.data.get('lead_id'):
                return resFun(status.HTTP_400_BAD_REQUEST, 'lead id is mandatory field',[])
            if service_category_instance == None:
                return resFun(status.HTTP_400_BAD_REQUEST, 'invalid lead id',[])

            
            serializer = CreateFollowUpSerializer(data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer.instance.created_by = request.user
            serializer.instance.save()
            service_category_instance.followup.add(serializer.instance)
            service_category_instance.save()

            res = resFun(status.HTTP_200_OK, 'follow up created', [])
            return res

        except: 
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])




def SendEmail(email, subject, message):
    subject = subject
    # message = '<h1>This email was sent from django</h1>'
    from_email = 'akshatnigamcfl@gmail.com'
    recipient_list = email
    text = 'email sent from MyDjango'
    email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
    email.attach_alternative(message, 'text/html')
    # email.attach_file('files/uploadFile_0dTGU7A.csv', 'text/csv')
    email.send()






class apiSubmitEmailProposal(GenericAPIView):
    serializer_class = ev_servicesSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None, *args, **kwargs):
        # print(commercial_id)
        try:
            client_id = request.data.get('client_id')
            commercial_id = request.data.get('commercial_id')
            if commercial_id == None:

                if not request.data.get('lead_id'):
                    return resFun(status.HTTP_400_BAD_REQUEST, 'lead id is required', [])
                if not request.data.get('custom_commercial'):
                    return resFun(status.HTTP_400_BAD_REQUEST, 'custom commercial is required', [])
                

                service_category_instance = Service_category.objects.get(lead_id=request.data.get('lead_id'))
                commercial_approval_instance = Commercial_Approval.objects.create(**{"commercial": request.data.get('custom_commercial')})
                service_category_instance.commercial_approval = commercial_approval_instance
                # service_category_instance.save()

                SendEmail([request.user.director.email], 'Commercial Approval Pending', f'''<h3>Hello {request.user.director.name},</h3></br><p><b>{request.user.name}</b> from <b>{request.user.department}</b> has requested you to approve a commercial. Check commercial details below</p></br>
                        <table class="table table-zebra" style="border: 1px solid black; border-collapse:collapse" border="1>
                            <thead>
                              <tr>
                                <th style="border: 1px solid black;">Segment</th>
                                <th style="border: 1px solid black;">Service</th>
                                <th style="border: 1px solid black;">Marketplace</th>
                                <th style="border: 1px solid black;">Commercial</th>
                                <th style="border: 1px solid black;">Requested By</th>
                              </tr>
                            </thead>
                            <tbody>
                                <tr>
                                  <td style="border: 1px solid black;">{service_category_instance.service.segment.segment}</td>
                                  <td style="border: 1px solid black;">{service_category_instance.service.service.service}</td>
                                  <td style="border: 1px solid black;">{service_category_instance.service.marketplace.marketplace}</td>
                                  <td style="border: 1px solid black;">{request.data.get('custom_commercial')}</td>
                                  <td style="border: 1px solid black;">{request.user.name}</td>
                                </tr>
                            </tbody>
                            </table>
                            </br>
                            <p>Please click link below to approve commercial</p>
                            <a href="#"><button>Approve</button></a>
                            <p><b>Regards,</b></p>
                          ''')

                res = resFun(status.HTTP_200_OK, 'commercial sent for approval, you will be notified once approved', [])
                return res
            else:
                lead_instance = Leads.objects.get(client_id=client_id, visibility=True)
                email = lead_instance.email_id
                service = None
                for ld in lead_instance.service_category_all.all():
                    print('ld', ld)
                    # service = 
                    for l in ld.service.commercials.all():
                        if l.id == commercial_id:
                            service = ld.service.service
                print('service',service)
                if service != None:
                    message = Proposal_Email.objects.get(service__id = service.id)
                    message = message.email
                    bank_details = ev_bank_details.objects.all().first()
                    account_name = bank_details.account_name
                    bank_name = bank_details.bank_name
                    account_number = bank_details.account_number
                    ifsc = bank_details.ifsc

                    # print(message)

                    # message = message.replace('{***account_name***}', account_name)
                    # message = message.replace('{***bank_name***}', bank_name)
                    # message = message.replace('{***account_number***}', account_number)
                    # message = message.replace('{***ifsc_code***}', ifsc)

                    message = message.replace('{***service***}', service.service)
                    message = message.replace('{***slab***}', Commercials.objects.get(id=commercial_id).commercials)
                    message = message.replace('{***sender***}', request.user.name)
                    # message = html.escape(message)
                    # print(message)
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
                        status_update=False
                        for ld in lead_instance.service_category_all.all():
                            if ld.service.service.id == service.id:
                                ld.pricing = Commercials.objects.get(id=commercial_id)
                                # ld.status = drp_lead_status.objects.get(title='proposal email sent')
                                ld.save()
                                status_history_instance = Status_history.objects.create(**{'status': drp_lead_status.objects.get(title='proposal email sent'), 'updated_by': request.user})
                                status_update = True
                                ld.status_history_all.add(status_history_instance)
                        # status_update = service.objects.filter(client_id__client_id=client_id, client_id__visibility=True).update(lead_status = getLeadStatusInst('proposal email sent'))
                        # print(status_update)
                        # lead_instance.save()

                        if status_update:
                            res = resFun(status.HTTP_200_OK, 'email sent', [] )
                        else:
                            res = resFun(status.HTTP_400_BAD_REQUEST, 'email not sent', [] )
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'email not sent', [] )
                else:
                    res = resFun(status.HTTP_204_NO_CONTENT, 'no email found against the service id', [] )
                return res
        
        except:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [] )
            return res
        



class AskForDetailEmail(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AskForDetailEmailSerializer
    def post(self, request):

        serializer = AskForDetailEmailSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)

        lead_instance = Leads.objects.filter(client_id=serializer.data['client_id'])
        if lead_instance.exists():

            message = canned_email.objects.filter(email_type = 'ask_for_details').first()
            message = message.email
            message = str(message).replace("{***sender***}", request.user.name)
            email_id = lead_instance.first().email_id
            subject = 'Details required to proceed further with your onboarding with evitamin!'

            SendEmail([email_id], subject, message)

            # message = Ask_For_Detail_Email.objects.filter()
            # pass

            res = resFun(status.HTTP_200_OK, "Email sent to the client, keep an eye on seller's response",[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, "invalid client id",[])
            
        return res
    


def generate_mou_validation(service_category_instance, lead_instance):
    error_data = []
    if service_category_instance.pricing == None:
        error_data.append('commercial')
    if lead_instance.client_name == None:
        error_data.append('client name')
    if lead_instance.contact_number == None:
        error_data.append('contact number')
    if lead_instance.email_id == None:
        error_data.append('email id')   
    if lead_instance.business_name == None:
        error_data.append('business name')
    if lead_instance.brand_name == None:
        error_data.append('brand name')
    if lead_instance.gst == None:
        error_data.append('gst')
    if lead_instance.seller_address == None:
        error_data.append('seller address')
    if lead_instance.client_designation == None:
        error_data.append('client designation')
    return error_data



def generate_mou(service_category_instance, lead_instance ):
    client_name = lead_instance.client_name.capitalize()
    email_id = lead_instance.email_id
    phone_number = lead_instance.contact_number
    business_name = lead_instance.business_name.capitalize()
    brand_name = lead_instance.brand_name
    name_for_mou = client_name.capitalize()
    designation = lead_instance.client_designation.title.capitalize()
    gst = lead_instance.gst.upper()
    seller_address = lead_instance.seller_address
    commercial = service_category_instance.pricing.commercials.capitalize()
    template = get_template('mou/mou.html')
    date = datetime.now()
    date = f"{date.strftime('%d')}/{date.strftime('%m')}/{date.strftime('%Y')}"
    context = {
        'current_date': date,
        'business_name': business_name, 
        'brand_name': brand_name, 
        'business_address': seller_address, 
        "service_name": service_category_instance.service.service.service, 
        "fees_slab": commercial, 
        "name_for_mou": name_for_mou, 
        'designation': designation, 
        'requester_name': client_name, 
        "email_id": email_id, 
        "gst": gst, 
        "phone_number": phone_number
        }
    html = template.render(context)
    res = BytesIO()
    result = pisa.CreatePDF(html, dest=res)
    if result.err:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'error': 'error generating pdf',
            'data': []
            })
    service_category_instance.status = drp_lead_status(title='mou generated')
    res.seek(0)
    return {'file': res, 'service_category_instance': service_category_instance,  'lead_instance': lead_instance }

        

class preview_mou(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = preview_mouSerializer
    def get(self, request, lead_id):
        try:
            # return FileResponse(file, content_type='application/pdf', as_attachment=True, filename=f'{business_name}.pdf')
            try:
                service_category_instance = Service_category.objects.get(lead_id=lead_id)
            except:
                service_category_instance = None

            if service_category_instance != None:

                try:
                    lead_instance = Leads.objects.get(service_category_all__id=service_category_instance.id)
                except:
                    lead_instance = None

                if lead_instance != None:

                    error_data = generate_mou_validation(service_category_instance, lead_instance)

                    if len(error_data) > 0:
                        return resFun(status.HTTP_400_BAD_REQUEST,', '.join(error_data)+', these fields are required, please update the seller details', [])
                    else:
                        res = generate_mou(service_category_instance, lead_instance)
                        print('res',res)
                        return FileResponse(res.get('file'), content_type='application/pdf', as_attachment=True, filename=f'{lead_instance.business_name}.pdf')
                else:
                    return resFun(status.HTTP_400_BAD_REQUEST, 'something went wrong', [])
            else:
                return resFun(status.HTTP_400_BAD_REQUEST, 'invalid lead id', [])

        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            



class email_mou(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = email_mouSerializer
    def get(self, request, lead_id):
        try:
            try:
                service_category_instance = Service_category.objects.get(lead_id=lead_id)
            except:
                service_category_instance = None

            if service_category_instance != None:

                try:
                    lead_instance = Leads.objects.get(service_category_all__id=service_category_instance.id)
                except:
                    lead_instance = None

                if lead_instance != None:

                    error_data = generate_mou_validation(service_category_instance, lead_instance)

                    if len(error_data) > 0:
                        return resFun(status.HTTP_400_BAD_REQUEST,', '.join(error_data)+', these fields are required, please update the seller details', [])
                    else:
                        res = generate_mou(service_category_instance, lead_instance)
                        # print('res',res['lead_instance'].business_name.replace(' ', '_'))

                        email = lead_instance.email_id

                        subject = f'MOU for {service_category_instance.service.service.service} with evitamin!'
                        text = 'PFA'
                        from_email = 'akshatnigamcfl@gmail.com'
                        recipient = [email]

                        email = EmailMultiAlternatives(subject, text, from_email, recipient)
                        email.attach_alternative('<h1>Hello</h1></br><p>Please seal & sign this MOU and revert back to the same email.</p>', 'text/html')
                        # email.attach(filename = res[f'{res['lead_instance'].business_name.replace(' ', '_')}_{res['service_category_instance'].service.service.service}'], content = res['file'], mimetype='application/pdf')

                        email.attach(lead_instance.business_name, res.get('file').read(), 'application/pdf')


                        email.send()

                        if email.send():

                            # print('getLeadStatusInst', getLeadStatusInst('pending payment proof'))
                            # service.objects.filter(lead_id__lead_id=lead_id, lead_id__visibility=True).update(lead_status = getLeadStatusInst('pending payment proof'))

                            service_category_instance.status = drp_lead_status.objects.get(title='pending for mou')
                            service_category_instance.save()

                            res = resFun(status.HTTP_200_OK,'email sent', [] )
                        else:
                            res = resFun(status.HTTP_400_BAD_REQUEST,'email not sent', [] )

                    return res

                        # return FileResponse(res['file'], content_type='application/pdf', as_attachment=True, filename=f'{res['business_name']}.pdf')
                else:
                    return resFun(status.HTTP_400_BAD_REQUEST, 'something went wrong', [])
            else:
                return resFun(status.HTTP_400_BAD_REQUEST, 'invalid lead id', [])

        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])




class upload_mou_approval(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = uploadFileSerializer
    def post(self, request, lead_id):
        try:
            if request.FILES:
                try:
                    service_category_instance = Service_category.objects.get(lead_id=lead_id)
                except:
                    service_category_instance = None

                if service_category_instance != None:
                    file = request.FILES['file']
                    service_category_instance.mou = file
                    # service_category_instance.mou_approval = False

                    service_category_instance.status = drp_lead_status.objects.get(title='pending for mou')
                    service_category_instance.save()

                    res = resFun(status.HTTP_200_OK, 'request successful', [])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'invalid lead id', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'file required to upload', [])
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])

            


class upload_payment_proof_approval(GenericAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = uploadFileSerializer
    def post(self, request, lead_id):
        try:
            if request.FILES:
                try:
                    service_category_instance = Service_category.objects.get(lead_id=lead_id)
                except:
                    service_category_instance = None

                if service_category_instance != None:
                    file = request.FILES['file']
                    service_category_instance.payment_proof = file
                    # service_category_instance.payment_approval = False
                    service_category_instance.status = drp_lead_status.objects.get(title='pending for mou')
                    service_category_instance.save()

                    res = resFun(status.HTTP_200_OK, 'request successful', [])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, 'invalid lead id', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'file required to upload', [])
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])

    






    

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


    