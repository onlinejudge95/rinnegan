import app.api.auth
import json
import jwt


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
        "/auth/register",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]


# Test user login passes
def test_user_login(test_app, monkeypatch):
    class MockDict(dict):
        def __init__(self, *args, **kwargs):
            super(MockDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

        def encode_token(self, user_id, token_type):
            return bytes("token", "utf-8")

    def mock_get_user_by_email(email):
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


# Test user login fails due to unregistered user
def test_user_login_unregistered_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return False

    monkeypatch.setattr(
        app.api.auth, "get_user_by_email", mock_get_user_by_email
    )
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
def test_user_login_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]


# Test refresh token passes
def test_refresh_token(test_app, monkeypatch):
    class MockUser(dict):
        def __init__(self, *args, **kwargs):
            super(MockUser, self).__init__(*args, **kwargs)
            self.__dict__ = self

        def encode_token(self, user_id, token_type):
            return bytes("refresh_token", "utf-8")

        @staticmethod
        def decode_token(token):
            return 1

    def mock_get_user_by_id(user_id):
        mock_user = MockUser()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(app.api.auth, "User", MockUser)
    monkeypatch.setattr(app.api.auth, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh_token"}),
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
def test_refresh_token_expired(test_app, monkeypatch):
    class MockUser(dict):
        def __init__(self, *args, **kwargs):
            super(MockUser, self).__init__(*args, **kwargs)
            self.__dict__ = self

        def encode_token(self, user_id, token_type):
            return bytes("refresh_token", "utf-8")

        @staticmethod
        def decode_token(token):
            raise jwt.ExpiredSignatureError()

    def mock_get_user_by_id(user_id):
        mock_user = MockUser()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(app.api.auth, "User", MockUser)
    monkeypatch.setattr(app.api.auth, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh_token"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Token expired" in data["message"]


# Test refresh token fails due to invalid token
def test_refresh_token_invalid(test_app, monkeypatch):
    class MockUser(dict):
        def __init__(self, *args, **kwargs):
            super(MockUser, self).__init__(*args, **kwargs)
            self.__dict__ = self

        def encode_token(self, user_id, token_type):
            return bytes("refresh_token", "utf-8")

        @staticmethod
        def decode_token(token):
            raise jwt.InvalidTokenError()

    def mock_get_user_by_id(user_id):
        mock_user = MockUser()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(app.api.auth, "User", MockUser)
    monkeypatch.setattr(app.api.auth, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh_token"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test refresh token fails due to invalid user id
# def test_refresh_token_invalid_user(test_app, monkeypatch):
#     class MockUser(dict):
#         def __init__(self, *args, **kwargs):
#             super(MockUser, self).__init__(*args, **kwargs)
#             self.__dict__ = self

#         def encode_token(self, user_id, token_type):
#             return bytes("refresh_token", "utf-8")

#         @staticmethod
#         def decode_token(token):
#             raise jwt.InvalidTokenError()

#     def mock_get_user_by_id(user_id):
#         return None

#     monkeypatch.setattr(app.api.auth, "User", MockUser)
#     monkeypatch.setattr(app.api.auth, "get_user_by_id", mock_get_user_by_id)

#     client = test_app.test_client()
#     response = client.post(
#         "/auth/refresh",
#         data=json.dumps({"refresh_token": "refresh_token"}),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#         },
#     )
#     assert response.status_code == 401

#     data = response.get_json()
#     assert "Invalid token" in data["message"]


# Test refresh token fails due to invalid headers
def test_refresh_token_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 415

    data = response.get_json()
    assert "define Content-Type header" in data["message"]


# Test user status passes
def test_user_status(test_app, monkeypatch):
    class MockUser(dict):
        def __init__(self, *args, **kwargs):
            super(MockUser, self).__init__(*args, **kwargs)
            self.__dict__ = self

        @staticmethod
        def decode_token(token):
            return 1

    def mock_get_user_by_id(user_id):
        mock_user = MockUser()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(app.api.auth, "User", MockUser)
    monkeypatch.setattr(app.api.auth, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    response = client.get(
        "/auth/status",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 200, response.get_json()

    data = response.get_json()
    assert data["username"] == "test_user"
    assert data["email"] == "test_user@mail.com"
    assert "password" not in data.keys()


# Test user status fails due to invalid access token
def test_user_status_invalid_token(test_app, monkeypatch):
    class MockUser(dict):
        def __init__(self, *args, **kwargs):
            super(MockUser, self).__init__(*args, **kwargs)
            self.__dict__ = self

        @staticmethod
        def decode_token(token):
            raise jwt.InvalidTokenError()

    def mock_get_user_by_id(user_id):
        mock_user = MockUser()
        mock_user.update(
            {
                "id": 1,
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        )
        return mock_user

    monkeypatch.setattr(app.api.auth, "User", MockUser)
    monkeypatch.setattr(app.api.auth, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    response = client.get(
        "/auth/status",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401

    data = response.get_json()
    assert "Invalid token" in data["message"]


# Test user status fails due to invalid headers
def test_user_status_invalid_header(test_app):
    client = test_app.test_client()
    response = client.get("/auth/status")
    assert response.status_code == 415

    data = response.get_json()
    assert "content type supported is application/json" in data["message"]
