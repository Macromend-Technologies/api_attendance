
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from app.models.developer_model import Developer
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
class DeveloperJWTAuthentication(JWTAuthentication):
 
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        # 1. Try Developer
        try:
            return Developer.objects.get(id=user_id)
        except Developer.DoesNotExist:
            pass

        # 2. Try CustomUser (default user model)
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")