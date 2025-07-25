from fastapi import APIRouter
"""
interface_helpers.swagger_ui.py

Helpers to modify route schemas and metadata for compatibility with Swagger UI
and OpenAPI visual tooling within the interface_helpers module. This includes
field visibility toggles, example injection, and alias remapping to improve
documentation and interactive behavior.
"""


from typing import Dict, Any
from pydantic import BaseModel, Field

# Interface preferences for Swagger route construction
SWAGGER_UI_PREFS = {
    "expose_all_fields": True,
    "collapse_advanced": True,
    "field_overrides": {
        "verbose": {"default": False, "visible": True, "example": False},
        "gpu_layers": {"visible": False},
        "ctx_size": {"visible": False},
        "main_gpu": {"visible": False},
        "numa": {"visible": False},
    },
}

def apply_swagger_overrides(schema: BaseModel, overrides: Dict[str, Dict[str, Any]]) -> BaseModel:
    """
    Apply Swagger-specific field visibility and customization rules to a Pydantic schema.

    Args:
        schema (BaseModel): The original Pydantic model.
        overrides (Dict[str, Dict[str, Any]]): A mapping of field names to override definitions.

    Returns:
        BaseModel: A modified schema with Swagger-visible field metadata patched in.
    """
    updated_fields = {}

    for field_name, model_field in schema.model_fields.items():
        override = overrides.get(field_name, {})
        if override.get("visible", True):
            extra = model_field.json_schema_extra or {}
            if "example" in override:
                extra["example"] = override["example"]
            updated_fields[field_name] = (model_field.annotation, Field(
                default=(model_field.default if not model_field.is_required() else ...),
                description=model_field.description,
                json_schema_extra=extra,
                alias=override.get("alias", model_field.alias),
            ))
        else:
            # TODO: Consider logging dropped fields for debugging or auditing
            pass

    return type(f"{schema.__name__}SwaggerView", (BaseModel,), updated_fields)

def get_interface_preferences() -> Dict[str, Any]:
    """
    Return the Swagger-specific interface preferences dict.

    This allows the route_factory to retrieve interface config without tightly coupling
    to the config module path or name.

    Returns:
        Dict[str, Any]: Swagger UI interface preference dictionary
    """
    return SWAGGER_UI_PREFS