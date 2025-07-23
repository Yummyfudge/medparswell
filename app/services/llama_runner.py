import subprocess
import logging
import shlex
from typing import Optional
from pathlib import Path
from app.config.settings import settings

logger = logging.getLogger(__name__)

class LlamaRunner:
    """Handles execution of the llama-cli binary with a given prompt and configuration."""

    def __init__(self):
        self.binary_path = Path(settings.llama_cli_path)
        self.model_path = Path(settings.model_path)
        self.gpu_layers = settings.gpu_layers
        self.ctx_size = settings.ctx_size
        self.main_gpu = settings.main_gpu
        self.numa = settings.numa

    def run_prompt(self, prompt: str, verbose: bool = False) -> str:
        """
        Executes llama-cli with the given prompt and configuration options.

        Args:
            prompt (str): The text prompt to send to the model.
            verbose (bool): If True, includes '--verbose' flag in command.

        Returns:
            str: The model's generated output as a single string.

        Raises:
            FileNotFoundError: If llama binary or model file is missing.
            RuntimeError: If the llama-cli command fails.
        """
        if not self.binary_path.is_file():
            raise FileNotFoundError(f"Llama binary not found: {self.binary_path}")
        if not self.model_path.is_file():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        cmd = [
            str(self.binary_path),
            "-m", str(self.model_path),
            "--prompt", prompt,
            "--ctx-size", str(self.ctx_size),
            "--gpu-layers", str(self.gpu_layers),
            "--main-gpu", str(self.main_gpu),
            "--numa", self.numa,
        ]

        if verbose:
            cmd.append("--verbose")

        logger.info("Executing llama-cli")
        logger.debug("Command: %s", " ".join(shlex.quote(arg) for arg in cmd))

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        logger.debug("Llama stdout: %s", result.stdout)
        logger.debug("Llama stderr: %s", result.stderr)

        if result.returncode != 0:
            logger.error("Llama execution failed with code %d", result.returncode)
            logger.error("Partial stdout:\n%s", result.stdout)
            logger.error("Stderr output:\n%s", result.stderr)
            raise RuntimeError(f"Llama execution failed:\n{result.stderr}")

        return result.stdout.strip()