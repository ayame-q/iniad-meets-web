from django.urls import path
from . import views

urlpatterns = [
    path("api/v2/circle/<uuid:pk>", views.CircleInfoAPIView.as_view(), name="api_circle_info"),
    path("api/v2/entry/", views.CircleEntryAPIView.as_view(), name="api_entry"),
    path("api/v2/user/", views.UserRetrieveUpdateAPIView.as_view(), name="api_user"),
    path("api/v2/is_authenticated", views.UserIsAuthenticatedAPI.as_view(), name="api_is_authenticated"),
    path("api/v2/movie_uploaded/<uuid:pk>", views.MovieUploadedAPI.as_view(), name="api_movie_uploaded"),
    path("api/v2/logo_uploaded/<uuid:pk>", views.LogoUploadedAPI.as_view(), name="api_logo_uploaded"),
    path("api/v2/is_slack_joined", views.IsSlackJoinedAPI.as_view(), name="api_is_slack_joined"),
    path('api/v2/slack/', views.SlackEventAPI.as_view(), name="slack_challenge"),
    path('api/v2/slack/team_join', views.SlackEventAPI.as_view(), name="slack_new_user_join"),
    path("share/img/<uuid:uuid>", views.sns_share_image, name="sns_share_image"),
    path("circle/join", views.CircleJoinView.as_view(), name="circle_join"),
    path("circle/list", views.CircleListView.as_view(), name="circle_list"),
    path('circle/admin/', views.CircleAdminGenericListView.as_view(), name="circle_admin"),
    path('circle/admin/<uuid:pk>', views.CircleAdminMenuView.as_view(), name="circle_admin"),
    path('circle/admin/info/', views.CircleAdminGenericListView.as_view(), name="circle_admin_info"),
    path('circle/admin/info/<uuid:pk>', views.CircleAdminInfoView.as_view(), name="circle_admin_info"),
    path('circle/admin/pamphlet/', views.CircleAdminGenericListView.as_view(), name="circle_admin_pamphlet"),
    path('circle/admin/pamphlet/<uuid:pk>', views.CircleAdminPamphletView.as_view(), name="circle_admin_pamphlet"),
    path('circle/admin/members/', views.CircleAdminGenericListView.as_view(), name="circle_admin_members"),
    path('circle/admin/members/<uuid:pk>', views.CircleAdminMembersView.as_view(), name="circle_admin_members"),
    path('circle/admin/entries/', views.CircleAdminGenericListView.as_view(), name="circle_admin_entries"),
    path('circle/admin/entries/<uuid:pk>', views.CircleAdminEntriesView.as_view(), name="circle_admin_entries"),
    path('circle/admin/entries/csv/', views.CircleAdminGenericListView.as_view(), name="circle_admin_entries_csv"),
    path('circle/admin/entries/csv/<uuid:pk>', views.circle_admin_entries_csv, name="circle_admin_entries_csv"),
]
