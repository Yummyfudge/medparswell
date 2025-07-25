import logging
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from app.config.logging_config import configure_logging

load_dotenv()

class LlamaSettings(BaseSettings):
    """Configuration settings for the llama-cli application."""
    llama_cli_path: str = Field(
        ...,
        description="Path to llama-cli binary",
        json_schema_extra={
            "example": "/usr/local/bin/llama-cli",
            "env_override": "Set LLAMA_CLI_PATH in your .env file to override"
        }
    )
    model_path: str = Field(
        ...,
        description="Path to .gguf model file",
        json_schema_extra={
            "example": "/models/DeepSeek-R1-0528-IQ1_S_R4-00001-of-00003.gguf",
            "env_override": "Set LLAMA_MODEL_PATH in your .env file to override"
        }
    )
    context_size: int = Field(
        default=2048,
        description="Context window size",
        json_schema_extra={
            "example": 2048,
            "env_override": "Set LLAMA_CONTEXT_SIZE in your .env file to override"
        }
    )
    gpu_layers: int = Field(
        default=2,
        description="Number of GPU layers to offload",
        json_schema_extra={
            "example": 2,
            "env_override": "Set LLAMA_GPU_LAYERS in your .env file to override"
        }
    )
    main_gpu: int = Field(
        default=0,
        description="Primary GPU index to use",
        json_schema_extra={
            "example": 0,
            "env_override": "Set LLAMA_MAIN_GPU in your .env file to override"
        }
    )
    numa: str = Field(
        default="isolate",
        description="NUMA configuration strategy",
        json_schema_extra={
            "example": "isolate",
            "env_override": "Set LLAMA_NUMA in your .env file to override"
        }
    )
    verbose: bool = Field(
        default=True,
        json_schema_extra={
            "description": "Enable verbose logging",
            "example": True,
            "env_override": "Set LLAMA_VERBOSE in your .env file to override"
        }
    )
    cli_timeout: int = Field(
        default=60,
        description="Timeout in seconds for llama-cli execution",
        json_schema_extra={
            "example": 180,
            "env_override": "Set LLAMA_CLI_TIMEOUT in your .env file to override"
        }
    )
    log_level: str = Field(
        default="INFO",
        json_schema_extra={
            "description": "Logging level (e.g. DEBUG, INFO, WARNING)",
            "example": "DEBUG",
            "env_override": "Set LLAMA_LOG_LEVEL in your .env file to override"
        }
    )
    log_file: str = Field(
        default="logs/medparswell.log",
        json_schema_extra={
            "description": "Path to the log file",
            "example": "logs/medparswell.log",
            "env_override": "Set LLAMA_LOG_FILE in your .env file to override"
        }
    )

    model_config = ConfigDict(env_prefix="LLAMA_", env_file=".env", env_file_encoding="utf-8")

    def get_logging_level(self):
        return getattr(logging, self.log_level.upper(), logging.INFO)

# Singleton-like instance used globally for configuration
settings = LlamaSettings()
configure_logging(settings.log_level, settings.log_file)
logging.info(f"🔧 Settings initialized: llama_cli_path={settings.llama_cli_path}, model_path={settings.model_path}")
logging.debug(f"🛠 Logging configured — level: {settings.log_level}, output: {settings.log_file}")