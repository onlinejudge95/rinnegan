import logging

from flask import request
from flask_restx import Resource
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError

from app.api.auth.crud import add_token
from app.api.auth.crud import get_user_id_by_token
from app.api.auth.crud import password_matches
from app.api.auth.crud import update_token
from app.api.auth.serializers import auth_namespace
from app.api.auth.serializers import fetch_registered_user
from app.api.auth.serializers import login_user
from app.api.auth.serializers import refresh
from app.api.auth.serializers import register_user
from app.api.auth.serializers import user_tokens
from app.api.users.crud import add_user
from app.api.users.crud import get_user_by_email


logger = logging.getLogger(__name__)


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
            logger.info(f"User with email {email} exists")
            auth_namespace.abort(
                400, f"Sorry.The provided email {email} is already registered"
            )

        user = add_user(
            request_data["username"], email, request_data["password"],
        )
        logger.info(f"User with email {email} added successfully")
        return user, 201


class Login(Resource):
    @staticmethod
    @auth_namespace.marshal_with(user_tokens)
    @auth_namespace.expect(login_user, validate=True)
    @auth_namespace.response(200, "Successfully logged the user in")
    @auth_namespace.response(401, "Invalid password for <email>")
    @auth_namespace.response(
        404, "User with email <user_email> does not exists"
    )
    def post():
        request_data = request.get_json()
        email = request_data.get("email")
        password = request_data.get("password")

        user = get_user_by_email(email)
        if not user:
            logger.info(f"User with email {email} does not exists")
            auth_namespace.abort(
                404, f"User with email {email} does not exists"
            )

        if not password_matches(password, user):
            logger.info(f"Invalid password for {email}")
            auth_namespace.abort(401, f"Invalid password for {email}")

        token = add_token(user.id)

        logger.info(f"User with email {email} logged in successfully")
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
            logger.info(f"Refreshed token for user with id {user_id}")
            return token, 200
        except ExpiredSignatureError:
            logger.error(f"Auth-token {refresh_token} has expired")
            auth_namespace.abort(401, "Token expired. Please log in again.")
        except InvalidTokenError:
            logger.error(f"Auth-token {refresh_token} is invalid")
            auth_namespace.abort(401, "Invalid token. Please log in again.")


auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
