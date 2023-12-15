from django.urls import path ,re_path
from .import views

urlpatterns = [
      path('login',views.LoginView.as_view()),
    #   path('test',views.TestView.as_view()),
      path('register',views.registration_VF.as_view()),
      path('user_links',views.userSpecificLinkHeader.as_view()),
]