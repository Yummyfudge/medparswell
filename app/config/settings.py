"""
settings.py — Application configuration and environment loader.

This module defines the AppSettings class that loads environment variables from
.env and provides structured, validated access to configuration values throughout
the application.

Specifically, this file:
- Loads raw .env fields such as ENABLED_INTERFACES and ENABLED_ENDPOINTS as strings
- Parses them into internal Enums (InterfaceType and EndpointType) using validation logic
- Provides clean access to downstream logic through .active_interfaces and .active_endpoints
"""
import logging
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, model_validator
from app.config.enums import InterfaceType, EndpointType
logger = logging.getLogger(__name__)
from app.config.logging_config import configure_logging

load_dotenv()

class AppSettings(BaseSettings):
    """
    Enum-backed configuration:
    - ENABLED_ENDPOINTS and ENABLED_INTERFACES are treated as comma-separated strings in the .env
    - These are parsed and mapped to Enums (EndpointType, InterfaceType) via properties
    - This ensures the .env remains user-friendly, while the app uses strongly typed internal values
    - Invalid entries are logged (but ignored) to ensure clarity without halting startup
    """
    """Configuration settings for the application."""
    host: str = Field(
        default="127.0.0.1",
        json_schema_extra={
            "description": "Host IP for FastAPI server",
            "example": "127.0.0.1",
            "env_override": "Set LLAMA_HOST in your .env file to override"
        }
    )
    port: int = Field(
        default=8000,
        json_schema_extra={
            "description": "Port number for FastAPI server",
            "example": 8000,
            "env_override": "Set LLAMA_PORT in your .env file to override"
        }
    )
    reload: bool = Field(
        default=False,
        description="Enable FastAPI auto-reload for development",
        json_schema_extra={
            "example": False,
            "env_override": "Set RELOAD in your .env file to enable auto-reload (True/False)"
        }
    )
    app_log_level: str = Field(
        default="INFO",
        json_schema_extra={
            "description": "Logging level (e.g. DEBUG, INFO, WARNING)",
            "example": "DEBUG",
            "env_override": "Set APP_LOG_LEVEL in your .env file to override"
        }
    )
    app_log_file: str = Field(
        default="logs/medparswell.log",
        json_schema_extra={
            "description": "Path to the log file",
            "example": "logs/medparswell.log",
            "env_override": "Set APP_LOG_FILE in your .env file to override"
        }
    )

    # Raw comma-separated strings from the .env file
    # These are user-facing values and parsed into internal Enums below
    active_endpoints_raw: str = Field(
        default="",
        description="Comma-separated list of backend endpoints to enable",
        json_schema_extra={
            "example": "ik_llama.text_summarization",
            "env_override": "Set ENABLED_ENDPOINTS in your .env file"
        }
    )
    # Raw comma-separated strings from the .env file
    # These are user-facing values and parsed into internal Enums below
    active_interfaces_raw: str = Field(
        default="",
        description="Comma-separated list of interface types to enable",
        json_schema_extra={
            "example": "swagger_ui",
            "env_override": "Set ENABLED_INTERFACES in your .env file"
        }
    )

    cli_path: str = Field(..., description="Path to the LLaMA CLI binary")
    model_path: str = Field(..., description="Path to the GGUF model file")
    context_size: int = Field(default=2048, description="LLaMA context window size")
    gpu_layers: int = Field(default=2, description="Number of layers to offload to GPU")
    main_gpu: int = Field(default=0, description="GPU device ID for primary execution")
    numa: str = Field(default="isolate", description="NUMA binding strategy")
    verbose: bool = Field(default=False, description="Enable verbose output from llama")
    cli_timeout: int = Field(default=360, description="Timeout (in seconds) for CLI calls")

    @model_validator(mode="before")
    @classmethod
    def validate_raw_env_fields(cls, values):
        """
        Preprocess .env fields that are expected as raw strings but might be passed as structured inputs.
        This prevents validation errors from misparsed environment data.
        """
        if "active_endpoints" in values and "active_endpoints_raw" not in values:
            values["active_endpoints_raw"] = values.pop("active_endpoints")
        if "active_interfaces" in values and "active_interfaces_raw" not in values:
            values["active_interfaces_raw"] = values.pop("active_interfaces")
        return values


    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def active_endpoints(self) -> list[EndpointType]:
        return self._parse_enum_list(self.active_endpoints_raw, EndpointType, "ENABLED_ENDPOINTS")

    @property
    def active_interfaces(self) -> list[InterfaceType]:
        return self._parse_enum_list(self.active_interfaces_raw, InterfaceType, "ENABLED_INTERFACES")

    def _parse_enum_list(self, raw: str, enum_cls, env_name: str) -> list:
        results = []
        for val in (v.strip() for v in raw.split(",") if v.strip()):
            try:
                results.append(enum_cls(val))
            except ValueError:
                logger.warning(f"⚠️ Unknown entry '{val}' in .env field {env_name} — skipping")
        return results

    def get_logging_level(self):
        return getattr(logging, self.app_log_level.upper(), logging.INFO)

# Singleton-like instance used globally for configuration
settings = AppSettings()
configure_logging(settings.app_log_level, settings.app_log_file)
logging.debug(f"🛠 Logging configured — level: {settings.app_log_level}, output: {settings.app_log_file}")