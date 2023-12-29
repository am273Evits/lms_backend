# from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # path('/api', home_VF)
        # lead_manager:


            path('get_associates', getAssociates.as_view()), #file upload
            path('view_all_user/<int:page>', viewAllUser.as_view()), #file upload
            path('view_user/<str:employee_id>', viewUserIndv.as_view()), #file upload

            path('add_user_delete_approval/<str:employee_id>', deleteUserApprovalWrite.as_view()),
            path('view_user_search/<str:employee_id>', viewAllLeadsSearch.as_view()), #view_all_leads

            path('official_details_submit/<str:employee_id>', officialDetailsSubmit.as_view()), #file upload

            path('view_employee/<str:table>/<str:employee_id>', viewEmployee.as_view()), #view_all_leads

            path('update_employee/<str:table>/<str:employee_id>', updateEmployee.as_view()), #view_all_leads


            # path('create_associate_basic', createAssociateBasic.as_view()), #file upload
            # path('create_associate_official', createAssociateOfficial.as_view()), #file upload

            
]