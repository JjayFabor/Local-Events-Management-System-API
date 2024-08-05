from rest_framework.permissions import BasePermission


class isGovernmentAuthority(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.groups.filter(name="Government Authority").exists()
        )
