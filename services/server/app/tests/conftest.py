import os

import pytest

from app import create_app
from app import db
from app.api.users.models import User
from app.api.auth.crud import add_token
from app.api.sentiment.crud import add_sentiment


@pytest.fixture(scope="function")
def test_app():
    app = create_app("testing")
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def test_database():
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="function")
def add_user():
    def _add_user(username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user


@pytest.fixture(scope="function")
def remove_user():
    def _remove_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

    return _remove_user


@pytest.fixture(scope="function")
def login_user():
    def _login_user(user_id):
        return add_token(user_id)

    return _login_user


@pytest.fixture(scope="function")
def add_sentiments():
    def _add_sentiments(user_id, keyword):
        return add_sentiment(keyword, user_id)

    return _add_sentiments


@pytest.fixture(scope="module")
def test_admin_app():
    os.environ["FLASK_ENV"] = "production"
    app = create_app("production")

    with app.app_context():
        yield app
