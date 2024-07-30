from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_organizer": {"read_only": True},
            "organizer_request": {"read_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def validate_name(self, first_name, last_name):
        if not first_name and last_name:
            raise serializers.ValidationError(_("This is field is required"))
        return first_name, last_name
