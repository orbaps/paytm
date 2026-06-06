from functools import lru_cache
from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Paytm Smart Reserve AI - Phase 1 Data Platform"
    app_env: str = "development"
    debug: bool = False
    api_prefix: str = "/api"

    database_url: str = Field(
        default="postgresql+psycopg://paytm:paytm@localhost:5432/paytm_smart_reserve"
    )
    auto_create_tables: bool = True

    api_basic_auth_enabled: bool = True
    api_username: str = "admin"
    api_password: str = "admin123"

    rate_limit_enabled: bool = True
    rate_limit_requests: int = 120
    rate_limit_window_seconds: int = 60

    cors_origins: list[AnyHttpUrl | str] = ["http://localhost:5173", "http://localhost:3000"]
    log_level: str = "INFO"

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: object) -> object:
        if isinstance(value, str) and value.strip().lower() in {"release", "prod", "production"}:
            return False
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
