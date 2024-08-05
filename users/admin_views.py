from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiRequest
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .openapi_examples import admin_user_example, admin2_user_example
from .permission import IsGovernmentAuthority, HasApiKey
from django.contrib.auth.models import Group


@extend_schema(
    tags=["Admin User"],
    request=OpenApiRequest(AdminSerializer, examples=[admin_user_example]),
    responses={
        201: AdminSerializer,
        400: MessageSerializer,
    },
    description="Created an Admin Account.",
)
class CreateAdminView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [HasApiKey]

    def perform_create(self, serializer):
        user = serializer.save()
        # Directly assign the user to the Government Authority group
        self.add_user_to_group(user)

    def add_user_to_group(self, user):
        # Since is_government_authority is always True for AdminSerializer
        government_group = Group.objects.get(name="Government Authority")
        user.groups.add(government_group)
        print(f"Added {user.email} to Government Authority group.")


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
    permission_classes = [IsGovernmentAuthority, IsAuthenticated]
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
