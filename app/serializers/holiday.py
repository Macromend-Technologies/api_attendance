from rest_framework import serializers

from app.models.holiday_model import HolidayMonthsDates, Holidays

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = [
            "id",
            "year", 
        ]
        
class HolidayMonthMappingSerializer(serializers.ModelSerializer):
    year = serializers.PrimaryKeyRelatedField(
        queryset=Holidays.objects.all()
    )
    class Meta:
        model = HolidayMonthsDates
        fields = [
            "id",
            "year", 
            "month",
            "date",
            "purpose"
        ]