from pydantic import BaseSettings, Field
import logging


class LlamaSettings(BaseSettings):
    llama_cli_path: str = Field(..., description="Path to llama-cli binary")
    model_path: str = Field(..., description="Path to .gguf model file")
    context_size: int = Field(default=2048, description="Context window size")
    gpu_layers: int = Field(default=2, description="Number of GPU layers to offload")
    main_gpu: int = Field(default=0, description="Primary GPU index to use")
    numa: str = Field(default="isolate", description="NUMA configuration strategy")
    verbose: bool = Field(default=True, description="Enable verbose logging")
    log_level: str = Field(default="INFO", description="Logging level (e.g. DEBUG, INFO, WARNING)")

    def get_logging_level(self):
        return getattr(logging, self.log_level.upper(), logging.INFO)

    class Config:
        env_prefix = "LLAMA_"
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = LlamaSettings()