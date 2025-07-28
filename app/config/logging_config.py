 # =============================================================================
 # This logging config is reused by the exploration branch (dynamic route prototype).
 # If multiple entrypoints use this file, split logs via distinct filenames or logger names.
 # =============================================================================
import logging
import logging.config
from pathlib import Path
from typing import Literal
import os

LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = os.getenv("APP_LOG_LEVEL", "INFO")
LOG_FILE = Path(os.getenv("APP_LOG_FILE", Path(__file__).resolve().parent.parent.parent / "logs" / "exploration_main.log"))
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(exc_info)s"

def setup_logging(level: str = LOG_LEVEL, log_file: Path = LOG_FILE) -> None:
    """
    Configures the Python logging system for the application.

    Args:
        level (str): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', etc.)
        log_file (Path): Path to the log file.
    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            },
        },
        # Note: traceback logging via logger.exception(...) will automatically include exc_info
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": str(log_file),
                "level": level,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": level,
            "propagate": True,
        },
    }

    logging.config.dictConfig(logging_config)

def configure_logging(level: str = LOG_LEVEL, log_file: Path = LOG_FILE) -> None:
    """
    Sets up the logging system (alias to setup_logging for semantic clarity).
    This function is intended to be imported by other modules.
    """
    setup_logging(level, log_file)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with the specified name.
    Assumes logging has already been configured via setup_logging() or configure_logging().
    """
    return logging.getLogger(name)

logger = get_logger("medparswell")