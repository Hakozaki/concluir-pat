import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuração base."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SIGEP_AUTH_API_URL: str = os.environ.get("SIGEP_AUTH_API_URL", "http://auth.sigep.docker.localhost/api/auth/login")


    @staticmethod
    def init_app(app) -> None:
        import logging
        from logging import FileHandler
        
        # Configure file logging
        file_handler = FileHandler("app.log")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Add handler to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        
        # Prevent double logging to console if the root logger also has handlers
        app.logger.propagate = False


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


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
