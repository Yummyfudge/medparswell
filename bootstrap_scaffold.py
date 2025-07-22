import os

folders = [
    "app",
    "app/api",
    "app/models",
    "app/services",
    "app/core",
    "app/utils",
    "app/tests",
    "app/assets",  # future use: OCR templates, images, model files
]

files = {
    "app/__init__.py": "",
    "app/main.py": '''\
from fastapi import FastAPI
from app.api.router import router as api_router

app = FastAPI(title="MedParseWell API")

app.include_router(api_router)
''',
    "app/api/__init__.py": "",
    "app/api/router.py": '''\
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong"}
''',
    "app/models/__init__.py": "",
    "app/models/schemas.py": "# Pydantic models go here\n",
    "app/services/__init__.py": "",
    "app/services/summarizer.py": "# summarizer logic here\n",
    "app/utils/__init__.py": "",
    "app/utils/ocr_utils.py": "# OCR helpers here\n",
    "app/core/config.py": '''\
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MedParseWell API"

settings = Settings()
''',
    "app/tests/__init__.py": "",
    "app/tests/test_main.py": '''\
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
''',
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with initial content
for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)

print("✅ MedParseWell scaffold created.")