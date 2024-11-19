from celery import shared_task

@shared_task
def send_attendance_reminder():
    pass

@shared_task
def send_grade_update_notification():
    pass
