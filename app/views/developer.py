from rest_framework.response import Response
from rest_framework import status
from app.core import BaseCORSExemptAPIView
from app.models.developer_model import Developer
from app.response import CustomResponse
from app.serializers.developer import DeveloperSerializer
 
from rest_framework_simplejwt.tokens import RefreshToken
 
from django.contrib.auth.hashers import check_password
class DeveloperCreateView(BaseCORSExemptAPIView):
    permission_classes = []  # public access
    def post(self, request):
        """Create new Developer"""
        try:
            serializer = DeveloperSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Developer created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error creating Developer",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        

class DeveloperLoginAPIView(BaseCORSExemptAPIView):
    permission_classes = []  # public access

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"success": False, "error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get user from Developer table
            user = Developer.objects.get(email=email)
        except Developer.DoesNotExist:
            return Response(
                {"success": False, "error": "Invalid login credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check the hashed password
        if check_password(password, user.password):
            if user.is_super:  # Only super users allowed
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "message": "Login successful",
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                        "user_details": DeveloperSerializer(user).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"success": False, "error": "You are not a super user."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"success": False, "error": "Invalid login credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )