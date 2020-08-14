import datetime

import jwt

from flask import current_app

from app import db


class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_token = db.Column(db.String(200), nullable=False)
    refresh_token = db.Column(db.String(200), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    def __init__(self, access_token, refresh_token, user_id):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id

    @staticmethod
    def encode_token(user_id, token_type):
        config = current_app.config
        time_to_live = (
            config.get("ACCESS_TOKEN_EXPIRATION")
            if token_type == "access"
            else config.get("REFRESH_TOKEN_EXPIRATION")
        )
        payload = {
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=time_to_live),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(
            payload=payload,
            key=config.get("SECRET_KEY"),
            algorithm=config.get("JWT_ENCODE_ALGORITHM"),
        )

    @staticmethod
    def decode_token(token):
        config = current_app.config
        payload = jwt.decode(
            jwt=token,
            key=config.get("SECRET_KEY"),
            algorithms=[config.get("JWT_ENCODE_ALGORITHM")],
        )
        return payload["sub"]
