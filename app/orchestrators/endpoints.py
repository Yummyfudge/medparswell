"""
orchestrators/endpoints.py

🔧 Purpose:
This module is reserved for coordinating backend service setup and teardown
(e.g., llama.cpp, spaCy) when endpoints are active independently of interfaces.

📦 Current Status:
No endpoint orchestration is needed yet. All backend logic is triggered via 
interface route handlers (e.g., through Swagger UI routes).

🚧 Future Use:
Once we support:
  - background jobs or scheduled tasks,
  - endpoint-only workflows (no interface),
  - shared endpoint logic across multiple interfaces (e.g., CLI + Swagger),
this module will manage those endpoints more explicitly.

🛑 Do not remove — this file is intentionally reserved.
"""

import importlib
from typing import Union
from types import ModuleType
from app.config.settings import settings
from app.config.logging_config import get_logger
from app.config.enums import EndpointType

def normalize_to_list(val: Union[str, list[str]]) -> list[str]:
    logger.debug(f"🧪 normalize_to_list() was started with value: {val!r}")
    if isinstance(val, str):
        result = [s.strip() for s in val.split(",") if s.strip()]
    else:
        result = val or []
    logger.debug(f"✅ normalize_to_list() completed with result: {result}")
    return result

logger = get_logger(__name__)
loaded_endpoints: dict[str, ModuleType] = {}

logger.debug(f"Active endpoints from settings: {settings.active_endpoints}")
logger.info("🛟 Looping over settings.active_endpoints to import schemas")
for endpoint_enum in settings.active_endpoints:
    endpoint_path = endpoint_enum.value
    try:
        module = importlib.import_module(f"app.endpoint_definitions.{endpoint_path}.schema")
        
        # Verify required attributes exist
        if not hasattr(module, "Schema") or not hasattr(module, "LLAMA_BACKEND_DEFAULTS"):
            logger.warning(f"⚠️ Endpoint '{endpoint_path}' missing required attributes.")

        loaded_endpoints[endpoint_path] = module
        logger.info(f"✅ Endpoint loaded: {endpoint_path}")
    except ModuleNotFoundError as e:
        logger.warning(f"⚠️ Failed to load endpoint '{endpoint_path}': {e}")
    except Exception as e:
        logger.error(f"🔥 Unexpected error loading endpoint '{endpoint_path}': {e}")

# Report summary of what was loaded
if loaded_endpoints:
    logger.info(f"🔌 Loaded {len(loaded_endpoints)} active endpoint(s).")
else:
    logger.warning("⚠️ No active endpoints found in settings — skipping backend route configuration.")

def get_loaded_endpoints() -> dict:
    """
    Return a dictionary of endpoint keys → loaded modules.
    Example: {'ik_llama.text_summarization': <module 'app.endpoint_definitions.ik_llama.text_summarization.schema'>}

    Note: settings.active_endpoints may be a string (comma-separated) or a list.
    """
    logger.info("🛟 get_loaded_endpoints() was started")
    return loaded_endpoints

def get_endpoint_metadata() -> dict:
    """
    Return a dictionary of endpoint metadata, including schema and defaults.
    Example:
    {
        'ik_llama.text_summarization': {
            'schema_class': 'TextSummarizationSchema',
            'defaults': { ... }
        }
    }
    """
    logger.info("🛟 get_endpoint_metadata() was started")
    metadata = {}
    for name, mod in loaded_endpoints.items():
        schema_cls = getattr(mod, "Schema", None)
        defaults = getattr(mod, "LLAMA_BACKEND_DEFAULTS", None)
        metadata[name] = {
            "schema_class": schema_cls.__name__ if schema_cls else None,
            "defaults": defaults,
        }
    return metadata


# TODO: Consider exposing get_endpoint_metadata() through a debug route or admin panel.


def get_active_endpoints() -> list[EndpointType]:
    """
    Return a validated list of EndpointType enums based on the ENABLED_ENDPOINTS in settings.
    Logs warnings for any unknown values.
    """
    logger.info("🛟 get_active_endpoints() was started")

    def _validate_endpoint(val: str) -> Union[EndpointType, None]:
        try:
            return EndpointType(val)
        except ValueError:
            logger.warning(f"⚠️ Unknown endpoint ignored in .env ENABLED_ENDPOINTS: {val!r}")
            return None

    raw_values = normalize_to_list(settings.active_endpoints)
    valid_endpoints = [
        endpoint for val in raw_values
        if (endpoint := _validate_endpoint(val)) is not None
    ]

    logger.info(f"✅ get_active_endpoints() completed — {len(valid_endpoints)} valid endpoint(s): {valid_endpoints}")
    return valid_endpoints



# --- Endpoint Backend Initialization ---

def initialize_endpoint_backend(endpoint_enum: EndpointType) -> None:
    """
    Prepare any required backend runtime environments for the given endpoint.
    This includes:
    - Model validation (e.g., file exists, format)
    - Optional loading steps (warmup, runner instantiation)
    - Metadata or capability registration

    Called at startup by the endpoint orchestrator.
    """
    logger.info(f"🛟 initialize_endpoint_backend() was started for: {endpoint_enum.value}")
    try:
        module = loaded_endpoints.get(endpoint_enum.value)
        if not module:
            logger.warning(f"🚫 Skipping initialization: endpoint '{endpoint_enum.value}' not in loaded_endpoints")
            return

        if hasattr(module, "initialize"):
            logger.debug(f"🔧 Calling 'initialize()' for endpoint: {endpoint_enum.value}")
            module.initialize()
        else:
            logger.info(f"ℹ️ No explicit initializer found for endpoint: {endpoint_enum.value}")

    except Exception as e:
        logger.error(f"💥 Failed to initialize backend for endpoint '{endpoint_enum.value}': {e}")


def initialize_all_endpoints() -> None:
    """
    Top-level initializer for all endpoints. Delegates to initialize_endpoint_backend().
    """
    logger.info("🛟 initialize_all_endpoints() was started")
    for endpoint_enum in get_active_endpoints():
        initialize_endpoint_backend(endpoint_enum)