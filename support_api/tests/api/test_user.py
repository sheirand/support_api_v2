import pytest


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
def test_login_user(user, client):
    response = client.post("/api/v1/user/login/",
                           dict(
                               email="old_hobbit@shire.com",
                               password="youshallnotpass"),
                           )
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_profile(user, auth_client):

    response = auth_client.get("/api/v1/user/session/")

    assert response.status_code == 200

    data = response.json()[0]

    assert data["id"] == user.pk
    assert data["last_name"] == user.last_name
    assert data["email"] == user.email
    assert data["is_staff"] == user.is_staff


