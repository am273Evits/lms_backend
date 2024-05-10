from django.shortcuts import render
from django.apps import apps
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from leads.views import resFun
from leads.models import Leads, drp_lead_status
from datetime import datetime
# from dropdown.models import ev_department, ev_designation, user_role_list
# from dropdown.models import list_employee
# from business_leads.serializers import allIdentifiersSerializer 
# from dropdown.serializers import dynamic_serializer
from account.models import *
# from dropdown.models import dropdown_fields

# from account.views import getLeadId, getProduct, getUserRole, getTeamLeader, getClientId, get_tokens_for_user , getAssociates as getAssociate, getModelFields




class dropdown_department(GenericAPIView):
    serializer_class = CommonDropdownSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if (str(user.department) == 'director') or (str(user.department) == 'admin' and str(user.designation) == 'user_manager') :

            department = Drp_Program.objects.values('department').distinct()
            print('department',department)
            if department.exists():
                data =[]
                for d in department:
                    data.append({'id': d.get('department'), 'value': Department.objects.get(id=d.get('department')).title})

                serializer = CommonDropdownSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res = resFun(status.HTTP_200_OK, 'request successful', serializer.data )
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'no department list found', [] )
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [] )
        return res








class dropdown_designation(GenericAPIView):
    serializer_class = CommonDropdownSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None, *args, **kwargs):
        user = request.user
        res = Response()
        if (str(user.department) == 'director') or (str(user.department) == 'admin' and str(user.designation) == 'user_manager'):
            # print(user.designation)

            try:
                designation = Drp_Program.objects.filter(department = id).values('designation').distinct()
                print('designation',designation)
                data = []
                for d in designation:
                    data.append({'id': d.get('designation'), 'value': Designation.objects.get(id=d.get('designation')).title})
                serializer = CommonDropdownSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res = resFun(status.HTTP_200_OK, 'request successful', serializer.data )
            except:
                res = resFun(status.HTTP_204_NO_CONTENT, 'no designation list found', [] )
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [] )

        return res
    



# class dropdown_program(GenericAPIView):
#     serializer_class = dropdown_programSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, id, format=None, *args, **kwargs):
#         user = request.user
#         res = Response()
#         if (str(user.department) == 'director'):
#             program = Drp_Program.objects.filter(designation = id).values('program').distinct()
#             print(program)
#             if program.exists():
#                 data = []
#                 for d in program:
#                     if d.get('program') == None:
#                         res.status_code = status.HTTP_400_BAD_REQUEST
#                         res.data = {
#                             'data': [],
#                             'status': status.HTTP_400_BAD_REQUEST,
#                             'message': 'invalid designation id',
#                         }
#                         res = resFun(status.HTTP_200_OK,'invalid designation id',[])

#                         return res                           
#                     else:
#                         data.append({'program_id': d.get('program'), 'program_name': Program.objects.get(id = d.get('program')).title})


#                 serializer = dropdown_programSerializer(data=data, many=True)
#                 serializer.is_valid(raise_exception=True)

#                 res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
#             else:
#                 res = resFun(status.HTTP_400_BAD_REQUEST,'no program list found',[])
#         else:
#             res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
#         return res

# class ()




class dropdown_employee_status(GenericAPIView):
    serializer_class = CommonDropdownSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        user = request.user
        # res = Response()
        if (str(user.department) == 'director') or (str(user.department) == 'admin' and str(user.designation) == 'user_manager'):

            employee_status = Employee_status.objects.values('title','id').distinct()
            # print('employee_status',employee_status)
            if employee_status.exists():
                data =[]
                for d in employee_status:
                    data.append({'id': d.get('id'), 'value': d.get('title')})

                serializer = CommonDropdownSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no employee_status list found',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res



def employeeListFun(searchData, searchAtr):

    if searchData==None:
        res = resFun(status.HTTP_400_BAD_REQUEST,'search attribute not valid',[])

    elif searchData.exists():
        data =[]
        for d in searchData:
            if searchAtr == 'team_member':

                employee_leave_instance = Employee_leaves.objects.filter(employee=d.id, status__title='approved')
                if employee_leave_instance.exists():
                    for em in employee_leave_instance:
                        today = datetime.now().date()
                        if not em.date_from <= today <= em.date_to:
                            data.append({'id': d.id, 'value': d.name})
                else:
                    data.append({'id': d.id, 'value': d.name})
            else:    
                data.append({'id': d.id, 'value': d.name})

        serializer = CommonDropdownSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        res = resFun(status.HTTP_200_OK,'request successful',{'data': serializer.data, 'search_attribute': searchAtr})
    else:
        res = resFun(status.HTTP_204_NO_CONTENT,'data not found',{'data': serializer.data, 'search_attribute': searchAtr})

    return res


class employee_list(GenericAPIView):
    serializer_class = CommonDropdownSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, searchAtr, format=None, *args, **kwargs):
        user = request.user
        # res = Response()
        if (str(user.department) == 'director') or (str(user.department) == 'admin' and str(user.designation) == 'user_manager'):

            try:
                if searchAtr == 'director':
                    searchData = UserAccount.objects.filter(department__title = searchAtr, visibility=True).distinct()
                elif searchAtr == 'user_manager':
                    searchData = UserAccount.objects.filter(designation__title = searchAtr, visibility=True).distinct()
                elif searchAtr == 'lead_manager':
                    searchData = UserAccount.objects.filter(designation__title = searchAtr, visibility=True).distinct()
                elif searchAtr == 'team_leader':
                    searchData = UserAccount.objects.filter(designation__title = searchAtr, visibility=True).distinct()
                
                res = employeeListFun(searchData, searchAtr)

            except:
                res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])

        elif (user.department.title == 'business_development' and user.designation.title == 'team_leader'):
            try:
                if searchAtr == 'team_member':
                    
                    # print('searchData',user.id)

                    searchData = UserAccount.objects.filter(team_leader__id = user.id).distinct()
                    # print('searchData',searchData)

                res = employeeListFun(searchData, searchAtr)
            except:
                res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])

        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])
        return res




class get_commercials(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommonDropdownSerializer
    def get(self, request, client_id, lead_id, format=None, *args, **kwargs):
        # try:
            lead_instance = Leads.objects.get(client_id=client_id, visibility=True)
            # print(lead_instance.service_category_all.all())
            service_category_instance = lead_instance.service_category_all.filter(lead_id=lead_id)
            print('service_category_instance',service_category_instance)

            if service_category_instance.exists():
                # lead_id =
                # print(ld.lead_id)
                # if ld.lead_id == lead_id:
                data=[{"id": l.id, "value": l.commercials} for l in service_category_instance.first().service.commercials.all() if not len(l.lead_id.all())>0 ]
                # data2 = [{"id": l.id, "value": l.commercials} for l in service_category_instance.first().service.commercials.all() if l.lead_id.filter(lead_id=service_category_instance.first().id).exists() ]

                for s in service_category_instance.first().service.commercials.all():
                    if s.lead_id.all().exists():
                        # data=[{"id": l.id, "value": l.commercials} for l in service_category_instance.first().service.commercials.all()]
                        if s.lead_id.filter(id = service_category_instance.first().id).exists() and service_category_instance.first().commercial_approval !=None and service_category_instance.first().commercial_approval.status.title =='approved':
                            data.append({"id": s.id, "value": s.commercials})

                # print('data2',data2)
                data.append({"id": 0, "value": 'others'})
                if len(data) > 0: 
                    serializer =  CommonDropdownSerializer(data=data, many=True)
                    serializer.is_valid(raise_exception=True)
                    res =  resFun(status.HTTP_200_OK, 'request successful', serializer.data)
                else:
                    res =  resFun(status.HTTP_204_NO_CONTENT, 'no data found, contact director to create commercials for this service', [])

            else:
                res =  resFun(status.HTTP_204_NO_CONTENT, 'no data', [])
            return res
        # except:
        #     return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
            





# Create your views here.

class dropdownOption(GenericAPIView):
    serializer_class = dropdownOptionSerializers
    permissions_classes = [IsAuthenticated]
    def get(self, request, table, format=None, *args, **kwargs):

        try:
            main_app = 'dropdown'
            print(main_app)
            if not(table == 'approval_status' or table == 'not_interested' or table == 'unresponsive'): 
                main_app = 'leads'

            model = apps.get_model(main_app, table)
            # if not model:
            #     print('else working') 

            data = model.objects.all().order_by('title')
            main_data = [{"id": d.id, "title": d.title } for d in data]
            serializer = dropdownOptionSerializers(data=main_data, many=True)
            serializer.is_valid(raise_exception=True)
            res = resFun(status.HTTP_200_OK, 'successful', {'data': serializer.data, 'table_name': table})
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])
    

class leadStatusList(GenericAPIView):
    permissions_classes = [IsAuthenticated]
    serializer_class = dropdownOptionSerializers
    def get(self, request, format=None, *args, **kwargs):

        print(request.data)

        try:
            lead_status = drp_lead_status.objects.all().values()
            print('lead_status',lead_status)

            serializer = dropdownOptionSerializers(data=list(lead_status), many=True)
            serializer.is_valid(raise_exception=True)

            res =  resFun(status.HTTP_200_OK, 'successful', serializer.data)
            return res
        except:
            return resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [])

        

# class dropdownOptionData1(GenericAPIView):
#     serializer_class = dropdownOptionSerializers
#     permissions_classes = [IsAuthenticated]
#     def get(self, request, table, data1,  format=None, *args, **kwargs):
#         # print(table)

#         model = apps.get_model('dropdown', table)
#         if table == 'ev_designation':
#             data = list(model.objects.filter(department__title = data1).values_list('title', flat=True).order_by('title'))
#             # print(data)
#             serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#             res = Response()
#             if serializer.is_valid(raise_exception=True):

#                 DS_LIST = []
#                 for s in serializer.data:
#                     for key in s["title"]:
#                         d = ev_designation.objects.filter(title = key).first()
#                         DS_LIST.append(d.title.title)
                        
#                 if len(DS_LIST) > 0:
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status': status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": {"title": DS_LIST, 'dropdown_name': table}
#                         }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         "message": 'no data found',
#                         "data": ''
#                         }

#             else :
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "message": 'request failed',
#                     "data": []
#                     }
#         elif table == 'country_state_city':
#             # print('working')
#             data = list(model.objects.filter(title = data1).values_list('state', flat=True).distinct().order_by('state'))
#             print('data', data)
#             if data:
#                 serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#                 res = Response()
#                 if serializer.is_valid(raise_exception=True):
#                     # print(serializer.data)

#                     DS_LIST = []
#                     for s in serializer.data:
#                         for d in s['title']:
#                             DS_LIST.append(d)
#                     print(DS_LIST)
                
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status': status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": {'title': DS_LIST, 'dropdown_name': table}
#                         }
#                 else :
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         "message": 'request failed',
#                         "data": []
#                         }
#                 return res

#         return res



# class dropdownOptionData2(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = dropdownOptionSerializers
#     def get(self, request, table, data1, data2, format=None, *args, **kwargs):

#         model = apps.get_model('dropdown', table)
#         if table == 'user_role_list':
#             data = list(model.objects.filter(department__title = data1, designation__title__title = data2).values_list('title', flat=True).order_by('title'))
#             # print('data', data)
#             serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#             res = Response()
#             if serializer.is_valid(raise_exception=True):

#                 DS_LIST = []
#                 for s in serializer.data:
#                     DS_LIST.append(*s['title'])
#                     # for key in s["title"]:
#                     #     print(key)
#                         # d = ev_designation.objects.filter(title = key).first()
#                         # DS_LIST.append(d.title.title)
                        
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'status': status.HTTP_200_OK,
#                     "message": 'successful',
#                     "data": {'title': DS_LIST, 'dropdown_name': table}
#                     }
#             else :
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "message": 'request failed',
#                     "data": []
#                     }
#         elif table == 'country_state_city':
#             data = list(model.objects.filter(title = data1, state = data2).values_list('city', flat=True).distinct().order_by('city'))
#             if data:
#                 serializer = dropdownOptionSerializers(data=[{'title': data}], many=True)
#                 res = Response()
#                 if serializer.is_valid(raise_exception=True):
                    
#                     DS_LIST = []
#                     for s in serializer.data:
#                         for d in s['title']:
#                             DS_LIST.append(d)
#                     # print(DS_LIST)

#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status': status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": {'title': DS_LIST, 'dropdown_name': table}
#                         }
#                 else :
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         "message": 'request failed',
#                         "data": []
#                         }
#                 return res
#         return res


# class employeesAllTables(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = employeesAllTablesSerializer
#     def get(self, request, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()
#         if user_role == 'admin' or user_role == 'lead_manager' or user_role == 'bd_tl' or user_role == 'bd_t_member':

#             tables = list_employee.objects.all()
#             # print(tables)
#             tablesList = [tb.table_name for tb in tables]
#             # print('tablesList',tablesList)
#             tables = {'tables': tablesList}
#             print(tables)
                    
#             serializer = employeesAllTablesSerializer(data=tables)
#             if serializer.is_valid(raise_exception=True):
                
#                 tables = serializer.data['tables']
#                 table_data = []
#                 for t in tables:
#                     table_data.append({'table_name': t if t != 'useraccount' else 'user account', 'table_reference': t})

#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'status': status.HTTP_200_OK,
#                     'message': 'successful',
#                     'data': table_data
#                 }
#             else :
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'unsuccessful',
#                     'data': serializer.data
#                 }
#         else :
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'you are not authorized',
#                 'data': []
#             }
#         return res
    


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