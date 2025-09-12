import email
from app.auth import User
from app.core import BaseCORSExemptAPIView
from app.models.user_model import CustomUser
from app.response import CustomResponse
from app.serializers.users import DevicesSerializer, LocationSerializer, UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()
class UsersListView(BaseCORSExemptAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="Users retrieved successfully.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            
            return CustomResponse.error(
                errors=str(e),
                message="Error retrieving users.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class UserRegisterView(BaseCORSExemptAPIView):
    permission_classes = []  # allow public access

    def post(self, request):
        try:
            user_data = request.data.get("users")
            location_data = request.data.get("location")
            device_data = request.data.get("device")
            with transaction.atomic():
                # Create user
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
 
                if location_data:
                    location_data["user"] = user.id
                    location_serializer = LocationSerializer(data=location_data)
                    location_serializer.is_valid(raise_exception=True)
                    location_serializer.save()
 
                if device_data:
                    device_data["user"] = user.id
                    device_serializer = DevicesSerializer(data=device_data)
                    device_serializer.is_valid(raise_exception=True)
                    device_serializer.save()

            return CustomResponse.success(
                data=user_serializer.data,
                message="User created successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return CustomResponse.error(
                message="Error creating user",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
## google login 
class GoogleLogin(BaseCORSExemptAPIView):
    permission_classes = []  # allow public access
    def post(self, request):
        try:
            user_data = request.data.get("users")
            email = user_data.get("email")
            location_data = request.data.get("location")
            device_data = request.data.get("device")

            # 1. Already user check
            user = User.objects.filter(email=email).first()
            if user:
                refresh = RefreshToken.for_user(user)
                return CustomResponse.success(
                    data={
                        "users": {
                            "id": user.id,
                            "name": user.name,
                            "email": user.email,
                        },
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    message="User login successfully.",
                    status_code=status.HTTP_200_OK,
                )
            # 2. New user create (with validation)
            with transaction.atomic():
                # validate & create user
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()

                # validate & create device
                device_response = None
                if device_data:
                    device_data["user"] = user.id
                    device_serializer = DevicesSerializer(data=device_data)
                    device_serializer.is_valid(raise_exception=True)  # datatype check
                    device_response = device_serializer.save()

                # validate & create location
                location_response = None
                if location_data:
                    location_data["user"] = user.id
                    location_serializer = LocationSerializer(data=location_data)
                    location_serializer.is_valid(raise_exception=True)  # datatype check
                    location_response = location_serializer.save()

                refresh = RefreshToken.for_user(user)

            return CustomResponse.success(
                data={
                    "users": UserSerializer(user).data,
                    "device": DevicesSerializer(device_response).data if device_response else None,
                    "location": LocationSerializer(location_response).data if location_response else None,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                message="User created successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return CustomResponse.error(
                message="Error creating user",
                errors=str(e),   # serializer error msg return pannum
                status_code=status.HTTP_400_BAD_REQUEST,
            )
