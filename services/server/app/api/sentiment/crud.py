from app import db
from app.api.sentiment.models import Sentiment


def add_user(keyword, user_id):
    """
    Adds a user with given details and returns an instance of it.

    :param: keyword
        keyword to find sentiment for
    :param: user_id
        Id of the user
    :returns:
        Sentiment with given details
    """
    sentiment = Sentiment(keyword=keyword, user_id=user_id)
    db.session.add(sentiment)
    db.session.commit()
    return sentiment
