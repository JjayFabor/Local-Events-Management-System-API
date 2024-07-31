from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser


class AllowIfNoAdminUserExists(BasePermission):
    def has_permission(self, request, view):
        if CustomUser.objects.filter(is_superuser=True).exists():
            raise PermissionDenied(detail="An admin user already exists.")
        return True
