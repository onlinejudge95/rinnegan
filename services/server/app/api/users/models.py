from app import bcrypt
from app import db
from flask import current_app
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func

import datetime
import jwt
import os


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()

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
            "sub": 1,
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


if os.getenv("FLASK_ENV") != "production":
    from app import admin

    admin.add_view(ModelView(User, db.session))
