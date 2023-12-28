from django.shortcuts import render
from .models import ev_services
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from account.views import getUserRole
from records.models import service_delete_approval
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
    serializer_class = viewServicesSerializer
    def get(self, request, page, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        limit = 10
        offset = int((page - 1)* limit)
        # print(user_role)
        res = Response()
        if user_role == 'admin':
            pagecount = math.ceil(ev_services.objects.filter(visibility=True).count()/limit)
            # print(pagecount)

            if int(page) <= pagecount:
                data = ev_services.objects.filter(visibility=True).all()[offset: offset+limit]
                data = list(data.values())
                serializer = viewServicesSerializer(data=data, many=True)
                if serializer.is_valid(raise_exception=True):
                    # print(serializer.data)
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
            data = ev_services.objects.filter(service_id = service_id, visibility=True).values().first()
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
            serviceData = ev_services.objects.filter(service_id = service_id, visibility=True).values().first()
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



class deleteServiceApprovalWrite(GenericAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = 
    def delete(self, request, service_id, format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin':
            if not service_delete_approval.objects.filter(service_id__service_id = service_id).exists():
                data = ev_services.objects.filter(service_id = service_id, visibility=True).first()
                if data:
                    lda = service_delete_approval.objects.create(**{'service_id': data})
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
    


class updateServices(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = viewAllServicesSerializer
    def put(self, request, service_id ,format=None, *args, **kwargs):
        user_role = getUserRole(request.user.id)
        res = Response()
        if user_role == 'admin':
            SER_INST = ev_services.objects.filter(service_id = service_id, visibility=True).first()
            if SER_INST:
                serializer = viewAllServicesSerializer(SER_INST, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    res.status_code = status.HTTP_200_OK
                    res.data = {
                        'status' : status.HTTP_200_OK,
                        'message': 'successful',
                        'data': serializer.data
                    }
                else:
                    res.status_code = status.HTTP_400_BAD_REQUEST
                    res.data = {
                        'status' : status.HTTP_400_BAD_REQUEST,
                        'message': 'request failed',
                        'data': []
                    }
            else:
                res.status_code = status.HTTP_400_BAD_REQUEST
                res.data = {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message': 'invalid service id',
                    'data': []
                }
            return res
        else:
            res.status_code = status.HTTP_401_UNAUTHORIZED
            res.data = {
                'status' : status.HTTP_401_UNAUTHORIZED,
                'message': 'you are not authorized to view this page',
                'data': []
            }
        return res
