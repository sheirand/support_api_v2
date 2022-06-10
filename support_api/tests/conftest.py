import pytest
from user.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    payload = dict(
        first_name="Bilbo",
        last_name="Bagiins",
        email="old_hobbit@shire.com",
        password="youshallnotpass",
    )

    user = User.objects.create_user(**payload)

    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    client.post("/api/v1/user/login/",
                dict(
                    email=user.email,
                    password="youshallnotpass",
                ))
    return client

