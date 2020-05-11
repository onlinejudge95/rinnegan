import os


# Test development config
def test_development_config(test_app):
    test_app.config.from_object("app.config.DevelopmentConfig")
    config = test_app.config

    assert config["TESTING"]
    assert config["SECRET_KEY"]
    assert config["JSON_SORT_KEYS"]


# Test testing config
def test_testing_config(test_app):
    test_app.config.from_object("app.config.TestingConfig")
    config = test_app.config

    assert config["TESTING"]
    assert config["SECRET_KEY"]
    assert not config["JSON_SORT_KEYS"]


# Test production config
def test_production_config(test_app):
    test_app.config.from_object("app.config.ProductionConfig")
    config = test_app.config

    assert not config["TESTING"]
    assert config["SECRET_KEY"]
    assert config["JSON_SORT_KEYS"]
