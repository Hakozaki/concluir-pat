import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class TestPATAutomation(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.utils.http_client.post")
    def test_pat_full_cycle_success(self, mock_post):
        # Mocking responses for the 4 steps
        mock_pat_resp = MagicMock()
        mock_pat_resp.status_code = 201
        mock_pat_resp.json.return_value = {"id": 123, "status": "success"}
        
        mock_demanda_resp = MagicMock()
        mock_demanda_resp.status_code = 201
        mock_demanda_resp.json.return_value = {"id": 456, "status": "success"}
        
        mock_tarefa_resp = MagicMock()
        mock_tarefa_resp.status_code = 201
        mock_tarefa_resp.json.return_value = {"id": 789, "status": "success"}
        
        mock_atividade_resp = MagicMock()
        mock_atividade_resp.status_code = 201
        mock_atividade_resp.json.return_value = {"status": "success"}
        
        mock_post.side_effect = [
            mock_pat_resp,
            mock_demanda_resp,
            mock_tarefa_resp,
            mock_atividade_resp
        ]

        response = self.client.post("/api/v1/automation/pat-full-cycle")
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["summary"]["id_pat"], 123)
        self.assertEqual(data["summary"]["id_demanda_pat"], 456)
        self.assertEqual(data["summary"]["id_tarefa"], 789)
        self.assertEqual(mock_post.call_count, 4)

    @patch("app.utils.http_client.post")
    def test_pat_full_cycle_failure(self, mock_post):
        # Mocking failure at the first step
        mock_pat_resp = MagicMock()
        mock_pat_resp.status_code = 400
        mock_pat_resp.raise_for_status.side_effect = Exception("Bad Request")
        
        mock_post.return_value = mock_pat_resp

        response = self.client.post("/api/v1/automation/pat-full-cycle")
        
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Bad Request", data["error"])

    @patch("app.utils.http_client.post")
    @patch("app.utils.http_client.patch")
    def test_pat_complete_closure_success(self, mock_patch, mock_post):
        # Mocking 7 responses
        m_pat = MagicMock(status_code=201)
        m_pat.json.return_value = {"idPAT": 123}
        
        m_demanda = MagicMock(status_code=201)
        m_demanda.json.return_value = {"idDemandaPat": 456}
        
        m_tarefa = MagicMock(status_code=201)
        m_tarefa.json.return_value = {"idTarefa": 789}
        
        m_atividade = MagicMock(status_code=201)
        m_atividade.json.return_value = {"status": "success"}
        
        # Closures
        m_t_close = MagicMock(status_code=200)
        m_t_close.json.return_value = {"status": "closed"}
        
        m_d_close = MagicMock(status_code=200)
        m_d_close.json.return_value = {"status": "closed"}
        
        m_p_close = MagicMock(status_code=200)
        m_p_close.json.return_value = {"status": "closed"}
        
        # POST calls order: PAT, Demanda, Tarefa, Atividade, then Closure PAT (last step)
        mock_post.side_effect = [m_pat, m_demanda, m_tarefa, m_atividade, m_p_close]
        # PATCH calls order: Tarefa closure, Demanda closure
        mock_patch.side_effect = [m_t_close, m_d_close]

        response = self.client.post("/api/v1/automation/pat-complete-closure")
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(data["summary"]["closed"])
        self.assertEqual(mock_post.call_count, 5)
        self.assertEqual(mock_patch.call_count, 2)

if __name__ == "__main__":
    unittest.main()
