from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.conf import settings

class ApiRequestLog(models.Model):
    """Лог запросов к API."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    endpoint = models.CharField(max_length=255)  
    method = models.CharField(max_length=10)  
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Request by {self.user} to {self.endpoint} at {self.timestamp}"


class CourseAnalytics(models.Model):
    """Аналитика популярности курсов."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    request_count = models.PositiveIntegerField(default=0)  # количество запросов к курсу

    def __str__(self):
        return f"{self.course.name} - {self.request_count} requests"

    def track_course_view(course):
        """Функция для отслеживания популярности курса."""
        analytics, created = CourseAnalytics.objects.get_or_create(course=course)
        analytics.request_count += 1
        analytics.save()

