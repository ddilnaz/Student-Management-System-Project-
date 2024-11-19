"""
URL configuration for StudentManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Student Management System API",
        default_version="v1",
        description="API documentation for the Student Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@sms.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include application URLs
    path('api/users/', include('users.urls')),           # URLs for users app
    path('api/students/', include('students.urls')),     # URLs for students app
    path('api/courses/', include('courses.urls')),       # URLs for courses app
    path('api/grades/', include('grades.urls')),         # URLs for grades app
    path('api/attendance/', include('attendance.urls')), # URLs for attendance app
    # path('api/notifications/', include('notifications.urls')), # URLs for notifications app

    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #bonus task
     path('analytics/', include('analytics.urls')),

    # changes about token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
