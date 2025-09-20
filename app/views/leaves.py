from datetime import datetime
from app.core import BaseCORSExemptAPIView
from app.models.leaves_model import LeaveType, Leaves, LeavesDates
from app.permission import CustomUser, DeveloperJWTAuthentication
from app.response import CustomResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
class LeaveRequestView(BaseCORSExemptAPIView):
    authentication_classes = [DeveloperJWTAuthentication]  # ✅ custom auth
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create new Leave Request"""
        try:
            data = request.data
            leave_type_id = data.get("leave_type")

            # Validate LeaveType in one step
            try:
                User = CustomUser.objects.get(id=request.user.id)
            except CustomUser.DoesNotExist:
                return CustomResponse.error(
                    message="Invalid User",
                    errors={"leave_type": f"User Invalid "},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            try:
                leave_type = LeaveType.objects.get(id=leave_type_id)
            except LeaveType.DoesNotExist:
                return CustomResponse.error(
                    message="Invalid leave type",
                    errors={"leave_type": f"LeaveType with id {leave_type_id} does not exist"},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Create the Leave
            leave = Leaves.objects.create(
                user=request.user,
                date_range=data.get("date_range"),
                leave_type=leave_type,
                purpose=data.get("purpose", ""),
            )

            # Bulk create LeaveDates if provided
            dates = data.get("dates") or []
            leave_dates = []
            for date_str in dates:
                try:
                    parsed_date = datetime.strptime(date_str, "%d/%m/%Y")  # convert "01/01/2025"
                    leave_dates.append(LeavesDates(leave=leave, date=parsed_date))
                except ValueError:
                    return CustomResponse.error(
                        message="Invalid date format. Use DD/MM/YYYY.",
                        errors={"date": date_str},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

            LeavesDates.objects.bulk_create(leave_dates)

            return CustomResponse.success(
                data={"leave_id": leave.id},
                message="Leave request created successfully",
                status_code=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return CustomResponse.error(
                message="Error creating leave request",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )