from fastapi import APIRouter
from app.config.logging_config import logger

router = APIRouter()

@router.get("/ping")
async def ping():
    logger.info("Health check ping received.")
    return {"status": "ok", "message": "medparswell is alive"}