from app import bcrypt
from app import db
from app.api.auth.models import Token


def add_token(user_id):
    """
    Adds a token for a given user

    :param: user_id
        ID of the user for whom the token is to be generated
    :returns:
        Generated JWT token
    """
    access_token = Token.encode_token(user_id, "access").decode("utf-8")
    refresh_token = Token.encode_token(user_id, "refresh").decode("utf-8")
    token = Token(
        access_token=access_token, refresh_token=refresh_token, user_id=user_id
    )
    db.session.add(token)
    db.session.commit()
    return token


def update_token(refresh_token, user_id):
    """
    Refresh the tokens for a given user

    :param: refresh_token
        Refresh token of the user
    :param: user_id
        ID of the user for whom the token is to be generated
    :returns:
        Generated JWT token
    """
    token = Token.query.filter_by(refresh_token=refresh_token).first()
    token.access_token = Token.encode_token(user_id, "access").decode("utf-8")
    token.refresh_token = Token.encode_token(user_id, "refresh").decode(
        "utf-8"
    )
    db.session.commit()
    return token


def get_user_id_by_token(token):
    """
    Decodes the token and provide the user)id associated with it

    :param: token
        Access token of the user
    :returns:
        ID of the user for whom the token is to be generated
    """
    return Token.decode_token(token)


def password_matches(password, user):
    """
    Checks if the password matches the hash stored in the DB

    :param: password
        Password entered by the user during login
    :param: user
        User object for given login
    :returns:
        Whether the password is correct or not
    """
    return bcrypt.check_password_hash(user.password, password)
