"""
Route factory module that constructs FastAPI routes using schema definitions,
backend configuration defaults, and interface preferences for any interface
(not just Swagger UI). The factory supports composition from schema, backend,
and interface configs for any interface.
"""

# TODO: "text_summarization" is hardcoded in multiple places — refactor to support dynamic route composition

import logging
from app.constructor.helpers.interface_helpers.fastapi_ui import (
    get_interface_prefs,
    apply_interface_overrides,
    get_api_router
)
from app.constructor.helpers.endpoint_helpers.ik_llama import (
    get_schema_and_defaults,
    build_prompt_args_from_payload,
    get_llama_runner
)

logger = logging.getLogger("medparswell.route_factory")

def _get_annotated_request_model():
    schema_cls, backend_defaults = get_schema_and_defaults("text_summarization")
    interface_prefs = get_interface_prefs()
    return apply_interface_overrides(
        model=schema_cls,
        backend_defaults=backend_defaults,
        interface_prefs=interface_prefs
    )

def build_text_summarization_route():
    # --------------------------------------------------------------------------
    # Route gating must happen in the orchestrator layer, not here.
    # This factory **must not** check enabled_endpoints, global settings, or .env
    # values directly. The orchestrator is responsible for determining if a route
    # such as "ik_llama.text_summarization" should be enabled, and only then
    # should it call this function to construct the route.
    #
    # Rationale:
    #   • Clean separation of concerns
    #   • Testability of this route in isolation
    #   • Support for alternative orchestration (e.g. CLI-only apps, batch runners)
    # --------------------------------------------------------------------------

    logger.info("Constructing FastAPI route for ik_llama.text_summarization endpoint")

    router = get_api_router()

    schema_cls, _ = get_schema_and_defaults("text_summarization")
    response_cls = schema_cls.get_response_model()
    request_model = _get_annotated_request_model()

    logger.debug("route_factory: Beginning construction of POST /summarize route for text_summarization")

    @router.post("/summarize", response_model=response_cls)
    def summarize_endpoint(payload: request_model):
        runner = get_llama_runner()
        prompt_args = build_prompt_args_from_payload(payload)
        result = runner.run_prompt(
            **prompt_args,
            dry_run=False
        )
        logger.debug("Generated summary: %s", result)
        return {"summary": result}

    logger.debug("route_factory: Route registered: POST /summarize with %s", request_model.__name__)
    return router