# Test development config
def test_development_config(test_app):
    test_app.config.from_object("app.config.DevelopmentConfig")
    config = test_app.config

    assert config["TESTING"]
    assert config["SECRET_KEY"]
    assert config["JSON_SORT_KEYS"]
    assert not config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    assert config["SQLALCHEMY_DATABASE_URI"]
    assert config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000
    assert test_app.config["JWT_ENCODE_ALGORITHM"] == "HS384"


# Test testing config
def test_testing_config(test_app):
    test_app.config.from_object("app.config.TestingConfig")
    config = test_app.config

    assert config["TESTING"]
    assert config["SECRET_KEY"]
    assert not config["JSON_SORT_KEYS"]
    assert not config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    assert config["SQLALCHEMY_DATABASE_URI"]
    assert config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 3
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 3
    assert test_app.config["JWT_ENCODE_ALGORITHM"] == "HS256"


# Test production config
def test_production_config(test_app):
    test_app.config.from_object("app.config.ProductionConfig")
    config = test_app.config

    assert not config["TESTING"]
    assert config["SECRET_KEY"]
    assert config["JSON_SORT_KEYS"]
    assert not config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    assert config["SQLALCHEMY_DATABASE_URI"]
    assert config["BCRYPT_LOG_ROUNDS"] == 13
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000
    assert test_app.config["JWT_ENCODE_ALGORITHM"] == "HS512"
