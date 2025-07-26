from pydantic import BaseModel, Field
from typing import Optional


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable description of the error")
    code: Optional[int] = Field(None, description="Optional internal application-specific error code")
    hint: Optional[str] = Field(None, description="Suggested fix or additional context for the error")