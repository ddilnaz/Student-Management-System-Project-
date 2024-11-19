from rest_framework import serializers
from .models import Student
from users.models import User


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'dob', 'registration_date']
