from fastapi import APIRouter
from app.schemas.text_summary_schema import SummarizeRequest, SummarizeResponse
from app.services import llama_runner
from app.config import settings

router = APIRouter()

@router.post("/text-summary", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    output = llama_runner.run_llama_cli(
        prompt=request.text,
        model_path=settings.llama_model_path,
        ctx_size=settings.llama_ctx_size,
        gpu_layers=settings.llama_gpu_layers,
        verbose=True,
    )
    return SummarizeResponse(summary=output)