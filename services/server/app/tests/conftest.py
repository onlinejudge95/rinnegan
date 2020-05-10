import pytest

from app import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    with app.app_context():
        yield app
