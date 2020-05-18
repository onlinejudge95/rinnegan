from app.api.users.crud import add_user
from app.api.users.crud import get_user_by_email
from flask import request
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import Resource


auth_namespace = Namespace("auth")
user_readable = auth_namespace.model(
    "Existing-User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

user_writable = auth_namespace.inherit(
    "New-User", user_readable, {"password": fields.String(required=True)},
)


class Register(Resource):
    @staticmethod
    @auth_namespace.marshal_with(user_readable)
    @auth_namespace.expect(user_writable, validate=True)
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
    def post():
        pass


class Refresh(Resource):
    @staticmethod
    def post():
        pass


class Status(Resource):
    @staticmethod
    def get():
        pass


auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
auth_namespace.add_resource(Status, "/status")
