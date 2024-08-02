from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = EventModel
        fields = "__all__"

    @extend_schema_field(serializers.CharField)
    def get_category_name(self, obj):
        return obj.category.name


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name"]


class EventDetailSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = EventModel
        fields = [
            "id",
            "event_name",
            "description",
            "image_url",
            "event_date",
            "location",
            "registration_deadline",
            "capacity",
            "created_at",
            "updated_at",
            "status",
            "category",
            "category_name",
            "participants",
        ]
