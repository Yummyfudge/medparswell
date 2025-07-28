
"""
enums.py

Centralized type-safe enumerations for interface and endpoint identifiers used in dynamic route construction.
This file defines which interfaces (e.g., Swagger UI, CLI) and endpoints (e.g., ik_llama, spaCy) are valid for use in the app.
These enums are used throughout the configuration system and orchestrators to validate .env inputs and control application behavior.
"""

from enum import Enum



# Enum of supported interface types used to expose routes (e.g., Swagger UI, Gradio)
class InterfaceType(str, Enum):
    """Supported interfaces that can expose endpoints.

    Used for validating interface identifiers and for generating dynamic routes.
    """
    SWAGGER_UI = "swagger_ui"
    GRADIO = "gradio"
    CLI = "cli"


# Enum of backend endpoint types the system can route requests to
class EndpointType(str, Enum):
    """Supported backend endpoints available for dynamic routing.

    Used for validating endpoint identifiers and for generating dynamic routes.
    """
    IK_LLAMA = "ik_llama"
    SPACY = "spacy"