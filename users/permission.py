from rest_framework import permissions
from .models import ApiKey


class HasApiKey(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get("Authorization")
        if not api_key:
            return False
        return ApiKey.objects.filter(key=api_key, is_active=True).exists()


class IsGovernmentAuthority(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.groups.filter(name="Government Authority").exists()
        )
