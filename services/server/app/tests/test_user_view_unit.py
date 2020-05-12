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


# Test fetching user list passes
def test_get_users(test_app, monkeypatch):
    def mock_get_all_users():
        return [
            {"id": 1, "username": "test_user_one", "email": "test_user_one@mail.com"},
            {"id": 2, "username": "test_user_two", "email": "test_user_two@mail.com"},
        ]

    monkeypatch.setattr(app.api.users.views, "get_all_users", mock_get_all_users)

    client = test_app.test_client()
    response = client.get("/users", headers={"Accept": "application/json"})

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert "test_user_one" in data[0]["username"]
    assert "test_user_one@mail.com" in data[0]["email"]
    assert not "password" in data[0]

    assert "test_user_two" in data[1]["username"]
    assert "test_user_two@mail.com" in data[1]["email"]
    assert not "password" in data[1]


# Test fetching single user passes
def test_single_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return {"id": 1, "username": "test_user", "email": "test_user@mail.com"}

    monkeypatch.setattr(app.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()

    response = client.get("/users/1", headers={"Accept": "application/json"})
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1, data
    assert data["username"] == "test_user"
    assert data["email"] == "test_user@mail.com"
    assert "password" not in data.keys()


# Test fetching single user fails due to incorrect id
def test_single_user_invalid_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(app.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()

    response = client.get("/users/1", headers={"Accept": "application/json"})
    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test removing a user passes
def test_remove_user(test_app, monkeypatch):
    class MockDict(dict):
        def __init__(self, *args, **kwargs):
            super(MockDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_id(user_id):
        mock_user = MockDict()
        mock_user.update(
            {"id": 1, "username": "test_user", "email": "test_user@mail.com"}
        )
        return mock_user

    def mock_remove_user(user):
        return True

    monkeypatch.setattr(app.api.users.views, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(app.api.users.views, "remove_user", mock_remove_user)

    client = test_app.test_client()

    response = client.delete(f"/users/1", headers={"Accept": "application/json"})
    assert response.status_code == 204


# Test removing a user fails due to invalid id
def test_remove_user_invalid_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(app.api.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()

    response = client.delete(f"/users/1", headers={"Accept": "application/json"})
    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]
