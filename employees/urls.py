# from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # path('/api', home_VF)
        # lead_manager:


            path('get_associates', getAssociates.as_view()), #file upload
            path('view_all_user/<int:page>', viewAllUser.as_view()), #file upload
            # path('official_details_submit', officialDetailsSubmit.as_view()), #file upload


            # path('create_associate_basic', createAssociateBasic.as_view()), #file upload
            # path('create_associate_official', createAssociateOfficial.as_view()), #file upload

            
]