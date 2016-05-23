"""Configuration for median-microservice."""


class BaseConfig(object):
    """Base config class for median-microservice."""

    DEBUG = False
    TESTING = False


class DevConfig(BaseConfig):
    """Dev-specific config for median-microservice."""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production-specific config for median-microservice."""

    pass
