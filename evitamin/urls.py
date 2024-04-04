# from django.contrib import admin
from django.urls import path, include, re_path
from .views import * 

urlpatterns = [
    # path('/api', home_VF)

        # lead_manager:
            # path('create_services', createServices.as_view()),
            # path('view_all_services/<int:page>', viewAllServices.as_view()),
            # path('view_services/<str:service_id>', viewServicesIndv.as_view()),
            # path('view_services_search/<str:service_id>', viewServicesSearch.as_view()),
            # path('update_services/<str:service_id>', updateServices.as_view()),
            # path('add_service_delete_approval/<str:service_id>', deleteServiceApprovalWrite.as_view()),
    
    
            path('create_commercials', CreateServiceAndCommercials.as_view()),
            path('view_commercials/<int:page>', ViewServiceAndCommercials.as_view()),
            path('view_commercials_indv/<str:type>/<int:id>', ViewServiceAndCommercialsIndv.as_view()),
            path('edit_commercials/<int:id>', EditServiceCommercials.as_view()),
            path('archive_commercials/<int:id>', ArchiveServiceCommercials.as_view()),
            path('view_archive_commercials/<int:page>', ViewArchivedServiceAndCommercials.as_view()),
            path('unarchive_commercials/<int:id>', UnarchiveServiceCommercials.as_view()),
            path('view_commercials_search/<str:type>/<str:search_attribute>/<str:search_term>', ViewServiceAndCommercialsSearch.as_view()),

            path('archive_commercial_ind/<int:id>', ArchiveServiceCommercialIndv.as_view()),
            path('unarchive_commercial_ind/<int:id>', UnarchiveServiceCommercialIndv.as_view()),  
              

]
