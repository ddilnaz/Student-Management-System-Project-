from celery import shared_task

@shared_task
def send_attendance_reminder():
    pass

@shared_task
def send_grade_update_notification():
    pass
from celery import shared_task

@shared_task
def send_notification(email, message):
    print(f"Sending notification to {email}: {message}")
    return f"Notification sent to {email}"
