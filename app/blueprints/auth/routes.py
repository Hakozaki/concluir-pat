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
                json_resp = response.json()
                # O caminho correto conforme o log é: data -> authorization -> token
                data_obj = json_resp.get("data", {})
                token = data_obj.get("authorization", {}).get("token")
                
                if not token:
                    # Fallbacks caso mude futuramente
                    token = data_obj.get("token") or json_resp.get("token")
                
                if token:
                    session["auth_token"] = token
                    session["usuario"] = username
                    flash("Login realizado com sucesso!", "success")
                    return redirect(url_for("main.dashboard"))
                else:
                    current_app.logger.error(f"Token não encontrado na resposta: {json_resp}")
                    flash("Erro ao processar token de autenticação.", "error")
            else:

                flash("Credenciais inválidas ou erro no servidor de autenticação.", "error")
        except Exception as e:
            current_app.logger.error(f"Erro ao conectar com a API de auth: {e}")
            flash("Sistema de autenticação indisponível no momento.", "error")
            
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("auth.login"))
