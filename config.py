import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuração base."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    @staticmethod
    def init_app(app) -> None:
        pass


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento."""
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'dev.db')}",
    )


class TestingConfig(Config):
    """Configuração de testes."""
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(Config):
    """Configuração de produção."""
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", "")

    @classmethod
    def init_app(cls, app) -> None:
        Config.init_app(app)
        import logging
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler("app.log", maxBytes=10_000, backupCount=3)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
