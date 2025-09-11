from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.auth import LoginAPIView, TokenRefreshUserView, VerifyAccessTokenView
from app.views.users import UserRegisterView, UsersListView

api_attendance_urls = [
    
    path("login_api/", LoginAPIView.as_view(), name="login_api"),
    path("token/", TokenRefreshUserView.as_view(), name="token_refresh_user"),
    path("token/access/", VerifyAccessTokenView.as_view(), name="verify_access"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User 
    path("user-list/", UsersListView.as_view(), name="user_list"),
    path("user-register/", UserRegisterView.as_view(), name="user_create"),
    
    
    ]

urlpatterns =  api_attendance_urls