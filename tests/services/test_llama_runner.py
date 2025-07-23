import pytest
from unittest.mock import patch, MagicMock
from app.services.llama_runner import run_llama_cli

@patch("app.services.llama_runner.subprocess.run")
def test_run_llama_cli_success(mock_run):
    # Arrange
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Paris"
    mock_result.stderr = ""
    mock_run.return_value = mock_result

    # Act
    result = run_llama_cli(prompt="What is the capital of France?", verbose=False)

    # Assert
    assert result == "Paris"
    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    assert "--prompt" in args[0]
    assert "France" in args[0]

@patch("app.services.llama_runner.subprocess.run")
def test_run_llama_cli_failure(mock_run):
    # Arrange
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Error occurred"
    mock_run.return_value = mock_result

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        run_llama_cli(prompt="What is the capital of France?", verbose=True)

    assert "Llama execution failed" in str(exc_info.value)