"""
orchestrators/endpoints.py

🔧 Purpose:
This module is reserved for coordinating backend service setup and teardown
(e.g., llama.cpp, spaCy) when endpoints are enabled independently of interfaces.

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
from app.config.settings import settings
from app.config.logging_config import get_logger

logger = get_logger(__name__)
loaded_endpoints = {}

for endpoint_path in settings.enabled_endpoints:
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
    logger.info(f"🔌 Loaded {len(loaded_endpoints)} enabled endpoint(s).")
else:
    logger.warning("⚠️ No enabled endpoints found in settings — skipping backend route configuration.")

def get_loaded_endpoints() -> dict:
    """
    Return a dictionary of endpoint keys → loaded modules.
    Example: {'ik_llama.text_summarization': <module 'app.endpoint_definitions.ik_llama.text_summarization.schema'>}
    """
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