import pytest
from issue import models as issue_models
from user import models as user_models


@pytest.mark.django_db
def test_user_create_issue(auth_client, user):
    payload = dict(
        title="Help",
        body="I need somebody"
    )

    response = auth_client.post("/api/v1/issue/", payload)

    assert response.status_code == 201

    data = response.data

    assert data['id']
    assert data['status'] == 'ACTIVE'
    assert data['created_by'] == user.email
    assert data['title'] == payload['title']
    assert data['body'] == payload['body']
    assert data['time_created']


@pytest.mark.django_db
def test_user_can_see_his_issue(user_created_issue_client, user):

    response = user_created_issue_client.get("/api/v1/issue/")

    assert response.status_code == 200

    data = response.data[0]

    assert data['created_by'] == user.email

    issue_from_db = issue_models.Issue.objects.all().first()

    assert data["title"] == issue_from_db.title

@pytest.mark.django_db
def test_user_can_see_his_issue_detail(user_created_issue_client, user):

    detail_id = user_created_issue_client.get("/api/v1/issue/").data[0]["id"]

    response = user_created_issue_client.get(f"/api/v1/issue/{detail_id}/")

    assert response.status_code == 200

    data = response.data

    assert data["id"] == detail_id
    assert data["created_by"] == user.email


@pytest.mark.django_db
def test_not_authenticated(client):

    response = client.get("/api/v1/issue/")

    assert response.status_code == 403


