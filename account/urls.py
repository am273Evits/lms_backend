from django.urls import path ,re_path
from .import views

urlpatterns = [
      path('login',views.LoginView.as_view()),
    #   path('test',views.TestView.as_view()),
      path('register',views.registration_VF.as_view()),
      # path('register',views.registration),
      # path('user_links',views.userSpecificLinkHeader.as_view()),


      path('view_users/<int:page>',views.view_users.as_view()),
      path('view_user_search/<str:searchAtr>/<str:id>',views.view_users_search.as_view()),
      # path('view_user_individual/<str:employee_id>',views.view_users_individual.as_view()),
      path('user_update/<str:employee_id>',views.user_update.as_view()),
      path('user_delete/<str:employee_id>',views.delete_user.as_view()),


      


      path('view_user_archive/<int:page>',views.view_users_archive.as_view()),
      path('view_user_archive_search/<int:page>',views.view_users_archive_search.as_view()),
      path('unarchive_user/<str:employee_id>',views.unarchive_user.as_view()),

]