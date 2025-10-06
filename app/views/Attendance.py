 
from datetime import date, datetime, timedelta
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from app import permission
from app.core import BaseCORSExemptAPIView
from app.models.attendence_model import Attendance
from app.serializers.Attendance import   AttendanceReportSerializer, AttendanceSerializer, DayAttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from app.response import CustomResponse
from django.contrib.auth import get_user_model
 
 
class AttendanceMarkView(BaseCORSExemptAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = []  # public access
    parser_classes = [MultiPartParser, FormParser]  

    def post(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                attendance = serializer.save()
                return CustomResponse.success(
                    message="Attendance marked successfully",
                    data=AttendanceSerializer(attendance).data,
                    status_code=status.HTTP_201_CREATED
                )
            else:
                return CustomResponse.error(
                    message="Error marking attendance",
                    errors=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return CustomResponse.error(
                message="Error creating attendance",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 
class AttendanceByUserView(BaseCORSExemptAPIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            UserModel = get_user_model()
            user_id = request.query_params.get('user_id')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            # ✅ Get user
            if user_id:
                try:
                    user = UserModel.objects.get(id=user_id)
                except UserModel.DoesNotExist:
                    return CustomResponse.error(
                        message="User not found",
                        errors=f"No user with id {user_id}",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            else:
                user = request.user
                if not user or not user.is_authenticated:
                    return CustomResponse.error(
                        message="Authentication required",
                        errors="Login required or provide user_id",
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )

            # ✅ Base Query
            attendances = Attendance.objects.filter(user=user).order_by('-check_in')

            # ✅ Date Range Filtering (optional)
            if start_date and end_date:
                try:
                    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                except ValueError:
                    return CustomResponse.error(
                        message="Invalid date format",
                        errors="Use format YYYY-MM-DD for start_date and end_date",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

                attendances = attendances.filter(check_in__date__range=[start_date_obj, end_date_obj])

            elif start_date or end_date:
                return CustomResponse.error(
                    message="Both start_date and end_date are required",
                    errors="Provide both start_date and end_date for range filter",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Serialize data
            serializer = AttendanceReportSerializer(attendances, many=True)

            # ✅ Display user name/email gracefully
            user_display = getattr(user, 'name', None) or getattr(user, 'full_name', None) or getattr(user, 'email', 'User')

            return CustomResponse.success(
                message=f"Attendance report for {user_display} fetched successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            return CustomResponse.error(
                message="Error fetching attendance report",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DayAttendanceView(BaseCORSExemptAPIView):

    authentication_classes = []   
    permission_classes = [] 
     

    def get(self, request, *args, **kwargs):
        date_str = request.query_params.get("date")

        if not date_str:
            return CustomResponse.error(
                message="Please provide ?date=YYYY-MM-DD",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return CustomResponse.error(
                message="Invalid date format. Use YYYY-MM-DD",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DayAttendanceSerializer({"date": selected_date})
        return CustomResponse.success(
            message=f"Attendance report for {selected_date}",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )