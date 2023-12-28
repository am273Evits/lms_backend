from django.shortcuts import render
from django.apps import apps
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from dropdown.models import ev_department, ev_designation, user_role_list
from dropdown.models import list_employee
from business_leads.serializers import allIdentifiersSerializer 
from dropdown.serializers import dynamic_serializer
from account.models import *
from dropdown.models import dropdown_fields

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
            print(serializer.data)
            DR_LIST = set()
            for s in serializer.data:
                for key in s:
                    for d in s[key]:
                        DR_LIST.add(d)
            
            print(DR_LIST)
                    
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                "message": 'successful',
                "data": {'title': DR_LIST, 'dropdown_name': table}
                }
        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                "message": 'request failed',
                "data": []
                }
        return res
    

class dropdownOptionData1(GenericAPIView):
    serializer_class = dropdownOptionSerializers
    permissions_classes = [IsAuthenticated]
    def get(self, request, table, data1,  format=None, *args, **kwargs):
        # print(table)

        model = apps.get_model('dropdown', table)
        if table == 'ev_designation':
            data = list(model.objects.filter(department__title = data1).values_list('title', flat=True).order_by('title'))
            # print(data)
            serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
            res = Response()
            if serializer.is_valid(raise_exception=True):

                DS_LIST = []
                for s in serializer.data:
                    for key in s["title"]:
                        d = ev_designation.objects.filter(title = key).first()
                        DS_LIST.append(d.title.title)
                        
                if len(DS_LIST) > 0:
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        "message": 'successful',
                        "data": {"title": DS_LIST, 'dropdown_name': table}
                        }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        "message": 'no data found',
                        "data": ''
                        }

            else :
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "message": 'request failed',
                    "data": []
                    }
        elif table == 'country_state_city':
            # print('working')
            data = list(model.objects.filter(title = data1).values_list('state', flat=True).distinct().order_by('state'))
            print('data', data)
            if data:
                serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
                res = Response()
                if serializer.is_valid(raise_exception=True):
                    # print(serializer.data)

                    DS_LIST = []
                    for s in serializer.data:
                        for d in s['title']:
                            DS_LIST.append(d)
                    print(DS_LIST)
                
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        "message": 'successful',
                        "data": {'title': DS_LIST, 'dropdown_name': table}
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        "message": 'request failed',
                        "data": []
                        }
                return res

        return res



class dropdownOptionData2(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = dropdownOptionSerializers
    def get(self, request, table, data1, data2, format=None, *args, **kwargs):

        model = apps.get_model('dropdown', table)
        if table == 'user_role_list':
            data = list(model.objects.filter(department__title = data1, designation__title__title = data2).values_list('title', flat=True).order_by('title'))
            # print('data', data)
            serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
            res = Response()
            if serializer.is_valid(raise_exception=True):

                DS_LIST = []
                for s in serializer.data:
                    DS_LIST.append(*s['title'])
                    # for key in s["title"]:
                    #     print(key)
                        # d = ev_designation.objects.filter(title = key).first()
                        # DS_LIST.append(d.title.title)
                        
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': status.HTTP_200_OK,
                    "message": 'successful',
                    "data": {'title': DS_LIST, 'dropdown_name': table}
                    }
            else :
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "message": 'request failed',
                    "data": []
                    }
        elif table == 'country_state_city':
            data = list(model.objects.filter(title = data1, state = data2).values_list('city', flat=True).distinct().order_by('city'))
            if data:
                serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
                res = Response()
                if serializer.is_valid(raise_exception=True):
                    
                    DS_LIST = []
                    for s in serializer.data:
                        for d in s['title']:
                            DS_LIST.append(d)
                    # print(DS_LIST)

                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        "message": 'successful',
                        "data": {'title': DS_LIST, 'dropdown_name': table}
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        "message": 'request failed',
                        "data": []
                        }
                return res
        return res


class employeesAllTables(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = employeesAllTablesSerializer
    def get(self, request, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin' or user_role == 'lead_manager' or user_role == 'bd_tl' or user_role == 'bd_t_member':

            tables = list_employee.objects.all()
            # print(tables)
            tablesList = [tb.table_name for tb in tables]
            # print('tablesList',tablesList)
            tables = {'tables': tablesList}
            print(tables)
                    
            serializer = employeesAllTablesSerializer(data=tables)
            if serializer.is_valid(raise_exception=True):
                
                tables = serializer.data['tables']
                table_data = []
                for t in tables:
                    table_data.append({'table_name': t if t != 'useraccount' else 'user account', 'table_reference': t})

                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': status.HTTP_200_OK,
                    'message': 'successful',
                    'data': table_data
                }
            else :
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'unsuccessful',
                    'data': serializer.data
                }
        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'you are not authorized',
                'data': []
            }
        return res
    


# class viewEmployee(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = allIdentifiersSerializer
#     def get(self, request, table, employee_id, format=None, *args, **kwargs):

#         user_role = getUserRole(request.user.id)
#         res = Response()

#         if table == 'useraccount':
#             models = apps.get_model('account', table)
#         else:
#             models = apps.get_model('employees', table)
        
#         modelFields = list(getModelFields(models))
#         model_fields = [mod for mod in modelFields if mod['type'] != 'ForeignKey' if mod['field'] != 'employee_id']
#         serializer_class = models

#         if table != 'useraccount':
#             lead_ref = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
#             if lead_ref:
#                 employee_id = lead_ref[0].id
#                 for i in range(len(model_fields)):
#                     if model_fields[i]:
#                         if model_fields[i]['field'] == 'employee_id':
#                             model_fields.pop(i)
#                             break
#             else:
#                 res.status_code = status.HTTP_403_FORBIDDEN
#                 res.data = {
#                     'status': status.HTTP_403_FORBIDDEN,
#                     'message': 'invalid lead id',
#                     'data' : []
#                 }
#                 return res
#         else:
#             lead_ref = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
#             if not lead_ref:
#                 res.status_code = status.HTTP_403_FORBIDDEN
#                 res.data = {
#                     'status': status.HTTP_403_FORBIDDEN,
#                     'message': 'invalid lead id',
#                     'data' : []
#                 }
#                 return res
                

#         if user_role == 'lead_manager' or user_role == 'admin':
#             data = ''
#             if table != 'useraccount':
#                 data = models.objects.select_related().filter(emp = employee_id)
#             else:
#                 data = models.objects.select_related().filter(employee_id = employee_id)

#             # associate_id = data[0].associate_id.id if data[0].associate_id != None else '' 
#             # data = data.values().first()
#             # nData = data
#             # nData['associate_id'] = associate_id
#             # data = list([nData])

#             dynamic = dynamic_serializer(models)
#             if table == 'useraccount':
#                 serializer = UserAccountSerializer(data=list(data.values()), many=True)
#             else:
#                 serializer = dynamic(data=list(data.values()), many=True)

#             serializer.is_valid(raise_exception=True)
#             # print('serializer.data',serializer.data)

#             # print(serializer.data)
#             s_data = dict(serializer.data[0])
#             # print(s_data)

#             # if table =='useraccount':
#             #     # print('model_fields', model_fields)

#             #     for i, m in enumerate(model_fields):
#             #             # print(m['field'])
#             #             model_fields.pop(i)
#             #             # print(i)
                
                
#             #     print(model_fields)

                
#                 # EO_INST = employee_official.objects.filter(emp__id = s_data['associate_id'], emp__visibility=True).first()
#                 # s_data['associate_id'] = {'name': EO_INST.emp.name if EO_INST!= None else '' , 'pk': s_data['associate_id'] if s_data['associate_id'] !=None else '' }

#             #     model_fields.append({'type': 'CharField', 'value': '', 'field': 'associate_id'})
#             # print(s_data)
#             for i, md in enumerate(model_fields):
#                 hidden_fields = ['employee_id', 'password' ,'email', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'visibility', 'updated_at']
#                 if table == 'useraccount' and (md['field'] in hidden_fields):
#                     if md['field'] in hidden_fields:
#                         model_fields.pop(i)
#                     # del md
#                 elif not md['type'] == 'ForeignKey':
#                     print(md)
#                     for key in md:
#                         # print('data', md['field'])
#                         # print(key)
#                         # print(md['field'])
#                         md['value'] =  s_data[md['field']]
#                         break

            
#             for mod in model_fields:
#                 mod['key'] = mod['field']
#                 del mod['field']

#             # print('model_fields',model_fields)
#             if table != 'all_identifiers':
#                 dropdown_fields_data = dropdown_fields.objects.all()
#                 for m in model_fields:
#                     # print(m['key'])
#                     for d in dropdown_fields_data:
#                         if d.title == m['key']:
#                             # print(d.title)
#                             m['type'] = 'dropdown'
#                             selectBoxData = []
#                             if d.ref_tb:
#                                 m['table'] = d.ref_tb
#                                 refModel = apps.get_model('dropdown', d.ref_tb)
#                                 refModelData = refModel.objects.all()
#                                 for rmd in refModelData:
#                                     selectBoxData.append(rmd.title)
#                                 m['dropdown'] = selectBoxData
#                             else:
#                                 pass

#             res.status_code = status.HTTP_200_OK
#             res.data = {
#                 'status': status.HTTP_200_OK,
#                 'message': 'successful',
#                 'data': {'data': serializer.data, "current_table": table, 'employee_id': employee_id, 'data_type': model_fields}
#                 }
#         elif user_role == 'bd_tl':
#             product = getProduct(request.user.id)
 
#             serviceData = service.objects.filter(employee_id = employee_id, service_category = product)
#             if serviceData:
#                 data = models.objects.filter(employee_id = employee_id)
#                 # print(data)
#                 data = list(data.values())
#                 serializer = models(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     "status": status.HTTP_200_OK,
#                     'message': 'successful',
#                     'data': {'data': serializer.data,"current_table": table, 'employee_id': employee_id, 'field_type': [model_fields]}
#                     }
#                 # return res
#         else:
#             res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#             res.data = {
#                 "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
#                 'message': 'you are not authorized to see this lead',
#                 'data': []
#                 }
        
#         return res
    


# class dropdownAjaxOption(GenericAPIView):
#     serializer_class = dropdownOptionSerializers
#     permissions_classes = [IsAuthenticated]
#     def get(self, request, table ,format=None, *args, **kwargs):

#         model = apps.get_model('dropdown', table)
#         if table == 'country_state_city':
#             data = list(model.objects.values_list('country', flat=True).distinct().order_by('country'))
#             print('data', data)
#             if data:
#                 serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#                 res = Response()
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status': status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": serializer.data
#                         }
#                 else :
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         "message": 'request failed',
#                         "data": []
#                         }
#                 return res
    


# class dropdownAjaxD1Option(GenericAPIView):
#     serializer_class = dropdownOptionSerializers
#     permissions_classes = [IsAuthenticated]
#     def get(self, request, table, country ,format=None, *args, **kwargs):

#         model = apps.get_model('dropdown', table)
#         if table == 'country_state_city':
#             data = list(model.objects.filter(country = country).values_list('state', flat=True).distinct().order_by('state'))
#             if data:
#                 serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#                 res = Response()
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status': status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": serializer.data
#                         }
#                 else :
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         "message": 'request failed',
#                         "data": []
#                         }
#                 return res
            


# class dropdownAjaxD2Option(GenericAPIView):
#     serializer_class = dropdownOptionSerializers
#     permissions_classes = [IsAuthenticated]
#     def get(self, request, table, country, state ,format=None, *args, **kwargs):

#         model = apps.get_model('dropdown', table)
#         if table == 'country_state_city':
#             data = list(model.objects.filter(country = country, state = state).values_list('city', flat=True).distinct().order_by('city'))
#             if data:
#                 serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#                 res = Response()
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status': status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": serializer.data
#                         }
#                 else :
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         "message": 'request failed',
#                         "data": []
#                         }
#                 return res