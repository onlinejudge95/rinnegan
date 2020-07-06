import json
import logging

from flask import current_app as app
from flask_restx import Namespace
from flask_restx import Resource


logger = logging.getLogger(__name__)
health_namespace = Namespace("health")


class Health(Resource):
    @staticmethod
    @health_namespace.response(200, "Health check passing")
    @health_namespace.response(404, "Health check failed")
    def get():
        health = "bad"
        try:
            with open(app.config["HEALTHCHECK_FILE_PATH"], "r") as fp:
                health = fp.read().strip()
                logger.info("Health check passing")
                return json.dumps({"health": health}), 200
        except IOError:
            logger.error("Health check fails", exc_info=True)
            return json.dumps({"health": health}), 404


health_namespace.add_resource(Health, "")
