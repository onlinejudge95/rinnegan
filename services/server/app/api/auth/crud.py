from app import db
from app.api.auth.models import Token


def add_token(user_id):
    access_token = Token.encode_token(user_id, "access").decode("utf-8")
    refresh_token = Token.encode_token(user_id, "refresh").decode("utf-8")
    token = Token(access_token=access_token, refresh_token=refresh_token)
    db.session.add(token)
    db.session.commit()
    return token


def update_token(refresh_token, user_id):
    token = Token.query.filter_by(refresh_token=refresh_token).first()
    token.access_token = Token.encode_token(user_id, "access").decode("utf-8")
    token.refresh_token = Token.encode_token(user_id, "refresh").decode(
        "utf-8"
    )
    db.session.commit()
    return token


def get_user_id_by_token(token):
    return Token.decode_token(token)
