import pytest

from app import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app("testing")
    with app.app_context():
        yield app
