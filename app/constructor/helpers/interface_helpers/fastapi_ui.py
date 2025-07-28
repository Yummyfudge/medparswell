from fastapi import APIRouter, Body
"""
interface_helpers.fastapi_ui.py

Helpers to modify route schemas and metadata for compatibility with FastAPI UI
and OpenAPI visual tooling within the interface_helpers module. This includes
field visibility toggles, example injection, and alias remapping to improve
documentation and interactive behavior.

Refactor-aware usage: Use `get_fastapi_ready_schema(schema)` to apply internal
preferences for FastAPI UI route schemas, or call `apply_fastapi_ui_overrides`
directly with custom overrides if needed.

Note: This module is aligned with Pydantic v3 standards exclusively.
"""


from typing import Dict, Any, Annotated, Type
from pydantic import BaseModel, Field, create_model
from app.interface_configs.config.fastapi_ui import FASTAPI_UI_PREFS


def apply_fastapi_ui_overrides(schema: BaseModel, overrides: Dict[str, Dict[str, Any]]) -> Type[BaseModel]:
    """
    Apply FastAPI UI-specific field visibility and customization rules to a Pydantic schema.

    Args:
        schema (BaseModel): The original Pydantic model.
        overrides (Dict[str, Dict[str, Any]]): A mapping of field names to override definitions.

    Returns:
        BaseModel: A modified schema with FastAPI UI-visible field metadata patched in.
    """
    updated_fields = {}

    for field_name, model_field in schema.model_fields.items():
        override = overrides.get(field_name, {})
        if not override.get("visible", True):
            continue

        extra = dict(model_field.json_schema_extra or {})
        if "example" in override:
            extra["example"] = override["example"]

        default = model_field.default if model_field.default is not None else ...

        annotated_type = Annotated[
            model_field.annotation,
            Field(
                description=model_field.description,
                alias=override.get("alias", model_field.alias or field_name),
                json_schema_extra=extra,
            )
        ]
        updated_fields[field_name] = (
            annotated_type,
            Body(default=default, embed=True),
        )

    from app.utils.logging_utils import get_logger
    logger = get_logger("medparswell.fastapi_ui")
    logger.debug(f"🧪 Final model fields for {schema.__name__}: {list(updated_fields.keys())}")

    return create_model(
        f"{schema.__name__}FastAPIUIRoute",
        __base__=schema,
        **updated_fields
    )


def get_fastapi_ui_preferences() -> Dict[str, Any]:
    """
    Return the preference dictionary used during dynamic route construction for FastAPI-compatible UI behavior.
    This is invoked by the route_factory during interface registration.

    This allows the route_factory to retrieve interface config without tightly coupling
    to the config module path or name.

    Returns:
        Dict[str, Any]: FastAPI UI interface preference dictionary
    """
    return FASTAPI_UI_PREFS


def get_fastapi_ready_schema(schema: BaseModel) -> BaseModel:
    """
    Convenience wrapper to apply FastAPI UI field overrides using internal preferences.

    Args:
        schema (BaseModel): The original Pydantic model.

    Returns:
        BaseModel: A modified schema with FastAPI UI-visible field metadata patched in,
            using internal interface preferences.
    """
    prefs = get_fastapi_ui_preferences()
    overrides = prefs.get("field_overrides", {})
    return apply_fastapi_ui_overrides(schema, overrides)


def get_interface_prefs() -> dict:
    """
    Expose FastAPI UI preferences for the route factory to consume,
    matching the naming convention used by other interface helpers.
    """
    return FASTAPI_UI_PREFS


def get_fastapi_router() -> APIRouter:
    """
    Provides a new FastAPI APIRouter instance for dynamic route registration.

    Returns:
        APIRouter: A fresh APIRouter instance scoped for FastAPI UI routes.
    """
    return APIRouter()