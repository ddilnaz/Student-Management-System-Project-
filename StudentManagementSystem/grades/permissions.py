from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherOrAdmin(BasePermission):
    """
    Allows only teachers or admins to create/update grades.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['teacher', 'admin']


class IsStudentTeacherOrAdmin(BasePermission):
    """
    Allows students to view their own grades, and teachers/admins full access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'student':
            return obj.student.user == request.user
        return request.user.role in ['teacher', 'admin']
