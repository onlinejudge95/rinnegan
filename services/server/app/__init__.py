from flask import Flask
import simplejson as json


def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def index():
        return json.dumps({"health": "good"})

    return app
