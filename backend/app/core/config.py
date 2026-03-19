from functools import lru_cache

from pydantic import computed_field, model_validator
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
    artist_ambre_password: str = "pass123"
    artist_celeste_password: str = "pass123"
    artist_santiago_password: str = "pass123"
    environment: str = "development"
    cms_project_id: str = "replace-me"
    cms_dataset: str = "production"
    cms_api_version: str = "2025-01-01"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @computed_field
    @property
    def docs_enabled(self) -> bool:
        return True

    @model_validator(mode="after")
    def validate_production_credentials(self):
        if self.environment.lower() != "production":
            return self

        default_passwords = {
            "FIRST_SUPERUSER_PASSWORD": "admin123",
            "ARTIST_AMBRE_PASSWORD": "pass123",
            "ARTIST_CELESTE_PASSWORD": "pass123",
            "ARTIST_SANTIAGO_PASSWORD": "pass123",
        }
        configured_passwords = {
            "FIRST_SUPERUSER_PASSWORD": self.first_superuser_password,
            "ARTIST_AMBRE_PASSWORD": self.artist_ambre_password,
            "ARTIST_CELESTE_PASSWORD": self.artist_celeste_password,
            "ARTIST_SANTIAGO_PASSWORD": self.artist_santiago_password,
        }

        weak_passwords = [name for name, value in configured_passwords.items() if value == default_passwords[name]]
        if weak_passwords:
            raise ValueError(
                "Production deployment requires non-default credentials for: " + ", ".join(weak_passwords)
            )

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
