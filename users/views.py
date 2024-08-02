from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema, OpenApiExample
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


@extend_schema(
    tags=["User"],
    request=CustomUserSerializer,
    responses={
        200: TokenSerializer,
        400: MessageSerializer,
    },
    description="Authenticate a user and return a CSRF token",
    examples=[
        OpenApiExample(
            "Successful Login",
            summary="A successful login example",
            description="Example of a successful login response",
            value={"message": "Login successful", "csrf_token": "csrf-token-value"},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Invalid Credentials",
            summary="An unsuccessful login example",
            description="Example of an unsuccessful login response due to invalid credentials",
            value={"error": "Invalid Credentials"},
            response_only=True,
            status_codes=["400"],
        ),
    ],
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
        responses={
            200: CustomUserSerializer,
            400: MessageSerializer,
        },
        description="Get the authenticated user's details",
        examples=[
            OpenApiExample(
                "Authenticated User",
                summary="Example of a successful response with authenticated user data",
                description="Returns the details of the authenticated user",
                value={
                    "email": "user@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "events_joined": ["list of events the user has join"],
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Unauthenticated User",
                summary="Example of an unauthenticated response",
                description="Returns an error message when the user is not authenticated",
                value={"error": "User is not authenticated"},
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST
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
        session_key = request.session.session_key
        if session_key:
            Session.objects.filter(session_key=request.session.session_key).delete()
        return Response(
            {"message": "Logout Successful"},
            status=status.HTTP_200_OK,
        )
