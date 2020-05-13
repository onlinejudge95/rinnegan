from app.api.users.crud import (
    get_user_by_email,
    add_user,
    get_all_users,
    get_user_by_id,
    remove_user,
    update_user,
)
from flask import request, abort
from flask_restx import Namespace, Resource, fields

users_namespace = Namespace("users")

user_readable = users_namespace.model(
    "Existing-User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

user_writable = users_namespace.inherit(
    "New-User", user_readable, {"password": fields.String(required=True)},
)


class UsersList(Resource):
    @staticmethod
    @users_namespace.expect(user_writable, validate=True)
    @users_namespace.response(400, "Sorry.The provided email <user_email> is already registered")
    def post():
        request_data = request.get_json()
        response = dict()

        user_exists = get_user_by_email(request_data["email"])
        if user_exists:
            response[
                "message"
            ] = f"Sorry.The provided email {request_data['email']} is already registered"
            return response, 400

        user_id = add_user(
            request_data["username"], request_data["email"], request_data["password"]
        )
        response["id"] = user_id
        response["message"] = f"{request_data['email']} was added"
        return response, 201

    @staticmethod
    @users_namespace.marshal_with(user_readable, as_list=True)
    def get():
        return get_all_users(), 200


class UsersDetail(Resource):
    @staticmethod
    @users_namespace.marshal_with(user_readable)
    @users_namespace.response(404, "User <user_id> does not exist")
    def get(user_id):
        user = get_user_by_id(user_id)
        response = dict()

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        return user, 200

    @staticmethod
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(user_id):
        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        remove_user(user)
        return dict(), 204

    @staticmethod
    @users_namespace.expect(user_readable, validate=True)
    @users_namespace.marshal_with(user_readable)
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(user_id):
        request_data = request.get_json()

        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        updated_user = update_user(user, request_data["username"], request_data["email"])

        return updated_user, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(UsersDetail, "/<int:user_id>")
