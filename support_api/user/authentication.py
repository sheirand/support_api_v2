import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from user import models


class CustomUserAuthentication(authentication.BaseAuthentication):
    """Authentication based on JWT in COOKIES"""
    def authenticate(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")

        user = models.User.objects.filter(id=payload["id"]).first()

        return user, None
