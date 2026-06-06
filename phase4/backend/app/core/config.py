from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Reserve AI - Phase 4"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

settings = Settings()
