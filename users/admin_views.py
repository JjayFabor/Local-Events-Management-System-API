from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import AdminSerializer, MessageSerializer
from .permissions import AllowIfNoAdminUserExists
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema


class BaseAdminCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer

    @extend_schema(
        responses={
            201: AdminSerializer,
            400: MessageSerializer,
        },
        description="Created an Admin Account.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class InitialAdminCreateView(BaseAdminCreateView):
    permission_classes = [AllowIfNoAdminUserExists]


class CreateAdminView(BaseAdminCreateView):
    permission_classes = [IsAuthenticated, IsAdminUser]
