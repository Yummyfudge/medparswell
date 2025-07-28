from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.config.logging_config import get_logger
from app.orchestrators.interfaces import get_active_interfaces
from app.orchestrators.endpoints import get_active_endpoints
from app.constructor.route_factory import build_route_for_interface

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧪 exploration_main FastAPI backend has started.")
    yield
    logger.info("🧪 exploration_main FastAPI backend is shutting down.")

exploration_app = FastAPI(lifespan=lifespan)

# Dynamically generate and include routers for all active endpoints/interfaces
for endpoint in get_active_endpoints():
    for interface in get_active_interfaces():
        router = build_route_for_interface(endpoint=endpoint, interface=interface)
        if router:
            exploration_app.include_router(router)