from rest_framework import serializers
from app.models.role_model import Designation, Roles
from app.models.usermail_model import CompanyUserMails
 
class CompanyUserMailsCreateSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Roles.objects.all()
    )
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all()
    )
    
    class Meta:
        model = CompanyUserMails
        fields = ["id", "email", "role", "designation"]

    def create(self, validated_data):
        roles = validated_data.pop("role", [])
        user = CompanyUserMails.objects.create(**validated_data)
        user.save()
        if roles:
            user.role.set(roles)
        return user
    
class CompanyUserMailsListSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"   # shows role names
    )
    designation = serializers.StringRelatedField()  # shows designation name

    class Meta:
        model = CompanyUserMails
        fields = ["id", "email", "role", "designation"]