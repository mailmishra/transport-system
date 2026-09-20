from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/transport"
    cors_origins: str = ""

    @field_validator("database_url")
    @classmethod
    def force_asyncpg_driver(cls, v: str) -> str:
        # Railway's managed Postgres (and most hosts) hand out a plain
        # postgresql:// or postgres:// URL. Our engine is async, so it needs
        # the asyncpg driver in the scheme — rewrite rather than requiring
        # every deploy target to know this detail.
        if v.startswith("postgres://"):
            return "postgresql+asyncpg://" + v[len("postgres://"):]
        if v.startswith("postgresql://"):
            return "postgresql+asyncpg://" + v[len("postgresql://"):]
        return v

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
