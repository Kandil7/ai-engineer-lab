"""Tests for settings URL normalization (managed Postgres connection strings)."""

from __future__ import annotations

from devmate.config import _to_asyncpg_url


def test_to_asyncpg_url_rewrites_platform_schemes() -> None:
    assert _to_asyncpg_url("postgres://u:p@h:5432/db") == "postgresql+asyncpg://u:p@h:5432/db"
    assert _to_asyncpg_url("postgresql://u:p@h:5432/db") == "postgresql+asyncpg://u:p@h:5432/db"


def test_to_asyncpg_url_is_idempotent() -> None:
    already = "postgresql+asyncpg://u:p@h:5432/db"
    assert _to_asyncpg_url(already) == already
