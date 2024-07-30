from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "is_organizer": {"read_only": True},
            "organizer_request": {"read_only": True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

    def validate_name(self, first_name, last_name):
        if not first_name and last_name:
            raise serializers.ValidationError(_("This is field is required"))
        return first_name, last_name
