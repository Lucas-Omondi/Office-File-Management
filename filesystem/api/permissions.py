from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Super Admin has full permissions, including adding/registering new users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "super_admin"


class IsAdmin(permissions.BasePermission):
    """
    Admin can upload, edit, and delete files but cannot add users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsBasicUser(permissions.BasePermission):
    """
    Basic User can only view and download files but cannot edit or delete.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "basic_user"

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS  # Only allows GET (view/download)
