import random
from datetime import datetime, timedelta
from flask import current_app
from faker import Faker
from app.utils import http_client

class PATWizardService:
    """Serviço para orquestrar o ciclo de vida completo de um PAT."""

    def __init__(self, auth_token=None):
        self.base_url = current_app.config.get("SIGEP_PATS_API_URL")
        self.fake = Faker('pt_BR')
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"

    def execute_full_cycle(self, custom_params=None):
        """Executa os 4 fluxos iniciais em sequência."""
        return self._run_workflow(steps=4, custom_params=custom_params)

    def execute_full_cycle_with_closure(self, custom_params=None):
        """Executa os 7 fluxos (Ciclo Completo + Encerramento) em sequência."""
        return self._run_workflow(steps=7, custom_params=custom_params)

    def _run_workflow(self, steps=4, custom_params=None):
        """Orquestrador genérico para os fluxos do PAT."""
        try:
            params = custom_params or {}
            results = {}
            
            # 1. Criar PAT
            pat_data = self._prepare_pat_data(params)
            pat_response = http_client.post(f"{self.base_url}/api/pats/store", json_data=pat_data, headers=self.headers)
            pat_response.raise_for_status()
            pat_result = pat_response.json()
            pat_data_obj = pat_result.get("data", {}) if isinstance(pat_result.get("data"), dict) else pat_result
            id_pat = pat_data_obj.get("idPAT") or pat_data_obj.get("idPat") or pat_data_obj.get("id")
            if not id_pat: raise ValueError(f"Falha ao obter idPAT: {pat_result}")
            results["pat"] = pat_result

            # 2. Atribuir Demanda
            demanda_data = self._prepare_demanda_data(id_pat, params)
            demanda_response = http_client.post(f"{self.base_url}/api/pats/demandas/store", json_data=demanda_data, headers=self.headers)
            demanda_response.raise_for_status()
            demanda_result = demanda_response.json()
            demanda_data_obj = demanda_result.get("data", {}) if isinstance(demanda_result.get("data"), dict) else demanda_result
            id_demanda_pat = demanda_data_obj.get("idDemandaPat") or demanda_data_obj.get("idPat") or demanda_data_obj.get("id")
            if not id_demanda_pat: raise ValueError(f"Falha ao obter idDemandaPat: {demanda_result}")
            results["demanda"] = demanda_result

            # 3. Atribuir Tarefa
            setor_context = demanda_data.get("idSetor")
            tarefa_data = self._prepare_tarefa_data(id_demanda_pat, setor_context, params)
            tarefa_response = http_client.post(f"{self.base_url}/api/pats/tarefas/store", json_data=tarefa_data, headers=self.headers)
            tarefa_response.raise_for_status()
            tarefa_result = tarefa_response.json()
            tarefa_data_obj = tarefa_result.get("data", {}) if isinstance(tarefa_result.get("data"), dict) else tarefa_result
            id_tarefa = tarefa_data_obj.get("idTarefa") or tarefa_data_obj.get("idPat") or tarefa_data_obj.get("id")
            if not id_tarefa: raise ValueError(f"Falha ao obter idTarefa: {tarefa_result}")
            results["tarefa"] = tarefa_result

            # 4. Cadastrar Atividade
            atividade_data = self._prepare_atividade_data(id_tarefa, params)
            atividade_response = http_client.post(f"{self.base_url}/api/pats/atividades/store", json_data=atividade_data, headers=self.headers)
            atividade_response.raise_for_status()
            results["atividade"] = atividade_response.json()

            if steps >= 7:
                # 5. Encerrar Tarefa (PATCH)
                tarefa_close_data = {"idTarefa": id_tarefa}
                t_close_resp = http_client.patch(f"{self.base_url}/api/pats/tarefas/encerrar", json_data=tarefa_close_data, headers=self.headers)
                t_close_resp.raise_for_status()
                results["encerramento_tarefa"] = t_close_resp.json()

                # 6. Encerrar Demanda (PATCH)
                demanda_close_data = {"idDemandaPat": id_demanda_pat, "despacho": None}
                d_close_resp = http_client.patch(f"{self.base_url}/api/pats/demandas/encerrar", json_data=demanda_close_data, headers=self.headers)
                d_close_resp.raise_for_status()
                results["encerramento_demanda"] = d_close_resp.json()

                # 7. Encerrar PAT (POST)
                pat_close_data = {"idPAT": id_pat, "despacho": None}
                p_close_resp = http_client.post(f"{self.base_url}/api/pats/encerrar", json_data=pat_close_data, headers=self.headers)
                p_close_resp.raise_for_status()
                results["encerramento_pat"] = p_close_resp.json()

            return {
                "success": True,
                "workflow_results": results,
                "summary": {
                    "id_pat": id_pat,
                    "id_demanda_pat": id_demanda_pat,
                    "id_tarefa": id_tarefa,
                    "closed": steps >= 7
                }
            }

        except Exception as e:
            current_app.logger.error(f"Erro no ciclo do PAT ({steps} passos): {str(e)}")
            return {"success": False, "error": str(e)}

    def _prepare_pat_data(self, params):
        prazo_days = random.randint(10, 20)
        prazo_date = (datetime.now() + timedelta(days=prazo_days)).strftime("%d/%m/%Y")
        
        return {
            "idEntidade": params.get("idEntidade", 2),
            "idEntidadeSolicitante": 2,
            "idProprietario": params.get("idProprietario", random.choice([2, 76, 114])),
            "idSetor": params.get("idSetor", random.choice([1488, 1059])),
            "prioridade": params.get("prioridade", random.choice([3, 4])),
            "tipoProcesso": "pedidoInterno",
            "numeroReferencia": None,
            "numeroProcesso": None,
            "descricaoPat": params.get("descricaoPat", self.fake.text(max_nb_chars=600)),
            "prazoPat": prazo_date,
            "justificativaPrioridade": None,
            "expectativaResposta": prazo_date,
            "idsQuesito": None
        }

    def _prepare_demanda_data(self, id_pat, params):
        return {
            "idPat": id_pat,
            "idDemanda": params.get("idDemanda", random.choice([10009, 10030, 30170])),
            "idSetor": params.get("idSetor", random.choice([1488, 1059])),
            "despacho": None
        }

    def _prepare_tarefa_data(self, id_demanda_pat, setor, params):
        # Lógica de Setor para usuários atribuídos
        usuarios = [2] if setor == 1488 else [114]
        
        return {
            "idDemandaPat": id_demanda_pat,
            "descricaoTarefa": params.get("descricaoTarefa", self.fake.sentence(nb_words=10)),
            "prazoTarefa": (datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y"),
            "idsUsuariosAtribuidos": usuarios
        }

    def _prepare_atividade_data(self, id_tarefa, params):
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return {
            "idTarefa": id_tarefa,
            "descricaoAtividade": params.get("descricaoAtividade", self.fake.sentence(nb_words=15)),
            "tempoCorrido": random.uniform(1.0, 5.0),
            "dataInicio": now_str,
            "dataTermino": now_str,
            "deslocamento": "N",
            "cidade": None
        }
