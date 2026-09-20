from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/transport"
    cors_origins: str = ""

    # Not used yet — Supabase auth is a future integration. Kept here so
    # turning it on later is a config change, not a schema/code change.
    supabase_url: str | None = None
    supabase_jwt_secret: str | None = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
