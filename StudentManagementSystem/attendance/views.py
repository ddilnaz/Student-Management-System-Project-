from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import IsTeacherOrAdmin, IsStudent


class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated & IsTeacherOrAdmin]


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated() & IsStudent()]
        return [IsAuthenticated() & IsTeacherOrAdmin()]
