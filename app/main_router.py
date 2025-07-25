from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
logger = logging.getLogger("medparswell")

router = APIRouter()

# Health check endpoint
@router.get("/health")
async def health_check():
    logger.debug("✅ Health check endpoint hit")
    return {"status": "ok"}

# Placeholder for future summarization logic
class DocumentRequest(BaseModel):
    content: str

@router.post("/summarize")
async def summarize_document(request: DocumentRequest):
    logger.info("📝 Received summarization request")
    logger.debug(f"📥 Raw content: {request.content}")
    # Placeholder for orchestrator logic:
    # e.g., extracted = extract_text(request.content)
    # summary = generate_summary(extracted)
    from app.services.llama_runner import LlamaRunner
    from app.config.settings import settings

    runner = LlamaRunner(binary_path=settings.llama_cli_path)
    summary = runner.run_prompt(prompt=request.content, verbose=settings.verbose)
    logger.debug(f"📤 Generated summary: {summary}")
    return {"summary": summary}


# 404 Exception handler

# Custom exception handler registration
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI

def add_custom_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            logger.warning(f"🚫 404 Not Found: {request.method} {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )