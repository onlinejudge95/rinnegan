import json
from flask import current_app as app
from flask_restx import Namespace, Resource

health_namespace = Namespace("health")


class Health(Resource):
    @health_namespace.response(200, "Health check passing")
    @health_namespace.response(404, "Health check failed")
    def get(self):
        try:
            with open(app.config["HEALTHCHECK_FILE_PATH"], "r") as fp:
                _ = fp.read()
        except IOError:
            return json.dumps({"health": "bad"}), 404
        else:
            return json.dumps({"health": "good"}), 200


health_namespace.add_resource(Health, "")
