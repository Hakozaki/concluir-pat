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
    from app.blueprints.auth import auth_bp

    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Registra handlers de erro
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Middleware global de autenticação
    from flask import session, redirect, url_for, request
    
    @app.before_request
    def require_login():
        # Lista de rotas públicas
        public_endpoints = ["auth.login", "static"]
        
        # Ignora se for rota pública ou se não houver endpoint definido (ex: favicon)
        if not request.endpoint or request.endpoint in public_endpoints:
            return
            
        # Verifica se tem o token na sessão
        token = session.get("auth_token")
        if not token:
            return redirect(url_for("auth.login"))

        # Valida o token contra a API externa
        from app.utils import http_client
        from flask import current_app
        
        payload_url = current_app.config.get("SIGEP_AUTH_PAYLOAD_URL")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            # Se não voltar 200, o token é considerado inválido
            response = http_client.post(payload_url, headers=headers, timeout=5)
            
            if response.status_code != 200:
                current_app.logger.warning(f"Sessão encerrada: Token inválido na API externa. Status: {response.status_code}")
                session.clear()
                return redirect(url_for("auth.login"))
        except Exception as e:
            current_app.logger.error(f"Erro ao validar token na API externa: {e}")
            session.clear()
            return redirect(url_for("auth.login"))

    return app

