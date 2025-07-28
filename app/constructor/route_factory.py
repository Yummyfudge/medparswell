"""
Route factory module that constructs FastAPI routes using schema definitions,
backend configuration defaults, and interface preferences for any interface
(not just Swagger UI). The factory supports composition from schema, backend,
and interface configs for any interface.
"""

# This route factory is driven by exploration_main.py using a push-based pattern.
# The orchestrator provides one interface and one endpoint at a time.
# The factory assembles schema, backend config, and interface preferences to build an APIRouter.
# Currently supports only InterfaceType.FASTAPI_UI.

# Add missing import for APIRouter
from fastapi import APIRouter, Body, HTTPException

from app.orchestrators.endpoints import get_active_endpoints, get_endpoint_metadata
# TODO: "text_summarization" is hardcoded in multiple places — refactor to support dynamic route composition

import logging
from app.constructor.helpers.interface_helpers.fastapi_ui import (
    get_interface_prefs,
    apply_fastapi_ui_overrides,
    get_fastapi_router
)

import importlib

def get_endpoint_helpers(endpoint_name: str):
    module = importlib.import_module(f"app.constructor.helpers.endpoint_helpers.{endpoint_name}")
    return {
        "get_schema_and_defaults": getattr(module, "get_schema_and_defaults"),
        "build_prompt_args_from_payload": getattr(module, "build_prompt_args_from_payload"),
        "get_llama_runner": getattr(module, "get_llama_runner"),
    }

logger = logging.getLogger("medparswell.route_factory")

from typing import Type, Callable, Any
from pydantic import BaseModel


def build_route_from_components(
    *,
    route_path: str,
    request_model: Type[BaseModel],
    response_model: Type[BaseModel],
    runner_callable: Callable[[dict], str]
) -> APIRouter:
    """
    Generic route builder. Accepts schema components and a callable runner.
    This decouples the constructor from backend-specific logic like `get_llama_runner`.
    """
    import json
    logger.debug("🔬 request_model JSON schema:\n%s", json.dumps(request_model.model_json_schema(), indent=2))
    logger.info("Constructing FastAPI route at path: %s", route_path)

    # Interface-specific router is now injected from helper, not defined locally
    from app.constructor.helpers.interface_helpers.fastapi_ui import get_fastapi_router
    router = get_fastapi_router()

    @router.post(route_path, response_model=response_model)
    def generated_endpoint(payload: request_model = Body(...)):
        prompt_args = payload.model_dump()
        try:
            result = runner_callable.run_prompt(**prompt_args)
            logger.debug("Generated summary: %s", result)
            return {
                "summary": result.get("output"),
                "success": result.get("status") == "success",
                "duration_ms": result.get("duration_ms"),
            }
        except Exception as e:
            logger.exception("❌ Internal error while processing payload: %s", prompt_args, exc_info=e)
            raise

    logger.debug("🔧 FastAPI endpoint will receive: %s", request_model.__annotations__)

    logger.debug("route_factory: Route registered: POST %s with %s", route_path, request_model.__name__)
    return router
from app.config.enums import InterfaceType, EndpointType

def get_route_components(endpoint: EndpointType):
    """
    Retrieves the full set of components required to build a route for the given endpoint.

    This includes:
    - schema_class
    - response_model
    - runner_callable
    - route_path
    """
    from app.constructor.helpers.endpoint_helpers import ik_llama  # NOTE: eventually dynamically resolve

    return {
        "schema_class": ik_llama.get_schema_and_defaults()[0],
        "response_model": ik_llama.get_schema_and_defaults()[1],
        "runner_callable": ik_llama.get_llama_runner(),
        "route_path": getattr(ik_llama, "get_route_path", lambda: f"/{endpoint.value}")()
    }


def build_route_for_interface(
    *,
    endpoint: EndpointType,
    interface: InterfaceType
) -> APIRouter | None:
    """
    Construct a single route for a given interface and endpoint.
    This version assumes push-style logic from the orchestrator.
    """
    logger.debug("🚦 build_route_for_interface() started for interface: %s and endpoint: %s", interface, endpoint)

    try:
        components = get_route_components(endpoint)
    except Exception as e:
        logger.exception("❌ Failed to retrieve route components for endpoint: %s", endpoint.value)
        return None

    schema_class = components["schema_class"]
    response_model = components["response_model"]
    runner_callable = components["runner_callable"]
    route_path = components["route_path"]

    # Interface-specific logic (only FASTAPI_UI supported for now)
    if interface == InterfaceType.SWAGGER_UI:
        interface_prefs = get_interface_prefs()
        request_model = apply_fastapi_ui_overrides(schema_class, interface_prefs)
    else:
        logger.warning("⚠️ Interface %s is not yet supported", interface)
        return None

    router = build_route_from_components(
        route_path=route_path,
        request_model=request_model,
        response_model=response_model,
        runner_callable=runner_callable
    )

    return router