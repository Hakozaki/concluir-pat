"""Testes para o blueprint de rotas principais."""

def test_index_route(client):
    """Testa se a página inicial está funcionando corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["message"] == "Welcome to the Concluir PAT Application"
    assert data["description"] == "This is a blank project page."
