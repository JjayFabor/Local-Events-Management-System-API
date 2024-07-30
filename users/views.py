from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from django.http import JsonResponse


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        Session.objects.filter(session_key=request.session.session_key).delete()
        return Response(
            {"message": "Logout Successful"},
            status=status.HTTP_200_OK,
        )
