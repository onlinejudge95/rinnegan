import os


class BaseConfig:
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    JSON_SORT_KEYS = True
    HEALTHCHECK_FILE_PATH = "/usr/src/app/heartbeat.txt"


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    JSON_SORT_KEYS = False


class ProductionConfig(BaseConfig):
    TESTING = False


cfg_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
