from app import db
from app.api.auth.models import Token


def get_token_by_id(token_id):
    return Token.query.get(token_id)


def remove_token(token):
    db.session.delete(token)
    db.session.commit()


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
