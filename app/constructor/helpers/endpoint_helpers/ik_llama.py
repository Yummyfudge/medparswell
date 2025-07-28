"""
Helpers for ik_llama endpoint route construction.

This module defines the schema accessors and payload transformations
for the text_summarization endpoint used in dynamic route generation.

It includes:
- Schema exposure for request/response typing
- Backend-specific defaults
- FastAPI interface-aware prompt argument builder
- Lazy instantiation of the LlamaRunner

This module is consumed by the dynamic route_factory and supports
interface-specific overrides injected at construction time.
"""

from typing import Any, Dict, Type, Annotated
from pydantic import BaseModel, Field, create_model

from app.endpoint_definitions.ik_llama.schema import text_summarization
from app.endpoint_definitions.ik_llama.schema.backend_defaults import TEXT_SUMMARIZATION_DEFAULTS
from app.runner_modules.llama_runner import LlamaRunner

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
        "backend_defaults": TEXT_SUMMARIZATION_DEFAULTS,
    }

def get_schema_and_defaults():
    """
    Adapter for route_factory compatibility.

    Returns a tuple of (schema_cls, response_cls),
    adapted from get_text_summarization_config(), for use in route factory dynamic import.
    """
    config = get_text_summarization_config()
    return config["schema_cls"], config["response_cls"]

def build_prompt_args_from_payload(payload):
    """
    Extracts and returns the prompt-related arguments from the request payload.

    This function is expected by the route factory and must return a dictionary
    compatible with LlamaRunner.run_prompt().
    """
    return {
        "prompt": payload.content,
        "language": payload.language,
        "verbose": getattr(payload, "verbose", False),
        "dry_run": getattr(payload, "dry_run", False),
    }

def get_llama_runner():
    """
    Returns an instance of LlamaRunner.
    """
    return LlamaRunner()

def apply_fastapi_ui_overrides(
    schema: Type[BaseModel],
    overrides: Dict[str, Any]
) -> Type[BaseModel]:
    """
    Applies FastAPI interface-specific visibility and field presentation overrides
    to a request schema. Returns a dynamically generated subclass of the schema
    with fields filtered or updated based on interface preferences.

    This version is fully compatible with Pydantic v3.
    """
    updated_fields = {}

    for field_name, model_field in schema.model_fields.items():
        override = overrides.get(field_name, {})
        if not override.get("visible", True):
            continue

        extra = dict(model_field.json_schema_extra or {})
        if "example" in override:
            extra["example"] = override["example"]

        default = (
            model_field.default if model_field.default is not None else ...
        )

        updated_fields[field_name] = Annotated[
            model_field.annotation,
            Field(
                default=default,
                description=model_field.description,
                alias=override.get("alias", model_field.alias),
                json_schema_extra=extra,
            )
        ]

    return create_model(
        f"{schema.__name__}FastAPIUIRoute",
        __base__=schema,
        **updated_fields
    )