"""
Data Engineering — 15: Storage Systems and Database Selection
==============================================================
Topics: object storage practices, file formats, partitioning, and the
        database-selection rubric (polyglot principle).

Why this matters:
    The storage choice is the choice of a query pattern and a cost curve.
    This exercise builds a partition-pruning helper, a format-chooser, and
    a database-selection rubric, all pure stdlib, proving that the right
    store follows the workload, not a default.

Run:      python 15-storage-and-databases.py
Verify:   python 15-storage-and-databases.py --verify
"""

from __future__ import annotations

import sys


def choose_format(access: str) -> str:
    """Pick a file format by access pattern."""
    if access == "columnar_analytics":
        return "parquet"
    if access == "hive_acid":
        return "orc"
    if access == "streaming_schema_evolution":
        return "avro"
    raise ValueError(f"unknown access pattern {access}")


def prune(partition_keys: list[tuple[str, str]], filters: dict[str, str]) -> bool:
    """Return True if the partition matches the filter keys (scan it)."""
    part = dict(partition_keys)
    return all(part.get(k) == v for k, v in filters.items())


def select_database(workload: dict) -> str:
    """A small rubric: match a workload shape to a database family."""
    shape = workload["shape"]
    if shape == "relationships":
        return "neo4j"  # multi-hop traversal
    if shape == "time_series":
        return "timescaledb"  # append-only, range-queried metrics
    if shape == "key_value_scale":
        return "dynamodb"  # fixed-key, write-heavy
    if shape == "structured_joins":
        return "postgresql"  # ACID, joins
    raise ValueError(f"unknown shape {shape}")


def main() -> None:
    # Format selection by access pattern.
    assert choose_format("columnar_analytics") == "parquet"
    assert choose_format("streaming_schema_evolution") == "avro"
    assert choose_format("hive_acid") == "orc"

    # Partition pruning: a filter on partition keys reads the matching prefix.
    partitions = [
        [("book_id", "b1"), ("source_version", "v1")],
        [("book_id", "b1"), ("source_version", "v2")],
        [("book_id", "b2"), ("source_version", "v1")],
    ]
    hit = [p for p in partitions if prune(p, {"book_id": "b1", "source_version": "v1"})]
    assert hit == [[("book_id", "b1"), ("source_version", "v1")]]  # exactly one prefix

    # A filter on a non-partition column does not prune by prefix.
    all_b1 = [p for p in partitions if prune(p, {"book_id": "b1"})]
    assert len(all_b1) == 2  # both b1 versions

    # Database selection by workload shape (the polyglot principle).
    assert select_database({"shape": "structured_joins"}) == "postgresql"
    assert select_database({"shape": "relationships"}) == "neo4j"
    assert select_database({"shape": "time_series"}) == "timescaledb"
    assert select_database({"shape": "key_value_scale"}) == "dynamodb"

    print(f"format: columnar -> {choose_format('columnar_analytics')}")
    print(f"pruned prefix count for b1/v1: {len(hit)}")
    print("polyglot: each data shape lands in a different store")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
