import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.main_router import router  # or wherever we end up placing the APIRouter
from app.routes import health_routes
from contextlib import asynccontextmanager
from app.config.logging_config import logger
from app.config.docs_config import custom_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 medparswell FastAPI backend has started.", extra={"component": "main"})
    yield
    logger.info("🟢 FastAPI lifespan completed startup steps.", extra={"component": "main"})

app = FastAPI(lifespan=lifespan)
def custom_openapi_wrapper():
    return custom_openapi(app)

app.openapi = custom_openapi_wrapper

from app.constructor.route_factory import register_routes
from app.config.settings import settings

# Dynamically register only the endpoints and interfaces explicitly enabled
if not settings.enabled_endpoints:
    logger.warning("⚠️ No endpoints are enabled in .env. No routes will be registered.")
    return
if not settings.enabled_interfaces:
    logger.warning("⚠️ No interfaces are enabled in .env. No routes will be registered.")
    return
if settings.enabled_endpoints and settings.enabled_interfaces:
    register_routes(
        app,
        enabled_endpoints=settings.enabled_endpoints,
        enabled_interfaces=settings.enabled_interfaces,
    )

from app.main_router import add_custom_handlers
add_custom_handlers(app)

@app.get("/")
async def root():
    logger.debug("📥 Root endpoint '/' was hit.", extra={"component": "main"})
    return {"status": "ok", "message": "medparswell API is running."}

app.include_router(router)
app.include_router(health_routes.router)