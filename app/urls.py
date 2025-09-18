from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.auth import LoginAPIView, TokenRefreshUserView, VerifyAccessTokenView
from app.views.company import CompanyUserMailsDetailView, MailListCreateView
from app.views.roles import AccessTypesDetailView, AccessTypesListCreateView, RoleDetailView, RoleListCreateView
from app.views.users import GoogleLogin, UserRegisterView, UsersDetailsList, UsersDetailsView

api_attendance_urls = [
    # Auth 
    path("user/login/", LoginAPIView.as_view(), name="login_api"),
    path("token/", TokenRefreshUserView.as_view(), name="token_refresh_user"),
    path("token/access/", VerifyAccessTokenView.as_view(), name="verify_access"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User GoogleLogin
    path("user/social_login/", GoogleLogin.as_view(), name="social_login"),
    path("user/list/", UsersDetailsList.as_view(), name="user_list"),
    path("user/register/", UserRegisterView.as_view(), name="user_create"),
    path("user/update/<int:pk>/", UsersDetailsView.as_view(), name="user_update"),
    
    # Role & Access
    path("access-types/", AccessTypesListCreateView.as_view(), name="access_list_create"),
    path("access-types/<int:pk>/", AccessTypesDetailView.as_view(), name="access-detail"),
    path("role-create-list/", RoleListCreateView.as_view(), name="role-list"),
    path("role-details/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
    # Company -Datils
    path("mail-create-list/", MailListCreateView.as_view(), name="mail-list"),
    path("mail-details/<int:pk>/", CompanyUserMailsDetailView.as_view(), name="mail-details"),
    
    ]

urlpatterns =  api_attendance_urls