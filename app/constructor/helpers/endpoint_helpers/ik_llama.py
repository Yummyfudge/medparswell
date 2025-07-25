"""
Helpers for ik_llama endpoint route construction.

This module contains utility functions that assist in translating
ik_llama-specific schema values and runtime behaviors into executable
FastAPI-compatible route handlers.

Each helper here is intended to be called by the main route factory, and
should abstract endpoint-specific logic away from the generic construction layer.
"""

from app.endpoints.ik_llama.schema import text_summarization
from app.endpoints.ik_llama.schema.backend_defaults import text_summarization_defaults
from app.services.llama_runner import LlamaRunner

def get_text_summarization_config():
    """
    Returns all configuration necessary to construct the text_summarization route.

    This includes:
    - The request and response schema classes
    - The backend CLI defaults
    - Interface-specific presentation preferences
    """
    return {
        "schema_cls": text_summarization.SummarizeRequest,
        "response_cls": text_summarization.SummarizeResponse,
        "backend_defaults": text_summarization_defaults,
    }