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
        
class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevices
        fields = [
            "id",
            "user",
            "device_name",
            "finger_print",
        ]


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "mobile",
            "location",  
            "device"     
        ]
    def get_location(self, obj):
        last = obj.user_location.order_by("-id").first()
        return LocationSerializer(last).data if last else None

    def get_device(self, obj):
        last = obj.user_device.order_by("-id").first()
        return DevicesSerializer(last).data if last else None

 
