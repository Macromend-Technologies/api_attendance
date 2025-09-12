from rest_framework import serializers
from app.models.device_model import UserDevices, UserLocation
from app.models.user_model import CustomUser

 
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = [
            "id",
            "user",
            "latitude",
            "longitude",
        ]
        extra_kwargs = {"user": {"write_only": True}}
        
class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevices
        fields = [
            "id",
            "user",
            "device_name",
            "finger_print",
        ]
        extra_kwargs = {"user": {"write_only": True}}

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "mobile", 
            "password"
        ]
        extra_kwargs = {
            "password": {"write_only": True}  # 🔥 hide password in response
        }
    def create(self, validated_data):
        print("validated_data",validated_data)
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)  # 🔥 hash password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # 🔥 update with hash
        instance.save()
        return instance
 
 
