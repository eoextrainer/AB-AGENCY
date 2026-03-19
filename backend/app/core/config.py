from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AB Agency API"
    api_prefix: str = "/api"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+psycopg://ab_agency:ab_agency@db:5432/ab_agency"
    cors_origins: list[str] = ["http://localhost:3000", "http://frontend:3000"]
    first_superuser_email: str = "admin@ab-agency.com"
    first_superuser_username: str = "admin"
    first_superuser_password: str = "admin123"
    environment: str = "development"
    cms_project_id: str = "replace-me"
    cms_dataset: str = "production"
    cms_api_version: str = "2025-01-01"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @computed_field
    @property
    def docs_enabled(self) -> bool:
        return True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
