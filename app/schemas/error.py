from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    detail: str
    code: Optional[int] = None
    hint: Optional[str] = None