from app import db
from app.api.sentiment.models import Sentiment
from app.api.users.crud import update_user_sentiment_quota


def add_sentiment(keyword, user_id):
    """
    Adds a sentiment with given details and returns an instance of it.

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

    update_user_sentiment_quota(user_id)
    return sentiment


def get_all_sentiments():

    """
    Returns the list of all sentiments

    :returns:
        List of all sentiments
    """
    return Sentiment.query.all()
