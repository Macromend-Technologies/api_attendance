from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from app.core import BaseCORSExemptAPIView
from app.models.attendence_model import Attendance
from app.serializers.Attendance import  AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from app.response import CustomResponse

 
 
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
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

# class AttendanceReportView(BaseCORSExemptAPIView):
#     permission_classes =[]

#     def get(self, request):
#         user = request.user

#         attendance_qs = Attendance.objects.filter(user=user).order_by('check_in')
#         serializer = AttendanceReportSerializer(attendance_qs, many = True)

#         return CustomResponse({
#             "status": True,
#             "message": "Request information received successfully",
#             "data": serializer.data
           
#         })
