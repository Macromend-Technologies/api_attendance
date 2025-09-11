from django.contrib.auth import authenticate, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from app.core import BaseCORSExemptAPIView
from app.response import CustomResponse
from app.serializers.users import UserSerializer
 
# Login  
class LoginAPIView(BaseCORSExemptAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login successful",
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                        "user_details": UserSerializer(user).data,
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
                
            else:
                return Response(
                    {
                        "error": "Account is inactive. Contact the admin for assistance.",
                        "success": False,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(
            {"error": "Invalid login credentials.", "success": False},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutAPIView(BaseCORSExemptAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            response = Response(
                {"message": "Logout successful", "success": True},
                status=status.HTTP_200_OK,
            )
            return response
        except Exception as e:
            return Response(
                {"error": str(e), "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


User = get_user_model()

@method_decorator(csrf_exempt, name="dispatch")
class TokenRefreshUserView(BaseCORSExemptAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")  # Proper way in Django 2.2+
        refresh_token = request.data.get("refresh")

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token_from_header = parts[1]
                print(f"Access Token from Authorization header: {token_from_header}")
            else:
                return Response(
                    {"error": "Invalid Authorization header format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not refresh_token:
            return Response(
                {"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            user = User.objects.get(id=refresh["user_id"])
            user_data = UserSerializer(user).data

            return Response(
                {"access": access_token, "user": user_data}, status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


@method_decorator(csrf_exempt, name="dispatch")
class VerifyAccessTokenView(BaseCORSExemptAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access")

        if not access_token:
            return Response(
                {"error": "Access token required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(access_token)
            user = User.objects.get(id=token["user_id"])
            user_data = UserSerializer(user).data

            return CustomResponse.success(
                message="Access token is successfully validated",
                data={"accessToken": access_token, "refreshToken": token, **user_data},
            )

        except TokenError:
            return Response(
                {"error": "Invalid or expired access token.", "success": False},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found.", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
