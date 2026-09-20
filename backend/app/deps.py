from collections.abc import AsyncGenerator
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


@dataclass
class Actor:
    id: str | None
    authenticated: bool


async def get_current_actor() -> Actor:
    """Stub auth dependency.

    No auth is enforced yet. This is the single place a future Supabase JWT
    check gets wired in (verify the bearer token, populate Actor.id from the
    `sub` claim) without touching routers or models — they already accept a
    nullable `created_by` and depend on this function.
    """
    return Actor(id=None, authenticated=False)
