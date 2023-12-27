# from django.contrib import admin
from django.urls import path, include, re_path
from .views import * 

urlpatterns = [
    # path('/api', home_VF)

        # lead_manager:
            path('create_services', createServices.as_view()),
            path('view_all_services/<int:page>', viewAllServices.as_view()),
            path('view_services/<str:service_id>', viewServicesIndv.as_view()),
            path('view_services_search/<str:service_id>', viewServicesSearch.as_view()),

            path('update_services/<str:service_id>', updateServices.as_view()),

            path('add_service_delete_approval/<str:service_id>', deleteServiceApprovalWrite.as_view()),




]
