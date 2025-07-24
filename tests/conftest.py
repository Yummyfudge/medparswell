import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Use the FastAPI test client
@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# Override the llama-cli path for tests
@pytest.fixture(autouse=True, scope="function")
def set_fake_llama_cli_path(monkeypatch):
    fake_path = os.path.abspath("tests/fakes/bin/llama-cli")
    monkeypatch.setenv("LLAMA_CLI_PATH", fake_path)