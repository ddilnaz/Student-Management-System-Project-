from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from .permissions import IsAdminOrInstructor, IsAdminInstructorOrStudent
from students.models import Student


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrInstructor]

    def list(self, request, *args, **kwargs):
        """
        Use caching to optimize the list endpoint.
        """
        cached_courses = cache.get('courses_list')
        if cached_courses:
            return Response(cached_courses, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set('courses_list', response.data, timeout=3600)  # Cache for 1 hour
        return response

    def perform_create(self, serializer):
        """
        Set the instructor as the logged-in user.
        """
        serializer.save(instructor=self.request.user)

    def perform_update(self, serializer):
        """
        Invalidate cache on update.
        """
        instance = serializer.save()
        cache.delete('courses_list')
        return instance


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminInstructorOrStudent]

    @action(detail=False, methods=['get'], permission_classes=[IsAdminInstructorOrStudent])
    def my_enrollments(self, request):
        """
        List enrollments for the logged-in student.
        """
        if request.user.role != 'student':
            return Response({"error": "Only students can view their enrollments."}, status=status.HTTP_403_FORBIDDEN)

        student = Student.objects.filter(user=request.user).first()
        if not student:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        enrollments = self.queryset.filter(student=student)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
