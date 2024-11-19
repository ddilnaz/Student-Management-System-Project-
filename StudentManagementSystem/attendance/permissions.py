from rest_framework.permissions import BasePermission


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['Teacher', 'Admin']


class IsStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student.user == request.user
