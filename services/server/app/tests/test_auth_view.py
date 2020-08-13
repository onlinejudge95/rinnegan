import json


# Test user registration passes
def test_user_registration(test_app, test_database):
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
def test_user_registration_empty_data(test_app, test_database):
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
def test_user_registration_duplicate_entry(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")

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
    assert response.status_code == 400

    data = response.get_json()
    assert "test_user@mail.com is already registered" in data["message"]


# Test user registration fails due to invalid headers
def test_user_registration_invalid_header(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/auth/register",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.post(
        "/auth/register",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test user login passes
def test_user_login(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 200

    data = response.get_json()

    assert data["access_token"]
    assert data["refresh_token"]


# Test user login fails due to wrong password
def test_user_login_wrong_password(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password_wrong"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()

    assert "Invalid password for" in data["message"]


# Test user login fails due to unregistered user
def test_user_login_unregistered_user(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 404

    data = response.get_json()

    assert "test_user@mail.com does not exists" in data["message"]


# Test user login fails due to invalid header
def test_user_login_invalid_header(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test refresh token passes
def test_refresh_token(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    refresh_token = data["refresh_token"]

    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data["refresh_token"]
    assert data["access_token"]


# Test refresh token fails due to expired token
def test_refresh_token_expired(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    test_app.config["REFRESH_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    refresh_token = data["refresh_token"]

    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test refresh token fails due to invalid token
def test_refresh_token_invalid(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "invalid_token"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test refresh token fails due to invalid headers
def test_refresh_token_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.post(
        "/auth/refresh",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]
