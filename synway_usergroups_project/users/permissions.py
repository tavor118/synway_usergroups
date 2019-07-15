"""Custom permissions for users application."""

from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    """Permissions for admin and logged in user."""
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
