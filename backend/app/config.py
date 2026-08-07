from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ImmoFix API"
    app_env: str = "development"
    database_url: str = "sqlite:///./immofix.db"
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "immofix_events"
    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    jwt_secret: str = "change-this-development-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    admin_email: str = "admin@immofix.de"
    admin_password: str = "ImmoFix2026!"
    admin_name: str = "ImmoFix Administration"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
