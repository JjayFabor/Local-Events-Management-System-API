from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from django.urls import reverse
from django.shortcuts import render
from django.db import transaction
from drf_spectacular.utils import (
    extend_schema,
    OpenApiRequest,
    OpenApiResponse,
)
from .serializers import *
from .models import CustomUser
from .openapi_examples import (
    regular_user_example,
    user_response_example,
    error_response_example,
    success_confirm_example,
    error_confirm_example,
    login_successful_example,
    login_invalid_credentials_example,
    authenticated_user_example,
    unauthenticated_user_example,
    retrieve_user_profile_examples,
    update_user_profile_examples,
)
from api.utils import send_confirmation_email


@extend_schema(
    tags=["User"],
    request=OpenApiRequest(CustomUserSerializer, examples=[regular_user_example]),
    responses={
        201: OpenApiResponse(
            response=CustomUserSerializer, examples=[user_response_example]
        ),
        400: OpenApiResponse(
            response=MessageSerializer, examples=[error_response_example]
        ),
    },
    description="Register a new user",
)
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    user.is_active = False
                    user.save()

                    # generate confirmation URL
                    confirmation_url = request.build_absolute_uri(
                        reverse("confirm-email", args=[user.id])
                    )

                    # send confirmation email
                    send_confirmation_email(user, confirmation_url)

                    headers = self.get_success_headers(serializer.data)
                    response_data = {
                        "message": "Check your email for account confirmation",
                        "user": serializer.data,
                        "user_id": user.id,
                    }
                    return Response(
                        response_data, status=status.HTTP_201_CREATED, headers=headers
                    )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handle email confirmation
@extend_schema(
    tags=["User"],
    responses={
        200: OpenApiResponse(
            description="Email confirmed, you can now log in.",
            examples=[success_confirm_example],
        ),
        404: OpenApiResponse(
            description="Invalid Confirmation Link.", examples=[error_confirm_example]
        ),
    },
    description="Handle email confirmation process",
)
class ConfirmEmailView(APIView):
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            return render(
                request,
                "emails/confirmed_email.html",
                {"message": "Email confirmed, you can now log in."},
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return render(
                request,
                "emails/confirmed_email.html",
                {"message": "Invalid Confirmation Link."},
                status=status.HTTP_404_NOT_FOUND,
            )


@extend_schema(
    tags=["User"],
    request=CustomUserSerializer,
    responses={
        200: TokenSerializer,
        400: MessageSerializer,
    },
    description="Authenticate a user and return a CSRF token",
    examples=[
        login_successful_example,
        login_invalid_credentials_example,
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


class UserProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        tags=["User"],
        operation_id="retrieve_user_profile",
        summary="Retrieve User Profile",
        description="Retrieve the profile details of the authenticated user.",
        responses={200: UserProfileSerializer},
        examples=retrieve_user_profile_examples,
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["User"],
        operation_id="update_user_profile",
        summary="Update User Profile",
        description="Update the profile details of the authenticated user. The email field is excluded from being updated.",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        examples=update_user_profile_examples,
    )
    def patch(self, request, *args, **kwargs):
        user = self.request.user

        data = request.data.copy()
        data.pop("email", None)

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
