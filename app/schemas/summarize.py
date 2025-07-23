from pydantic import BaseModel
from typing import Optional
from app.core.component_loader import create_component

class SummarizeRequest(BaseModel):
    content: str = create_component("string", "Raw text to summarize", example="Explain quantum entanglement in simple terms.")
    language: Optional[str] = create_component("string", "Optional language code (e.g., 'en', 'es')", default=None, example="en")

class SummarizeResponse(BaseModel):
    summary: str = create_component("string", "Generated summary", example="Quantum entanglement is a phenomenon where particles remain connected...")
    success: bool = create_component("boolean", "Whether summarization was successful", example=True)
    duration_ms: Optional[int] = create_component("integer", "Processing time in milliseconds", default=None, example=142)