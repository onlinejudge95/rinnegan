from flask_restx import fields
from flask_restx import Namespace


sentiment_namespace = Namespace("sentiment")

parser = sentiment_namespace.parser()
parser.add_argument("Authorization", location="headers")

sentiment_schema = sentiment_namespace.model(
    "Sentiment",
    {
        "id": fields.Integer(readOnly=True),
        "user_id": fields.Integer(required=True),
        "keyword": fields.String(required=True),
    },
)

update_sentiment_schema = sentiment_namespace.model(
    "Update Sentiment",
    {
        "id": fields.Integer(readOnly=True),
        "keyword": fields.String(required=True),
    },
)
