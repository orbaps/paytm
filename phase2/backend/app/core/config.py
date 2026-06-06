from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Reserve Core Engine"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

settings = Settings()
