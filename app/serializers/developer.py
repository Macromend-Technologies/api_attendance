from rest_framework import serializers

from app.models.developer_model import Developer


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = [
            "name",
            "email",
            "password",
            
        ]
    