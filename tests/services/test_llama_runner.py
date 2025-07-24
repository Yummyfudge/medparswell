import os
from pathlib import Path
import pytest
from app.services.llama_runner import LlamaRunner

def test_run_llama_cli_success(set_fake_llama_cli_path):
    fake_binary = Path(__file__).parent.parent / "fakes" / "bin" / "llama-cli"
    runner = LlamaRunner(binary_path=fake_binary)
    result = runner.execute(prompt="What is the capital of France?", verbose=False)
    assert result == "Paris"

def test_run_llama_cli_failure(set_fake_llama_cli_path):
    fake_binary = Path(__file__).parent.parent / "fakes" / "bin" / "llama-cli"
    runner = LlamaRunner(binary_path=fake_binary)
    with pytest.raises(RuntimeError) as exc_info:
        runner.execute(prompt="What is the capital of France?", verbose=True)
    assert "Llama execution failed" in str(exc_info.value)