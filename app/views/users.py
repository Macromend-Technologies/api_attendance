from app.core import BaseCORSExemptAPIView
from app.models.user_model import CustomUser
from app.models.usermail_model import CompanyUserMails
from app.response import CustomResponse
from app.serializers.users import DevicesSerializer, LocationSerializer, UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

 
            
class UserRegisterView(BaseCORSExemptAPIView):
    permission_classes = []  # allow public access
    def post(self, request):
        try:
            user_data = request.data.get("users")
            location_data = request.data.get("location")
            device_data = request.data.get("device")
            user_email = user_data.get("email")
            # check company mail
            company_mail = CompanyUserMails.objects.filter(email=user_email).first()
            if not company_mail:
                return CustomResponse.error(
                    message="User not allowed, contact HR",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            with transaction.atomic():
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
                if hasattr(company_mail, "role"):
                    user.role = company_mail.role
                    user.save(update_fields=["role"])

                # create location
                if location_data:
                    location_data["user"] = user.id
                    location_serializer = LocationSerializer(data=location_data)
                    location_serializer.is_valid(raise_exception=True)
                    location_serializer.save()

                # create device
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
        

class UsersDetailsList(BaseCORSExemptAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        """Retrieve single user or all users"""
        try:
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="Users retrieved successfully.",
                status_code=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return CustomResponse.error(
                message="User not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return CustomResponse.error(
                errors=str(e),
                message="Error retrieving users.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class UsersDetailsView(BaseCORSExemptAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        """Retrieve single user or all users"""
        try:
            if pk:
                user = CustomUser.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return CustomResponse.success(
                    data=serializer.data,
                    message="User retrieved successfully.",
                    status_code=status.HTTP_200_OK,
                )
             
        except CustomUser.DoesNotExist:
            return CustomResponse.error(
                message="User not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return CustomResponse.error(
                errors=str(e),
                message="Error retrieving users.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
 
    def patch(self, request, pk):
        """Update existing user"""
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="User updated successfully.",
                status_code=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return CustomResponse.error(
                message="User not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return CustomResponse.error(
                errors=str(e),
                message="Error updating user.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, pk):
        """Delete user"""
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return CustomResponse.success(
                message="User deleted successfully.",
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except CustomUser.DoesNotExist:
            return CustomResponse.error(
                message="User not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return CustomResponse.error(
                errors=str(e),
                message="Error deleting user.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
