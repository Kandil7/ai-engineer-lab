"""
Challenge 40: uv - The Reproducible Environment - Tests
========================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/40-uv/test_challenge.py -q

Guards are measured (parse-call counts, tracemalloc peak), never wall-clock.
"""

from __future__ import annotations

import importlib.util
import os
import tracemalloc
from collections.abc import Iterator
from pathlib import Path

import pytest

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def parse_wheel(filename: str) -> dict:
    """Test-local reference parser (the oracle Silver's guard counts against)."""
    stem = filename[:-4]
    parts = stem.split("-")
    return {
        "name": parts[0],
        "version": parts[1],
        "python_tag": parts[-3],
        "abi_tag": parts[-2],
        "platform_tag": parts[-1],
    }


class CountingParser:
    """Parse callable that counts invocations."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, filename: str) -> dict:
        self.calls += 1
        return parse_wheel(filename)


def make_wheels(count: int = 200) -> list[str]:
    """Deterministic wheel list: pure-python, abi3, and platform-specific."""
    wheels: list[str] = []
    for i in range(count):
        kind = i % 4
        if kind == 0:
            wheels.append(f"pkg{i:03d}-1.{i % 10}.0-py3-none-any.whl")
        elif kind == 1:
            wheels.append(f"pkg{i:03d}-1.{i % 10}.0-cp39-abi3-win_amd64.whl")
        elif kind == 2:
            wheels.append(f"pkg{i:03d}-1.{i % 10}.0-cp312-cp312-win_amd64.whl")
        else:
            wheels.append(f"pkg{i:03d}-1.{i % 10}.0-cp312-cp312-linux_x86_64.whl")
    return wheels


# ---------------------------------------------------------------- Bronze


def test_bronze_full_tags():
    assert mod.wheel_tags("numpy-1.26.4-cp312-cp312-win_amd64.whl") == {
        "name": "numpy",
        "version": "1.26.4",
        "python_tag": "cp312",
        "abi_tag": "cp312",
        "platform_tag": "win_amd64",
    }


def test_bronze_pure_python_wheel():
    assert mod.wheel_tags("ruff-0.5.0-py3-none-any.whl") == {
        "name": "ruff",
        "version": "0.5.0",
        "python_tag": "py3",
        "abi_tag": "none",
        "platform_tag": "any",
    }


def test_bronze_normalized_name_keeps_underscores():
    tags = mod.wheel_tags("my_pkg-1.0.0-cp39-abi3-manylinux_2_17_x86_64.whl")
    assert tags["name"] == "my_pkg"
    assert tags["platform_tag"] == "manylinux_2_17_x86_64"


def test_bronze_non_wheel_raises():
    with pytest.raises(ValueError):
        mod.wheel_tags("setup.txt")


def test_bronze_too_few_parts_raises():
    with pytest.raises(ValueError):
        mod.wheel_tags("x-1.0.whl")


# ---------------------------------------------------------------- Silver


def test_silver_selects_exact_and_pure_and_abi3():
    index = mod.WheelIndex(
        [
            "a-1.0-cp312-cp312-win_amd64.whl",
            "b-1.0-cp39-abi3-win_amd64.whl",
            "c-1.0-py3-none-any.whl",
            "d-1.0-cp312-cp312-linux_x86_64.whl",
            "e-1.0-cp311-cp311-win_amd64.whl",
        ],
        parse_wheel,
    )
    assert index.select("cp312", "win_amd64") == [
        "a-1.0-cp312-cp312-win_amd64.whl",
        "b-1.0-cp39-abi3-win_amd64.whl",
        "c-1.0-py3-none-any.whl",
    ]


def test_silver_abi3_requires_older_or_equal_cpython():
    index = mod.WheelIndex(
        [
            "old-1.0-cp39-abi3-win_amd64.whl",
            "new-1.0-cp313-abi3-win_amd64.whl",
        ],
        parse_wheel,
    )
    assert index.select("cp312", "win_amd64") == ["old-1.0-cp39-abi3-win_amd64.whl"]


def test_silver_order_is_preserved():
    wheels = ["a-1.0-py3-none-any.whl", "b-1.0-py3-none-any.whl"]
    index = mod.WheelIndex(wheels, parse_wheel)
    assert index.select("cp310", "linux_x86_64") == wheels


def test_silver_no_match_returns_empty():
    index = mod.WheelIndex(["a-1.0-cp312-cp312-win_amd64.whl"], parse_wheel)
    assert index.select("cp39", "linux_x86_64") == []


def test_silver_empty_index():
    index = mod.WheelIndex([], parse_wheel)
    assert index.select("cp312", "win_amd64") == []


def test_silver_parse_budget():
    wheels = make_wheels(200)
    parser = CountingParser()
    index = mod.WheelIndex(wheels, parser)
    for _ in range(100):
        assert index.select("cp312", "win_amd64") is not None
    budget = len(wheels) + 5
    assert parser.calls <= budget, (
        f"{parser.calls} parses for {len(wheels)} wheels over 100 queries; "
        "parse each filename once at construction and select from the index"
    )


# ------------------------------------------------------------------ Gold

ADVISORIES: dict[str, list[dict]] = {
    "pkg000010": [{"id": "PYSEC-2026-1", "fixed_in": "9.9.9"}],
    "pkg000020": [{"id": "PYSEC-2026-2", "fixed_in": None}],
    "pkg000030": [
        {"id": "PYSEC-2026-3", "fixed_in": "1.5.0"},
        {"id": "PYSEC-2026-4", "fixed_in": "0.5.0"},
    ],
}


def package_stream(count: int) -> Iterator[dict]:
    """Deterministic package iterator; yields, never accumulates."""
    for i in range(count):
        yield {"name": f"pkg{i:06d}", "version": f"1.{i % 10}.{i % 5}"}


def test_gold_finds_vulnerable_and_nofix():
    findings = mod.audit_stream(package_stream(100), ADVISORIES)
    assert findings == [
        "pkg000010==1.0.0 PYSEC-2026-1 (fixed in 9.9.9)",
        "pkg000020==1.0.0 PYSEC-2026-2 (no fix available)",
        "pkg000030==1.0.0 PYSEC-2026-3 (fixed in 1.5.0)",
    ]


def test_gold_version_equal_to_fix_is_not_vulnerable():
    advisories = {"a": [{"id": "V-1", "fixed_in": "1.0.0"}]}
    packages = [{"name": "a", "version": "1.0.0"}]
    assert mod.audit_stream(iter(packages), advisories) == []


def test_gold_version_above_fix_is_not_vulnerable():
    advisories = {"a": [{"id": "V-1", "fixed_in": "1.0.0"}]}
    packages = [{"name": "a", "version": "2.0.0"}]
    assert mod.audit_stream(iter(packages), advisories) == []


def test_gold_minor_version_comparison_is_numeric():
    advisories = {"a": [{"id": "V-1", "fixed_in": "2.9.9"}]}
    packages = [{"name": "a", "version": "2.10.0"}]
    assert mod.audit_stream(iter(packages), advisories) == []
    packages = [{"name": "a", "version": "2.9.1"}]
    assert mod.audit_stream(iter(packages), advisories) == ["a==2.9.1 V-1 (fixed in 2.9.9)"]


def test_gold_ignore_drops_by_id():
    findings = mod.audit_stream(package_stream(100), ADVISORIES, {"PYSEC-2026-1"})
    assert findings == [
        "pkg000020==1.0.0 PYSEC-2026-2 (no fix available)",
        "pkg000030==1.0.0 PYSEC-2026-3 (fixed in 1.5.0)",
    ]


def test_gold_empty_input():
    assert mod.audit_stream(iter([]), ADVISORIES) == []


def test_gold_unknown_packages_are_ignored():
    advisories = {"ghost": [{"id": "V-1", "fixed_in": None}]}
    assert mod.audit_stream(package_stream(10), advisories) == []


def test_gold_exit_code():
    assert mod.audit_exit_code([]) == 0
    assert mod.audit_exit_code(["a==1.0 V-1 (no fix available)"]) == 1


def test_gold_memory_ceiling():
    tracemalloc.start()
    findings = mod.audit_stream(package_stream(20_000), ADVISORIES)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert len(findings) == 3
    assert peak < 1_000_000, (
        f"peak {peak} bytes exceeds the 1 MB ceiling for 20,000 packages; "
        "consume the iterator one package at a time instead of list()-ing it"
    )
