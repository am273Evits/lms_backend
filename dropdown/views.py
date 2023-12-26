from django.shortcuts import render
from django.apps import apps
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from dropdown.models import ev_department, ev_designation, user_role_list

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