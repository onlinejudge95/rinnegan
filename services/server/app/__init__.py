from flask import Flask
import simplejson as json
from app.config import cfg_map


def create_app(environemnt=None):
    app = Flask(__name__)
    app.config.from_object(cfg_map[environemnt])

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    @app.route("/health")
    def index():
        return json.dumps({"health": "good"})

    return app
