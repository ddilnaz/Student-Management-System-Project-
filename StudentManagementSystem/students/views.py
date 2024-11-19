from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from .models import Student
from .serializers import StudentSerializer
from .permissions import IsAdminOrReadOnly, IsStudentOrAdmin

import logging
from django.http import HttpResponse


logger = logging.getLogger('my_project')

def student_view(request):
    try:
       
        logger.info("Successfully accessed the students page.")
        return HttpResponse("Success")
    except Exception as e:
        
        logger.error("An error occurred while accessing students: %s", e)
        return HttpResponse("Error", status=500)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        """
        Use caching to optimize profile retrieval.
        """
        student_id = kwargs['pk']
        cached_student = cache.get(f"student_{student_id}")
        if cached_student:
            return Response(cached_student, status=status.HTTP_200_OK)

        student = self.get_object()
        serializer = self.get_serializer(student)
        cache.set(f"student_{student_id}", serializer.data, timeout=3600)  # Cache for 1 hour
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsStudentOrAdmin])
    def my_profile(self, request):
        """
        Allow a student to view their own profile.
        """
        student = self.queryset.filter(user=request.user).first()
        if not student:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(student)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Invalidate cache on update.
        """
        instance = serializer.save()
        cache.delete(f"student_{instance.id}")
        return instance
