import pytest
from rest_framework.test import APIClient

from user.models import User


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
def user_staff():
    payload = dict(
        first_name="Luke",
        last_name="Skywalker",
        email="jedi@starwars.com",
        password="forcebewithyou",
        is_staff=True
    )

    user = User.objects.create_user(**payload)

    return user


@pytest.fixture
def superuser():
    payload = dict(
        first_name="Geralt",
        last_name="of Rivia",
        email="witcher@neverland.com",
        password="nolesserevil",
    )

    user = User.objects.create_superuser(**payload)

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


@pytest.fixture
def auth_staff_client(user_staff, client):
    client.post("/api/v1/user/login/",
                dict(
                    email=user_staff.email,
                    password="forcebewithyou"
                ))

    return client


@pytest.fixture
def auth_admin_client(superuser, client):
    client.post("/api/v1/user/login/",
                dict(
                    email=superuser.email,
                    password="nolesserevil"
                ))

    return client


@pytest.fixture
def user_created_issue_client(auth_client, user):
    auth_client.post("/api/v1/issue/",
                     dict(
                         title="Help!",
                         body="I need somebody!"
                     ))

    return auth_client
