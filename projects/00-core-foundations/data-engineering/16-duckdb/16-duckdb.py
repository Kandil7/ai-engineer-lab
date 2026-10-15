"""
Data Engineering — 16: DuckDB profiling over Parquet
=====================================================
Topics: read_parquet in place, SUMMARIZE, null-rate / distinct-count /
        duplicate queries, approximate quantiles, profile-as-a-table export.

Why this matters:
    Profiling measures the corpus before the quality gates judge it. Polars owns
    cleaning and transformation; DuckDB owns profiling and measurement (ADR-0011).

Run:      python 16-duckdb.py
Verify:   python 16-duckdb.py --verify
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import duckdb
import polars as pl

N_ROWS = 10
N_COLUMNS = 4
EXPECTED_DUPES = 2
EXPECTED_TEXT_NULLS = 2


def build_fixture(path: Path) -> None:
    """Write the skewed fixture with Polars: nulls, dupes, skew, all-null notes."""
    frame = pl.DataFrame(
        {
            "passage_id": [
                "b1:p1:0",
                "b1:p2:0",
                "b1:p3:0",
                "b1:p1:0",
                "b1:p4:0",
                "b1:p5:0",
                "b1:p6:0",
                "b1:p2:0",
                "b1:p7:0",
                "b1:p8:0",
            ],
            "text": [
                "نص التمرين الأول",
                "نص التمرين الثاني",
                "نص التمرين الثالث",
                "نص التمرين الأول",
                "نص التمرين الرابع",
                None,
                "نص التمرين السادس",
                "نص التمرين الثاني",
                "نص التمرين السابع",
                None,
            ],
            "score": [0.10, 0.20, 0.90, 0.10, 0.95, None, 0.85, 0.20, 0.92, 0.88],
            "notes": pl.Series("notes", [None] * N_ROWS, dtype=pl.String),
        }
    )
    frame.write_parquet(path)


def sql_literal(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        parquet_path = Path(tmp) / "fixture.parquet"
        build_fixture(parquet_path)
        parquet = sql_literal(parquet_path)
        con = duckdb.connect()
        con.execute(
            "CREATE OR REPLACE VIEW docs AS SELECT * FROM read_parquet(" + parquet + ")"
        )
        count_row = con.execute("SELECT COUNT(*) FROM docs").fetchone()
        assert count_row is not None
        row_count = count_row[0]
        assert row_count == N_ROWS, f"row count {row_count} != {N_ROWS}"

        con.execute(
            "CREATE OR REPLACE TABLE column_profile AS "
            "SELECT 'passage_id' AS column_name, "
            "COUNT(*) FILTER (WHERE passage_id IS NULL) * 1.0 / COUNT(*) "
            "AS null_rate, COUNT(DISTINCT passage_id) AS distinct_count FROM docs "
            "UNION ALL SELECT 'text', "
            "COUNT(*) FILTER (WHERE text IS NULL) * 1.0 / COUNT(*), "
            "COUNT(DISTINCT text) FROM docs "
            "UNION ALL SELECT 'score', "
            "COUNT(*) FILTER (WHERE score IS NULL) * 1.0 / COUNT(*), "
            "COUNT(DISTINCT score) FROM docs "
            "UNION ALL SELECT 'notes', "
            "COUNT(*) FILTER (WHERE notes IS NULL) * 1.0 / COUNT(*), "
            "COUNT(DISTINCT notes) FROM docs"
        )
        rows = con.execute(
            "SELECT column_name, null_rate, distinct_count FROM column_profile"
        ).fetchall()
        profile = {name: (rate, distinct) for name, rate, distinct in rows}

        text_rate = profile["text"][0]
        assert abs(text_rate - EXPECTED_TEXT_NULLS / N_ROWS) < 1e-9, (
            f"text null rate {text_rate}"
        )

        notes_rate = profile["notes"][0]
        assert abs(notes_rate - 1.0) < 1e-9, f"all-null column not caught: {notes_rate}"

        dupe_row = con.execute(
            "SELECT COUNT(*) - COUNT(DISTINCT passage_id) FROM docs"
        ).fetchone()
        assert dupe_row is not None
        dupes = dupe_row[0]
        assert dupes == EXPECTED_DUPES, f"duplicate count {dupes} != {EXPECTED_DUPES}"

        summary = con.execute("SELECT * FROM (SUMMARIZE docs)").fetchall()
        assert len(summary) == N_COLUMNS, f"summary rows {len(summary)} != {N_COLUMNS}"

        quant_row = con.execute(
            "SELECT approx_quantile(score, 0.5), approx_quantile(score, 0.9) FROM docs"
        ).fetchone()
        assert quant_row is not None
        med, p90 = quant_row
        assert 0.0 <= med <= 1.0 and 0.0 <= p90 <= 1.0, "quantiles out of range"

        rates = {name: round(rate, 3) for name, (rate, _) in profile.items()}
        distinct = {name: d for name, (_, d) in profile.items()}
        print(f"rows: {row_count}, duplicate passages: {dupes}")
        print(f"null rates: {rates} | distinct: {distinct}")
        print(f"score quantiles: median~{med:.2f} p90~{p90:.2f} (skewed high)")
        print(f"summary rows: {len(summary)} for {N_COLUMNS} columns")
        print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
