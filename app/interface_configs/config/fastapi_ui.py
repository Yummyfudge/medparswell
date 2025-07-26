from typing import Dict, Any

"""
📘 Swagger UI Field Customization for OpenAPI Consumers

This configuration file defines how Swagger UI (an OpenAPI-compatible consumer)
should render fields exposed via FastAPI routes.

🔄 This config is now wired into the new dynamic routing system introduced in `exploration_main.py`.
It is activated via `.env` using:
    ENABLED_INTERFACES=swagger_ui

🎯 Purpose:
- Control visibility, default values, and display hints for fields shown in Swagger UI.
- Override or suppress fields like internal settings, deprecated flags, or debug toggles.
- Coordinate with dynamic route generation powered by:
    - `app/constructor/helpers/interface_helpers/swagger_ui.py`
    - `app/orchestrators/interfaces.py`

🧠 Reminder:
- This config does not affect CLI or Gradio routes.
- It also does not launch the FastAPI app itself — see `fastapi_runner.py` for that logic.
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