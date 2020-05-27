from app.api.auth.models import Token


# Test encoding of access token works
def test_encode_access_token_works(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@gmail.com", "test_password")

    access_token = Token.encode_token(user.id, "access")
    assert isinstance(access_token, bytes)


# Test decoding of access token works
def test_decode_access_token_works(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@gmail.com", "test_password")

    access_token = Token.encode_token(user.id, "access")
    assert isinstance(access_token, bytes)

    user_id = Token.decode_token(access_token)
    assert user_id == user.id


# Test encoding of refresh token works
def test_encode_refresh_token_works(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@gmail.com", "test_password")

    refresh_token = Token.encode_token(user.id, "refresh")
    assert isinstance(refresh_token, bytes)
