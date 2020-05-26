
from flask_restx import Namespace
from flask_restx import fields


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
