from fastapi import FastAPI
from app.main_router import router  # or wherever we end up placing the APIRouter
from app.routes import health_routes
from contextlib import asynccontextmanager
from app.config.logging_config import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 medparswell FastAPI backend has started.")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "message": "medparswell API is running."}

app.include_router(router)
app.include_router(health_routes.router)