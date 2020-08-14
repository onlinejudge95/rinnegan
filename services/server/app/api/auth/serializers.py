from flask_restx import fields
from flask_restx import Namespace


auth_namespace = Namespace("auth")

parser = auth_namespace.parser()
parser.add_argument("Authorization", location="headers")

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
access_token = auth_namespace.model(
    "Access", {"access_token": fields.String(required=True)}
)
user_tokens = auth_namespace.inherit(
    "Tokens",
    refresh,
    {
        "access_token": fields.String(required=True),
        "user_id": fields.Integer(readOnly=True),
    },
)
