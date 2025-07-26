import subprocess
import shlex
from typing import Optional
from pathlib import Path
from app.config.settings import settings
from app.config.logging_config import logger

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

        logger.debug("Initialized LlamaRunner with config: "
                     f"binary_path={self.binary_path}, model_path={self.model_path}, "
                     f"gpu_layers={self.gpu_layers}, ctx_size={self.ctx_size}, "
                     f"main_gpu={self.main_gpu}, numa={self.numa}")

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
        logger.debug("run_prompt() called with prompt=%r, verbose=%s, dry_run=%s", prompt, verbose, dry_run)

        if not self.binary_path.is_file():
            logger.error("Llama binary not found at path: %s", self.binary_path)
            raise FileNotFoundError(f"Llama binary not found: {self.binary_path}")
        if not self.model_path.is_file():
            logger.error("Model file not found at path: %s", self.model_path)
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        logger.debug("Using binary path: %s", self.binary_path)
        logger.debug("Using model path: %s", self.model_path)
        logger.debug("Using context size: %s", self.ctx_size)
        logger.debug("Using GPU layers: %s", self.gpu_layers)
        logger.debug("Using main GPU: %s", self.main_gpu)
        logger.debug("Using NUMA setting: %s", self.numa)

        cmd = [
            str(self.binary_path),
            "-m", str(self.model_path),
            "--prompt", prompt,
            "--ctx-size", str(self.ctx_size),
            "--gpu-layers", str(self.gpu_layers),
            "--main-gpu", str(self.main_gpu),
            "--numa", self.numa,
        ]

        logger.debug("Built command: %s", " ".join(cmd))

        if verbose:
            logger.debug("Verbose mode enabled; adding --verbose flag to command.")
            cmd.append("--verbose")

        if dry_run:
            logger.debug("Dry run detected. Simulating execution.")
            logger.info("[DRY RUN] Command that would have been executed: %s", " ".join(shlex.quote(arg) for arg in cmd))
            logger.debug("Dry run enabled; skipping execution and returning placeholder output.")
            logger.info("Dry run complete. Returning simulated output.")
            return "[DRY RUN] Llama output placeholder."

        logger.info("Launching llama-cli subprocess...")
        logger.debug("Subprocess command arguments: %s", cmd)
        logger.debug("About to invoke subprocess with command.")

        try:
            logger.debug("⏳ Timeout set to %s seconds", settings.cli_timeout)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=settings.cli_timeout, check=True)
            logger.debug("Subprocess finished with return code: %d", result.returncode)
        except subprocess.CalledProcessError as e:
            logger.error("Llama CLI failed with return code %d", e.returncode)
            logger.error("Stdout:\n%s", e.stdout)
            logger.error("Stderr:\n%s", e.stderr)
            logger.debug("Exception raised: %s", str(e))
            raise RuntimeError(f"Llama execution failed:\n{e.stderr}")

        logger.info("Llama CLI executed successfully")
        logger.debug("Raw stdout:\n%s", result.stdout)
        logger.debug("Raw stderr:\n%s", result.stderr)
        logger.debug("Final output returned: %s", result.stdout.strip())
        logger.debug("Returning output from run_prompt method.")

        return result.stdout.strip()