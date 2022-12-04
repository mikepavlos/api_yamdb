from rest_framework import permissions
from reviews.models import User


class IsAdminRole(permissions.BasePermission):
    """Разрешения для администратора"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.ADMIN
            or request.user.is_staff
            or request.user.is_superuser
        )
