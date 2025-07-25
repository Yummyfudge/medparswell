import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Use the FastAPI test client
@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# Override the llama-cli path with a mock script for tests
@pytest.fixture(autouse=True, scope="function")
def set_fake_llama_cli_path(monkeypatch):
    mock_path = os.path.abspath("tests/mocks/llama_cpp/fake_llama_cli.sh")
    monkeypatch.setenv("LLAMA_CLI_PATH", mock_path)