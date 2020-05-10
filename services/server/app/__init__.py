import functools
from flask import Flask, request, abort

from app.config import cfg_map


def create_app(environemnt):
    app = Flask(__name__)
    app.config.from_object(cfg_map[environemnt])

    from app.api import api

    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    @app.before_request
    def check_headers(*args, **kwargs):
        accepts = request.headers.get("Accept")

        if not accepts or accepts != "application/json":
            abort(415, "Only content type supported is application/json")

    return app
