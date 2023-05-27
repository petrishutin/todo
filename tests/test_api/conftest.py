import pytest
from faker import Faker
from fastapi import testclient

from app.main import app


@pytest.fixture(scope="module")
def fake():
    faker = Faker()
    yield faker


@pytest.fixture(scope="module")
def client():
    with testclient.TestClient(app) as client:  # noqa
        yield client


@pytest.fixture(scope="module")
def create_user_data(fake: Faker):  # noqa
    def _create_user_data():
        return {"email": f"{fake.email()}", "password1": "test", "password2": "test"}

    return _create_user_data


@pytest.fixture(scope="module")
def existing_user_id(client, create_user_data):
    user = create_user_data()
    response = client.post("/api/v1/user", json=user)
    return response.json()


@pytest.fixture(scope="module")
def auth_header(client, create_user_data):
    user = create_user_data()
    client.post("/api/v1/user", json=user)
    response = client.post("/api/v1/login", data={"username": user["email"], "password": user["password1"]})
    assert response.status_code == 200, response.json()
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
