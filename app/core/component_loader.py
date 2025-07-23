from typing import Any, Dict

def create_component(component_type: str, **kwargs) -> Dict[str, Any]:
    """
    Create a well-structured component definition with mandatory 'type' and 'description'.
    This is used to support automatic API metadata generation.

    Args:
        component_type (str): The data type of the component (e.g., 'string', 'number').
        **kwargs: Additional keyword arguments representing component attributes.

    Returns:
        Dict[str, Any]: A dictionary representing the component with enforced metadata.
    """
    if 'description' not in kwargs or not isinstance(kwargs['description'], str):
        raise ValueError(f"Component '{component_type}' is missing a valid string description.")

    return {
        'type': component_type,
        'description': kwargs.pop('description'),
        **kwargs
    }
