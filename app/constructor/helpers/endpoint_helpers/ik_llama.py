"""
Helpers for ik_llama endpoint route construction.

This module was split from the legacy main to isolate ik_llama-specific logic.
It is primarily used within the exploration branch to facilitate iterative development.

Each helper here is intended to be called by the main route factory, and
should abstract endpoint-specific logic away from the generic construction layer.
"""

# from app.endpoints.ik_llama.schema import text_summarization  # TODO: Replace legacy import path
# from app.endpoints.ik_llama.schema.backend_defaults import text_summarization_defaults  # TODO: Replace legacy import path
# from app.services.llama_runner import LlamaRunner  # TODO: Replace legacy import path

def get_text_summarization_config():
    """
    Returns all configuration necessary to construct the text_summarization route.

    This includes:
    - The request and response schema classes
    - The backend CLI defaults
    - Interface-specific presentation preferences

    Note:
    This function is part of a dynamically routed endpoint system.
    """
    return {
        "schema_cls": text_summarization.SummarizeRequest,
        "response_cls": text_summarization.SummarizeResponse,
        "backend_defaults": text_summarization_defaults,
    }