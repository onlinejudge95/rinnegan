from app.api.users.models import User


# Test passwords are randomly hashed
def test_passwords_hashed_randomly(test_app, test_database, add_user):
    user_one = add_user("test_user_one", "test_user_one@mail.com", "test_password")
    user_two = add_user("test_user_two", "test_user_two@mail.com", "test_password")

    assert user_one.password != user_two.password
    assert user_one.password != "test_password"
    assert user_two.password != "test_password"


# Test encoding of access token works
def test_encode_access_token_works(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@gmail.com", "test_password")

    access_token = user.encode_token(user.id, "access")
    assert isinstance(access_token, bytes)


# Test decoding of access token works
def test_decode_access_token_works(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@gmail.com", "test_password")

    access_token = user.encode_token(user.id, "access")
    assert isinstance(access_token, bytes)

    user_id = User.decode_token(access_token)
    assert user_id == user.id


# Test encoding of refresh token works
def test_encode_refresh_token_works(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@gmail.com", "test_password")

    refresh_token = user.encode_token(user.id, "refresh")
    assert isinstance(refresh_token, bytes)
