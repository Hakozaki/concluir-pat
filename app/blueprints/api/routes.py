"""Rotas da API v1."""
from flask import jsonify

from app.blueprints.api import api_bp


@api_bp.get("/health")
def health_check():
    """Verifica se a API está operacional."""
    return jsonify({"status": "ok"}), 200
