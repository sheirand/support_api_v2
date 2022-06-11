from core.celery import app
from issue.services import send_email


@app.task
def send_notification(user_email: str = None, pk: int = None, status: str = None, assignee: str = None):
    """Email notification task for Celery"""
    send_email(user_email, pk, status, assignee)
