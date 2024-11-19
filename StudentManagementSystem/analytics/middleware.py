from .models import ApiRequestLog

class ApiRequestLoggingMiddleware:
    """Middleware для логирования запросов к API."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):  # или другой путь для вашего API
            ApiRequestLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                endpoint=request.path,
                method=request.method
            )

        response = self.get_response(request)
        return response
