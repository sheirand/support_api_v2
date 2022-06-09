from django.core.mail import send_mail


def send_email(user_email: str = None, pk: int = None, status: str = None, assignee: str = None):
    """ Email notification for status change and assign """
    print(user_email, type(user_email))
    print(assignee, type(assignee))
    if status:
        send_mail(
            "Notification from support team!",
            f"The status of your issue (id: {pk}) has been changed to {status}!\n\nBest regards, support team",
            "evosdota@gmail.com",
            [user_email],
            fail_silently=False,
        )
    if assignee:
        send_mail(
            "New issue!",
            f"The issue (id: {pk}) has been assigned to you now!",
            "evosdota@gmail.com",
            [assignee],
            fail_silently=False
        )


