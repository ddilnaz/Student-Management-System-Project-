from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allows access only to Admin for unsafe methods, but allows read-only access for others.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsStudentOrAdmin(BasePermission):
    """
    Allows students to manage their own profiles, and admins to manage all profiles.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.user == request.user
