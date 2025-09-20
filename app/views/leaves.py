from datetime import datetime
from app.core import BaseCORSExemptAPIView
from app.core_utiliy import FormDataPageNumberPagination
from app.models.leaves_model import LeaveType, Leaves, LeavesDates
from app.permission import CustomUser, DeveloperJWTAuthentication
from app.response import CustomResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app.serializers.leaves import LeaveSerializer, LeaveTypeSerializer

# LeaveTypes CRUDS-FUNCTIONS
class LeaveTypeListCreateView(BaseCORSExemptAPIView):
    permission_classes = []  # public access

    def get(self, request):
        """List all AccessTypes"""
        try:
            leave_types = LeaveType.objects.all()
            serializer = LeaveTypeSerializer(leave_types, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="LeaveTypes list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error retrieving LeaveTypes list",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """Create new AccessType"""
        try:
            serializer = LeaveTypeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="LeaveTypes created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error creating LeaveTypes",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class LeaveTypesDetailView(BaseCORSExemptAPIView):
    permission_classes = []  # public access

    def get_object(self, pk):
        try: 
            return LeaveType.objects.get(pk=pk)
        except LeaveType.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve single AccessType"""
        role = self.get_object(pk)
        if not role:
            return CustomResponse.error(
                message="LeaveType not found",
                errors=f"LeaveType with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = LeaveTypeSerializer(role)
        return CustomResponse.success(
            data=serializer.data,
            message="LeaveType retrieved successfully",
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        """Update AccessType"""
        role = self.get_object(pk)
        if not role:
            return CustomResponse.error(
                message="LeaveType not found",
                errors=f"LeaveType with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = LeaveTypeSerializer(role, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="LeaveType updated successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error updating LeaveType",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """Delete LeaveType"""
        role = self.get_object(pk)
        if not role:
            return CustomResponse.error(
                message="LeaveType not found",
                errors=f"LeaveType with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        role.delete()
        return CustomResponse.success(
            message="LeaveType deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class LeaveRequestView(BaseCORSExemptAPIView):
    # authentication_classes = []  # ✅ custom auth
    permission_classes = []

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
                user=User,
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
            
            
class LeaveRequestListView(BaseCORSExemptAPIView):
    permission_classes = []
    pagination_class = FormDataPageNumberPagination
    def get(self, request):
        """List all AccessTypes"""
        try:
            leave_types = Leaves.objects.all()
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                leave_types, request, view=self
            )
            
            if paginated_queryset is not None:
                serializer = LeaveSerializer(paginated_queryset, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = LeaveSerializer(leave_types, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="Leave list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error retrieving LeaveTypes list",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    