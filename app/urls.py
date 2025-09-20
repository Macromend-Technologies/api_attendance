from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.auth import LoginAPIView, TokenRefreshUserView, VerifyAccessTokenView
from app.views.company import CompanyUserMailsDetailView, MailListCreateView
from app.views.developer import DeveloperCreateView, DeveloperLoginAPIView
from app.views.holiday import HolidayMappingCreate, HolidayMappingList
from app.views.leaves import LeaveRequestView
from app.views.roles import  AccessListCreateView, DesignationDetailView, DesignationListCreateView, RoleDetailView, RoleListCreateView
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
    path("user/register/", UserRegisterView.as_view(), name="user_create"),
    path("user/list/", UsersDetailsList.as_view(), name="user_list"),
    path("user/detail/<int:pk>/", UsersDetailsView.as_view(), name="user_detail"),
    path("user/update/<int:pk>/", UsersDetailsView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", UsersDetailsView.as_view(), name="user_delete"),
    # Role,Designation & Access
    path("access/list/", AccessListCreateView.as_view(), name="access_list"),
    path("access/create/", AccessListCreateView.as_view(), name="access_create"),
    # Designation
    path("designation/list/", DesignationListCreateView.as_view(), name="designation_list"),
    path("designation/create/", DesignationListCreateView.as_view(), name="designation_create"),
    path("designation/detail/<int:pk>/", DesignationDetailView.as_view(), name="designation_detail"), 
    path("designation/update/<int:pk>/", DesignationDetailView.as_view(), name="designation_update"), 
    path("designation/delete/<int:pk>/", DesignationDetailView.as_view(), name="designation_delete"), 
    # Role
    path("role/list/", RoleListCreateView.as_view(), name="role_list"),
    path("role/create/", RoleListCreateView.as_view(), name="role_create"),
    path("role/details/<int:pk>/", RoleDetailView.as_view(), name="role_detail"),
    path("role/update/<int:pk>/", RoleDetailView.as_view(), name="role_update"),
    path("role/delete/<int:pk>/", RoleDetailView.as_view(), name="role_delete"),
    # Company-Mail
    path("mail/list/", MailListCreateView.as_view(), name="mail_list"),
    path("mail/create/", MailListCreateView.as_view(), name="mail_create"),
    path("mail/details/<int:pk>/", CompanyUserMailsDetailView.as_view(), name="mail_detail"),
    path("mail/update/<int:pk>/", CompanyUserMailsDetailView.as_view(), name="mail_update"), 
    path("mail/delete/<int:pk>/", CompanyUserMailsDetailView.as_view(), name="mail_delete"),
    # Developer
    path("developer/create/",DeveloperCreateView.as_view(), name="developer_create"),
    path("developer/login/",DeveloperLoginAPIView.as_view(), name="developer_login"),
    # Holiday Mapping
    path("holiday/list/",HolidayMappingList.as_view(), name="holiday_mapping_list"),
    path("holiday/create/",HolidayMappingCreate.as_view(), name="holiday_mapping_create"),
    
    
    # Leaves
    
    path("leave/request/",LeaveRequestView.as_view(), name="leave_request"),
    
    
    ]

urlpatterns =  api_attendance_urls