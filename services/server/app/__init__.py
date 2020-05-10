from flask import Flask

from app.config import cfg_map


def create_app(environemnt):
    app = Flask(__name__)
    app.config.from_object(cfg_map[environemnt])

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    from app.api import api

    api.init_app(app)

    return app
