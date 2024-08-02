from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import *
from .permissions import AllowIfNoAdminUserExists
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


@extend_schema(
    tags=["Admin User"],
    responses={
        201: AdminSerializer,
        400: MessageSerializer,
    },
    description="Created an Admin Account.",
)
class BaseAdminCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer


class InitialAdminCreateView(BaseAdminCreateView):
    permission_classes = [AllowIfNoAdminUserExists]


class CreateAdminView(BaseAdminCreateView):
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema(
    tags=["Admin User"],
    request=AdminSerializer,
    responses={
        200: TokenSerializer,
        400: MessageSerializer,
    },
    description="Admin User loging and return refresh and access token",
)
class AdminUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Admin User"],
    responses={
        200: MessageSerializer,
    },
    description="Logout admin user",
)
class AdminUserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Admin Logout Successful"}, status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
