import pytest
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
