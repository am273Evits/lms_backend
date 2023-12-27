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
from records.models import user_delete_approval
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
            EMOF_arr = []
            EMOF_data = employee_official.objects.all()[offset: offset + limit]
            for d in EMOF_data:
                EMOF_arr.append({"employee_id": d.emp.employee_id, 'name': d.emp.name, 'user_role': d.user_role if d.user_role != '' else '-', 'designation': d.designation if d.designation != '' else '-', 'department': d.department if d.department != '' else '-', 'product': d.product if d.product != '' else '-'})
            
            serializer = viewAllUserSerializer(data=EMOF_arr, many=True)
            if serializer.is_valid(raise_exception=True):
                print('serializer.data',serializer.errors)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'message': 'successful',
                    "data": serializer.data,
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
                
                EMOF_data = employee_official.objects.filter(emp__employee_id = employee_id)
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
            emp_id = employee_official.objects.filter(emp__id = request.user.id).first()
            if emp_id.emp.employee_id == employee_id:
                EMOF_data = employee_official.objects.filter(emp__employee_id = employee_id)
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
    def delete(self, request, employee_id, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin' or user_role == 'lead_manager' or user_role == 'bd_tl': 
            if not user_delete_approval.objects.filter(employee_id__employee_id = employee_id).exists():
                data = employee_official.objects.filter(emp__employee_id=employee_id).first()
                # print(employee_id)
                if data:
                    lda = user_delete_approval.objects.create(**{'employee_id': data.emp})
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
            serviceData = employee_official.objects.select_related().filter(emp__employee_id = employee_id)
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
            emp_id = employee_official.objects.filter(emp__id = request.user.id).first()
            emp_id_list = getAssociate(emp_id.emp.employee_id)
            emp_id_list = [a['employee_id'] for a in emp_id_list]
            if employee_id in emp_id_list:
                serviceData = employee_official.objects.select_related().filter(emp__employee_id = employee_id)
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
                
                UA_data = employee_official.objects.filter(emp__employee_id = data.get('employee_id')).first()
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