from app.core import BaseCORSExemptAPIView
from app.models.role_model import AccessTypes, Roles
from app.response import CustomResponse
from app.serializers.roles import  AccessTypesSerializer, RolesSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
 

class AccessTypesListCreateView(BaseCORSExemptAPIView):
    permission_classes = []  # public access

    def get(self, request):
        """List all AccessTypes"""
        try:
            access_list = AccessTypes.objects.all()
            serializer = AccessTypesSerializer(access_list, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="Access list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error retrieving access list",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """Create new AccessType"""
        try:
            serializer = AccessTypesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Access created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error creating Access",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class AccessTypesDetailView(BaseCORSExemptAPIView):
    permission_classes = [IsAuthenticated]  # public access

    def get_object(self, pk):
        try: 
            return AccessTypes.objects.get(pk=pk)
        except AccessTypes.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve single AccessType"""
        access = self.get_object(pk)
        if not access:
            return CustomResponse.error(
                message="Access not found",
                errors=f"Access with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = AccessTypesSerializer(access)
        return CustomResponse.success(
            data=serializer.data,
            message="Access retrieved successfully",
            status_code=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update AccessType"""
        access = self.get_object(pk)
        if not access:
            return CustomResponse.error(
                message="Access not found",
                errors=f"Access with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = AccessTypesSerializer(access, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Access updated successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error updating Access",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """Delete AccessType"""
        access = self.get_object(pk)
        if not access:
            return CustomResponse.error(
                message="Access not found",
                errors=f"Access with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        access.delete()
        return CustomResponse.success(
            message="Access deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )
# ROLE CRUDS-FUNCTIONS
class RoleListCreateView(BaseCORSExemptAPIView):
    permission_classes = []  # public access

    def get(self, request):
        """List all AccessTypes"""
        try:
            role_list = Roles.objects.all()
            serializer = RolesSerializer(role_list, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="Roles list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error retrieving Roles list",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """Create new AccessType"""
        try:
            serializer = RolesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Role created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error creating Access",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class RoleDetailView(BaseCORSExemptAPIView):
    permission_classes = []  # public access

    def get_object(self, pk):
        try: 
            return Roles.objects.get(pk=pk)
        except Roles.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve single AccessType"""
        role = self.get_object(pk)
        if not role:
            return CustomResponse.error(
                message="Role not found",
                errors=f"Role with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = RolesSerializer(role)
        return CustomResponse.success(
            data=serializer.data,
            message="Role retrieved successfully",
            status_code=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        """Update AccessType"""
        role = self.get_object(pk)
        if not role:
            return CustomResponse.error(
                message="Access not found",
                errors=f"Access with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = RolesSerializer(role, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Role updated successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error updating Access",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """Delete AccessType"""
        role = self.get_object(pk)
        if not role:
            return CustomResponse.error(
                message="Role not found",
                errors=f"Role with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        role.delete()
        return CustomResponse.success(
            message="Access deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )