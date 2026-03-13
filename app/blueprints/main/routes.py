"""Rotas principais da aplicação."""
from flask import jsonify

from app.blueprints.main import main_bp

@main_bp.route("/")
def index():
    """Página inicial do projeto em branco."""
    return jsonify({
        "message": "Welcome to the Concluir PAT Application",
        "description": "This is a blank project page."
    }), 200
