import pytest
import database.db as db_module
from app import app as flask_app


@pytest.fixture()
def app(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test_spendly.db")
    original_connect = db_module.sqlite3.connect

    def patched_connect(path, **kwargs):
        if path == "spendly.db":
            return original_connect(db_path, **kwargs)
        return original_connect(path, **kwargs)

    monkeypatch.setattr(db_module.sqlite3, "connect", patched_connect)

    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test-secret"})
    db_module.init_db()
    db_module.create_user("Test User", "user@test.com", "password123")

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()
