from rest_framework import serializers
from app.models.role_model import Designation, Roles
from app.models.usermail_model import CompanyUserMails
 
class CompanyUserMailsSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all()
    )
    designation = serializers.SlugRelatedField(
        many=True,
        slug_field="id",               # accept IDs when writing
        queryset=Designation.objects.all()
    )
    class Meta:
        model = CompanyUserMails
        fields = [
            "id",
            "email",
            "role",
            "designation"
        ]
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["role"] = {
            "id": instance.role.id,
            "name": instance.role.name
        }
        response["designation"]=[
                {
                    "id": a.id,
                    "designation": a.name,
                }for a in instance.designation.all() 
            ]
        return response