from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from .models import Grade
from .serializers import GradeSerializer
from .permissions import IsTeacherOrAdmin, IsStudentTeacherOrAdmin


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_permissions(self):
        """
        Set different permissions for different actions.
        """
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsStudentTeacherOrAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Set the teacher as the logged-in user.
        """
        serializer.save(teacher=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsStudentTeacherOrAdmin])
    def my_grades(self, request):
        """
        List grades for the logged-in student.
        """
        if request.user.role != 'student':
            return Response({"error": "Only students can view their grades."}, status=status.HTTP_403_FORBIDDEN)

        grades = self.queryset.filter(student__user=request.user)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Use caching to optimize the list endpoint.
        """
        cached_grades = cache.get('grades_list')
        if cached_grades:
            return Response(cached_grades, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set('grades_list', response.data, timeout=3600)  # Cache for 1 hour
        return response

    def perform_update(self, serializer):
        """
        Invalidate cache on update.
        """
        instance = serializer.save()
        cache.delete('grades_list')
        return instance
