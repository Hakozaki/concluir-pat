from flask import render_template, session, current_app
from app.blueprints.main import main_bp
from app.utils import http_client

@main_bp.route("/")
def index():
    """Página inicial do projeto em branco."""
    return render_template("auth/login.html")

@main_bp.route("/dashboard")
def dashboard():
    """Página de dashboard com contadores do PAT."""
    if "auth_token" not in session:
        return render_template("auth/login.html")
    
    contadores = {
        "aguardando_analise": 0,
        "concluidos": 0,
        "pendentes": 0
    }
    
    try:
        api_url = f"{current_app.config['SIGEP_DATA_API_URL']}/api/pats/contadores-gerais"
        headers = {
            'Authorization': f"Bearer {session.get('auth_token')}"
        }
        response = http_client.get(api_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Mapeamento dos campos conforme retorno esperado da API (exemplo baseado em nomes comuns)
            # Precisaremos ajustar se o contrato for diferente
            contadores = data.get("data", data)
        else:
            current_app.logger.warning(f"Erro ao buscar contadores: API retornou status {response.status_code}")
    except Exception as e:
        current_app.logger.error(f"Exceção ao buscar contadores do PAT: {str(e)}")
        
    return render_template("main/dashboard.html", contadores=contadores)
