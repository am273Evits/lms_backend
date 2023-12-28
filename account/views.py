from django.shortcuts import render
from django.apps import apps
from django.db.models import fields
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.generics import GenericAPIView
from .models import UserAccount
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
import random

from employees.models import *
from dropdown.models import user_links, lead_status, ev_department, ev_designation, user_role_list


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


def getProduct(id):
    user = employee_official.objects.get(emp = id)
    return user.product

def getUserRole(id):
    user = employee_official.objects.get(emp = id)
    return user.user_role

def getTeamLeader(emp):
    data = employee_official.objects.filter(emp__employee_id = emp).first()
    return data.team_leader

def getTeamLeaderInst(emp):
    data = employee_official.objects.filter(emp__employee_id = emp).first()
    tl = employee_official.objects.filter(emp__employee_id = data.team_leader).first()
    return tl

def getLeadStatusInst(status):
    data = lead_status.objects.filter(title = status).first().id
    # print(data)
    return data

def getLeadId():
    date = datetime.now()
    date = date.strftime('%Y%m%d%H%M%S%f')
    random_int = random.randint(100,499) + random.randint(100,499)
    lead_id = f'L{str(date) + str(random_int)}'
    return lead_id

def getServiceId():
    date = datetime.now()
    date = date.strftime('%Y%m%d%H%M%S%f')
    random_int = random.randint(100,499) + random.randint(100,499)
    lead_id = f'S{str(date) + str(random_int)}'
    return lead_id


def getClientId():
    date = datetime.now()
    date = date.strftime('%Y%m%d%H%M%S%f')
    random_int = random.randint(100,499) + random.randint(100,499)
    lead_id = f'C{str(date) + str(random_int)}'
    return lead_id

def getAssociates(emp):
    datalist = []
    data = employee_official.objects.filter(team_leader=emp)
    for d in data:
        datalist.append({'employee_id': d.emp.employee_id, 'name': d.emp.name, 'user_role': d.user_role, 'emp': d.emp.id})
    return datalist


def getModelFields(model):
    allfields = []
    for f in model._meta.get_fields():
        if isinstance(f, fields.AutoField):
            continue
        allfields.append({'field': f.name, 'type': f.get_internal_type()})
    return allfields


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
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            try:
               UserAccount.objects.get(email=email, visibility=True)
            except:
               return Response({'status': status.HTTP_404_NOT_FOUND,'message':'no user account with this email id','data':[]}, status=status.HTTP_404_NOT_FOUND)          
            
            user=authenticate(email=email,password=password)
            res = Response()
            if user.visibility:
                if user is not None:
                    token=get_tokens_for_user(user)
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status': status.HTTP_200_OK,
                        'message': "registrations successful",
                        'data': {'user_details': user_VF(user.id),"token": token, "user_links": userSpecificLinkHeader(user.id)},
                    } 
                else:
                    res.status_code =status.HTTP_404_NOT_FOUND
                    res.data = {'status': status.HTTP_404_NOT_FOUND,'message':'Email or password is not Valid','data':{}}
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status': status.HTTP_200_OK,
                    'message': 'user is inactive, please contact administrator',
                    'data': []
                }
            return res
         

class registration_VF(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = registrationSerializer
    def post(self, request, format=None, *args, **kwargs):
        # EMOF_data = employee_official.objects.get(emp__id = request.user.id)
        Muser_role = getUserRole(request.user.id)
        res = Response()
        if Muser_role == 'admin' or Muser_role == 'lead_manager':

            employee_id = request.data.get('employee_id')
            name = request.data.get('name')
            designation = request.data.get('designation')
            department = request.data.get('department')
            user_role = request.data.get('user_role')

            if Muser_role == 'lead_manager':
                if user_role == 'admin':
                    res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                    res.data = {"status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, "message": "you are not authorized to create admin user, please select a different user role", 'data': [] }
                    return res
    
            data = request.data
    
            if employee_id == None:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {"status": status.HTTP_400_BAD_REQUEST, "message": "employee_id field id is required", 'data': [] }
                # return Response(, status = status.HTTP_400_BAD_REQUEST)
            if name == None:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "name field is required", 'data': [] }
                return res
            if department == None:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "department is required", 'data': [] }
                return res
            elif not ev_department.objects.filter(title = department):
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "invalid field department", 'data': [] }
                return res
            if designation == None:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "designation is required", 'data': [] }
                return res
            elif not ev_designation.objects.filter(department__title = department, title__title = designation) :
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "invalid field designation", 'data': [] }
                return res
            if user_role == None:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "user role is required", 'data': [] }
                return res
            elif not user_role_list.objects.filter(title = user_role):
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "invalid field user role", 'data': [] }
                return res
            
    
    
            serializer = registrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
    
            date = datetime.now()
            date = date.strftime("%Y-%m-%d")
    
            employee_official.objects.create(emp = user, joining_date = date, department = department, designation = designation, user_role = user_role)
    
            if user is not None:
                res.status_code = status.HTTP_201_CREATED
                res.data = {"status": status.HTTP_201_CREATED, "message": "user registered", 'data': [] }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "user not registered", 'data':[]}
                # return Response(, status=status.HTTP_404_NOT_FOUND)
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "you are not authorized to create a user", 'data':[]}

        return res
        


def userSpecificLinkHeader(user_id):
    usr_role = employee_official.objects.filter(emp = user_id).first()
    usr_role = usr_role.user_role
    links = user_links.objects.filter(access_department = usr_role, link_status = True)
    usr_link = []
    for link in links:
        usr_link.append({"title": link.title, 'navigation': link.user_link })
    serializer = userSpecificLinkSerializer(data=usr_link, many=True)
    if serializer.is_valid(raise_exception=True):
        return serializer.data
    else:        
        return "unsuccessful"

def user_VF(id):
    user = employee_official.objects.get(emp=id)
    data = {
        'user_role' : user.user_role if user.user_role != '' else '-' ,
        'product' : user.product if user.product != '' else '-',
        'name' : user.emp.name,
        'employee_id' : user.emp.employee_id,
        'email' : user.emp.email,
    }
    serializer = userSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return  {'user': serializer.data}
