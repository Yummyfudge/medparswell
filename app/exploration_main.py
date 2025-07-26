from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.config.logging_config import get_logger
from app.orchestrators.interfaces import get_enabled_interfaces
from app.orchestrators.endpoints import get_enabled_endpoints
from app.constructor.route_factory import construct_routes

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧪 exploration_main FastAPI backend has started.")
    yield
    logger.info("🧪 exploration_main FastAPI backend is shutting down.")

exploration_app = FastAPI(lifespan=lifespan)

# Dynamically generate router based on enabled components
enabled_interfaces = get_enabled_interfaces()
enabled_endpoints = get_enabled_endpoints()
dynamic_router = construct_routes(enabled_endpoints, enabled_interfaces)

# Include constructed router
exploration_app.include_router(dynamic_router)