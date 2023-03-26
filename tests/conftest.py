import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

@pytest.fixture(scope='session', autouse=True)
def init_db():
    from db.database import create_tables, drop_tables
    create_tables()
    yield
    drop_tables()

@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)

@pytest.fixture(scope="module")
def error_messages():
    from app.utils.csv import ERROR_MESSAGES
    return ERROR_MESSAGES
