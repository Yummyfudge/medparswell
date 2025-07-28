import uvicorn
from app.config.settings import settings
from app.exploration_main import exploration_app

if __name__ == "__main__":
    uvicorn.run(
        app=exploration_app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.app_log_level.lower(),
    )
