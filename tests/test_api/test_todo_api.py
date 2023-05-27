import pytest
from beanie import PydanticObjectId


@pytest.fixture(scope="function")
def existing_todo_id(client, auth_header):
    response = client.post(
        "/api/v1/todo",
        json={"title": "test", "description": "test", "status": "todo"},
        headers=auth_header,
    )
    return response.json()


def test_create_todo_for_user_200(client, auth_header):  # noqa
    response = client.post(
        "/api/v1/todo",
        json={"title": "test", "description": "test", "status": "todo"},
        headers=auth_header,
    )
    assert response.status_code == 200, response.json()
    assert PydanticObjectId(response.json())


def test_get_todos_for_user_200(client, auth_header):
    client.post(
        "/api/v1/todo",
        json={"title": "test", "description": "test", "status": "todo"},
        headers=auth_header,
    )
    response = client.get("/api/v1/todo", headers=auth_header)
    assert response.status_code == 200, response.json()
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_todo_for_user_200(client, auth_header):
    response = client.post(
        "/api/v1/todo",
        json={"title": "test", "description": "test", "status": "todo"},
        headers=auth_header,
    )
    todo_id = response.json()
    response = client.get(f"/api/v1/todo/{todo_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["_id"] == todo_id
    for key, value in {"title": "test", "description": "test", "status": "todo"}.items():
        assert response.json()[key] == value


def test_update_todo_200(client, auth_header, existing_todo_id):
    response = client.put(
        f"/api/v1/todo/{existing_todo_id}",
        json={"title": "test1", "description": "test1", "status": "in_progress"},
        headers=auth_header,
    )
    assert response.status_code == 200, response.json()
    response = client.get(f"/api/v1/todo/{existing_todo_id}", headers=auth_header)
    assert response.status_code == 200, response.json()
    assert response.json()["title"] == "test1"
    assert response.json()["description"] == "test1"
    assert response.json()["status"] == "in_progress"


def test_patch_todo_200(client, auth_header, existing_todo_id):
    response = client.patch(f"/api/v1/todo/{existing_todo_id}", params={"status": "done"}, headers=auth_header)
    assert response.status_code == 200, response.json()
    assert response.json()["status"] == "done"


def test_delete_todo_204(client, auth_header, existing_todo_id):
    response = client.get(f"/api/v1/todo/{existing_todo_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["_id"] == existing_todo_id
    response = client.delete(f"/api/v1/todo/{existing_todo_id}", headers=auth_header)
    assert response.status_code == 204, response.json()
    response = client.get(f"/api/v1/todo/{existing_todo_id}", headers=auth_header)
    assert response.status_code == 404
