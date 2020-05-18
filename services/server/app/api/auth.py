from app.api.users.crud import add_user
from app.api.users.crud import get_user_by_email
from app.api.users.crud import get_user_by_id
from app.api.users.models import User
from flask import request
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import Resource

import jwt


auth_namespace = Namespace("auth")

parser = auth_namespace.parser()
parser.add_argument("Authorization", location="header")

fetch_registered_user = auth_namespace.model(
    "Existing-User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
    },
)
register_user = auth_namespace.inherit(
    "New-User",
    fetch_registered_user,
    {"password": fields.String(required=True)},
)
login_user = auth_namespace.model(
    "Log-In",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)
refresh = auth_namespace.model(
    "Refresh", {"refresh_token": fields.String(required=True)},
)
user_tokens = auth_namespace.inherit(
    "Tokens", refresh, {"access_token": fields.String(required=True)},
)


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
        response = {
            "access_token": user.encode_token(user.id, "access").decode(
                "utf-8"
            ),
            "refresh_token": user.encode_token(user.id, "refresh").decode(
                "utf-8"
            ),
        }
        return response, 200


class Refresh(Resource):
    @staticmethod
    @auth_namespace.marshal_with(user_tokens)
    @auth_namespace.expect(refresh, validate=True)
    @auth_namespace.response(200, "Successfully logged the user in")
    @auth_namespace.response(401, "Invalid token. Please log in again.")
    def post():
        request_data = request.get_json()
        refresh_token = request_data.get("refresh_token")

        try:
            user_id = User.decode_token(refresh_token)
            user = get_user_by_id(user_id)
            response = {
                "access_token": user.encode_token(user.id, "access"),
                "refresh_token": user.encode_token(user.id, "refresh"),
            }
            return response, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Invalid token. Please log in again.")


class Status(Resource):
    @staticmethod
    @auth_namespace.marshal_with(fetch_registered_user)
    @auth_namespace.expect(parser)
    @auth_namespace.response(200, "Successfully got the user status")
    @auth_namespace.response(401, "Invalid token. Please log in again.")
    def get():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            auth_namespace.abort(403, "Token required to fetch the status")

        try:
            access_token = auth_header.split()[1]
            user_id = User.decode_token(access_token)
            user = get_user_by_id(user_id)
            return user, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Invalid token. Please log in again.")


auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
auth_namespace.add_resource(Status, "/status")
