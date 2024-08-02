from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = "__all__"


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
