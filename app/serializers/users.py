from rest_framework import serializers
from app.models.device_model import UserDevices, UserLocation
from app.models.user_model import CustomUser
from app.serializers.roles import RolesDetailsSerializer

 
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
class UserListSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"   # shows role names
    )
    designation = serializers.StringRelatedField()  # shows designation name

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "mobile",
            "role", 
            "designation"
        ]
class UserDetailsSerializer(serializers.ModelSerializer):
    role = RolesDetailsSerializer(many=True, read_only=True)  # nested roles + access
    designation = serializers.StringRelatedField()  # shows designation name
    devices = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "mobile",
            "devices",
            "locations",
            "role", 
            "designation"
        ]
    def get_devices(self, obj):
        latest = obj.user_device.order_by("-id").first()  # get latest device
        if latest:
            return {
                "id": latest.id,
                "device_name": latest.device_name,
                "finger_print": latest.finger_print
            }
        return None

    def get_locations(self, obj):
        latest = obj.user_location.order_by("-id").first()  # get latest location
        if latest:
            return {
                "id": latest.id,
                "latitude": str(latest.latitude),
                "longitude": str(latest.longitude)
            }
        return None

 
