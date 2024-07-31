from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import *


class CategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class EventView(generics.CreateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
