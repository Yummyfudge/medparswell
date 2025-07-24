from typing import Any, Dict

"""
Registry for UI- and API-facing components.
Supports Gradio, FastAPI, CLI tools, and future introspection tooling.
"""
component_registry: Dict[str, Any] = {}

def register_component(name_component_tuple: tuple[str, Any]) -> Any:
    """
    Stores a component in the global registry for introspection and testing.
    This wrapper allows compatibility with Gradio layout constructs like:
        with gr.Row() as register_component(("row-name", gr.Row(...))):
    """
    name, component = name_component_tuple
    component_registry[name] = component
    return component