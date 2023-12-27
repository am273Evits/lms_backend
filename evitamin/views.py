from django.shortcuts import render
from .models import ev_services
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from account.views import getUserRole
import math
# Create your views here.


class createServices(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = servicesSerializer
    def post(self, request, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin':
            # print(request.data)
            data = request.data
            serializer = servicesSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                res.status_code = status.HTTP_200_OK
                res.data = {
                    'status': status.HTTP_200_OK,
                    "message": 'new service created successfully',
                    'data': serializer.data
                }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message': "service creation failed",
                    'data': []
                }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'message': 'you are not authorized to create new service',
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': []
            }
        return res
    


class viewAllServices(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewAllServicesSerializer
    def get(self, request, page, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        limit = 10
        offset = int((page - 1)* limit)
        # print(user_role)
        res = Response()
        if user_role == 'admin':
            pagecount = math.ceil(ev_services.objects.count()/limit)

            if int(page) <= pagecount:
                data = ev_services.objects.all()[offset: offset+limit]
                data = list(data.values())
                serializer = viewAllServicesSerializer(data=data, many=True)
                if serializer.is_valid(raise_exception=True):
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        "status": status.HTTP_200_OK,
                        "message": 'successful',
                        "data": {'data': serializer.data, 'total_pages': pagecount, "current_page": page}
                        }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'request failed',
                        'data': []
                    }

            else :
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": 'the page is unavailable',
                    "data": {'data': [], 'total_pages': pagecount, "current_page": page}
                    }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status': status.HTTP_401_UNAUTHORIZED,
                'message': 'you are not authroized to view this page',
                'data' : []
            }
        return res
    



class viewServicesIndv(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewAllServicesSerializer
    def get(self, request, service_id, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin':
            data = ev_services.objects.filter(service_id = service_id).values().first()
            serializer = viewAllServicesSerializer(data=data)
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
                    'message': 'request failed',
                    'data': []
                }
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status': status.HTTP_401_UNAUTHORIZED,
                'message': 'you are not authorized to view this page',
                'admin': []
            }
        return res
    

class viewServicesSearch(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewAllServicesSerializer
    def get(self, request, service_id, format=None, *args, **kwargs):
        user = request.user
        user_role = getUserRole(user.id)
        data = []
        res =  Response()
        if user_role == 'admin':
            serviceData = ev_services.objects.filter(service_id = service_id).values().first()
            print(serviceData)
            if serviceData:

                serializer = viewAllServicesSerializer(data=serviceData)
                if serializer.is_valid(raise_exception=True):

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
                        'message': 'request failed',
                        'data' : []
                    }

            else:
                res.status_code = status.HTTP_403_FORBIDDEN
                res.data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'invalid service id',
                    'data' : []
                }
        else:
            res.status_code = status.HTTP_400_BAD_REQUEST
            res.data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'unauthorized access', 
                'data': [],
            }
        
        return res
