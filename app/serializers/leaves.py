
from rest_framework import serializers
from app.models.device_model import UserDevices, UserLocation
from app.models.leaves_model import Leaves
from app.models.user_model import CustomUser

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = [
            "id",
            "user",
            "purpose" ,
            
        ]