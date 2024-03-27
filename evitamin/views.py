from django.shortcuts import render
# from .models import ev_services
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
# from business_leads.serializers import visibility_dynamic_serializer
# from account.views import getUserRole
# from records.models import service_delete_approval
from leads.views import resFun
from leads.models import *
import math
# Create your views here.



class CreateServiceAndCommercials(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateServicesCommercialsSerializer
    def post(self, request, format=None, *args, **kwargs):
        user = request.user
        res =  Response()
        if (str(user.department) == 'director'):

            segment = request.data.get('segment')
            service = request.data.get('service')
            marketplace = request.data.get('marketplace')
            program = request.data.get('program')
            sub_program = request.data.get('sub_program')
            commercials = request.data.get('commercials')

            if sub_program == None:
                service_commercials = Services_and_Commercials.objects.filter(segment=segment, service=service, marketplace=marketplace,program=program)
                print('service_commercials',service_commercials)
            else:
                service_commercials = Services_and_Commercials.objects.filter(segment=segment, service=service, marketplace=marketplace,program=program,sub_program=sub_program)
                print('service_commercials',service_commercials)

            # unique_commercials = []


            if service_commercials:
                res = resFun(status.HTTP_400_BAD_REQUEST, 'already created, you can edit from commercials list.',[])
                # saved_commercials = [s.commercials for s in service_commercials.first().commercials.all() ]
                # print('saved_commercials',saved_commercials)
                # print('commercials',commercials)

                # for c in commercials:
                #     if not c.strip() in saved_commercials:
                        
                #         commercial = Commercials.objects.create(**{'commercials' : c.strip() })
                #         service_commercials.first().commercials.add(commercial)
                
                # res = resFun(status.HTTP_200_OK, 'commercial saved',[])
            else:

                if sub_program == None:
                    serializer = CreateServicesCommercialsSerializer_NSP(data=request.data)
                else:
                    serializer = CreateServicesCommercialsSerializer(data=request.data)


                
                if serializer.is_valid(raise_exception=True):
                    if serializer.save():
                            res = resFun(status.HTTP_200_OK, 'added successfully', serializer.data)
                    else:
                        res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [] )
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors if serializer.errors else 'request failed', [] )
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [] )
        return res



class ViewServiceAndCommercials(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceAndCommercialSerializer
    def get(self,request,page, format=None, *args, **kwargs):
        user=request.user
        limit = 10
        offset = int((page - 1) * limit)
        if (str(user.department) == 'director'):
            
            service_commercials = Services_and_Commercials.objects.filter(segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=True)[offset : offset + limit]
            print('service_commercials',service_commercials)
            if service_commercials.exists():
                data=[]
                # service_commercials = service_commercials
                for sc in service_commercials:
                    d = {
                        'id':sc.id,
                        'segment': {"id": sc.segment.id, "segment_name": sc.segment.segment},
                        'service': {"id": sc.service.id, "service_name": sc.service.service},
                        'marketplace': {"id": sc.marketplace.id, "marketplace_name": sc.marketplace.marketplace},
                        'program': {"id": sc.program.id, 'program_name': sc.program.program},
                        'sub_program': {"id": sc.sub_program.id if sc.sub_program!=None else 0 ,'sub_program_name': sc.sub_program.sub_program if sc.sub_program!=None else '-'},
                        'commercials': { 'active': [{ 'id': s.id, 'commercials_name': s.commercials} for s in sc.commercials.all() if s.visibility==True ], "archive": [{ 'id': s.id, 'commercials_name': s.commercials} for s in sc.commercials.all() if s.visibility==False] }
                    }
                    data.append(d)
            
                serializer = ViewServiceAndCommercialSerializer(data=data,many=True)
                pagecount = math.ceil(Services_and_Commercials.objects.filter(segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=True).count()/limit)

                if serializer.is_valid():
                    res = resFun(status.HTTP_200_OK,'request successful', {'data': serializer.data, 'total_pages': pagecount, "current_page": page})
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
            else:
                res = resFun(status.HTTP_204_NO_CONTENT,'data not available',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])

        return res





class EditServiceCommercials(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateServicesCommercialsSerializer
    def put(self, request,id, format=None, *args, **kwargs):
        user = request.user

        if (str(user.department) == 'director'):

            # print(id)
            segment = request.data.get('segment')
            service = request.data.get('service')
            marketplace = request.data.get('marketplace')
            program = request.data.get('program')
            sub_program = request.data.get('sub_program')
            commercials = request.data.get('commercials')



            if sub_program == None:
                # print('this working')
                service_commercials = Services_and_Commercials.objects.filter(segment=segment, service=service, marketplace=marketplace,program=program)
            else:
                service_commercials = Services_and_Commercials.objects.filter(segment=segment, service=service, marketplace=marketplace,program=program,sub_program=sub_program)


            print('service_commercials',service_commercials.first().id)


            if service_commercials.exists() and id != service_commercials.first().id:
                # print(id,segment, service, marketplace, program, sub_program)
                res = resFun(status.HTTP_400_BAD_REQUEST, 'already exists', [])

            else:

                # print('working')

                serviceCommercials=Services_and_Commercials.objects.filter(id=id)
                serviceCommercials=serviceCommercials.first()
                serviceCommercials.segment = Segment.objects.get(id=segment)
                serviceCommercials.service = Service.objects.get(id=service)
                serviceCommercials.marketplace = Marketplace.objects.get(id=marketplace)
                serviceCommercials.program = Program.objects.get(id=program)
                
                if not sub_program == None:
                    serviceCommercials.sub_program = Sub_Program.objects.get(id=sub_program)

                saved_Commercials = [ s.commercials for s in serviceCommercials.commercials.all() if s.visibility==True ]
                
                if len(saved_Commercials) > 0:

                    print('if',saved_Commercials)

                    duplicate_commercials = []

                    for c in commercials:
                        if not c['id'] == None:
                            commercial_instance = Commercials.objects.filter(id=c['id'])
                            commercial_instance=commercial_instance.first()
                            commercial_instance.commercials = c['value']
                            commercial_instance.save()
                        else:
                            # commercial_instance = Commercials.objects.filter(commercials=c['value'])
                            if c['value'].strip() in saved_Commercials:
                                duplicate_commercials.append(c)
                            else:
                                new_commercial=Commercials.objects.create(**{'commercials':c['value'].strip()})
                                serviceCommercials.commercials.add(new_commercial)

                else:
                    for c in commercials:
                        new_commercial=Commercials.objects.create(**{'commercials':c['value'].strip()})
                        serviceCommercials.commercials.add(new_commercial)
                    
                serviceCommercials.save()

                res = resFun(status.HTTP_200_OK, 'duplicate commercials found' if len(duplicate_commercials)>0 else 'updated successfully', {'duplicate_commercials': duplicate_commercials} if len(duplicate_commercials)>0 else [])


            # serviceCommercials.save()
            

            # print('serviceCommercials',serviceCommercials.segment)

            # serializer = CreateServicesCommercialsSerializer(data=request.data)
            # if serializer.is_valid(raise_exception=True):
            #     if serializer.save():
            #             res = resFun(status.HTTP_200_OK, 'added successfully', serializer.data)
            #     else:
            #         res = resFun(status.HTTP_400_BAD_REQUEST, 'request failed', [] )
            # else:
            #     res = resFun(status.HTTP_400_BAD_REQUEST, serializer.errors if serializer.errors else 'request failed', [] )
            # else:
            #     res = resFun(status.HTTP_400_BAD_REQUEST, 'services already exists', [] )
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST, 'you are not authorized for this action', [])
        return res



class ArchiveServiceCommercials(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceAndCommercialSerializer
    def delete(self,request,id, format=None, *args, **kwargs):
        user=request.user
        if (str(user.department) == 'director'):
            try:
                service_commercials = Services_and_Commercials.objects.filter(id=id,visibility=True)
            except:
                service_commercials = Services_and_Commercials.objects.filter(pk__in=[])

            if service_commercials.exists():
                service_commercials=service_commercials.first()
                service_commercials.visibility = False
                service_commercials.save()
                
                res = resFun(status.HTTP_200_OK,'archive successful',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])

        return res



class ViewArchivedServiceAndCommercials(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceAndCommercialSerializer
    def get(self,request,page, format=None, *args, **kwargs):
        user=request.user
        limit = 10
        offset = int((page - 1) * limit)
        if (str(user.department) == 'director'):
            
            service_commercials = Services_and_Commercials.objects.filter(segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False)[offset : offset + limit]

        
            print('service_commercials',service_commercials)

            if service_commercials.exists():
                data=[]
                # for sc in service_commercials:
                #     d = {
                #         'id':sc.id,
                #         'segment': sc.segment.segment,
                #         'service': sc.service.service,
                #         'marketplace': sc.marketplace.marketplace,
                #         'program':sc.program.program,
                #         'sub_program':sc.sub_program.sub_program if sc.sub_program!=None else '-',
                #         'commercials': [{ 'id': s.id, 'commercials': s.commercials} for s in sc.commercials.all()]
                #     }
                #     data.append(d)

                for sc in service_commercials:
                    d = {
                        'id':sc.id,
                        'segment': {"id": sc.segment.id, "segment_name": sc.segment.segment},
                        'service': {"id": sc.service.id, "service_name": sc.service.service},
                        'marketplace': {"id": sc.marketplace.id, "marketplace_name": sc.marketplace.marketplace},
                        'program': {"id": sc.program.id, 'program_name': sc.program.program},
                        'sub_program': {"id": sc.sub_program.id if sc.sub_program!=None else 0 ,'sub_program_name': sc.sub_program.sub_program if sc.sub_program!=None else '-'},
                        'commercials': { 'active': [{ 'id': s.id, 'commercials_name': s.commercials} for s in sc.commercials.all() if s.visibility==True ], "archive": [{ 'id': s.id, 'commercials_name': s.commercials} for s in sc.commercials.all() if s.visibility==False] }
                    }
                    data.append(d)
            
                serializer = ViewServiceAndCommercialSerializer(data=data,many=True)
                pagecount = math.ceil(Services_and_Commercials.objects.filter(segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False).count()/limit)

                if serializer.is_valid():
                    res = resFun(status.HTTP_200_OK,'request successful', {'data': serializer.data, 'total_pages': pagecount, "current_page": page})
                else:
                    res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
            else:
                res = resFun(status.HTTP_204_NO_CONTENT,'data not available',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])

        return res



class UnarchiveServiceCommercials(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceAndCommercialSerializer
    def put(self,request,id, format=None, *args, **kwargs):
        user=request.user
        if (str(user.department) == 'director'):
            try:
                service_commercials = Services_and_Commercials.objects.filter(id=id,visibility=False)
            except:
                service_commercials = Services_and_Commercials.objects.filter(pk__in=[])

            if service_commercials.exists():
                service_commercials=service_commercials.first()
                service_commercials.visibility = True
                service_commercials.save()
                
                res = resFun(status.HTTP_200_OK,'restored successful',[])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
        else:
            res = resFun(status.HTTP_400_BAD_REQUEST,'you are not authorized for this action',[])

        return res



class ViewServiceAndCommercialsSearch(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewServiceAndCommercialSerializer
    def get(self, request, type, search_attribute,search_term, format=None, *args, **kwargs):

        search_term_R = search_term.replace("_",' ')

        if type=='active':
            if search_attribute=='segment':
                services_and_commercials = Services_and_Commercials.objects.filter(segment__segment__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=True)

                print('services_and_commercials',services_and_commercials)
                # pagecount = math.ceil(services_and_commercials.count()/limit)

            elif  search_attribute=='service':
                services_and_commercials = Services_and_Commercials.objects.filter(service__service__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=True)
            elif  search_attribute=='marketplace':
                services_and_commercials = Services_and_Commercials.objects.filter(marketplace__marketplace__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=True)
            elif  search_attribute=='program':
                services_and_commercials = Services_and_Commercials.objects.filter(program__program__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=True)

        elif type == 'archives':
            if search_attribute=='segment':
                services_and_commercials = Services_and_Commercials.objects.filter(segment__segment__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False)
                # pagecount = math.ceil(services_and_commercials.count()/limit)
            elif  search_attribute=='service':
                services_and_commercials = Services_and_Commercials.objects.filter(service__service__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False)
            elif  search_attribute=='marketplace':
                services_and_commercials = Services_and_Commercials.objects.filter(marketplace__marketplace__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False)
            elif  search_attribute=='program':
                services_and_commercials = Services_and_Commercials.objects.filter(program__program__icontains=search_term_R, segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False)


        if services_and_commercials.exists():
            data=[]
            # for sc in services_and_commercials:
            #     d = {
            #         'id':sc.id,
            #         'segment': sc.segment.segment,
            #         'service': sc.service.service,
            #         'marketplace': sc.marketplace.marketplace,
            #         'program':sc.program.program,
            #         'sub_program':sc.sub_program.sub_program if sc.sub_program!=None else '-',
            #         'commercials': [{ 'id': s.id, 'commercials': s.commercials} for s in sc.commercials.all()]
            #     }
            #     data.append(d)

            for sc in services_and_commercials:
                d = {
                    'id':sc.id,
                    'segment': {"id": sc.segment.id, "segment_name": sc.segment.segment},
                    'service': {"id": sc.service.id, "service_name": sc.service.service},
                    'marketplace': {"id": sc.marketplace.id, "marketplace_name": sc.marketplace.marketplace},
                    'program': {"id": sc.program.id, 'program_name': sc.program.program},
                    'sub_program': {"id": sc.sub_program.id if sc.sub_program!=None else 0 ,'sub_program_name': sc.sub_program.sub_program if sc.sub_program!=None else '-'},
                    'commercials': { 'active': [{ 'id': s.id, 'commercials_name': s.commercials} for s in sc.commercials.all() if s.visibility==True ], "archive": [{ 'id': s.id, 'commercials_name': s.commercials} for s in sc.commercials.all() if s.visibility==False] }
                }
                data.append(d)
        
            serializer = ViewServiceAndCommercialSerializer(data=data,many=True)
            # pagecount = math.ceil(Services_and_Commercials.objects.filter(segment__visibility=True, service__visibility=True, marketplace__visibility=True, program__visibility=True, visibility=False).count()/limit)
            if serializer.is_valid():
                res = resFun(status.HTTP_200_OK,'request successful', {'data':serializer.data, 'type':type, 'search_attribute': search_attribute, 'search_term': search_term})
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,'request failed',[])
        else:
            res = resFun(status.HTTP_204_NO_CONTENT,'data not available',[])
        return res
    



# class createServices(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = servicesSerializer
#     def post(self, request, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()
#         if user_role == 'admin':
#             # print(request.data)
#             data = request.data
#             serializer = servicesSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'status': status.HTTP_200_OK,
#                     "message": 'new service created successfully',
#                     'data': serializer.data
#                 }
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'status' : status.HTTP_400_BAD_REQUEST,
#                     'message': "service creation failed",
#                     'data': []
#                 }
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'message': 'you are not authorized to create new service',
#                 'status': status.HTTP_401_UNAUTHORIZED,
#                 'data': []
#             }
#         return res
    


# class viewAllServices(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = viewServicesSerializer
#     def get(self, request, page, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         limit = 10
#         offset = int((page - 1)* limit)
#         # print(user_role)
#         res = Response()
#         if user_role == 'admin':
#             pagecount = math.ceil(ev_services.objects.filter(visibility=True).count()/limit)
#             # print(pagecount)

#             if int(page) <= pagecount:
#                 data = ev_services.objects.filter(visibility=True).all()[offset: offset+limit]
#                 data = list(data.values())
#                 serializer = viewServicesSerializer(data=data, many=True)
#                 if serializer.is_valid(raise_exception=True):
#                     # print(serializer.data)
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         "status": status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": {'data': serializer.data, 'total_pages': pagecount, "current_page": page}
#                         }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                         'data': []
#                     }

#             else :
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     "status": status.HTTP_400_BAD_REQUEST,
#                     "message": 'the page is unavailable',
#                     "data": {'data': [], 'total_pages': pagecount, "current_page": page}
#                     }
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'status': status.HTTP_401_UNAUTHORIZED,
#                 'message': 'you are not authroized to view this page',
#                 'data' : []
#             }
#         return res
    



# class viewServicesIndv(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = viewAllServicesSerializer
#     def get(self, request, service_id, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()
#         if user_role == 'admin':
#             data = ev_services.objects.filter(service_id = service_id, visibility=True).values().first()
#             serializer = viewAllServicesSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 res.status_code = status.HTTP_200_OK
#                 res.data = {
#                     'status': status.HTTP_200_OK,
#                     'message': 'successful',
#                     'data': serializer.data
#                 }
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     'message': 'request failed',
#                     'data': []
#                 }
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'status': status.HTTP_401_UNAUTHORIZED,
#                 'message': 'you are not authorized to view this page',
#                 'admin': []
#             }
#         return res
    

# class viewServicesSearch(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = viewAllServicesSerializer
#     def get(self, request, service_id, format=None, *args, **kwargs):
#         user = request.user
#         user_role = getUserRole(user.id)
#         data = []
#         res =  Response()
#         if user_role == 'admin':
#             serviceData = ev_services.objects.filter(service_id = service_id, visibility=True).values().first()
#             print(serviceData)
#             if serviceData:

#                 serializer = viewAllServicesSerializer(data=serviceData)
#                 if serializer.is_valid(raise_exception=True):

#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         "status": status.HTTP_200_OK,
#                         "message": 'successful',
#                         "data": [serializer.data]
#                         }
#                 else:
#                     res.status_code = status.HTTP_403_FORBIDDEN
#                     res.data = {
#                         'status': status.HTTP_403_FORBIDDEN,
#                         'message': 'request failed',
#                         'data' : []
#                     }

#             else:
#                 res.status_code = status.HTTP_403_FORBIDDEN
#                 res.data = {
#                     'status': status.HTTP_403_FORBIDDEN,
#                     'message': 'invalid service id',
#                     'data' : []
#                 }
#         else:
#             res.status_code = status.HTTP_400_BAD_REQUEST
#             res.data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'message': 'unauthorized access', 
#                 'data': [],
#             }
        
#         return res



# class deleteServiceApprovalWrite(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     # serializer_class = 
#     def delete(self, request, service_id, format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()
#         if user_role == 'admin':
#             if not service_delete_approval.objects.filter(service_id__service_id = service_id).exists():
#                 data = ev_services.objects.filter(service_id = service_id, visibility=True).first()
#                 if data:
#                     lda = service_delete_approval.objects.create(**{'service_id': data})
#                     if lda:
#                         dynamic = visibility_dynamic_serializer(ev_services)
#                         serializer = dynamic(data, data={'visibility': False}, partial=True)
#                         serializer.is_valid(raise_exception=True)
#                         serializer.save()
#                         res.status_code = status.HTTP_201_CREATED
#                         res.data = {
#                             'status': status.HTTP_201_CREATED,
#                             'message': 'sent for approval, this user will be removed after the approval of admin',
#                             'data': []
#                         }
#                 else :
#                     res.status_code = status.HTTP_400_BAD_REQUEST,
#                     res.data = {
#                         'status': status.HTTP_400_BAD_REQUEST,
#                         'message': 'employee id do not exists',
#                         'data': []
#                     }
#             else :
#                 res.status_code = status.HTTP_208_ALREADY_REPORTED
#                 res.data = {
#                     'status': status.HTTP_208_ALREADY_REPORTED,
#                     'message': 'already submitted',
#                     'data': [] 
#                 }
#         else:
#             res.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
#             res.data = {
#                 'status': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
#                 'message': 'you are not authorized to delete user',
#                 'data': []
#             }
#         return res
    


# class updateServices(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = viewAllServicesSerializer
#     def put(self, request, service_id ,format=None, *args, **kwargs):
#         user_role = getUserRole(request.user.id)
#         res = Response()
#         if user_role == 'admin':
#             SER_INST = ev_services.objects.filter(service_id = service_id, visibility=True).first()
#             if SER_INST:
#                 serializer = viewAllServicesSerializer(SER_INST, data=request.data, partial=True)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save()
#                     res.status_code = status.HTTP_200_OK
#                     res.data = {
#                         'status' : status.HTTP_200_OK,
#                         'message': 'successful',
#                         'data': serializer.data
#                     }
#                 else:
#                     res.status_code = status.HTTP_400_BAD_REQUEST
#                     res.data = {
#                         'status' : status.HTTP_400_BAD_REQUEST,
#                         'message': 'request failed',
#                         'data': []
#                     }
#             else:
#                 res.status_code = status.HTTP_400_BAD_REQUEST
#                 res.data = {
#                     'status' : status.HTTP_400_BAD_REQUEST,
#                     'message': 'invalid service id',
#                     'data': []
#                 }
#             return res
#         else:
#             res.status_code = status.HTTP_401_UNAUTHORIZED
#             res.data = {
#                 'status' : status.HTTP_401_UNAUTHORIZED,
#                 'message': 'you are not authorized to view this page',
#                 'data': []
#             }
#         return res
