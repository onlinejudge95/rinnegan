import os


class BaseConfig:
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    JSON_SORT_KEYS = True
    HEALTHCHECK_FILE_PATH = "/usr/src/app/heartbeat.txt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900
    REFRESH_TOKEN_EXPIRATION = 2592000
    JWT_ENCODE_ALGORITHM = "HS256"
    SENTIMENT_QUOTA_LIMIT = 5


class DevelopmentConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 4
    JWT_ENCODE_ALGORITHM = "HS384"


class TestingConfig(BaseConfig):
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    TESTING = False
    JWT_ENCODE_ALGORITHM = "HS512"


cfg_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
