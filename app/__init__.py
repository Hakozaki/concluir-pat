"""Application Factory."""
import os
from flask import Flask
from config import config
from app.extensions import db, migrate, ma


def create_app(config_name: str | None = None) -> Flask:
    """Cria e configura a instância da aplicação Flask."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Garante que a pasta instance existe
    os.makedirs(app.instance_path, exist_ok=True)

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Registra blueprints
    from app.blueprints.api import api_bp
    from app.blueprints.main import main_bp

    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Registra handlers de erro
    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
