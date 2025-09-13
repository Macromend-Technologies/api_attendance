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
    def update_user_related_data(self, user, device_data=None, location_data=None):
        """Helper: create/update device & location data for user"""
        if device_data:
            device_data["user"] = user.id
            serializer = DevicesSerializer(data=device_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if location_data:
            location_data["user"] = user.id
            serializer = LocationSerializer(data=location_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def post(self, request):
        try:
            user_data = request.data.get("users")
            location_data = request.data.get("location")
            device_data = request.data.get("device")
            email = user_data.get("email")
            password = user_data.get("password")
            
            if not email and not password:
                return CustomResponse.error(
                    message="Invalid request",
                    errors="Email is required & Password is required",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            user_mail = CompanyUserMails.objects.filter(email=email).first()
            if not user_mail:
                return CustomResponse.error(
                    message="Error creating user",
                    errors="Contact HR - Invalid User",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            with transaction.atomic():
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
                user.set_password(password)
                user.save()
                # assign role from CompanyUserMails
                if user_mail.role:
                    user.role = user_mail.role
                    user.save()
                self.update_user_related_data(user, device_data, location_data)
 
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

class GoogleLogin(BaseCORSExemptAPIView):
    permission_classes = []  # allow public access

    def generate_password(self, length=8):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))

    def update_user_related_data(self, user, device_data=None, location_data=None):
        """Helper: create/update device & location data for user"""
        if device_data:
            device_data["user"] = user.id
            serializer = DevicesSerializer(data=device_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if location_data:
            location_data["user"] = user.id
            serializer = LocationSerializer(data=location_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def generate_tokens(self, user):
        """Helper: return JWT tokens for a user"""
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def post(self, request):
        try:
            user_data = request.data.get("users") or {}
            email = user_data.get("email")
            device_data = request.data.get("device")
            location_data = request.data.get("location")

            if not email:
                return CustomResponse.error(
                    message="Invalid request",
                    errors="Email is required",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # 🔹 Case 1: Existing user
            user = User.objects.filter(email=email).first()
            if user:
                self.update_user_related_data(user, device_data, location_data)
                tokens = self.generate_tokens(user)
                return CustomResponse.success(
                    message="User login successfully.",
                    data={**tokens, "user_details": UserSerializer(user).data},
                    status_code=status.HTTP_200_OK,
                )
            # 🔹 Case 2: New user (check allowed emails)
            user_mail = CompanyUserMails.objects.filter(email=email).first()
            if not user_mail:
                return CustomResponse.error(
                    message="Error creating user",
                    errors="Contact HR - Invalid User",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                serializer = UserSerializer(data=user_data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.set_password(self.generate_password())
                user.save()
                # assign role from CompanyUserMails
                if user_mail.role:
                    user.role = user_mail.role
                    user.save()

                self.update_user_related_data(user, device_data, location_data)
                tokens = self.generate_tokens(user)

            return CustomResponse.success(
                message="User created successfully.",
                data={**tokens, "user_details": UserSerializer(user).data},
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error processing request",
                errors=str(e),
                message="Error deleting user.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



