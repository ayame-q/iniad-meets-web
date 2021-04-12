from django.urls import path
from . import views

urlpatterns = [
    path("api/v2/circle/<uuid:pk>", views.CircleInfoAPIView.as_view(), name="api_circle_info"),
    #path("api/v2/user/", ),
    #path("api/v2/entry/<int:pk>"),
    path("api/v2/movie_uploaded/<uuid:pk>", views.MovieUploadedAPI.as_view(), name="api_movie_uploaded"),
    path("api/v2/logo_uploaded/<uuid:pk>", views.LogoUploadedAPI.as_view(), name="api_logo_uploaded"),
    path("api/v2/is_slack_joined", views.IsSlackJoinedAPI.as_view(), name="api_is_slack_joined"),
    path('api/v2/slack/', views.SlackEventAPI.as_view(), name="slack_challenge"),
    path('api/v2/slack/team_join', views.SlackEventAPI.as_view(), name="slack_new_user_join"),
    path("circle/join", views.CircleJoinView.as_view(), name="circle_join"),
    path("circle/list", views.CircleListView.as_view(), name="circle_list"),
    path('circle/admin/', views.CircleAdminGenericListView.as_view(), name="circle_admin"),
    path('circle/admin/<uuid:pk>', views.CircleAdminMenuView.as_view(), name="circle_admin"),
    path('circle/admin/info/', views.CircleAdminGenericListView.as_view(), name="circle_admin_info"),
    path('circle/admin/info/<uuid:pk>', views.CircleAdminInfoView.as_view(), name="circle_admin_info"),
    path('circle/admin/members/', views.CircleAdminGenericListView.as_view(), name="circle_admin_members"),
    path('circle/admin/members/<uuid:pk>', views.CircleAdminMembersView.as_view(), name="circle_admin_members"),
    #path('circle/admin/', views.circle_admin_list, name="circle_admin_list"),
    #path('', views.app, name="top"),
    #path('circle_admin/<int:pk>/entries/csv', views.circle_admin_entry_csv, name="circle_entry_csv"),
    #path('system_admin/', views.system_admin, name="system_admin"),
    #path('api/user/name/update', views.api_user_name_update, name="api_username_update"),
    #path('api/user/display_name/update', views.api_user_display_name_update, name="api_user_display_name_update"),
    #path('api/entry/<int:pk>', views.api_entry, name="api_entry"),
    #path('api/admin_users/add', views.api_admin_users_add, name="admin_users_add"),
    #path('api/staff_users/add', views.api_staff_users_add, name="staff_users_add"),
    #path('api/my_questions', views.api_get_my_questions, name="my_questions"),
    #path('api/staff_questions', views.api_get_staff_questions, name="get_questions"),
    #path('api/status', views.api_get_status, name="status"),
]
