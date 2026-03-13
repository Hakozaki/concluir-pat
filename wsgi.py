"""Entrypoint para Gunicorn em produção.

Uso: gunicorn wsgi:app
"""
from app import create_app

app = create_app("production")
