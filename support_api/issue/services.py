from django.conf import settings
from django.core.mail import send_mail


def send_email(user_email: str = None, pk: int = None, status: str = None, assignee: str = None):
    """ Email notification for status change and assign """

    if status:
        send_mail(
            "Notification from support team!",
            f"The status of your issue (id: {pk}) has been changed to {status}!\n\nBest regards, support team",
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
    if assignee:
        send_mail(
            "New issue!",
            f"The issue (id: {pk}) has been assigned to you now!",
            settings.EMAIL_HOST_USER,
            [assignee],
            fail_silently=False
        )
