from app.api.users.crud import get_user_by_email, add_user
from flask import request, abort
from flask_restx import Namespace, Resource, fields

users_namespace = Namespace("users")

user_model = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
    },
)

user_post_model = users_namespace.inherit(
    "User Create", user_model, {"password": fields.String(required=True)}
)


class UsersList(Resource):
    @users_namespace.expect(user_post_model, validate=True)
    @users_namespace.response(
        400, "Sorry.The provided email <user_email> is already registered"
    )
    def post(self):
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


users_namespace.add_resource(UsersList, "")
