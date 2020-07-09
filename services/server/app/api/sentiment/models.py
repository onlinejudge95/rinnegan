import os

from app import db
from app.api.sentiment.admin import SentimentAdminView


class Sentiment(db.Model):

    __tablename__ = "sentiment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(128), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    def __init__(self, keyword, user_id):
        self.keyword = keyword
        self.user_id = user_id


if os.getenv("FLASK_ENV") != "production":
    from app import admin

    admin.add_view(SentimentAdminView(Sentiment, db.session))
