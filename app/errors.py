"""Handlers de erro globais."""
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """Registra handlers de erro na aplicação."""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Requisição inválida", "detail": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Não autorizado"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Acesso proibido"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Método não permitido"}), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": "Dados inválidos", "detail": str(e)}), 422

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Erro interno: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.description}), e.code
