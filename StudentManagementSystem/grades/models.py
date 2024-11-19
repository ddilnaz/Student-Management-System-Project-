from django.db import models
from django.conf import settings
from courses.models import Course
from students.models import Student


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'teacher'},
        related_name='given_grades'
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['date']

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.grade}"
