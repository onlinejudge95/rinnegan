import os

from flask import current_app

from app import bcrypt
from app import db
from app.api.users.admin import UserAdminView


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()


if os.getenv("FLASK_ENV") != "production":
    from app import admin

    admin.add_view(UserAdminView(User, db.session))
