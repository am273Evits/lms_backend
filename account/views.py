from django.shortcuts import render
from django.apps import apps
from django.db.models import fields
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
import random
import math
from django.core.mail import EmailMultiAlternatives


# from employees.models import *
# from dropdown.models import user_links, lead_status, ev_department, ev_designation, user_role_list


from account.models import UserAccount
from leads.models import Program
from leads.views import resFun



# def cookieAuth(request):
#     token = request.COOKIES.get('session')
#     print('token', request.COOKIES)
#     if token is None:
#         raise AuthenticationFailed('unauthenticated')
#     try:
#         payload = jwt.decode(token, 'secret', 'HS256')
#         # print('payload', payload)
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('unauthenticated')
#     id = payload['id']
#     user = Users.objects.filter(id=id).first()
#     return {'user': user, 'id': id}


# def getProduct(id):
#     user = employee_official.objects.get(emp = id)
#     return user.product

def getUserDepartment(id):
    user = UserAccount.objects.get(id = id)
    return user.department

def getUserDesignation(id):
    user = UserAccount.objects.get(id = id)
    return user.designation

# def getTeamLeader(emp):
#     data = employee_official.objects.filter(emp__employee_id = emp).first()
#     return data.team_leader

# def getTeamLeaderInst(emp):
#     data = employee_official.objects.filter(emp__employee_id = emp).first()
#     tl = employee_official.objects.filter(emp__employee_id = data.team_leader).first()
#     return tl

# def getLeadStatusInst(status):
#     data = lead_status.objects.filter(title = status).first().id
#     # print(data)
#     return data

def getLeadId():
    date = datetime.now()
    date = date.strftime('%Y%m%d%H%M%S%f')
    random_int = random.randint(100,499) + random.randint(100,499)
    lead_id = f'L{str(date) + str(random_int)}'
    return lead_id

# def getServiceId():
#     date = datetime.now()
#     date = date.strftime('%Y%m%d%H%M%S%f')
#     random_int = random.randint(100,499) + random.randint(100,499)
#     lead_id = f'S{str(date) + str(random_int)}'
#     return lead_id


# def getClientId():
#     date = datetime.now()
#     date = date.strftime('%Y%m%d%H%M%S%f')
#     random_int = random.randint(100,499) + random.randint(100,499)
#     lead_id = f'C{str(date) + str(random_int)}'
#     return lead_id

# def getAssociates(emp):
#     datalist = []
#     data = employee_official.objects.filter(team_leader=emp)
#     for d in data:
#         datalist.append({'employee_id': d.emp.employee_id, 'name': d.emp.name, 'user_role': d.user_role, 'emp': d.emp.id})
#     return datalist

# def getModelFields(model):
#     allfields = []
#     for f in model._meta.get_fields():
#         if isinstance(f, fields.AutoField):
#             continue
#         allfields.append({'field': f.name, 'type': f.get_internal_type()})
#     return allfields




class IgnoreBearerTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']

            if auth_header.startswith('Bearer'):
                return None
        return super().authenticate(request)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

class LoginView(GenericAPIView):
    serializer_class=loginSerializer
    authentication_classes = [IgnoreBearerTokenAuthentication]
    def post(self,request,format=None):
        serializer=loginSerializer(data=request.data)
        res = Response()
        if serializer:
            if serializer.is_valid(raise_exception=True):
                email=serializer.data.get('email')  
                password=serializer.data.get('password')
                try:
                   UserAccount.objects.get(email=email, visibility=True)
                except:
                   return Response({'status': status.HTTP_404_NOT_FOUND,'message':'no user account with this email id','data':[]}, status=status.HTTP_404_NOT_FOUND)          

                user=authenticate(email=email,password=password)
                if user is not None:
                    if user.visibility:
                        print(user)
                        token=get_tokens_for_user(user)
                        # print(token)
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'message': "registrations successful",
                            'data': {'user_details': user_VF(user.id),"token": token},
                            # 'data': {'user_details': user_VF(user.id),"token": token, "user_links": userSpecificLinkHeader(user.id)},
                        } 
                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'message': 'user is inactive, please contact administrator',
                            'data': []
                        }
                else:
                        res.status_code =status.HTTP_404_NOT_FOUND
                        res.data = {'status': status.HTTP_404_NOT_FOUND,'message':'Email or password is not Valid','data':{}}
                return res
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_200_OK,
                'message': serializer.errors if serializer.errors else 'login failed',
                'data': []
            }
        


class registration_VF(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminRegistrationSerializer
    def post(self, request, format=None, *args, **kwargs):
        # EMOF_data = employee_official.objects.get(emp__id = request.user.id)
        userDepartment = getUserDepartment(request.user.id)
        userDesignation = getUserDesignation(request.user.id)
        serializer = ''

        userDepartment = str(userDepartment.title)
        # userDesignation = str(userDesignation.title)
        res = Response()

        existing_user  = UserAccount.objects.filter(employee_id = request.data.get('employee_id').lower())
        if existing_user.exists():
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'data': [],
                'message': 'user already registered with this employee id, please contact admin'
            }
            return res


        if userDepartment == None:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'data': [],
                'message': 'User Department not set, please contact admin'
            }
            return res

        elif userDepartment == 'director':
            serializer = AdminRegistrationSerializer(data = request.data)
        
        elif userDepartment == 'lead_management' and userDesignation == 'lead_manager':
            # print('request.user', request.data)
            serializer = LeadManagerRegistrationSerializer(data = request.data)

        if not serializer == '':
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                # data = {}
                # data['name'] = request.POST['name']
                # data['contact_number'] = request.POST['contact_number']
                # data['email_id'] = request.POST['email_id']
                # data['client_token'] = generate_random_code()
                # upload = AddClientForm(data)
                # if upload.is_valid():
                #     instance = upload.save()
        
                print('upload.data',serializer.data['email'])
                ua_ser = UserAccount.objects.filter(email=serializer.data['email']).first()

                message = canned_email.objects.get(email_type = 'welcome_email')
                message = message.email
                message = str(message).replace("{{{link}}}", f'<a href="http://127.0.0.1:8000/account/generate_password/{ua_ser.pk}/{ua_ser.user_pwd_token}">fill more details</a>')
    
                email_id = ua_ser.email
    
                subject = 'Welcome to Evitamin!'
                from_email = 'akshatnigamcfl@gmail.com'
                recipient_list = [email_id]
                text = 'email sent from MyDjango'
    
                # if send_mail(subject, message, from_email, recipient_list):
    
                email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
                email.attach_alternative(message, 'text/html')
                # email.attach_file('files/uploadFile_0dTGU7A.csv', 'text/csv')
                email.send()


                
                #welcome email to the user, authentication

                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status' : status.HTTP_200_OK,
                    'message' : 'registration successful',
                    'data': serializer.data
                }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'registration failed',
                    'data': [] 
                }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status' : status.HTTP_400_BAD_REQUEST,
                'message' : serializer.errors if not serializer=='' else 'registration failed',
                'data': [] 
            }
        return res
    


class view_users(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewUserSerializer
    def get(self, request, page, format=None, *args, **kwargs):
        limit = 10
        offset = int((page - 1) * limit)
        
        res = Response()
        if str(request.user.department) == 'director' or str(request.user.department) == 'lead_management' and str(request.user.designation) == 'lead_manager':
            users = UserAccount.objects.filter(visibility=True)[offset: offset+limit]
            count = math.ceil(UserAccount.objects.all().count() / 10)
            if users.exists():
                data = []
                for u in users:
                    # print(u.id)
                    data.append({
                        'id': u.id ,
                        'employee_id': u.employee_id, 
                        'name': u.name if u.name else '-', 
                        'email_id': u.email if u.email else '-', 
                        'designation': {'designation_id':u.designation.id,'designation': u.designation.title} if u.designation else {'designation_id':'','designation':''}, 
                        'department': {'department_id': u.department.id, 'department': u.department.title} if u.department else {'department_id':'','department': ''},
                        # 'program': {'program_id': u.program.id, 'program': u.program.title} if u.program else {'program_id':'','program': ''},
                        'employee_status': {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id': 0,'employee_status': ''}
                        # {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id':'','employee_status': ''}
                        })
                    
                serializer = viewUserSerializer(data=data, many=True)
                if serializer.is_valid():
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'data': {"data": serializer.data, 'current_page': page, 'total_pages': count},
                        'message': 'request successful',
                        'status': status.HTTP_200_OK
                    }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'data': serializer.errors,
                        'message': 'request failed',
                        'status': status.HTTP_400_BAD_REQUEST
                    }    
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': {'data': [], 'current_page': page, 'total_pages': count},
                    'message': 'no data found',
                    'status': status.HTTP_400_BAD_REQUEST
                }

        # elif :




        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'data': [],
                'message': 'you are not authorized to view this data',
                'status': status.HTTP_400_BAD_REQUEST
            }
        return res
    


class view_users_archive(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewUserSerializer
    def get(self, request, page, format=None, *args, **kwargs):
        limit = 10
        offset = int((page - 1) * limit)
        
        res = Response()
        if str(request.user.department) == 'director' or str(request.user.department) == 'lead_management' and str(request.user.designation) == 'lead_manager':
            users = UserAccount.objects.filter(visibility=False)[offset: offset+limit]
            count = math.ceil(UserAccount.objects.all().count() / 10)
            if users.exists():
                data = []
                for u in users:
                    # print(u.id)
                    data.append({
                        'id': u.id ,
                        'employee_id': u.employee_id, 
                        'name': u.name if u.name else '-', 
                        'email_id': u.email if u.email else '-', 
                        'designation': {'designation_id':u.designation.id,'designation': u.designation.title} if u.designation else {'designation_id':'','designation':''}, 
                        'department': {'department_id': u.department.id, 'department': u.department.title} if u.department else {'department_id':'','department': ''},
                        # 'program': {'program_id': u.program.id, 'program': u.program.title} if u.program else {'program_id':'','program': ''},
                        'employee_status': {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id': 0,'employee_status': ''}
                        # {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id':'','employee_status': ''}
                        })
                    
                serializer = viewUserSerializer(data=data, many=True)
                if serializer.is_valid():
                    res = resFun(status.HTTP_200_OK,'request successful',{"data": serializer.data, 'current_page': page, 'total_pages': count})
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',serializer.errors)
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no data found',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized to view this data',[])
        return res



class view_users_search(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewUserSerializer
    def get(self, request, searchAtr ,id, format=None, *args, **kwargs):
        res = Response()
        if str(request.user.department) == 'director' or str(request.user.department) == 'lead_manager' and str(request.user.designation) == 'lead_management':
            if searchAtr == 'name':
                name = id.replace('_',' ')
                user = UserAccount.objects.filter(name__contains = name, visibility=True)
            elif searchAtr == 'employee_id':
                user = UserAccount.objects.filter(employee_id__contains = id, visibility=True)
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'message': 'invalid search term',
                    'status': status.HTTP_400_BAD_REQUEST
                }
                return res

            if user.exists():
                data = []
                for u in user:
                    data.append({
                        'id': u.id ,
                        'employee_id': u.employee_id, 
                        'name': u.name if u.name else '-', 
                        'email_id': u.email if u.email else '-', 
                        # 'designation': u.designation.title if u.designation else '-', 
                        # 'department': u.department.title if u.department else '-',

                        # 'employee_id': u.employee_id, 
                        # 'name': u.name if u.name else '-', 
                        'designation': {'designation_id':u.designation.id,'designation': u.designation.title} if u.designation else {'designation_id':'','designation':''}, 
                        'department': {'department_id': u.department.id, 'department': u.department.title} if u.department else {'designation_id':'','designation': ''},
                        # 'program': {'program_id': u.program.id, 'program': u.program.title} if u.program else {'designation_id':'','designation': ''},
                        'employee_status': {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id': 0,'employee_status': ''}
                        # {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id':'','employee_status': ''}

                        })

                serializer = viewUserSerializer(data=data, many=True)
                if serializer.is_valid(raise_exception=True):
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'data': serializer.data,
                        'message': 'request successful',
                        'status': status.HTTP_200_OK
                    }  
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'data': [],
                        'message': 'no user found',
                        'status': status.HTTP_400_BAD_REQUEST
                    }  

            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'message': 'no user found',
                    'status': status.HTTP_400_BAD_REQUEST
                }         
  
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'data': [],
                'message': 'you are not authorized to view this data',
                'status': status.HTTP_400_BAD_REQUEST
            }
        return res
    


class view_users_archive_search(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewUserSerializer
    def get(self, request, searchAtr ,id, format=None, *args, **kwargs):
        res = Response()
        if str(request.user.department) == 'director' or str(request.user.department) == 'lead_manager' and str(request.user.designation) == 'lead_management':
            if searchAtr == 'name':
                name = id.replace('_',' ')
                user = UserAccount.objects.filter(name__contains = name, visibility=False)
            elif searchAtr == 'employee_id':
                user = UserAccount.objects.filter(employee_id__contains = id, visibility=False)
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'message': 'invalid search term',
                    'status': status.HTTP_400_BAD_REQUEST
                }
                return res

            if user.exists():
                data = []
                for u in user:
                    data.append({
                        'id': u.id ,
                        'employee_id': u.employee_id, 
                        'name': u.name if u.name else '-', 
                        'email_id': u.email if u.email else '-', 
                        # 'designation': u.designation.title if u.designation else '-', 
                        # 'department': u.department.title if u.department else '-',
                        # 'employee_id': u.employee_id, 
                        # 'name': u.name if u.name else '-', 
                        'designation': {'designation_id':u.designation.id,'designation': u.designation.title} if u.designation else {'designation_id':'','designation':''}, 
                        'department': {'department_id': u.department.id, 'department': u.department.title} if u.department else {'designation_id':'','designation': ''},
                        # 'program': {'program_id': u.program.id, 'program': u.program.title} if u.program else {'designation_id':'','designation': ''},
                        'employee_status': {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id': 0,'employee_status': ''}
                        # {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id':'','employee_status': ''}

                        })

                serializer = viewUserSerializer(data=data, many=True)
                if serializer.is_valid(raise_exception=True):
                    res = resFun(status.HTTP_200_OK,'request successful',serializer.data)
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'no user found',[])

            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'no user found',[])
  
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized to view this data',[])
        return res    



# class view_users_individual(GenericAPIView):
#     serializer_class = viewUserIndividualSerializer
#     permission_classes = [IsAuthenticated]
#     def get(self, request, employee_id ,format=None, *args, **kwargs):
#         res = Response()
#         if request.user.department.title =='director' and request.user.designation.title == 'super admin' or request.user.department.title =='lead_management' and request.user.designation.title == 'lead_manager':
#             user = UserAccount.objects.filter(employee_id = employee_id, visibility=True)
#             if user.exists():
#                 data=[]
#                 for u in user:
#                     data.append({
#                         'id': u.id ,
#                         'employee_id': u.employee_id, 
#                         'name': u.name if u.name else '-', 
#                         'designation': {'designation_id':u.designation.id,'designation': u.designation.title} if u.designation else {'designation_id':'','designation':''}, 
#                         'department': {'department_id': u.department.id, 'department': u.department.title} if u.department else {'designation_id':'','designation': ''},
#                         'product': {'product_id': u.product.id, 'product': u.product.title} if u.product else {'designation_id':'','designation': ''},
#                         'employee_status': {'employee_status_id': u.employee_status.id, 'employee_status': u.employee_status.title} if u.employee_status else {'employee_status_id':'','employee_status': ''}
#                         # 'employee_id': u.employee_id, 
#                         # 'name': u.name if u.name else '-', 
#                         # 'email_id': u.email if u.email else '-', 
#                         # 'department': [{'department': u.department.title, 'id': int(u.department.id)}] if u.department else [{'department': '-', 'id': '-'}], 
#                         # 'designation': [{'designation': u.designation.title, 'id': int(u.designation.id)}] if u.designation else [{'designation': '-', 'id': '-'}], 
#                         # 'product': [{'product': u.product.title, 'id': int(u.product.id)}] if u.product else [{'product': '-', 'id': '-'}], 
#                         # 'employee_status': [{'employee_status' : u.employee_status.title, 'id': int(u.employee_status.id)}] if u.employee_id else [{'employee_status': '-', 'id': '-'}]
#                         })

#                 serializer = viewUserIndividualSerializer(data=data, many=True)
#                 if serializer.is_valid(raise_exception=True):
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'data': serializer.data,
#                         'message': 'request successful',
#                         'status': status.HTTP_200_OK
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'data': [],
#                         'message': 'request failed',
#                         'status': status.HTTP_400_BAD_REQUEST
#                     }

#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'data': [],
#                     'message': 'no data found',
#                     'status': status.HTTP_400_BAD_REQUEST
#                 }

#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'data': [],
#                 'message': 'you are not authorized to view this data',
#                 'status': status.HTTP_400_BAD_REQUEST
#             }
#         return res
    

class user_update(GenericAPIView):
    serializer_class = updateUserSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, employee_id ,format=None, *args, **kwargs):

        # print(request.user)
        res = Response()
        if request.user.department.title == 'director' or request.user.department.title == 'lead_management' and request.user.designation.title == 'lead_manager':
            user = UserAccount.objects.filter(employee_id = employee_id)
            
            if request.user.department.title == 'lead_management' and request.user.designation.title == 'lead_manager':
                if user.first().department.title == 'director':
                    raise serializers.ValidationError('you are not authorized to make changes to this user')


            print('user', user)
            if user.exists():
                new_data = {key: values for key, values in request.data.items() if values != '-'}
                serializer = updateUserSerializer(user.first(), data=new_data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res.status_code = status.HTTP_200_OK  
                    res.data = {
                        'data': serializer.data,
                        'message': 'changes saved successfully',
                        'status': status.HTTP_200_OK    
                    }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'data': [],
                        'message': serializer.errors if serializer.errors else 'request data',
                        'status': status.HTTP_400_BAD_REQUEST
                    }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'message': 'invalid employee id',
                    'status': status.HTTP_400_BAD_REQUEST
                }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'data': [],
                'message': 'you are not authorized to view this data',
                'status': status.HTTP_400_BAD_REQUEST
            }
        return res



class delete_user(GenericAPIView):
    serializer_class = userDeleteSerializer
    permission_classes = [IsAuthenticated]
    def delete(self, request, employee_id ,format=None, *args, **kwargs):
        
        res = Response()
        if request.user.department.title == 'director':
            user = UserAccount.objects.filter(employee_id = employee_id)
            if user.exists():
                serializer = userDeleteSerializer(user.first(), data={'visibility': False}, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'data': [],
                        'message': 'user deleted successfully',
                    }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'data': [],
                        'message': 'request failed',
                        'status': status.HTTP_400_BAD_REQUEST
                    }

            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'message': 'invalid employee id',
                    'status': status.HTTP_400_BAD_REQUEST
                }
        
        elif request.user.department.title == 'lead_management' or request.user.designation.title == 'lead_manager':

            user = UserAccount.objects.get(employee_id = employee_id)            
            if user:
                user_del_ch = user_delete.objects.filter(user=user.id)
                if user_del_ch:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'data': [],
                        'message': 'already submitted',
                    }
                    return res
                else:
                    serializer = userDeleteSerializer(user, data={'visibility': False}, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        user_delete.objects.create(user = user)
                        res.status_code = status.HTTP_200_OK
                        res.data = {
                            'status': status.HTTP_200_OK,
                            'data': [],
                            'message': 'sent for approval, user will be deleted after admin approval',
                        }

                    else:
                        res.status_code = status.HTTP_400_BAD_REQUEST
                        res.data = {
                            'data': [],
                            'message': 'request failed',
                            'status': status.HTTP_400_BAD_REQUEST
                        }

            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'data': [],
                    'message': 'invalid employee id',
                    'status': status.HTTP_400_BAD_REQUEST
                }

        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'data': [],
                'message': 'you are not authorized to view this data',
                'status': status.HTTP_400_BAD_REQUEST
            }
        return res





            # print('data saved')


        #     if Muser_role == 'lead_manager':
        #         if user_role == 'admin':
        #             res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        #             res.data = {"status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, "message": "you are not authorized to create admin user, please select a different user role", 'data': [] }
        #             return res
    
        #     data = request.data
    

            
    
    
        #     serializer = registrationSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     user = serializer.save()
    
        #     date = datetime.now()
        #     date = date.strftime("%Y-%m-%d")
    
        #     employee_official.objects.create(emp = user, joining_date = date, department = department, designation = designation, user_role = user_role)
    
        #     if user is not None:
        #         res.status_code = status.HTTP_201_CREATED
        #         res.data = {"status": status.HTTP_201_CREATED, "message": "user registered", 'data': [] }
        #     else:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "user not registered", 'data':[]}
        #         # return Response(, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     res.status_code = status.HTTP_400_BAD_REQUEST
        #     res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "you are not authorized to create a user", 'data':[]}

        # return res



        # res = Response()
        # if Muser_role == 'admin' or Muser_role == 'lead_manager':

        #     employee_id = request.data.get('employee_id')
        #     name = request.data.get('name')
        #     designation = request.data.get('designation')
        #     department = request.data.get('department')
        #     user_role = request.data.get('user_role')

        #     if Muser_role == 'lead_manager':
        #         if user_role == 'admin':
        #             res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        #             res.data = {"status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, "message": "you are not authorized to create admin user, please select a different user role", 'data': [] }
        #             return res
    
        #     data = request.data
    
        #     if employee_id == None:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data = {"status": status.HTTP_400_BAD_REQUEST, "message": "employee_id field id is required", 'data': [] }
        #         # return Response(, status = status.HTTP_400_BAD_REQUEST)
        #     if name == None:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "name field is required", 'data': [] }
        #         return res
        #     if department == None:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "department is required", 'data': [] }
        #         return res
        #     elif not ev_department.objects.filter(title = department):
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "invalid field department", 'data': [] }
        #         return res
        #     if designation == None:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "designation is required", 'data': [] }
        #         return res
        #     elif not ev_designation.objects.filter(department__title = department, title__title = designation) :
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "invalid field designation", 'data': [] }
        #         return res
        #     if user_role == None:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "user role is required", 'data': [] }
        #         return res
        #     elif not user_role_list.objects.filter(title = user_role):
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "invalid field user role", 'data': [] }
        #         return res
            
    
    
        #     serializer = registrationSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     user = serializer.save()
    
        #     date = datetime.now()
        #     date = date.strftime("%Y-%m-%d")
    
        #     employee_official.objects.create(emp = user, joining_date = date, department = department, designation = designation, user_role = user_role)
    
        #     if user is not None:
        #         res.status_code = status.HTTP_201_CREATED
        #         res.data = {"status": status.HTTP_201_CREATED, "message": "user registered", 'data': [] }
        #     else:
        #         res.status_code = status.HTTP_400_BAD_REQUEST
        #         res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "user not registered", 'data':[]}
        #         # return Response(, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     res.status_code = status.HTTP_400_BAD_REQUEST
        #     res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "you are not authorized to create a user", 'data':[]}

        # return res
    

class unarchive_user(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=userUnarchiveSerializer
    def put(self, request, employee_id ,format=None, *args, **kwargs):
        res = Response()
        if request.user.department.title == 'director':
            user = UserAccount.objects.filter(employee_id = employee_id)
            if user.exists():
                serializer = userDeleteSerializer(user.first(), data={'visibility': True}, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res = resFun(status.HTTP_200_OK,'user restored successfully',[])
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
            else:     
                res = resFun(status.HTTP_400_BAD_REQUEST,'invalid employee id',[])

        
        # elif request.user.department.title == 'lead_management' or request.user.designation.title == 'lead_manager':

        #     user = UserAccount.objects.get(employee_id = employee_id)            
        #     if user:
        #         user_del_ch = user_delete.objects.filter(user=user.id)
        #         if user_del_ch:
        #             res = resFun(status.HTTP_400_BAD_REQUEST,'already submitted',[])
        #             return res
        #         else:
        #             serializer = userDeleteSerializer(user, data={'visibility': False}, partial=True)
        #             if serializer.is_valid(raise_exception=True):
        #                 serializer.save()
        #                 user_delete.objects.create(user = user)
        #                 res = resFun(status.HTTP_400_BAD_REQUEST,'sent for approval, user will be deleted after admin approval',[])
        #             else:
        #                 res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
        #     else:
        #         res = resFun(status.HTTP_400_BAD_REQUEST,'invalid employee id',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized to view this data',[])
        return res
    


# def UserLinks(user_id):
#     department = UserAccount.objects.filter(id = user_id).first()
#     usr_role = usr_role.user_role
#     links = user_links.objects.filter(access_department = usr_role, link_status = True)
#     usr_link = []
#     for link in links:
#         usr_link.append({"title": link.title, 'navigation': link.user_link })
#     serializer = userSpecificLinkSerializer(data=usr_link, many=True)
#     if serializer.is_valid(raise_exception=True):
#         return serializer.data
#     else:        
#         return "unsuccessful"



def user_VF(id):
    user = UserAccount.objects.get(id=id)
    # print(user.program)
    data = {
        # 'program' : user.program.program if user and user.program and user.program.program != '' else '-',
        'department' : user.department.title if user and user.department and user.department.title != '' else '-',
        'designation' : user.designation.title if user and user.designation and user.designation.title != '' else '-',
        'name' : user.name,
        'employee_id' : user.employee_id,
        'email' : user.email,
    }

    serializer = userSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return  {'user': serializer.data}



def GeneratePassword(request, id, token):

    try:
        user = UserAccount.objects.get(id=id,user_pwd_token=token)

        if request.POST:
            password = request.POST.get('password')
            repeat_password = request.POST.get('repeat_password')
            if password != repeat_password:
                return render(request, 'generate_password.html', {'data': user, "error":"password & repeat password doesn't match" })
            else:
                user.user_pwd_token=generate_random_code()
                user.password = make_password(password)
                user.save()
                return render(request, 'generate_password.html', {'data': user, "success":"password updated successfully" })
            
    except:
        return render(request, 'generate_password.html', {'data': 'no data found', "link_error":"link is invalid or expired!" })
        

    # print(id, token)
    # print('user',user)

    return render(request, 'generate_password.html', {'data': user})
