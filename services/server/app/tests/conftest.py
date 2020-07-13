from pytest import fixture

from app import create_app
from app import db
from app.api.auth.crud import add_token as add_token_service
from app.api.sentiment.crud import add_sentiment as add_sentiment_service
from app.api.users.crud import add_user as add_user_service
from app.api.users.crud import get_user_by_id as get_user_by_id_service
from app.api.users.crud import remove_user as remove_user_service


@fixture(scope="function")
def test_app():
    app = create_app("testing")
    with app.app_context():
        yield app


@fixture(scope="function")
def test_database():
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()


@fixture(scope="function")
def add_user():
    def _add_user(username, email, password):
        return add_user_service(username, email, password)

    return _add_user


@fixture(scope="function")
def remove_user():
    def _remove_user(user_id):
        user = get_user_by_id_service(user_id)
        remove_user_service(user)

    return _remove_user


@fixture(scope="function")
def login_user():
    def _login_user(user_id):
        return add_token_service(user_id)

    return _login_user


@fixture(scope="function")
def add_sentiments():
    def _add_sentiments(user_id, keyword):
        return add_sentiment_service(keyword, user_id)

    return _add_sentiments
