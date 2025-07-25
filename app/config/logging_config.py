import logging
import logging.config
from pathlib import Path
from typing import Literal

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "app.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logging(level: str = LOG_LEVEL) -> None:
    """
    Configures the Python logging system for the application.

    Args:
        level (str): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', etc.)
    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": str(LOG_FILE),
                "level": level,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": level,
        },
    }

    logging.config.dictConfig(logging_config)

def configure_logging(level: str = LOG_LEVEL) -> None:
    """
    Sets up the logging system (alias to setup_logging for semantic clarity).
    This function is intended to be imported by other modules.
    """
    setup_logging(level)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with the specified name.
    Automatically sets up logging if not already initialized.
    """
    setup_logging()
    return logging.getLogger(name)

logger = get_logger("medparswell")