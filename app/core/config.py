from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MedParseWell API"

settings = Settings()
