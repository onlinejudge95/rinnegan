import json


# Test user creation passes
def test_add_user(test_app, test_database):
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
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data.keys()
    assert "test_user@email.com" in data["message"]


# Test user creation fails due to empty data
def test_add_user_empty_data(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test user creation fails due to invalid data
def test_add_user_invalid_data(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test user creation fails due to duplicate entry
def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
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
    response = client.post(
        "/users",
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


# Test user creation fails due to invalid content-type header
def test_add_user_invalid_header(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test fetching user list passes
def test_get_users(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    client = test_app.test_client()
    response = client.get(
        "/users",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert "test_user_one" in data[0]["username"]
    assert "test_user_one@mail.com" in data[0]["email"]
    assert "password" not in data[0]

    assert "test_user_two" in data[1]["username"]
    assert "test_user_two@mail.com" in data[1]["email"]
    assert "password" not in data[1]


# Test fetching user list fails due to missing token
def test_get_users_missing_token(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    client = test_app.test_client()

    response = client.get("/users", headers={"Accept": "application/json"})
    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test fetching user list fails due to expired token
def test_get_users_expired_token(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        "/users",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test fetching user list fails due to invalid token
def test_get_users_invalid_token(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    client = test_app.test_client()

    response = client.get(
        "/users",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test fetching single user passes
def test_single_user(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
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
    access_token = data["access_token"]

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == user.id
    assert data["username"] == "test_user"
    assert data["email"] == "test_user@mail.com"
    assert "password" not in data.keys()


# Test fetching single user fails due to incorrect id
def test_single_user_invalid_id(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        "/users/2",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test fetching single user fails due to missing token
def test_single_user_missing_token(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.get(
        f"/users/{user.id}", headers={"Accept": "application/json"}
    )

    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test fetching single user fails due to expired token
def test_single_user_expired_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test fetching single user fails due to invalid token
def test_single_user_invalid_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    client = test_app.test_client()

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test removing a user passes
def test_remove_user(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 204


# Test removing a user fails due to invalid id
def test_remove_user_invalid_id(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.delete(
        "/users/2",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test removing a user fails due to missing token
def test_remove_user_missing_token(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.delete(
        f"/users/{user.id}", headers={"Accept": "application/json"}
    )

    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test removing a user fails due to expired token
def test_remove_user_expired_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test removing a user fails due to invalid token
def test_remove_user_invalid_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    client = test_app.test_client()

    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test update a user passes
def test_update_user(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == 1, data
    assert data["username"] == "test_user_update"
    assert data["email"] == "test_user_update@mail.com"


# Test update a user fails due to empty data
def test_update_user_empty_data(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "Input payload validation failed" in data["message"]


# Test update a user fails due to invalid id
def test_update_user_invalid_id(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.put(
        "/users/10",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 404

    data = response.get_json()
    assert "does not exist" in data["message"]


# Test update a user fails due to invalid headers
def test_update_user_invalid_headers(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()
    response = client.put(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]

    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "supported is application/json" in data["message"]


# Test update a user fails due to missing token
def test_update_user_missing_token(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 403

    data = response.get_json()
    assert "Token required" in data["message"]


# Test update a user fails due to expired token
def test_update_user_expired_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test update a user fails due to invalid token
def test_update_user_invalid_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    client = test_app.test_client()

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]
