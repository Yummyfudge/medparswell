from fastapi import FastAPI
from app.main_router import router  # or wherever we end up placing the APIRouter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 medparswell FastAPI backend has started.")

@app.get("/")
async def root():
    return {"status": "ok", "message": "medparswell API is running."}

app.include_router(router)