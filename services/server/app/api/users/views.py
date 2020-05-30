from app.api.auth.crud import get_user_id_by_token
from app.api.auth.serializers import parser
from app.api.users.crud import add_user
from app.api.users.crud import get_all_users
from app.api.users.crud import get_user_by_email
from app.api.users.crud import get_user_by_id
from app.api.users.crud import remove_user
from app.api.users.crud import update_user
from app.api.users.serializers import user_readable
from app.api.users.serializers import user_writable
from app.api.users.serializers import users_namespace
from flask import request
from flask_restx import Resource

import jwt
import logging


logger = logging.getLogger(__name__)


class UsersList(Resource):
    @staticmethod
    @users_namespace.expect(user_writable, validate=True)
    @users_namespace.response(201, "Successfully added the user")
    @users_namespace.response(
        400, "Sorry.The provided email <user_email> is already registered"
    )
    def post():
        request_data = request.get_json()
        email = request_data["email"]
        response = dict()

        user_exists = get_user_by_email(email)
        if user_exists:
            logger.debug(f"User with email {email} exists")
            response[
                "message"
            ] = f"Sorry.The provided email {email} is already registered"
            return response, 400

        user = add_user(
            request_data["username"],
            request_data["email"],
            request_data["password"],
        )
        response["id"] = user.id
        response["message"] = f"{request_data['email']} was added"
        logger.debug(f"User with email {email} added successfully")
        return response, 201

    @staticmethod
    @users_namespace.expect(parser, validate=True)
    @users_namespace.marshal_with(user_readable, as_list=True)
    def get():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.debug(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user list")

        try:
            get_user_id_by_token(auth_header.split()[1])
            return get_all_users(), 200
        except jwt.ExpiredSignatureError:
            logger.error(f"Auth-token {auth_header.split()[1]} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            logger.error(f"Auth-token {auth_header.split()[1]} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")


class UsersDetail(Resource):
    @staticmethod
    @users_namespace.expect(parser, validate=True)
    @users_namespace.marshal_with(user_readable)
    @users_namespace.response(404, "User <user_id> does not exist")
    def get(user_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.debug(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user")

        try:
            get_user_id_by_token(auth_header.split()[1])

            user = get_user_by_id(user_id)

            if not user:
                logger.debug(f"User ID for given token {auth_header.split()[1]} is invalid")
                users_namespace.abort(404, f"User {user_id} does not exist")

            return user, 200
        except jwt.ExpiredSignatureError:
            logger.error(f"Auth-token {auth_header.split()[1]} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            logger.error(f"Auth-token {auth_header.split()[1]} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")

    @staticmethod
    @users_namespace.expect(parser, validate=True)
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(user_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.debug(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user")

        try:
            get_user_id_by_token(auth_header.split()[1])

            user = get_user_by_id(user_id)

            if not user:
                logger.debug(f"User ID for given token {auth_header.split()[1]} is invalid")
                users_namespace.abort(404, f"User {user_id} does not exist")

            remove_user(user)

            return dict(), 204
        except jwt.ExpiredSignatureError:
            logger.error(f"Auth-token {auth_header.split()[1]} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            logger.error(f"Auth-token {auth_header.split()[1]} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")

    @staticmethod
    @users_namespace.expect(user_readable, validate=True)
    # TODO Use multiple expect blocks in swagger UI
    # @users_namespace.expect(parser)
    @users_namespace.marshal_with(user_readable)
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(user_id):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.debug(f"Authorization header not found in {request}")
            users_namespace.abort(403, "Token required to fetch the user")

        try:
            get_user_id_by_token(auth_header.split()[1])

            request_data = request.get_json()

            user = get_user_by_id(user_id)

            if not user:
                logger.debug(f"User ID for given token {auth_header.split()[1]} is invalid")
                users_namespace.abort(404, f"User {user_id} does not exist")

            updated_user = update_user(
                user, request_data["username"], request_data["email"]
            )

            return updated_user, 200
        except jwt.ExpiredSignatureError:
            logger.error(f"Auth-token {auth_header.split()[1]} has expired")
            users_namespace.abort(401, "Token expired. Please log in again.")
        except jwt.InvalidTokenError:
            logger.error(f"Auth-token {auth_header.split()[1]} is invalid")
            users_namespace.abort(401, "Invalid token. Please log in again.")


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(UsersDetail, "/<int:user_id>")
