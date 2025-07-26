def create_component(component_type: str, description: str = "", **kwargs):
    """
    Create a component definition dictionary used by Pydantic field aliases.

    Args:
        component_type (str): The type of component, e.g., "string", "number".
        description (str): A human-readable description of the field.
        **kwargs: Any additional metadata such as `example`, `title`, etc.

    Returns:
        dict: A dictionary suitable for Pydantic `Field(..., json_schema_extra=...)`.
    """
    return {
        "json_schema_extra": {
            "x-component": {
                "type": component_type,
                "description": description,
                **kwargs,
            }
        }
    }