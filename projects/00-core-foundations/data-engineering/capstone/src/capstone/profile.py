"""Profile a Parquet file with DuckDB (reference implementation)."""

from __future__ import annotations

import duckdb


def _quote_literal(path: str) -> str:
    """Quote a filesystem path as a SQL string literal."""
    return "'" + path.replace("'", "''") + "'"


def _quote_ident(name: str) -> str:
    """Quote a column name as a SQL identifier."""
    return '"' + name.replace('"', '""') + '"'


def _scalar(con: duckdb.DuckDBPyConnection, sql: str) -> int:
    """Run a single-row, single-column query and return it as int."""
    row = con.execute(sql).fetchone()
    assert row is not None, f"scalar query returned no rows: {sql}"
    return int(row[0])


def profile_parquet(path: str) -> dict[str, object]:
    """Return the profile dict the quality gates consume.

    Contract (keys are fixed)::
        {
            "rows": int,                    # total row count
            "null_rates": {col: float},     # fraction null per column
            "distinct_ids": int,            # COUNT(DISTINCT passage_id)
            "duplicate_ids": int,           # rows - distinct passage_ids (>0 means dupes)
        }

    Read with ``read_parquet`` in place (no full-frame load). ``path`` may be a
    plain filesystem path; quote it safely for SQL.
    """
    lit = _quote_literal(path)
    con = duckdb.connect()
    try:
        rows = _scalar(con, f"SELECT COUNT(*) FROM read_parquet({lit})")
        cols = [
            d[0]
            for d in con.execute(
                f"SELECT * FROM read_parquet({lit}) LIMIT 0"
            ).description
        ]
        null_rates: dict[str, float] = {}
        for col in cols:
            ident = _quote_ident(col)
            nulls = _scalar(
                con,
                f"SELECT COUNT(*) FILTER (WHERE {ident} IS NULL)"
                f" FROM read_parquet({lit})",
            )
            null_rates[col] = (nulls / rows) if rows else 0.0
        distinct_ids = _scalar(
            con, f"SELECT COUNT(DISTINCT passage_id) FROM read_parquet({lit})"
        )
    finally:
        con.close()
    return {
        "rows": rows,
        "null_rates": null_rates,
        "distinct_ids": distinct_ids,
        "duplicate_ids": rows - distinct_ids,
    }
