from flask import current_app as app

from app import db
from app.api.users.models import User


def get_user_by_email(email):
    """
    Returns the user with the given email ID if it valid.
    If the given user does not exists returns None

    :param: email
        Email of the user
    :returns:
        User with the given email ID or None if the user does not exists
    """
    return User.query.filter_by(email=email).first()


def add_user(username, email, password):
    """
    Adds a user with given details and returns an instance of it.

    :param: username
        Username of the user
    :param: email
        Email of the user
    :param: password
        Password of the user
    :returns:
        User with given details
    """
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def get_all_users():
    """
    Returns the list of all users

    :returns:
        List of all users
    """
    return User.query.all()


def get_user_by_id(user_id):
    """
    Returns the user with given id

    :param: user_id
        ID of the user
    :returns:
        User with given ID
    """
    return User.query.get(user_id)


def remove_user(user):
    """
    Removes the given user

    :param: user
        User to be removed
    """
    db.session.delete(user)
    db.session.commit()


def update_user(user, username, email):
    """
    Updates a given user with given details and returns an instance of it.

    :param: user
        User to be updated
    :param: username
        Username of the user
    :param: email
        Email of the user
    :returns:
        Updated user
    """
    user.username = username
    user.email = email
    db.session.commit()
    return user


def is_user_sentiment_quota_exhausted(user_id):
    """
    Utility method to find if user has exhausted their
    sentiment quota for keyword analysis

    :param: user_id
        ID of the user
    :returns:
        Status of quota
    """
    user = get_user_by_id(user_id)

    return user.sentiment_quota < app.config.get("SENTIMENT_QUOTA_LIMIT")


def update_user_sentiment_quota(user_id):
    """
    Utility method to update sentiment quota for a user

    :param: user_id
        ID of the user
    """
    user = get_user_by_id(user_id)

    user.sentiment_quota -= 1
    db.session.commit()
