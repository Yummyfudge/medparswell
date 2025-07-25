from typing import Dict, Any

"""
📘 Swagger UI Field Customization for OpenAPI Consumers

This configuration file defines how Swagger UI (an OpenAPI specification consumer)
should render fields associated with each exposed API route.

🧠 Context:
- OpenAPI is a standard for describing RESTful APIs.
- Swagger UI is a frontend tool that reads OpenAPI specs and displays an interactive API browser.

🎯 Purpose:
- Control visibility, defaults, and display behavior of fields within Swagger UI.
- Hide backend-specific or deprecated fields from end users.
- Provide documentation-friendly overrides for select fields.

🔄 This is one of several consumer configs. Others may include:
    - CLI preferences (e.g., verbosity, dry-run)
    - Gradio UI behavior

See also: `backend_defaults.py` and `text_summarization.py` under `app/endpoints/ik_llama/`.
"""
# Configuration for how Swagger UI should render endpoint fields

SWAGGER_UI_PREFS: Dict[str, Any] = {
    "expose_all_fields": True,  # Show all documented fields, including optional ones
    "collapse_advanced": True,  # Collapse advanced sections (like debug or developer-only fields)
    "field_overrides": {
        "verbose": {
            "default": False,
            "visible": True,
            "description": "Enable detailed logging output for debugging.",
        },
        "gpu_layers": {
            "visible": False,  # Hide from UI entirely, set via backend default or advanced config
        },
        "ctx_size": {
            "visible": False,  # Deprecated field, still accepted by backend, but hidden from UI
        },
        "model_path": {
            "visible": False,  # Too backend-specific; not user-adjustable in Swagger
        },
        "max_tokens": {
            "default": 128,
            "visible": True,
            "description": "Maximum tokens to generate in the summary.",
        },
    },
}