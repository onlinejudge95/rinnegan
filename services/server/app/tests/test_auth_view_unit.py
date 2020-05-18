import app.api.auth
import json


# Test user registration passes
def test_user_registration(test_app, monkeypatch):
    class MockDict(dict):
        def __init__(self, *args, **kwargs):
            super(MockDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_email(email):
        return None

    def mock_add_user(username, email, password):
        mock_user = MockDict()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(
        app.api.auth, "get_user_by_email", mock_get_user_by_email
    )

    monkeypatch.setattr(app.api.auth, "add_user", mock_add_user)

    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 201

    data = response.get_json()
    assert "password" not in data.keys()
    assert data["id"] == 1
    assert data["username"] == "test_user"
    assert data["email"] == "test_user@mail.com"


# Test user registration fails due to empty data
def test_user_registration_empty_data(test_app):
    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test user registration fails due to invalid data
def test_user_registration_invalid_data(test_app, test_database):
    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "test_user"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test user registration fails due to duplicate entry
def test_user_registration_duplicate_entry(test_app, monkeypatch):
    class MockDict(dict):
        def __init__(self, *args, **kwargs):
            super(MockDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_email(email):
        return None

    def mock_get_user_by_email_fail(email):
        return True

    def mock_add_user(username, email, password):
        mock_user = MockDict()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(
        app.api.auth, "get_user_by_email", mock_get_user_by_email
    )

    monkeypatch.setattr(app.api.auth, "add_user", mock_add_user)

    client = test_app.test_client()

    client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    monkeypatch.setattr(
        app.api.auth, "get_user_by_email", mock_get_user_by_email_fail
    )
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@email.com",
                "password": "test_password",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "test_user@email.com is already registered" in data["message"]


# Test user registration fails due to invalid headers
def test_user_registration_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]
