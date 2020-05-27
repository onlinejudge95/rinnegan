from app.api.auth.crud import add_token
from app.api.auth.crud import get_user_id_by_token
from app.api.auth.crud import update_token
from app.api.auth.serializers import auth_namespace
from app.api.auth.serializers import fetch_registered_user
from app.api.auth.serializers import login_user
from app.api.auth.serializers import refresh
from app.api.auth.serializers import register_user
from app.api.auth.serializers import user_tokens
from app.api.users.crud import add_user
from app.api.users.crud import get_user_by_email
from flask import request
from flask_restx import Resource

import jwt


class Register(Resource):
    @staticmethod
    @auth_namespace.marshal_with(fetch_registered_user)
    @auth_namespace.expect(register_user, validate=True)
    @auth_namespace.response(201, "Successfully registered a new user")
    @auth_namespace.response(
        400, "Sorry.The provided email <user_email> is already registered"
    )
    def post():
        request_data = request.get_json()
        email = request_data.get("email")

        user_exists = get_user_by_email(email)
        if user_exists:
            auth_namespace.abort(
                400, f"Sorry.The provided email {email} is already registered"
            )

        user = add_user(
            request_data["username"],
            request_data["email"],
            request_data["password"],
        )
        return user, 201


class Login(Resource):
    @staticmethod
    @auth_namespace.marshal_with(user_tokens)
    @auth_namespace.expect(login_user, validate=True)
    @auth_namespace.response(200, "Successfully logged the user in")
    @auth_namespace.response(
        404, "User with email <user_email> does not exists"
    )
    def post():
        request_data = request.get_json()
        email = request_data.get("email")

        user = get_user_by_email(email)
        if not user:
            auth_namespace.abort(
                404, f"User with email {email} does not exists"
            )
        token = add_token(user.id)
        return token, 200


class Refresh(Resource):
    @staticmethod
    @auth_namespace.marshal_with(user_tokens)
    @auth_namespace.expect(refresh, validate=True)
    @auth_namespace.response(200, "Successfully refreshed the tokens")
    @auth_namespace.response(401, "Invalid token. Please log in again.")
    def post():
        request_data = request.get_json()
        refresh_token = request_data.get("refresh_token")

        try:
            user_id = get_user_id_by_token(refresh_token)
            token = update_token(refresh_token, user_id)
            return token, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Invalid token. Please log in again.")


auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
