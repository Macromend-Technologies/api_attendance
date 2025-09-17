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

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "mobile",   
        ]
 

 
