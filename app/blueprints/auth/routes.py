"""Rotas de autenticacao."""
from flask import render_template, request, redirect, url_for, flash, session, current_app

from app.blueprints.auth import auth_bp
from app.utils import http_client

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("loginUsuarioSistema")
        password = request.form.get("senhaUsuarioSistema")
        
        if not username or not password:
            flash("Usuário e senha são obrigatórios.", "error")
            return render_template("auth/login.html")
            
        api_url = current_app.config.get("SIGEP_AUTH_API_URL", "")
        if not api_url.endswith("/api/auth/login"):
            api_url = api_url.rstrip("/") + "/api/auth/login"
            
        payload = {
            "loginUsuarioSistema": username,
            "senhaUsuarioSistema": password
        }
        
        try:
            response = http_client.post(api_url, json_data=payload, timeout=5)
            if response.status_code == 200:

                data = response.json()
                # Salva o token da estrutura data.authorization.token conforme solicitado
                token = data.get("authorization", {}).get("token")
                
                if token:
                    session["auth_token"] = token
                    session["usuario"] = username
                    flash("Login realizado com sucesso!", "success")
                    return redirect(url_for("main.index"))
                else:
                    flash("Erro ao processar token de autenticação.", "error")
            else:

                flash("Credenciais inválidas ou erro no servidor de autenticação.", "error")
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Erro ao conectar com a API de auth: {e}")
            flash("Sistema de autenticação indisponível no momento.", "error")
            
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("auth.login"))
