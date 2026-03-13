from flask import render_template, session

from app.blueprints.main import main_bp

@main_bp.route("/")
def index():
    """Página inicial do projeto em branco."""
    return render_template("auth/login.html")

@main_bp.route("/dashboard")
def dashboard():
    """Página de dashboard."""
    if "auth_token" not in session:
        return render_template("auth/login.html")
    return render_template("main/dashboard.html")
