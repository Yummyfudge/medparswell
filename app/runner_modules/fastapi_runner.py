import uvicorn
from logging import getLogger

logger = getLogger("medparswell")

def launch_fastapi_app(settings, app):
    logger.info("🚀 Launching FastAPI app via Uvicorn...")
    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
