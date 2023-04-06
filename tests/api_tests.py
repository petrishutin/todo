import pytest
from beanie import PydanticObjectId
from fastapi import testclient
from main import app


@pytest.fixture(scope="module")
def client():
    with testclient.TestClient(app) as client:  # noqa
        yield client


@pytest.fixture(scope="module")
def existing_user_id(client):
    response = client.post(
        "/api/v1/user", json={"name": "test", "email": "test1@test.com", "password1": "test", "password2": "test"}
    )
    return response.json()


def test_create_user_200(client):  # noqa
    response = client.post(
        "/api/v1/user", json={"name": "test", "email": "test@test.com", "password1": "test", "password2": "test"}
    )
    assert response.status_code == 200, response.json()
    assert PydanticObjectId(response.json())


def test_get_user_200(client, existing_user_id):  # noqa
    response = client.get(f"/api/v1/user/{existing_user_id}")
    assert response.status_code == 200, response.json()
    for key in ("name", "email", "hashed_password"):
        assert key in response.json(), response.json()


def test_create_todo_for_user_200(client, existing_user_id):  # noqa
    response = client.post(
        f"/api/v1/user/{existing_user_id}/todo", json={"title": "test", "description": "test", "status": "todo"}
    )
    assert response.status_code == 200, response.json()
    assert PydanticObjectId(response.json())


def test_get_todos_for_user_200(client, existing_user_id):
    response = client.get(f"/api/v1/user/{existing_user_id}/todo")
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)


def test_get_todo_for_user_200(client, existing_user_id):
    response = client.get(f"/api/v1/user/{existing_user_id}/todo")
    todo_id = response.json()[0]["_id"]
    response = client.get(f"/api/v1/user/{existing_user_id}/todo/{todo_id}")
    assert response.status_code == 200, response.json()
    for key, value in {"title": "test", "description": "test", "status": "todo"}.items():
        assert response.json()[key] == value


def test_update_todo_200(client, existing_user_id):
    response = client.get(f"/api/v1/user/{existing_user_id}/todo")
    todo_id = response.json()[0]["_id"]
    response = client.put(
        f"/api/v1/user/{existing_user_id}/todo/{todo_id}",
        json={"title": "test1", "description": "test1", "status": "in_progress"},
    )
    assert response.status_code == 200, response.json()
    response = client.get(f"/api/v1/user/{existing_user_id}/todo/{todo_id}")
    assert response.status_code == 200, response.json()
    assert response.json()["title"] == "test1"
    assert response.json()["description"] == "test1"
    assert response.json()["status"] == "in_progress"


def test_delete_todo_200(client, existing_user_id):
    response = client.get(f"/api/v1/user/{existing_user_id}/todo")
    todo_id = response.json()[0]["_id"]
    response = client.delete(f"/api/v1/user/{existing_user_id}/todo/{todo_id}")
    assert response.status_code == 200, response.json()
    response = client.get(f"/api/v1/user/{existing_user_id}/todo/{todo_id}")
    assert response.status_code == 404, response.json()
