from app import db
from flask import current_app

import datetime
import jwt


class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(128), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    active = db.Column(db.Boolean())

    def __init__(self, token, token_type):
        self.token = token
        self.token_type = token_type
        self.active = True
    
    def encode_token(self, user_id, token_type):
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