import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = dict(
        first_name="Bilbo",
        last_name="Bagiins",
        email="old_hobbit@shire.com",
        password="youshallnotpass"
    )

    response = client.post("/api/v1/user/", payload)

    data = response.data

    assert data["first_name"] == payload["first_name"]
