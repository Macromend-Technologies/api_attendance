from rest_framework import serializers
from app.models.role_model import AccessTypes, Designation, Roles
 
class AccessTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTypes
        fields = [
            "id",
            "actions",
            "param",
        ]
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = [
            "id",
            "name", 
        ]
class RolesSerializer(serializers.ModelSerializer):
    access = serializers.SlugRelatedField(
        many=True,
        slug_field="id",               # accept IDs when writing
        queryset=AccessTypes.objects.all()
    )


    class Meta:
        model = Roles
        fields = ["id", "name", "access"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "access": [
                {
                    "id": a.id,
                    "actions": a.actions,
                    "param": a.param
                } for a in instance.access.all()
            ]  
        }