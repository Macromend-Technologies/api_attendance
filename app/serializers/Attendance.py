from rest_framework import serializers
from app.models.attendence_model import Attendance
from app.models.device_model import UserDevices, UserLocation

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            "id",
            "user",
            "mark_type",
            "check_in",
            "check_out",
            "image",
            "latitude",
            "longitude",
            "fingerprint",
             
        ]
        read_only_fields = ["created_at", "time", "user"]

    def validate(self, attrs):
        user = self.context['request'].user
        mark_type = attrs.get('mark_type')
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        fingerprint = attrs.get('fingerprint')
        image = attrs.get('image')      

        # Check if fingerprint matches registered fingerprint
        user_fingerprints = UserDevices.objects.filter(user__email=user.email).values_list('finger_print', flat=True)
        if fingerprint not in  user_fingerprints:
            raise serializers.ValidationError("Fingerprint does not match registered user")
        
        user_location = UserLocation.objects.filter(user=user).first()
        if not user_location:
            raise serializers.ValidationError("User location not registered")

        # Check location match (tolerance 0.01 ~ 1km)
        lat_diff = abs(float(latitude) - float(user_location.latitude))
        lon_diff = abs(float(longitude) - float(user_location.longitude))
        if lat_diff > 0.01 or lon_diff > 0.01:
            raise serializers.ValidationError("Current location does not match registered location")
        
        if mark_type == "IN" and not check_in:
            raise serializers.ValidationError({"check_in": "Check-in datetime is required"})
        if mark_type == "OUT" and not check_out:
            raise serializers.ValidationError({"check_out": "Check-out datetime is required"})


        # Check check_in exists
        if mark_type == "IN":
            if Attendance.objects.filter(user=user, mark_type="IN", check_in__date=check_in.date()).exists():
                raise serializers.ValidationError("User already checked in for today")
        elif mark_type == "OUT":
            # find last IN today
            last_in = Attendance.objects.filter(user=user, mark_type="IN", check_in__date=check_out.date()).last()
            if not last_in:
                raise serializers.ValidationError("User has not checked in today")
            # find last OUT linked to that IN
            last_out = Attendance.objects.filter(user=user, mark_type="OUT", check_in=last_in.check_in).last()
            # allow multiple OUT
            attrs['check_in'] = last_in.check_in
            if last_out:
                attrs['time'] = (last_out.time or (last_out.check_out - last_in.check_in)) + (check_out - last_out.check_out)
            else:
                attrs['time'] = check_out - last_in.check_in
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        image = validated_data.get('image')
        instance = Attendance.objects.create(user=user, **validated_data)
        
        if image:
            instance.image = image

        if instance.check_in and instance.check_out:
            instance.time = instance.check_out - instance.check_in
            instance.save()

        return instance
    

# class AttendanceReportSerializer(serializers.ModelSerializer):
#     is_leave = serializers.SerializerMethodField()
#     is_permission = serializers.SerializerMethodField()
#     is_holiday = serializers.SerializerMethodField()
#     check_in_time = serializers.SerializerMethodField()
#     check_out_time = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()


#     class Meta:
#         model = Attendance
#         fields =[
#             "id",
#             "date",
#             "is_leave",
#             "is_permission",
#             "is_holiday",
#             "check_in_time",
#             "check_out_time",
#             "image"
#         ]  

#     def get_data(self,obj):
#         return obj.check_in.date() if obj.check_in else None

#     def get_is_leave(self, obj):
#         user = obj.user 
#         return LeaveRequest.object.filter(user=user, date=obj.check_in.date(), leave_type="leave").exists()
          
#     def get_is_permission(self, obj):
#         user = obj.user 
#         return LeaveRequest.objects.filter(user=user, date=obj.check_in.date(),leave_type="permission").exists()
    
#     def get_is_holiday(self,obj):
#         return False
    
#     def get_check_in_time(self, obj):
#         return obj.check_in.strftime("%I:%M %p") if obj.check_in else None
    
#     def get_check_out_time(self, obj):
#         return obj.check_out.strftime("%I:%M %p") if obj.check_out else None
    
#     def get_image(self, obj):
#         return obj.selfie.url if obj.selfie else None