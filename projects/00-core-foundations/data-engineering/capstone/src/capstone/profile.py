"""Profile a Parquet file with DuckDB. YOUR TURN: implement profile_parquet."""

from __future__ import annotations

import duckdb  # noqa: F401  (scaffold seam: used once profile_parquet is implemented)


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
    raise NotImplementedError(
        "YOUR TURN: implement profile_parquet (DuckDB over Parquet)"
    )
