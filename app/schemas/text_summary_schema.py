from pydantic import BaseModel, constr
from typing import Optional
from app.core.component_loader import create_component

class SummarizeRequest(BaseModel):
    content: constr(strip_whitespace=True, min_length=1) = create_component(
        component_type="string",
        description="Raw text to summarize",
        example="Explain quantum entanglement in simple terms."
    )
    language: Optional[str] = create_component(
        component_type="string",
        description="Optional language code (e.g., 'en', 'es')",
        default=None,
        example="en"
    )

class SummarizeResponse(BaseModel):
    summary: str = create_component(
        component_type="string",
        description="Generated summary",
        example="Quantum entanglement is a phenomenon where particles remain connected..."
    )
    success: bool = create_component(
        component_type="boolean",
        description="Whether summarization was successful",
        example=True
    )
    duration_ms: Optional[int] = create_component(
        component_type="integer",
        description="Processing time in milliseconds",
        default=None,
        example=142
    )