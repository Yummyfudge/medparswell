from fastapi import FastAPI
from app.main_router import router  # or wherever we end up placing the APIRouter

app = FastAPI()

app.include_router(router)