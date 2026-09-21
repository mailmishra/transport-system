"""Shared pagination envelope + helper, used by every list_() in app/crud.

One `Page[T]` response shape and one `paginate()` helper so `q`/`sort`/
`page`/`limit` behave identically across resources instead of each router
reinventing offset math.
"""
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import ColumnElement

T = TypeVar("T")

MAX_LIMIT = 100
DEFAULT_LIMIT = 25


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int


def apply_sort(
    stmt: Select,
    sort: str | None,
    allowed: dict[str, ColumnElement],
    default: list[ColumnElement],
):
    """Apply a whitelisted `sort` query param (e.g. "-bilti_date", "bilti_no")
    to `stmt`, falling back to `default` (a list of .order_by()-ready
    expressions, applied as-is) when `sort` is absent or not in `allowed` --
    never build `.order_by()` from unvalidated client input. `default` is
    always appended after a valid `sort` column as a stable tiebreaker.
    """
    if not sort:
        return stmt.order_by(*default)
    desc = sort.startswith("-")
    key = sort[1:] if desc else sort
    column = allowed.get(key)
    if column is None:
        return stmt.order_by(*default)
    return stmt.order_by(column.desc() if desc else column.asc(), *default)


async def paginate(
    db: AsyncSession, stmt: Select, page: int, limit: int
) -> tuple[list, int, int, int]:
    """Returns (items, total, page, limit) -- page/limit come back clamped
    so callers (routers building the Page[T] envelope) don't have to
    re-derive the same clamping rules.
    """
    page = max(page, 1)
    limit = max(1, min(limit, MAX_LIMIT))
    total = (
        await db.execute(select(func.count()).select_from(stmt.subquery()))
    ).scalar_one()
    stmt = stmt.offset((page - 1) * limit).limit(limit)
    items = list((await db.execute(stmt)).scalars().all())
    return items, total, page, limit
