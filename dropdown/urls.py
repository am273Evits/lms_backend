# from django.contrib import admin
from django.urls import path, include, re_path
from .views import * 

urlpatterns = [
    # path('/api', home_VF)

        # lead_manager:
            path('options/<str:table>', dropdownOption.as_view()),
            path('options/<str:table>/<str:data1>', dropdownOptionData1.as_view()),
            # path('options/<str:table>/<str:data1>/<str:data2>', dropdownOptionData2.as_view()),

            path('options_ajax/<str:table>', dropdownAjaxOption.as_view()),
            path('options_ajax/<str:data1>/<str:table>', dropdownAjaxD1Option.as_view()),
            path('options_ajax/<str:table>/<str:country>/<str:state>', dropdownAjaxD2Option.as_view())
            
]