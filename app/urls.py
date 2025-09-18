from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.auth import LoginAPIView, TokenRefreshUserView, VerifyAccessTokenView
from app.views.company import CompanyUserMailsDetailView, MailListCreateView
from app.views.developer import DeveloperCreateView, DeveloperLoginAPIView
from app.views.holiday import HolidayMappingCreate, HolidayMappingList
from app.views.roles import AccessTypesDetailView, AccessTypesListCreateView, DesignationDetailView, DesignationListCreateView, RoleDetailView, RoleListCreateView
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
    # Role,Designation & Access
    path("access/types/", AccessTypesListCreateView.as_view(), name="access_list_create"),
    path("access/types/<int:pk>/", AccessTypesDetailView.as_view(), name="access-detail"),
    path("designation/", DesignationListCreateView.as_view(), name="designation_detail"),
    path("designation/<int:pk>/", DesignationDetailView.as_view(), name="designation_update"), 
    path("role/create_list", RoleListCreateView.as_view(), name="role-list"),
    path("role/details/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),
    # Company -Datils
    path("mail/create-list/", MailListCreateView.as_view(), name="mail-list"),
    path("mail/details/<int:pk>/", CompanyUserMailsDetailView.as_view(), name="mail-details"),
    path("developer/create/",DeveloperCreateView.as_view(), name="developer_create"),
    path("developer/login/",DeveloperLoginAPIView.as_view(), name="developer_login"),
    # Holiday Mapping
     
    path("holiday/list/",HolidayMappingList.as_view(), name="holiday_mapping_list"),
    path("holiday/create/",HolidayMappingCreate.as_view(), name="holiday_mapping_create"),

    ]

urlpatterns =  api_attendance_urls