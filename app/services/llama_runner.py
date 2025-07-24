import subprocess
import logging
import shlex
from typing import Optional
from pathlib import Path
from app.config.settings import settings

logger = logging.getLogger(__name__)

class LlamaRunner:
    """Handles execution of the llama-cli binary with a given prompt and configuration.

    Configuration is loaded from environment variables via `settings`:
        - llama_cli_path: Path to the llama-cli binary
        - model_path: Path to the model GGUF file
        - gpu_layers: Number of GPU layers to use
        - ctx_size: Context size (in tokens)
        - main_gpu: GPU device index
        - numa: NUMA binding mode
    """

    def __init__(self, binary_path: Optional[Path] = None):
        self.binary_path = Path(binary_path) if binary_path else Path(settings.llama_cli_path)
        self.model_path = Path(settings.model_path)
        self.gpu_layers = settings.gpu_layers
        self.ctx_size = settings.context_size
        self.main_gpu = settings.main_gpu
        self.numa = settings.numa

    def run_prompt(self, prompt: str, verbose: bool = False, dry_run: bool = False) -> str:
        """
        Executes llama-cli with the given prompt and configuration options.

        Args:
            prompt (str): The text prompt to send to the model.
            verbose (bool): If True, includes '--verbose' flag in command.
            dry_run (bool): If True, log the command and return a dummy string instead of executing.

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

        if dry_run:
            logger.info("[DRY RUN] Command: %s", " ".join(shlex.quote(arg) for arg in cmd))
            return "[DRY RUN] Llama output placeholder."

        logger.info("Executing llama-cli")
        logger.debug("Command: %s", " ".join(shlex.quote(arg) for arg in cmd))

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=True)
        except subprocess.CalledProcessError as e:
            logger.error("Llama CLI failed with return code %d", e.returncode)
            logger.error("Stdout:\n%s", e.stdout)
            logger.error("Stderr:\n%s", e.stderr)
            raise RuntimeError(f"Llama execution failed:\n{e.stderr}")

        logger.debug("Llama stdout: %s", result.stdout)
        logger.debug("Llama stderr: %s", result.stderr)

        return result.stdout.strip()