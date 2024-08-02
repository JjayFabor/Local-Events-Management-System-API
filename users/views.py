from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema
from .serializers import *
from .models import CustomUser


@extend_schema(
    tags=["User"],
    responses={
        201: CustomUserSerializer,
        400: MessageSerializer,
    },
    description="Register a new user",
)
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=["User"],
    request=CustomUserSerializer,
    responses={
        200: TokenSerializer,
        400: MessageSerializer,
    },
    description="Authenticate a user and return a CSRF token",
)
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session["email"] = email
            request.session.save()
            csrf_token = get_token(request)
            return Response(
                {"message": "Login successful", "csrf_token": csrf_token},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid Credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    tags=["User"],
    responses={
        200: MessageSerializer,
    },
    description="Log out the authenticated user",
)
class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        Session.objects.filter(session_key=request.session.session_key).delete()
        return Response(
            {"message": "Logout Successful"},
            status=status.HTTP_200_OK,
        )
