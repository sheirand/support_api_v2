import pytest

from user import models


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name="Bilbo",
        last_name="Bagiins",
        email="old_hobbit@shire.com",
        password="youshallnotpass"
    )

    response = client.post("/api/v1/user/", payload)

    assert response.status_code == 201

    data = response.data

    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_superuser_register_staff_user(auth_admin_client):
    payload = dict(
        first_name="Severus",
        last_name="Snape",
        email="potionteacher@hogwarts.com",
        password="Forhowlong?Always!",
        is_staff=True
    )
    response = auth_admin_client.post("/api/v1/user/", payload)

    assert response.status_code == 201

    data = response.data

    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert data["is_staff"] == payload["is_staff"]
    assert "password" not in data


@pytest.mark.django_db
def test_login_user(user, client):
    response = client.post("/api/v1/user/login/",
                           dict(
                               email=user.email,
                               password="youshallnotpass"),
                           )
    assert response.status_code == 200


@pytest.mark.django_db
def test_fail_login_user(user, client):
    response = client.post("/api/v1/user/login/",
                           dict(
                               email=user.email,
                               password="youcouldpass"),
                           )
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_profile(user, auth_client):

    response = auth_client.get("/api/v1/user/session/")

    assert response.status_code == 200

    data = response.json()[0]

    assert data["id"] == user.pk
    assert data["last_name"] == user.last_name
    assert data["email"] == user.email
    assert data["is_staff"] == user.is_staff


@pytest.mark.django_db
def test_user_logout(auth_client):

    response = auth_client.post("/api/v1/user/logout/")

    assert response.status_code == 200

    assert response.data["detail"] == "Success, goodbye!"


@pytest.mark.django_db
def test_user_delete(auth_admin_client, user):

    response = auth_admin_client.delete(f"/api/v1/user/{user.pk}/")

    assert response.status_code == 204

    with pytest.raises(models.User.DoesNotExist):
        user.refresh_from_db()


@pytest.mark.django_db
def test_user_detail_forbidden(auth_client):

    response = auth_client.get("/api/v1/user/1/")

    assert response.status_code == 403

@pytest.mark.django_db
def test_user_cant_register_staff(auth_client):
    payload = dict(
        first_name="Severus",
        last_name="Snape",
        email="potionteacher@hogwarts.com",
        password="Forhowlong?Always!",
        is_staff=True
    )

    response = auth_client.post("/api/v1/user/", payload)

    data = response.data

    assert data['is_staff'] != payload['is_staff']
