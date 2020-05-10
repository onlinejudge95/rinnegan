import os


# Test development config
def test_development_config(test_app):
    test_app.config.from_object("app.config.DevelopmentConfig")
    config = test_app.config

    assert config["TESTING"]


# Test testing config
def test_testing_config(test_app):
    test_app.config.from_object("app.config.TestingConfig")
    config = test_app.config

    assert config["TESTING"]


# Test production config
def test_production_config(test_app):
    test_app.config.from_object("app.config.ProductionConfig")
    config = test_app.config

    assert not config["TESTING"]
