def test_login(client, create_user_data):
    user = create_user_data()
    response = client.post("/api/v1/user", json=user)
    assert response.status_code == 201, response.json()
    response = client.post("/api/v1/login", data={"username": user["email"], "password": user["password1"]})
    assert response.status_code == 200, response.json()
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
