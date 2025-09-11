from app.core import BaseCORSExemptAPIView
from app.models.user_model import CustomUser
from app.response import CustomResponse
from app.serializers.users import DevicesSerializer, LocationSerializer, UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

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