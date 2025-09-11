from app.core import BaseCORSExemptAPIView
from app.models.user_model import CustomUser
from app.response import CustomResponse
from app.serializers.users import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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
                message="Error retrieving users.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class UserRegisterView(BaseCORSExemptAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            print(request.data.get("users"))
            user =request.data.get("users")
            if user:
                userserializer = UserSerializer(user)
                print("serializer user",userserializer)
                userserializer.save()
                
                
            users = CustomUser.objects.all()
            serializer = UserSerializer(userserializer )
            return CustomResponse.success(
                data=serializer.data,
                message="Users Create successfully.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            
            return CustomResponse.error(
                message="Error retrieving users.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )