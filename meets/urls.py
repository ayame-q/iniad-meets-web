from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name="top"),
    path('circle_admin/', views.circle_admin_list, name="circle_admin_list"),
    path('circle_admin/<int:pk>', views.circle_admin_page, name="circle_admin_page"),
    path('circle_admin/<int:pk>/entries/csv', views.circle_admin_entry_csv, name="circle_entry_csv"),
    path('api/user/name/update', views.api_user_name_update, name="api_username_update"),
    path('api/user/display_name/update', views.api_user_display_name_update, name="api_user_display_name_update"),
    path('api/entry/<int:pk>', views.api_entry, name="api_entry"),
    path('api/admin_users/add', views.api_admin_users_add, name="admin_users_add"),
    path('api/staff_users/add', views.api_staff_users_add, name="staff_users_add"),
    path('api/get_questions', views.api_get_questions, name="get_questions"),
]