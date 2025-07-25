import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from pathlib import Path
import pytest
from app.services.llama_runner import LlamaRunner

from unittest.mock import patch, MagicMock
from subprocess import CompletedProcess

def test_run_llama_cli_success():
    fake_binary = Path("/fake/path/to/llama-cli")
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("subprocess.run") as mock_run:
            mock_result = CompletedProcess(args=[], returncode=0, stdout="Paris", stderr="")
            mock_run.return_value = mock_result
            runner = LlamaRunner(binary_path=fake_binary)
            result = runner.run_prompt(prompt="What is the capital of France?", verbose=False)
            assert result == "Paris"

def test_run_llama_cli_failure():
    fake_binary = Path("/fake/path/to/llama-cli")
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = RuntimeError("Llama execution failed")
            runner = LlamaRunner(binary_path=fake_binary)
            with pytest.raises(RuntimeError) as exc_info:
                runner.run_prompt(prompt="What is the capital of France?", verbose=True)
            assert "Llama execution failed" in str(exc_info.value)