from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ApiRequestLog, CourseAnalytics

class AnalyticsView(APIView):
    """Представление для отображения статистики."""
    def get(self, request):
        # Получаем количество всех запросов
        total_requests = ApiRequestLog.objects.count()

        # Получаем топ-5 популярных курсов
        top_courses = CourseAnalytics.objects.order_by('-request_count')[:5]

        return Response({
            'total_requests': total_requests,
            'top_courses': [{
                'course_name': course.course.name,
                'request_count': course.request_count
            } for course in top_courses]
        })
