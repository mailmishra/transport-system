"""No DB needed - Settings is a plain Pydantic model."""
from app.config import Settings


def test_plain_postgres_scheme_gets_asyncpg_driver():
    s = Settings(database_url="postgres://user:pass@host:5432/db")
    assert s.database_url == "postgresql+asyncpg://user:pass@host:5432/db"


def test_postgresql_scheme_gets_asyncpg_driver():
    s = Settings(database_url="postgresql://user:pass@host:5432/db")
    assert s.database_url == "postgresql+asyncpg://user:pass@host:5432/db"


def test_already_asyncpg_scheme_is_left_alone():
    url = "postgresql+asyncpg://user:pass@host:5432/db"
    assert Settings(database_url=url).database_url == url


def test_cors_origin_list_splits_and_strips():
    s = Settings(cors_origins=" https://a.com, https://b.com ,")
    assert s.cors_origin_list == ["https://a.com", "https://b.com"]


def test_cors_origin_list_empty_by_default():
    assert Settings(cors_origins="").cors_origin_list == []
