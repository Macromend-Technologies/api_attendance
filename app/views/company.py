from app.core import BaseCORSExemptAPIView
from app.models.usermail_model import CompanyUserMails
from app.response import CustomResponse
from app.serializers.company import CompanyUserMailsCreateSerializer, CompanyUserMailsListSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 

class MailListCreateView(BaseCORSExemptAPIView):
    permission_classes = [ ]  # public access

    def get(self, request):
        """List all AccessTypes"""
        try:
            mails_list = CompanyUserMails.objects.all()
            serializer = CompanyUserMailsListSerializer(mails_list, many=True)
            return CustomResponse.success(
                data=serializer.data,
                message="User mail list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error retrieving Mail list",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """Create new AccessType"""
        try:
            serializer = CompanyUserMailsCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Mails created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error creating Mails",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class CompanyUserMailsDetailView(BaseCORSExemptAPIView):
    permission_classes = [IsAuthenticated]  # public access

    def get_object(self, pk):
        try: 
            return CompanyUserMails.objects.get(pk=pk)
        except CompanyUserMails.DoesNotExist:
            return None

    def get(self, request, pk):
        """Retrieve single AccessType"""
        user_mail = self.get_object(pk)
        if not user_mail:
            return CustomResponse.error(
                message="Company Mails not found",
                errors=f"Company Mails with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = CompanyUserMailsSerializer(user_mail)
        return CustomResponse.success(
            data=serializer.data,
            message="Company Mails retrieved successfully",
            status_code=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        """Update AccessType"""
        user_mail = self.get_object(pk)
        if not user_mail:
            return CustomResponse.error(
                message="Access not found",
                errors=f"Access with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = CompanyUserMailsSerializer(user_mail, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Company Mails updated successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return CustomResponse.error(
                message="Error updating Company Mails",
                errors=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """Delete AccessType"""
        user_mail = self.get_object(pk)
        if not user_mail:
            return CustomResponse.error(
                message="Company Mail not found",
                errors=f"Company Mail with id {pk} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        user_mail.delete()
        return CustomResponse.success(
            message="Company Mail deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )