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
from dropdown.models import user_links


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
    # # print('working till here')
    # print(emp.id)
    # # user = UserAccount.objects.filter(employee_id = emp).first()
    # # user_id = user.id
    # product = employee_official.objects.select_related.filter(emp = emp).first()
    # # print(product)
    # return "sdfsdf"

def getTeamLeader(emp):
    data = employee_official.objects.filter(emp__employee_id = emp).first()
    return data.team_leader

def getLeadId():
    date = datetime.now()
    date = date.strftime('%Y%m%d%H%M%S%f')
    random_int = random.randint(100,499) + random.randint(100,499)
    lead_id = f'L{str(date) + str(random_int)}'
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
        datalist.append({'employee_id': d.emp.employee_id, 'name': d.emp.name, 'user_role': d.user_role })
    # data = list(data.values())
    # print(data[0])
    return datalist
    # print('data, emp',data)
    # pass 
    # emp_list = []
    # for d in data:
    #     associate_data = employee_basic.objects.filter(employee_id = d['employee_id']).first()
    #     emp_list.append({'employee_id' : associate_data.employee_id, 'name' : associate_data.name})
    # return emp_list


def getModelFields(model):
    allfields = []
    for f in model._meta.get_fields():
        if isinstance(f, fields.AutoField):
            continue
        allfields.append({'field': f.name, 'type': f.get_internal_type()})
    return allfields


    # print(emp_list)
    # return 

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         "access" : str(refresh),
#         "refresh": str(refresh.access_token)
#     }










class IgnoreBearerTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Check if the "Authorization" header is present in the request
        if 'Authorization' in request.headers:
            # Get the value of the "Authorization" header
            auth_header = request.headers['Authorization']

            # If the header starts with "Bearer", ignore it and return None for authentication
            if auth_header.startswith('Bearer'):
                return None

        # Return the result of the super method, even if it's None
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
               user_obj=UserAccount.objects.get(email=email)
            except:
               return Response({'status': status.HTTP_404_NOT_FOUND,'message':'Please Registerd user first','data':{"xyz":"123"}}, status=status.HTTP_404_NOT_FOUND)          
            user=authenticate(email=email,password=password)

            res = Response()
            if user is not None:
                token=get_tokens_for_user(user)
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': 200,
                    'message': "registrations successful",
                    'data': {'user_details': user_VF(user.id),"token": token},
                } 
            else:
                res.status_code =status.HTTP_404_NOT_FOUND
                res.data = {'status': status.HTTP_404_NOT_FOUND,'message':'Email or password is not Valid','data':{}}
            return res
         
         
# class TestView(GenericAPIView):
#    permission_classes=[IsAuthenticated]
#    def get(self,request,format=None):
#        print(request.user.username,"work")  
#        return Response({'status': status.HTTP_404_NOT_FOUND,'message':'','data':[request.user.username,request.user.id,request.user.employee_id]}, status=status.HTTP_404_NOT_FOUND)

class registration_VF(GenericAPIView):
    serializer_class = registrationSerializer
    def post(self, request, format=None, *args, **kwargs):
        employee_id = request.data.get('employee_id')
        name = request.data.get('name')

        res = Response()
        if employee_id == None:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {"status": status.HTTP_400_BAD_REQUEST, "message": "employee_id field id is required", 'data': [] }
            # return Response(, status = status.HTTP_400_BAD_REQUEST)
        if name == None:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data={"status": status.HTTP_400_BAD_REQUEST, "message": "name field is required", 'data': [] }
            return res

        serializer = registrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user is not None:
            res.status_code = status.HTTP_201_CREATED
            res.data = {"status": status.HTTP_201_CREATED, "message": "user registered", 'data': [] }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {'status': status.HTTP_400_BAD_REQUEST, "message": "user not registered", 'data':[]}
            # return Response(, status=status.HTTP_404_NOT_FOUND)
        return res
        



class userSpecificLinkHeader(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = userSpecificLinkSerializer
    def get(self, request, format=None, *args, **kwargs):
        user = request.user

        usr_role = employee_official.objects.filter(emp = user.id).first()
        print(usr_role)
        usr_role = usr_role.user_role
        links = user_links.objects.filter(access_department = usr_role, link_status = True)
        usr_link = []
        for link in links:
            usr_link.append({"title": link.title, 'link_type': link.link_type, 'link': link.user_link })

        serializer = userSpecificLinkSerializer(data=usr_link, many=True)
        res = Response()
        if serializer.is_valid(raise_exception=True):
            res.status_code = status.HTTP_200_OK
            res.data = {"status": status.HTTP_200_OK, "message": "successfully fetched", "data":{ "user_link" : serializer.data}}
        else:        
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {"status": status.HTTP_200_OK, "message": "unsuccessful", "data":{}}
        return res
    



def user_VF(id):
    
    print('id', id)
    user = employee_official.objects.get(emp=id)
    data = {
        'user_role' : user.user_role,
        'product' : user.product,
        'name' : user.emp.name,
        'employee_id' : user.emp.employee_id,
        'email' : user.emp.email,
    }
    serializer = userSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return  {'user': serializer.data}
