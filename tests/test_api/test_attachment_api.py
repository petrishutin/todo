import os

import pytest


@pytest.fixture(scope="session")
def image():
    with open(os.path.join(os.getcwd(), "tests", "photo.jpg"), "rb") as f:
        return f.read()


def test_upload_attachment_201(client, existing_user_token, image):
    response = client.post(
        "/api/v1/attachments",
        headers={"Authorization": f"Bearer {existing_user_token}"},
        files={"file": ("photo.jpg", image)},
    )
    assert response.status_code == 201, response.json()
    assert response.json()["_id"]
    assert response.json()["user_id"]
    assert response.json()["file_name"] == "photo.jpg"
    assert response.json()["file_url"]
    assert response.json()["file_size"]
    assert response.json()["file_mime_type"] == "image/jpeg"
    assert response.json()["file_uid"]
    assert response.json()["created_at"]


def test_download_attachment_200(client, existing_user_token, image):
    file_uid = client.post(
        "/api/v1/attachments",
        headers={"Authorization": f"Bearer {existing_user_token}"},
        files={"file": ("photo.jpg", image)},
    ).json()["file_uid"]
    response = client.get(
        f"/api/v1/attachments/{file_uid}",
        headers={"Authorization": f"Bearer {existing_user_token}"},
    )
    assert response.status_code == 200, response.json()
    assert response.content == image
