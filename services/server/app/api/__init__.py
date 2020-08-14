from flask_restx import Api

from app.api.auth.views import auth_namespace
from app.api.health import health_namespace
from app.api.sentiment.views import sentiment_namespace
from app.api.users.views import users_namespace


api = Api(version="1.0", title="Sentimental API", doc="/swagger/")

api.add_namespace(health_namespace, path="/health")
api.add_namespace(users_namespace, path="/users")
api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(sentiment_namespace, path="/sentiment")
