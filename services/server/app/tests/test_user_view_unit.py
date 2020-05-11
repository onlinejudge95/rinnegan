import json
import app.api.users.views


# Test user creation passes
def test_add_user_passes(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_add_user(username, email, password):
        return 1

    monkeypatch.setattr(
        app.api.users.views, "get_user_by_email", mock_get_user_by_email
    )

    monkeypatch.setattr(app.api.users.views, "add_user", mock_add_user)

    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@email.com",
                "password": "test_password",
            }
        ),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data.keys()
    assert "test_user@email.com" in data["message"]


# Test user creation fails due to empty data
def test_add_user_empty_data(test_app):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({}),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test user creation fails due to invalid data
def test_add_user_invalid_data(test_app):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test user creation fails due to duplicate entry
def test_add_user_duplicate_email(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_get_user_by_email_fail(email):
        return True

    def mock_add_user(username, email, password):
        return 1

    monkeypatch.setattr(
        app.api.users.views, "get_user_by_email", mock_get_user_by_email
    )

    monkeypatch.setattr(app.api.users.views, "add_user", mock_add_user)

    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@email.com",
                "password": "test_password",
            }
        ),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    monkeypatch.setattr(
        app.api.users.views, "get_user_by_email", mock_get_user_by_email_fail
    )
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@email.com",
                "password": "test_password",
            }
        ),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "test_user@email.com is already registered" in data["message"]


# Test user creation fails due to invalid content-type header
def test_add_user_empty_data(test_app):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define a Content-Type header" in data["message"]
