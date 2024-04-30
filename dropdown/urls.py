# from django.contrib import admin
from django.urls import path, include, re_path
from .views import * 

urlpatterns = [
    
    
            path('department', dropdown_department.as_view()),
            path('designation/<int:id>', dropdown_designation.as_view()),
            path('employee_status', dropdown_employee_status.as_view()),

            path('employee_list/<str:searchAtr>', employee_list.as_view()),
            
            path('get_commercials/<str:client_id>/<int:lead_id>', get_commercials.as_view()),

            
            # path('dropdown_program/<int:id>', dropdown_program.as_view()),
    
    
    # path('/api', home_VF)


        # lead_manager:
            path('options/<str:table>', dropdownOption.as_view()),

            path('lead_status_list', leadStatusList.as_view()),

            # path('options/<str:table>/<str:data1>', dropdownOptionData1.as_view()),
            # path('options/<str:table>/<str:data1>/<str:data2>', dropdownOptionData2.as_view()),

            # path('employee_all_tables', employeesAllTables.as_view()), #all tables submit

            # path('view_employee/<str:table>/<str:employee_id>', viewEmployee.as_view()), #view_all_leads

            # path('options/<str:table>/<str:data1>/<str:data2>', dropdownOptionData2.as_view()),

            # path('options_ajax/<str:table>', dropdownAjaxOption.as_view()),
            # path('options_ajax/<str:table>/<str:country>', dropdownAjaxD1Option.as_view()),
            # path('options_ajax/<str:table>/<str:country>/<str:state>', dropdownAjaxD2Option.as_view())
            
]