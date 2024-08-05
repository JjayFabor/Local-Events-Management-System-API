from rest_framework import permissions


class IsGovernmentAuthority(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.groups.filter(name="Government Authority").exists()
        )
