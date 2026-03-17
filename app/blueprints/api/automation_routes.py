from flask import jsonify, request
from app.blueprints.api import api_bp
from app.services.pat_wizard_service import PATWizardService

@api_bp.post("/automation/pat-full-cycle")
def execute_pat_full_cycle():
    """
    Executa o ciclo completo de um PAT (Criação -> Demanda -> Tarefa -> Atividade).
    Pode receber parâmetros customizados no corpo da requisição.
    """
    custom_params = request.get_json(silent=True) if request.is_json else None
    from flask import session
    auth_token = session.get("auth_token")
    
    wizard = PATWizardService(auth_token=auth_token)
    result = wizard.execute_full_cycle(custom_params)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@api_bp.post("/automation/pat-complete-closure")
def execute_pat_complete_closure():
    """
    Executa o ciclo completo de um PAT seguido de encerramento de tarefa, demanda e PAT.
    """
    custom_params = request.get_json(silent=True) if request.is_json else None
    from flask import session
    auth_token = session.get("auth_token")
    
    wizard = PATWizardService(auth_token=auth_token)
    result = wizard.execute_full_cycle_with_closure(custom_params)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500
