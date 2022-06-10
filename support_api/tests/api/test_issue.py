import pytest

from issue import models as issue_models


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

    issue_from_db = issue_models.Issue.objects.all().first()

    assert data["title"] == issue_from_db.title


@pytest.mark.django_db
def test_user_can_see_his_issue(user_created_issue_client, user):

    response = user_created_issue_client.get("/api/v1/issue/")

    assert response.status_code == 200

    data = response.data[0]

    assert data['created_by'] == user.email


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


@pytest.mark.django_db
def test_staff_issue_list(auth_staff_client, user):

    issue = issue_models.Issue.objects.create(title="First issue",
                                                    body="body",
                                                    created_by=user)

    response = auth_staff_client.get("/api/v1/issue/")

    assert response.status_code == 200

    data = response.json()[0]

    assert data['title'] == issue.title


@pytest.mark.django_db
def test_user_cant_see_other_issues(auth_client, user_staff):

    issue = issue_models.Issue.objects.create(title="Issue",
                                              body="body",
                                              created_by=user_staff)

    issue.refresh_from_db()
    response = auth_client.get(f"/api/v1/issue/{issue.pk}/")

    assert response.status_code == 404


# to run this test your redis+celery should be up
@pytest.mark.django_db
def test_staff_can_change_status(auth_staff_client, user, user_staff):
    payload = dict(
        assignee=user_staff.pk,
        status="RESOLVED",
    )
    issue = issue_models.Issue.objects.create(title="Issue",
                                              body="body",
                                              created_by=user)
    response = auth_staff_client.put(f"/api/v1/issue/{issue.pk}/", payload)

    assert response.status_code == 200

    issue.refresh_from_db()

    assert response.data['status'] == issue.status
    assert response.data['assignee'] == issue.assignee.pk


@pytest.mark.django_db
def test_user_leave_comment(user_created_issue_client, user):
    payload = dict(
        body="Comment"
    )
    detail_id = user_created_issue_client.get("/api/v1/issue/").data[0]["id"]

    response = user_created_issue_client.post(f"/api/v1/issue/{detail_id}/comment/", payload)

    assert response.status_code == 201

    data = response.data

    assert data['body'] == payload['body']
