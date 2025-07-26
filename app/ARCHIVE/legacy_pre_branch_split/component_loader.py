from pydantic import Field
from typing import Any

def create_component(component_type: str, **kwargs) -> Any:
    """
    Create a structured Field using Pydantic, ensuring 'description' is present.
    This supports automatic schema and metadata generation (e.g. for FastAPI or Gradio).

    Args:
        component_type (str): The logical type (e.g., 'string', 'number'), not directly used but useful for documentation.
        **kwargs: Additional field metadata, must include 'description'.

    Returns:
        Any: A Pydantic Field with validated metadata.
    """
    if 'description' not in kwargs or not isinstance(kwargs['description'], str):
        raise ValueError(f"Component '{component_type}' is missing a valid string description.")

    return Field(**kwargs)
