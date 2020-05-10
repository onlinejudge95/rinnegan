class BaseConfig:
    TESTING = True


class DevelopmentConfig(BaseConfig):
    name = "dev"


class TestingConfig(BaseConfig):
    name = "test"


class ProductionConfig(BaseConfig):
    TESTING = False


cfg_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    None: BaseConfig,
}
