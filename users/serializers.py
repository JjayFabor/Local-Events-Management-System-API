from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class BaseUserSerializer(serializers.ModelSerializer):
    events_joined = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="event_name"
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name", "events_joined"]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def _create_user(self, validated_data, is_staff=False, is_superuser=False):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user


class CustomUserSerializer(BaseUserSerializer):
    def create(self, validated_data):
        """
        Create a regular user.
        """
        return self._create_user(validated_data)


class AdminSerializer(BaseUserSerializer):
    def create(self, validated_data):
        """
        Create an admin user with staff and superuser status
        """
        return self._create_user(validated_data, is_staff=True, is_superuser=True)


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    csrf_token = serializers.CharField()
