from rest_framework import serializers
from app.models.user_model import CustomUser

 


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "mobile",
            # "department_name",
            # "role_name",
        ]

 
