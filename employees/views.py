from django.shortcuts import render
from django.apps import apps
from django.db.models import fields
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from business_leads.serializers import allIdentifiersSerializer 
from .serializers import dynamic_serializer
from business_leads.serializers import visibility_dynamic_serializer
from .serializers import *
from employees.models import *
from dropdown.models import *
from records.models import user_delete_approval
import math
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



class viewAllUser(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewAllUserSerializer
    def get(self, request, page ,format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        limit = 10
        offset = int((page - 1) * limit)
        res = Response()
        if user_role == 'admin' or user_role == 'lead_manager':
            pagecount = math.ceil(employee_official.objects.filter(emp__visibility=True).count()/limit)
            if int(page) <= pagecount: 
                EMOF_arr = []
                EMOF_data = employee_official.objects.filter(emp__visibility=True).all()[offset: offset + limit]
                for d in EMOF_data:
                    EMOF_arr.append({"employee_id": d.emp.employee_id, 'name': d.emp.name, 'user_role': d.user_role if d.user_role != '' else '-', 'designation': d.designation if d.designation != '' else '-', 'department': d.department if d.department != '' else '-', 'product': d.product if d.product != '' else '-'})

                serializer = viewAllUserSerializer(data=EMOF_arr, many=True)
                if serializer.is_valid(raise_exception=True):
                    # print('serializer.data',serializer.errors)
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'message': 'successful',
                        "data": {'data': serializer.data, 'total_pages': pagecount, "current_page": page},
                        'status': status.HTTP_200_OK
                    }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'message': serializer.errors,
                        "data": [],
                        'status': status.HTTP_400_BAD_REQUEST
                    }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": 'the page is unavailable',
                    "data": {'data': [], 'total_pages': pagecount, "current_page": page}
                    }

        else:
            res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            res.data = {
                'message': 'you are not authorized',
                "data": [],
                'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            } 
        return res


class viewUserIndv(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewUserIndvSerializer
    def get(self, request, employee_id, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)

        def addUserAccountDetails(EMOF_val,EMOF_qrs):
            for e in EMOF_val:
                e['name'] = EMOF_qrs.emp.name if EMOF_qrs.emp.name != '' else '-' 
                e['employee_id'] = EMOF_qrs.emp.employee_id if EMOF_qrs.emp.employee_id != '' else '-' 
                e['email'] = EMOF_qrs.emp.email if EMOF_qrs.emp.email != '' else '-' 
                e['age'] = EMOF_qrs.emp.age if EMOF_qrs.emp.age != '' else '-' 
                e['gender'] = EMOF_qrs.emp.gender if EMOF_qrs.emp.gender != '' else '-' 
                e['mobile_number'] = EMOF_qrs.emp.mobile_number if EMOF_qrs.emp.mobile_number != '' else '-' 
                e['alternate_mobile_number'] = EMOF_qrs.emp.alternate_mobile_number if EMOF_qrs.emp.alternate_mobile_number != '' else '-' 
                e['blood_group'] = EMOF_qrs.emp.blood_group if EMOF_qrs.emp.blood_group != '' else '-' 
                e['date_of_birth'] = str(EMOF_qrs.emp.date_of_birth if EMOF_qrs.emp.date_of_birth != '' else '-' )
                e['disability'] = EMOF_qrs.emp.disability if EMOF_qrs.emp.disability != '' else '-' 
                e['employee_status'] = EMOF_qrs.emp.employee_status if EMOF_qrs.emp.employee_status != '' else '-' 
                e['marital_status'] = EMOF_qrs.emp.marital_status if EMOF_qrs.emp.marital_status != '' else '-' 
                e['nationality'] = EMOF_qrs.emp.nationality if EMOF_qrs.emp.nationality != '' else '-'

        res = Response()
        if user_role == 'admin' or user_role == 'lead_manager':
            EMOF_data = employee_official.objects.filter(emp__employee_id = employee_id)
            if EMOF_data:
                EMOF_val = EMOF_data.values()
                EMOF_qrs = EMOF_data.first()

                addUserAccountDetails(EMOF_val, EMOF_qrs)

            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'user not found',
                    'data': []
                }

            
        elif user_role == 'bd_tl':
            emp = employee_official.objects.filter(emp=request.user.id).first()
            associates = getAssociate(emp.emp.employee_id)
            print(associates)
            emp_id_list= [a['employee_id'] for a in associates]
            if employee_id in emp_id_list:
                # print('employee_id', employee_id)
                
                EMOF_data = employee_official.objects.filter(emp__employee_id = employee_id, emp__visibility=True)
                if EMOF_data:
                    EMOF_val = EMOF_data.values()
                    EMOF_qrs = EMOF_data.first()
                    addUserAccountDetails(EMOF_val, EMOF_qrs)
                else:
                    res.status_code = status.HTTP_204_NO_CONTENT
                    res.data = {
                        'message': 'not data found',
                        'status': status.HTTP_204_NO_CONTENT,
                        'data': []
                    }
                    return res
            else:
                res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                res.data = {
                    'message': 'you are not authorized to view this user',
                    'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    'data': []
                }
                return res
        elif user_role == 'bd_t_member':
            emp_id = employee_official.objects.filter(emp__id = request.user.id, emp__visibility=True).first()
            if emp_id.emp.employee_id == employee_id:
                EMOF_data = employee_official.objects.filter(emp__employee_id = employee_id, emp__visibility=True)
                if EMOF_data:
                    EMOF_val = EMOF_data.values()
                    EMOF_qrs = EMOF_data.first()
                    addUserAccountDetails(EMOF_val, EMOF_qrs)
            else:
                res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                res.data = {
                    'message': 'you are not authorized to view this user',
                    'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    'data': []
                }
                return res

        serializer = viewUserIndvSerializer(data=EMOF_val[0])
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': serializer.data
            }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
                'data': []
            }
            
        return res
    

    

class deleteUserApprovalWrite(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = deleteUserSerializer
    def delete(self, request, employee_id, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin' or user_role == 'lead_manager' or user_role == 'bd_tl': 
            if not user_delete_approval.objects.filter(employee_id__employee_id = employee_id).exists():
                data = employee_official.objects.filter(emp__employee_id=employee_id, emp__visibility=True).first()
                # print(employee_id)
                if data:
                    lda = user_delete_approval.objects.create(**{'employee_id': data.emp})
                    dynamic = visibility_dynamic_serializer(UserAccount)
                    serializer = dynamic(data.emp, data={'visibility': False}, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    if lda:
                        res.status_code = status.HTTP_201_CREATED
                        res.data = {
                            'status': status.HTTP_201_CREATED,
                            'message': 'sent for approval, this user will be removed after the approval of admin',
                            'data': []
                        }
                else :
                    res.status_code = status.HTTP_400_BAD_REQUEST,
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'employee id do not exists',
                        'data': []
                    }
            else :
                res.status_code = status.HTTP_208_ALREADY_REPORTED
                res.data = {
                    'status': status.HTTP_208_ALREADY_REPORTED,
                    'message': 'already submitted',
                    'data': [] 
                }
        else:
            res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            res.data = {
                'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                'message': 'you are not authorized to delete user',
                'data': []
            }
        return res



class viewAllLeadsSearch(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewAllUserSerializer
    def get(self, request, employee_id, format=None, *args, **kwargs):
        user = request.user
        user_role = getUserRole(user.id)
        data = []
        res =  Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'unauthorized access', 
                'data': [],
            }
        )
        if user_role == 'lead_manager' or user_role == 'admin':
            data = []
            serviceData = employee_official.objects.select_related().filter(emp__employee_id = employee_id, emp__visibility=True)
            if serviceData:
                for sd in serviceData:
                    data.append({'employee_id': sd.emp.employee_id, 'name': sd.emp.name, 'user_role': sd.user_role if sd.user_role !='' else '-' , 'designation': sd.designation if sd.designation !='' else '-' , 'department': sd.department if sd.department !='' else '-' , 'product': sd.product if sd.product !='' else '-'}) 

                serializer = viewAllUserSerializer(data=data, many=True)
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
                return res
        elif user_role == 'bd_tl':
            product = getProduct(user.id)
            data = []
            emp_id = employee_official.objects.filter(emp__id = request.user.id, emp__visibility=True).first()
            emp_id_list = getAssociate(emp_id.emp.employee_id)
            emp_id_list = [a['employee_id'] for a in emp_id_list]
            if employee_id in emp_id_list:
                serviceData = employee_official.objects.select_related().filter(emp__employee_id = employee_id, emp__visibility=True)
                if serviceData:
                    for sd in serviceData:
                        data.append({'employee_id': sd.emp.employee_id, 'name': sd.emp.name, 'user_role': sd.user_role if sd.user_role !='' else '-' , 'designation': sd.designation if sd.designation !='' else '-' , 'department': sd.department if sd.department !='' else '-' , 'product': sd.product if sd.product !='' else '-'}) 

                        serializer = viewAllUserSerializer(data=data, many=True)
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
            else :
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'you are not authorized',
                    'data' : []
                }

        return res






    # 'name': , 'employee_id': , 'email_id': , 'age': , 'gender': , 'mobile_number': , 'alternate_mobile_number': , 'blood_group': , 'date_of_birth': , 'disability': , 'employee_status': , 'marital_status': , 'nationality':
    

class officialDetailsSubmit(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = employee_officialSerializer
    def put(self, request, employee_id, format=None, *args, **kwargs):
        print('wrking here')
        user_role = getUserRole(request.user.id)
        print(user_role)

        res = Response()
        if user_role == 'admin' or user_role == 'lead_manager':
            try:
                data = request.data

                if not data.get('employee_id'):
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'employee_id field is required',
                        'data': []
                    }
                    return res
                if not data.get('department'):
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'department field is required',
                        'data': []
                    }
                    return res
                if not data.get('designation'):
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'designation field is required',
                        'data': []
                    }
                    return res
                if not data.get('product'):
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'product field is required',
                        'data': []
                    }
                    return res
                if not data.get('team_leader'):
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'team_leader field is required',
                        'data' : []
                    }
                    return res
                if not data.get('user_role'):
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'team_leader field is required',
                        'data' : []
                    }
                    return res
                
                UA_data = employee_official.objects.filter(emp__employee_id = data.get('employee_id'), emp__visibility=True).first()
                print(UA_data.id)
                
                del data['employee_id']
                print('data', data)

                serializer = employee_officialSerializer(UA_data, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        "message": 'data saved',
                        'data': serializer.data,
                        'status': status.HTTP_200_OK
                    }
                    return res
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        "message": 'unsuccessful',
                        'data': [],
                        'status': status.HTTP_400_BAD_REQUEST
                    }
                    
            except ValueError as e:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                    'data': []
                    }

        else :
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'you are not authorized for this action',
                'data': []
            }

        return res
    


class viewEmployee(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = allIdentifiersSerializer
    def get(self, request, table, employee_id, format=None, *args, **kwargs):

        user_role = getUserRole(request.user.id)
        res = Response()

        if table == 'useraccount':
            models = apps.get_model('account', table)
        else:
            models = apps.get_model('employees', table)
        
        modelFields = list(getModelFields(models))
        model_fields = [mod for mod in modelFields if mod['type'] != 'ForeignKey' if mod['field'] != 'employee_id']
        serializer_class = models

        if table != 'useraccount':
            lead_ref = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
            if lead_ref:
                employee_id = lead_ref[0].id
                for i in range(len(model_fields)):
                    if model_fields[i]:
                        if model_fields[i]['field'] == 'employee_id':
                            model_fields.pop(i)
                            break
            else:
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid lead id',
                    'data' : []
                }
                return res
        else:
            lead_ref = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
            if not lead_ref:
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid lead id',
                    'data' : []
                }
                return res
                

        if user_role == 'lead_manager' or user_role == 'admin':
            data = ''
            if table != 'useraccount':
                data = models.objects.select_related().filter(emp = employee_id)
            else:
                data = models.objects.select_related().filter(employee_id = employee_id)

            # associate_id = data[0].associate_id.id if data[0].associate_id != None else '' 
            # data = data.values().first()
            # nData = data
            # nData['associate_id'] = associate_id
            # data = list([nData])

            dynamic = dynamic_serializer(models)
            if table == 'useraccount':
                serializer = UserAccountSerializer(data=list(data.values()), many=True)
            else:
                serializer = dynamic(data=list(data.values()), many=True)

            serializer.is_valid(raise_exception=True)
            # print('serializer.data',serializer.data)

            # print(serializer.data)
            s_data = dict(serializer.data[0])
            # print(s_data)

            # if table =='useraccount':
            #     # print('model_fields', model_fields)

            #     for i, m in enumerate(model_fields):
            #             # print(m['field'])
            #             model_fields.pop(i)
            #             # print(i)
                
                
            #     print(model_fields)

                
                # EO_INST = employee_official.objects.filter(emp__id = s_data['associate_id'], emp__visibility=True).first()
                # s_data['associate_id'] = {'name': EO_INST.emp.name if EO_INST!= None else '' , 'pk': s_data['associate_id'] if s_data['associate_id'] !=None else '' }

            #     model_fields.append({'type': 'CharField', 'value': '', 'field': 'associate_id'})
            # print(s_data)
            for i, md in enumerate(model_fields):
                hidden_fields = ['employee_id', 'password' ,'email', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'visibility', 'updated_at']
                if table == 'useraccount' and (md['field'] in hidden_fields):
                    if md['field'] in hidden_fields:
                        model_fields.pop(i)
                    # del md
                elif not md['type'] == 'ForeignKey':
                    print(md)
                    for key in md:
                        # print('data', md['field'])
                        # print(key)
                        # print(md['field'])
                        md['value'] =  s_data[md['field']]
                        break

            
            for mod in model_fields:
                mod['key'] = mod['field']
                del mod['field']

            # print('model_fields',model_fields)
            if table != 'all_identifiers':
                dropdown_fields_data = dropdown_fields.objects.all()
                for m in model_fields:
                    # print(m['key'])
                    for d in dropdown_fields_data:
                        if d.title == m['key']:
                            # print(d.title)
                            m['type'] = 'dropdown'
                            selectBoxData = []
                            if d.ref_tb:
                                m['table'] = d.ref_tb
                                refModel = apps.get_model('dropdown', d.ref_tb)
                                refModelData = refModel.objects.all()
                                for rmd in refModelData:
                                    selectBoxData.append(rmd.title)
                                m['dropdown'] = selectBoxData
                            else:
                                pass

            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': {'data': serializer.data, "current_table": table, 'employee_id': employee_id, 'data_type': model_fields}
                }
        elif user_role == 'bd_tl':
            product = getProduct(request.user.id)
 
            serviceData = service.objects.filter(employee_id = employee_id, service_category = product)
            if serviceData:
                data = models.objects.filter(employee_id = employee_id)
                # print(data)
                data = list(data.values())
                serializer = models(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    "status": status.HTTP_200_OK,
                    'message': 'successful',
                    'data': {'data': serializer.data,"current_table": table, 'employee_id': employee_id, 'field_type': [model_fields]}
                    }
                # return res
        else:
            res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            res.data = {
                "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                'message': 'you are not authorized to see this lead',
                'data': []
                }
        
        return res





class updateEmployee(GenericAPIView):
    # serializer_class = dynamic_employee_update_serializer
    permission_classes = [IsAuthenticated]
    def put(self, request, table, employee_id, format=None, *args, **kwargs):
        main_data = request.data

        OF_data = employee_official.objects.filter(emp = request.user.id).first()
        product = OF_data.product
        user_role = OF_data.user_role

        # print(user_role)
        # user_role = getUserRole(request.user.id)
        # print(user_role)

        res = Response()

        if table == 'useraccount':
            models = apps.get_model('account', table)
            # print(models)
        else:
            models = apps.get_model('employees', table)
        
        # modelFields = list(getModelFields(models))
        # model_fields = [mod for mod in modelFields if mod['type'] != 'ForeignKey' if mod['field'] != 'employee_id']
        # serializer_class = models
        dynamic = dynamic_employee_update_serializer(models)

        if table == 'useraccount':
            # print('working')
            data = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
            # print('lead_ref' , lead_ref)
            if data:
                # print(data)
                serializer = dynamic(data, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'message': 'invalid lead id',
                        'data' : serializer.data
                    }

                else:
                    res.status_code = status.HTTP_403_FORBIDDEN
                    res.data = {
                        'status': status.HTTP_403_FORBIDDEN,
                        'message': 'invalid lead id',
                        'data' : []
                
                }

            #     employee_id = lead_ref[0].id
            #     for i in range(len(model_fields)):
            #         if model_fields[i]:
            #             if model_fields[i]['field'] == 'employee_id':
            #                 model_fields.pop(i)
            #                 break
            else:
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid lead id',
                    'data' : []
                }
            return res
        else:
            lead_ref = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
            if not lead_ref:
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid lead id',
                    'data' : []
                }
                return res
                

        if user_role == 'lead_manager' or user_role == 'admin':
            data = ''
            if table != 'useraccount':
                data = models.objects.select_related().filter(emp = employee_id)
            else:
                data = models.objects.select_related().filter(employee_id = employee_id)

            dynamic = dynamic_serializer(models)

            if table == 'useraccount':
                serializer = UserAccountSerializer(data=list(data.values()), many=True)
            else:
                serializer = dynamic(data=list(data.values()), many=True)

            serializer.is_valid(raise_exception=True)
            s_data = dict(serializer.data[0])

            # for i, md in enumerate(model_fields):
            #     hidden_fields = ['employee_id', 'password' ,'email', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'visibility', 'updated_at']
            #     if table == 'useraccount' and (md['field'] in hidden_fields):
            #         if md['field'] in hidden_fields:
            #             model_fields.pop(i)
            #         # del md
            #     elif not md['type'] == 'ForeignKey':
            #         print(md)
            #         for key in md:
            #             md['value'] =  s_data[md['field']]
            #             break

            
            # for mod in model_fields:
            #     mod['key'] = mod['field']
            #     del mod['field']

            # if table != 'all_identifiers':
            #     dropdown_fields_data = dropdown_fields.objects.all()
            #     for m in model_fields:
            #         for d in dropdown_fields_data:
            #             if d.title == m['key']:
            #                 m['type'] = 'dropdown'
            #                 selectBoxData = []
            #                 if d.ref_tb:
            #                     m['table'] = d.ref_tb
            #                     refModel = apps.get_model('dropdown', d.ref_tb)
            #                     refModelData = refModel.objects.all()
            #                     for rmd in refModelData:
            #                         selectBoxData.append(rmd.title)
            #                     m['dropdown'] = selectBoxData
            #                 else:
            #                     pass

            res.status_code = status.HTTP_200_OK
            res.data = {
                'status': status.HTTP_200_OK,
                'message': 'successful',
                'data': {'data': serializer.data, "current_table": table, 'employee_id': employee_id, 'data_type': model_fields}
                }




        # res = Response()
        # # user = cookieAuth(request)

        # model = apps.get_model('business_leads', table)
        # if model is not None:
        #     dynamic = dynamic_employee_update_serializer(model)

        #     if user_role == 'lead_manager' or user_role == 'admin':
        #         if table != 'all_identifiers':

        #             if table == 'followup':
        #                 main_data['created_by'] = request.user.employee_id

        #             data = model.objects.filter(lead_id__lead_id=lead_id).first()
        #             p_id = data.lead_id.id
        #             main_data['lead_id'] = p_id

        #             serializer = dynamic(data, data=main_data, partial=True)

        #             if serializer.is_valid(raise_exception=True):
        #                 serializer.save()


        #                 if table == 'followup':
        #                     serviceObjData = service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = getLeadStatusInst('follow up'))
        #                     lead_status_instance = lead_status.objects.get(title = 'yet to contact')
        #                     lead_status_record.objects.create(**{'lead_id': serviceObjData.lead_id, 'status': lead_status_instance})
        #                 res.status_code = status.HTTP_200_OK
        #                 res.data = {
        #                     "status":status.HTTP_200_OK,
        #                     "message": 'updations successful',
        #                     "data": {'message' : "changes saved successfully"}
        #                     }
        #             else :
        #                 res.status_code = status.HTTP_400_BAD_REQUEST
        #                 res.data = {
        #                 'status': status.HTTP_400_BAD_REQUEST,
        #                 'message': 'request failed',
        #                 'data': []
        #                 }

        #             return res
                
        #         else:
        #             res.status_code = status.HTTP_400_BAD_REQUEST
        #             res.data = {
        #                 'status': status.HTTP_400_BAD_REQUEST,
        #                 'message': 'you are not authorized to make any changes to all identifiers',
        #                 'data': []
        #                 }
        #             return res


        #     elif user_role == 'bd_tl':
        #         if table != 'all_identifiers':
        #             lead_service_category = all_identifiers.objects.filter(lead_id = lead_id).first()
        #             lead_service_category = lead_service_category.service_category
        #             print(lead_service_category)

        #             if product == lead_service_category:
        #                 # model = apps.get_model('business_leads', table)
        #                 # dynamic = dynamic_serializer_submit(model)

        #                 if table == 'followup':
        #                     main_data['created_by'] = request.user.employee_id

        #                 data = model.objects.filter(lead_id__lead_id=lead_id).first()
        #                 p_id = data.lead_id.id
        #                 print(data)

        #                 if table != 'all_identifiers':
        #                     main_data['lead_id'] = p_id

        #                 serializer = dynamic(data, data=main_data, partial=True)
        #                 if serializer.is_valid(raise_exception=True):
        #                     serializer.save()

        #                     if table == 'followup':
        #                         service.objects.filter(lead_id__lead_id=lead_id).update(lead_status = getLeadStatusInst('follow up'))
        #                         lead_status_instance = lead_status.objects.get(title = 'yet to contact')
        #                         lead_status_record.objects.create(**{'lead_id': serviceObjData.lead_id, 'status': lead_status_instance})

        #                     res.status_code = status.HTTP_200_OK
        #                     res.data = {
        #                         "status":status.HTTP_200_OK,
        #                         "data": 'successful',
        #                         "data": serializer.data
        #                         }
        #                 else :
        #                     res.status_code = status.HTTP_400_BAD_REQUEST
        #                     res.data = {
        #                     'status': status.HTTP_400_BAD_REQUEST,
        #                     'message': 'request failed',
        #                     'data': []
        #                     }

        #                 return res
        #             else:
        #                 res.status_code = status.HTTP_400_BAD_REQUEST
        #                 res.data = {
        #                     'status': status.HTTP_400_BAD_REQUEST,
        #                     'message': 'unauthorized access to this lead',
        #                     'data': []
        #                     }
        #                 return res
        #         else:
        #             res.status_code = status.HTTP_400_BAD_REQUEST
        #             res.data = {
        #                 'status': status.HTTP_400_BAD_REQUEST,
        #                 'message': 'you are not authorized to make any changes to all identifiers',
        #                 'data': []
        #                 }
        #             return res
        #     return res
        # else:
        #     res.status_code = status.HTTP_400_BAD_REQUEST
        #     res.data = {
        #         'status': status.HTTP_400_BAD_REQUEST,
        #         'message': 'the table do not exists',
        #         'data': []
        #         }
        #     return res
    


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