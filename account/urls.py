from django.urls import path ,re_path
from .import views

urlpatterns = [
    
      path('page_refresher',views.page_refresher),
    
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
      path('view_user_archive_search/<str:searchAtr>/<str:id>',views.view_users_archive_search.as_view()),
      path('unarchive_user/<str:employee_id>',views.unarchive_user.as_view()),


      path('my_info',views.my_info.as_view()),
      path('apply_for_leave',views.apply_for_leave.as_view()),
      path('view_leave',views.view_leave.as_view()),
      path('edit_leave/<int:leave_id>',views.edit_leave.as_view()),
      path('cancel_leave/<int:leave_id>',views.cancel_leave.as_view()),

      path('view_all_leaves/<int:page>',views.view_all_leaves.as_view()),
      path('approve_leave/<int:leave_id>',views.approve_leave.as_view()),
      path('reject_leave/<int:leave_id>',views.reject_leave.as_view()),

      path('generate_password/<int:id>/<str:token>', views.GeneratePassword),
]