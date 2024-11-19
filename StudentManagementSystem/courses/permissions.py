from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrInstructor(BasePermission):
    """
    Grants access to Admins and Instructors for unsafe methods.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['admin', 'teacher']


class IsAdminInstructorOrStudent(BasePermission):
    """
    Allows Admins and Instructors full access. Students can view their enrollments only.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin', 'teacher']:
            return True
        if hasattr(obj, 'student'):
            return obj.student.user == request.user
        return False
