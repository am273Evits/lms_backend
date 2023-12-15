# from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # path('/api', home_VF)
        # lead_manager:
            path('get_associates', getAssociates.as_view()), #file upload
            # path('get_table_fields/<str:table>', getTableFields.as_view()), #file upload


            # path('create_associate_basic', createAssociateBasic.as_view()), #file upload
            # path('create_associate_official', createAssociateOfficial.as_view()), #file upload

            
]