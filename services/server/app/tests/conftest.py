from app import create_app
from app import db
from app.api.users.models import User

import pytest


@pytest.fixture(scope="module")
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
