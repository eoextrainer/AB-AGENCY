def test_login_returns_access_token(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@ab-agency.com", "password": "admin12345"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "admin@ab-agency.com"


def test_create_user_requires_admin(client, auth_headers):
    response = client.post(
        "/api/auth/users",
        headers=auth_headers,
        json={
            "email": "new.user@ab-agency.com",
            "full_name": "New User",
            "password": "new-user-pass",
            "role": "editor",
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "editor"