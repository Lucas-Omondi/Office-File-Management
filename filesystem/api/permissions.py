from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user_role = getattr(request.user, 'role', 'No role found')
        is_super_admin = request.user.is_authenticated and user_role == "Super admin"

        print(f"DEBUG: Checking IsSuperAdmin for {request.user}, Role={user_role}, IsSuperAdmin={is_super_admin}")

        if is_super_admin:
            print("DEBUG: ✅ IsSuperAdmin passed")
        else:
            print("DEBUG: ❌ IsSuperAdmin failed")

        return is_super_admin
class IsAdmin(permissions.BasePermission):
    """
    Admin can upload, edit, and delete files but cannot add users.
    """
    def has_permission(self, request, view):
        user_role = getattr(request.user, 'role', 'No role found')
        is_admin = request.user.is_authenticated and user_role == "Admin"

        print(f"DEBUG: Checking IsAdmin for {request.user}, Role={user_role}, IsAdmin={is_admin}")
        return is_admin  # ✅ True if user is an admin

class IsBasicUser(permissions.BasePermission):
    """
    Basic User can only view and download files but cannot edit or delete.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "Basic"

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS  # Only allows GET (view/download)


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user_role = getattr(request.user, 'role', 'No role found')
        is_admin = request.user.is_authenticated and user_role == "Admin"
        is_super_admin = request.user.is_authenticated and user_role == "Super admin"

        print(f"DEBUG: Checking IsAdminOrSuperAdmin for {request.user}, Role={user_role}, IsAdmin={is_admin}, IsSuperAdmin={is_super_admin}")

        if is_admin or is_super_admin:
            print("DEBUG: ✅ Access granted to Admin or SuperAdmin")
            return True

        print("DEBUG: ❌ Access denied for Admin & SuperAdmin")
        return False