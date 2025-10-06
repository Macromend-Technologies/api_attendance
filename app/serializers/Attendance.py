
from rest_framework import serializers
from app.auth import User
from app.models.attendence_model import Attendance
from app.models.device_model import UserDevices, UserLocation
from app.models.leaves_model import LeavesDates
from app.models.holiday_model import HolidayMonthsDates

 
    
    
class AttendanceReportSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    is_leave = serializers.SerializerMethodField()
    is_permission = serializers.SerializerMethodField()
    is_holiday = serializers.SerializerMethodField()
    check_in_time = serializers.SerializerMethodField()
    check_out_time = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "date",
            "is_leave",
            "is_permission",
            "is_holiday",
            "check_in_time",
            "check_out_time",
            "image",
            "message"
        ]

    def get_date(self, obj):
        return obj.check_in.strftime("%d/%m/%Y") if obj.check_in else None

    def get_is_leave(self, obj):
        if obj.check_in:
            return LeavesDates.objects.filter(
                date=obj.check_in.date(),
                leave__user=obj.user,
                leave__date_range="single"
            ).exists()
        return False
              
    def get_is_permission(self, obj):
        user = obj.user
        if not obj.check_in:
            return False
        return LeavesDates.objects.filter(
            date=obj.check_in.date(),
            leave__user=obj.user,
            leave__date_range="single"
        ).exists()

    def get_is_holiday(self, obj):
        if obj.check_in:
            return HolidayMonthsDates.objects.filter(
                date=obj.check_in.day,
                month=obj.check_in.strftime("%B"),
                year__year=obj.check_in.year
            ).exists()
        return False

    def get_check_in_time(self, obj):
        return obj.check_in.strftime("%I:%M %p") if obj.check_in else None

    def get_check_out_time(self, obj):
        return obj.check_out.strftime("%I:%M %p") if obj.check_out else None

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_message(self, obj):
        if self.get_is_holiday(obj):
            return "Today is a holiday"
        elif self.get_is_leave(obj):
            return "On leave"
        elif self.get_is_permission(obj):
            return "Permission granted"
        else:
            return "Thank You"

    def to_representation(self, obj):
        rep = super().to_representation(obj)

        # If leave, holiday or permission, remove check_in_time, check_out_time, image fields entirely
        if rep.get("is_leave") or rep.get("is_holiday") or rep.get("is_permission"):
            rep.pop("check_in_time", None)
            rep.pop("check_out_time", None)
            rep.pop("image", None)

        return rep    
  

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
            "time",  # only DurationField
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

        if not image:
            raise serializers.ValidationError("Image is required for attendance marking.")

        user_fingerprints = UserDevices.objects.filter(user__email=user.email).values_list('finger_print', flat=True)
        if fingerprint not in user_fingerprints:
            raise serializers.ValidationError("Fingerprint does not match registered user")

        user_location = UserLocation.objects.filter(user=user).first()
        if not user_location:
            raise serializers.ValidationError("User location not registered")

        lat_diff = abs(float(latitude) - float(user_location.latitude))
        lon_diff = abs(float(longitude) - float(user_location.longitude))
        if lat_diff > 0.01 or lon_diff > 0.01:
            raise serializers.ValidationError("Current location does not match registered location")

        if mark_type == "IN" and not check_in:
            raise serializers.ValidationError({"check_in": "Check-in datetime is required"})
        if mark_type == "OUT" and not check_out:
            raise serializers.ValidationError({"check_out": "Check-out datetime is required"})

        if mark_type == "IN":           
            if Attendance.objects.filter(user=user, mark_type="IN", check_in__date=check_in.date()).exists():
                raise serializers.ValidationError("User already checked in for today")
        elif mark_type == "OUT":
            last_in = Attendance.objects.filter(user=user, mark_type="IN", check_in__date=check_out.date()).last()
            if not last_in:
                raise serializers.ValidationError("User has not checked in today")

            last_out = Attendance.objects.filter(user=user, mark_type="OUT", check_in=last_in.check_in).last()
            attrs['check_in'] = last_in.check_in

            if last_out:
                previous_time = last_out.time if last_out.time else (last_out.check_out - last_in.check_in)
                attrs['time'] = previous_time + (check_out - last_out.check_out)
            else:
                attrs['time'] = check_out - last_in.check_in

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        image = validated_data.pop('image', None)

        instance = Attendance.objects.create(user=user, **validated_data)

        if image:
            instance.image = image

        # Ensure time is correct
        if instance.check_in and instance.check_out:
            instance.time = instance.check_out - instance.check_in
            instance.save()

        return instance
    

class DayUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)
    check_in_time =serializers.SerializerMethodField()
    check_out_time = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ["user_id", "user_name", "check_in_time","check_out_time"]

    def get_check_in_time(self, obj): 
            return obj.check_in.strftime("%I:%M %p") if obj.check_in else None
    
    def get_check_out_time(self,obj):
        return obj.check_out.strftime("%I:%M %p") if obj.check_out else None


class DayAttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        date =obj.get("date")
        same_day_users = Attendance.objects.filter(check_in__date=date).select_related("user")
        return DayUserSerializer(same_day_users, many=True).data


 
 