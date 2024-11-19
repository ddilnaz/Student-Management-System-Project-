from django.urls import path
from . import views

urlpatterns = [
    path('attendances/', views.AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendances/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
]
