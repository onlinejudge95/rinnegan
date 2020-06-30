from app.api.sentiment.crud import add_sentiment
from app.api.sentiment.serializers import sentiment_namespace
from app.api.sentiment.serializers import sentiment_schema
from app.api.users.crud import get_user_by_id
from flask import request
from flask_restx import Resource

import logging


logger = logging.getLogger(__name__)


class SentimentList(Resource):
    @staticmethod
    @sentiment_namespace.expect(sentiment_schema, validate=True)
    @sentiment_namespace.response(201, "Successfully added the user")
    @sentiment_namespace.response(
        400, "Sorry.The provided email <user_email> is not registered"
    )
    def post():
        request_data = request.get_json()
        keyword = request_data["keyword"]
        user_id = request_data["user_id"]
        response = {}

        user_exists = get_user_by_id(user_id)
        if not user_exists:
            logger.info(f"User with id {user_id} does not exists")
            response["message"] = "Sorry.The provided user is not registered"
            return response, 400

        sentiment = add_sentiment(
            request_data["keyword"], request_data["user_id"]
        )
        response["id"] = sentiment.id
        response["message"] = f"{request_data['keyword']} was added"
        logger.info(f"Sentiment for {keyword} added successfully")
        return response, 201


class SentimentDetail(Resource):
    pass


sentiment_namespace.add_resource(SentimentList, "")
sentiment_namespace.add_resource(SentimentDetail, "/<int:user_id>")
