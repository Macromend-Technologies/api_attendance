
from rest_framework import serializers
from app.models.device_model import UserDevices, UserLocation
from app.models.leaves_model import LeaveType, Leaves
from app.models.user_model import CustomUser


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            "id",
            "name"
            
        ]

class LeaveSerializer(serializers.ModelSerializer):
    # user =  serializers.StringRelatedField() 
    
    class Meta:
        model = Leaves
        fields = [
            "id",
            "user",
            "purpose" , 
            "leave_type",
            "status"
        ]