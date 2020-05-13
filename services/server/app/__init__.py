import functools
from flask import Flask, request, abort
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from app.config import cfg_map


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(environemnt):
    app = Flask(__name__)
    app.config.from_object(cfg_map[environemnt])

    db.init_app(app)
    bcrypt.init_app(app)

    from app.api import api

    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.before_request
    def check_headers(*args, **kwargs):
        if "swagger" not in request.path:
            accepts = request.headers.get("Accept")
            if not accepts or accepts != "application/json":
                abort(415, "Only content type supported is application/json")
            if request.method in ["POST", "PUT"]:
                content_type = request.headers.get("Content-Type")
                if not content_type or content_type != "application/json":
                    abort(415, "POST & PATCH requests should define a Content-Type header")

    return app
