from user.models import User
import datetime
import jwt
from django.conf import settings


def select_user_via_email(email: str) -> "User":
    user = User.objects.filter(email=email).first()

    return user


def create_jwt_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        iat=datetime.datetime.utcnow(),
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    )
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    return token


REQUIRED_FIELDS = {
    "email": "This field is required",
    "password": "This field is required"
}
