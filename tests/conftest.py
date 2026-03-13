"""Fixtures de teste."""
import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Cria a aplicação em modo de testes."""
    flask_app = create_app("testing")
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Cliente de teste Flask."""
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    """Sessão de banco dados limpa por teste."""
    with app.app_context():
        yield _db
        _db.session.rollback()
