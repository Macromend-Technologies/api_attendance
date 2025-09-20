from rest_framework import serializers
from app.models.role_model import  Access, AccessItems, Actions, Designation, Roles
 
class AccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Access
        fields = [
            "id",
            "role",
            "action",
            "param",
        ]

        
        
class AccessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Access
        fields = ["id", "role", "actions", "param"]

    def to_representation(self, instance):
        # Grouped representation by role
        return {
            "id": instance.id,
            "role": instance.role.name if instance.role else None,
            "action_details": [
                {
                    "id": instance.action.id,
                    "action": instance.action.name,
                    "param": [p.param for p in instance.param.all()],
                }
            ]
        }
        
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = [
            "id",
            "name", 
        ]
class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Roles
        fields = ["id", "name" ]

class RolesDetailsSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField()

    class Meta:
        model = Roles
        fields = ["id", "name", "access"]

    def get_access(self, obj):
        accesses = Access.objects.filter(role=obj)
        if not accesses.exists():
            return []  # return empty list if no access
        return [
            {
                "id": access.id,
                "action": {
                    "id": access.action.id,
                    "name": access.action.name,
                },
                "param": [p.param for p in access.param.all()],
            }
            for access in accesses
        ]

     
