from rest_framework import serializers
from app.models.role_model import Roles
from app.models.usermail_model import CompanyUserMails
 
class CompanyUserMailsSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all()
    )
    class Meta:
        model = CompanyUserMails
        fields = [
            "id",
            "email",
            "role",
        ]
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["role"] = {
            "id": instance.role.id,
            "name": instance.role.name
        }
        return response