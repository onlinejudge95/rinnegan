from flask_restx import Api
from app.api.health import health_namespace

api = Api(version="1.0", title="Sentimental API", doc="/swagger/")

api.add_namespace(health_namespace, path="/health")
