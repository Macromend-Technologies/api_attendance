from app.core import BaseCORSExemptAPIView
from app.models.holiday_model import HolidayMonthsDates, Holidays
from app.response import CustomResponse
from app.serializers.holiday import HolidayMonthMappingSerializer, HolidaySerializer
from rest_framework import status
# Create Holiday Mapping
from django.db import transaction


class HolidayMappingList(BaseCORSExemptAPIView):
    permission_classes = []
    def get(self, request):
        try:
            holidays_instance =HolidayMonthsDates.objects.all()
            
            return CustomResponse.success(
                data={
                     "holidays": HolidayMonthMappingSerializer(holidays_instance, many=True).data,
                },
                message="Holidays created successfully",
                status_code=status.HTTP_201_CREATED,
            )
             
        except Exception as e:
            # ✅ if error → rollback
            return CustomResponse.error(
                message="Error creating Holidays",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    

class HolidayMappingCreate(BaseCORSExemptAPIView):
    permission_classes = []
    def post(self, request):
        try:
            with transaction.atomic():  # ✅ wrap everything in one transaction
                # Save year
                year_serializer = HolidaySerializer(data={"year": request.data.get("year")})
                year_serializer.is_valid(raise_exception=True)
                year_instance = year_serializer.save()

                holidays_data = request.data.get("holidays", [])

                # Flatten nested structure
                holiday_objects = [
                    HolidayMonthsDates(
                        year=year_instance,
                        month=month_name,
                        date=int(h.get("date")),
                        purpose=h.get("holiday"),
                    )
                    for month_dict in holidays_data
                    for month_name, holiday_list in month_dict.items()
                    for h in holiday_list
                ]

                # Bulk create in one query
                HolidayMonthsDates.objects.bulk_create(holiday_objects)

            # ✅ if no error → commit
            return CustomResponse.success(
                data={
                    "year": HolidaySerializer(year_instance).data,
                    "holidays": HolidayMonthMappingSerializer(holiday_objects, many=True).data,
                },
                message="Holidays created successfully",
                status_code=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # ✅ if error → rollback
            return CustomResponse.error(
                message="Error creating Holidays",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            

class HolidayMappingUpdate(BaseCORSExemptAPIView):
    permission_classes = []

    def patch(self, request, pk):
        try:
            with transaction.atomic():
                # 🔹 Get existing year object
                year_instance = Holidays.objects.get(pk=pk)

                # 🔹 Update year if provided
                year_data = request.data.get("year")
                if year_data:
                    year_serializer = HolidaySerializer(year_instance, data={"year": year_data}, partial=True)
                    year_serializer.is_valid(raise_exception=True)
                    year_instance = year_serializer.save()
                else:
                    year_serializer = HolidaySerializer(year_instance)

                # 🔹 Replace old holidays with new ones
                holidays_data = request.data.get("holidays", [])

                # Delete old holidays for this year (clean update)
                HolidayMonthsDates.objects.filter(year=year_instance).delete()

                # Prepare new holiday objects
                holiday_objects = [
                    HolidayMonthsDates(
                        year=year_instance,
                        month=month_name,
                        date=int(h.get("date")),
                        purpose=h.get("holiday"),
                    )
                    for month_dict in holidays_data
                    for month_name, holiday_list in month_dict.items()
                    for h in holiday_list
                ]

                # Bulk create
                HolidayMonthsDates.objects.bulk_create(holiday_objects)

            return CustomResponse.success(
                data={
                    "year": year_serializer.data,
                    "holidays": HolidayMonthMappingSerializer(holiday_objects, many=True).data,
                },
                message="Holidays updated successfully",
                status_code=status.HTTP_200_OK,
            )

        except Holidays.DoesNotExist:
            return CustomResponse.error(
                message="Year not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return CustomResponse.error(
                message="Error updating Holidays",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )