import pytest
from unittest.mock import patch, MagicMock
from flask import session, url_for

def test_protected_route_valid_token(client, app):
    """Testa se o acesso é permitido com um token válido."""
    with client.session_transaction() as sess:
        sess['auth_token'] = 'valid-token'

    with patch('app.utils.http_client.post') as mock_post:
        # Simula resposta 200 da API de payload
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Acessa a rota principal (dashboard/index)
        response = client.get('/')
        
        # Como o plano diz para redirecionar se não estiver logado, 
        # e aqui estamos logados (simulado), deve retornar 200
        assert response.status_code == 200
        mock_post.assert_called_once()

def test_protected_route_invalid_token(client, app):
    """Testa se o usuário é redirecionado se o token for inválido na API externa."""
    with client.session_transaction() as sess:
        sess['auth_token'] = 'invalid-token'

    with patch('app.utils.http_client.post') as mock_post:
        # Simula resposta 401 da API de payload
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        # Tenta acessar rota protegida
        response = client.get('/', follow_redirects=False)
        
        # Deve redirecionar para o login
        assert response.status_code == 302
        assert response.location.endswith(url_for('auth.login'))
        
        # A sessão deve ter sido limpa
        with client.session_transaction() as sess:
            assert 'auth_token' not in sess

def test_protected_route_api_error(client, app):
    """Testa se o usuário é redirecionado em caso de erro na API externa."""
    with client.session_transaction() as sess:
        sess['auth_token'] = 'some-token'

    with patch('app.utils.http_client.post') as mock_post:
        # Simula erro de conexão
        mock_post.side_effect = Exception("API Down")

        # Tenta acessar rota protegida
        response = client.get('/', follow_redirects=False)
        
        # Deve redirecionar para o login (conforme lógica implementada)
        assert response.status_code == 302
        assert response.location.endswith(url_for('auth.login'))

def test_public_route_no_token(client):
    """Testa se rotas públicas continuam acessíveis sem token."""
    response = client.get('/login')
    assert response.status_code == 200
