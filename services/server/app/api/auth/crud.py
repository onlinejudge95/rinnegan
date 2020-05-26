from app import db
from app.api.auth.models import Token


def get_token_by_id(token_id):
    return Token.query.get(token_id)


def remove_token(token):
    db.session.delete(token)
    db.session.commit()


def add_token(token, token_type):
    token = Token(token=token, token_type=token_type)
    db.session.add(token)
    db.session.commit()
    return token


def update_token(token, token_value, token_type, active):
    token.token = token_value
    token.token_type = token_type
    token.active = active
    db.session.commit()
    return token
