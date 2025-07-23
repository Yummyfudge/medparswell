from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "ok"}

# Placeholder for future summarization logic
class DocumentRequest(BaseModel):
    content: str

@router.post("/summarize")
async def summarize_document(request: DocumentRequest):
    # Placeholder for orchestrator logic:
    # e.g., extracted = extract_text(request.content)
    # summary = generate_summary(extracted)
    return {"summary": "<summary will be generated here>"}
