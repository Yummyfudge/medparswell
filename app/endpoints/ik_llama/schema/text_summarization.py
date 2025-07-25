from pydantic import BaseModel, constr, Field
from typing import Optional, Annotated

NonEmptyStr = constr(min_length=1, strip_whitespace=True)

class SummarizeRequest(BaseModel):
    content: Annotated[
        NonEmptyStr,
        Field(
            description="Raw text to summarize",
            json_schema_extra={"example": "Explain quantum entanglement in simple terms."}
        )
    ]
    language: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Optional language code (e.g., 'en', 'es')",
            json_schema_extra={"example": "en"}
        )
    ]

class SummarizeResponse(BaseModel):
    summary: Annotated[
        str,
        Field(
            description="Generated summary",
            json_schema_extra={"example": "Quantum entanglement is a phenomenon where particles remain connected..."}
        )
    ]
    success: Annotated[
        bool,
        Field(
            description="Whether summarization was successful",
            json_schema_extra={"example": True}
        )
    ]
    duration_ms: Annotated[
        Optional[int],
        Field(
            default=None,
            description="Processing time in milliseconds",
            json_schema_extra={"example": 142}
        )
    ]