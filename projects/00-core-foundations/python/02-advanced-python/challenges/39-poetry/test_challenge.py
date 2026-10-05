"""
Challenge 39: Poetry - The CI Dependency Gate - Tests
======================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/39-poetry/test_challenge.py -q

Performance guards use comparison counting and a fetch counter - never
wall-clock time.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest
import tomllib  # type: ignore[import-not-found]

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

_PROJECT_KEYS = (
    "name",
    "version",
    "description",
    "requires-python",
    "dependencies",
    "optional-dependencies",
)
_POETRY_KEYS = ("source", "extras", "dev-dependencies", "group", "dependencies")

MANIFEST = """\
[project]
name = "serving"
version = "0.3.0"
description = "Model serving API"
requires-python = ">=3.10"
dependencies = ["numpy (>=1.26,<3.0.0)", "pydantic (>=2.5,<3.0.0)"]

[tool.poetry.group.dev.dependencies]
pytest = ">=8.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = ">=1.6"

[tool.ruff]
line-length = 100
"""

RUFF_EDITED_MANIFEST = MANIFEST.replace("line-length = 100", "line-length = 88")

STALE_MANIFEST = MANIFEST.replace(
    'dependencies = ["numpy (>=1.26,<3.0.0)"',
    'dependencies = ["httpx (>=0.27)", "numpy (>=1.26,<3.0.0)"',
)


def _content_hash(text: str) -> str:
    """Reference copy of the hash algorithm documented in README.md."""
    manifest = tomllib.loads(text)
    relevant: dict = {}
    project = manifest.get("project")
    if project:
        section = {k: project[k] for k in _PROJECT_KEYS if k in project}
        if section:
            relevant["project"] = section
    if manifest.get("dependency-groups"):
        relevant["dependency-groups"] = manifest["dependency-groups"]
    poetry = (manifest.get("tool") or {}).get("poetry")
    if poetry:
        section = {k: poetry[k] for k in _POETRY_KEYS if k in poetry}
        if section:
            relevant["tool"] = {"poetry": section}
    payload = json.dumps(relevant, sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


LOCK = f"""\
[[package]]
name = "mkdocs"
version = "1.6.0"

[[package]]
name = "numpy"
version = "1.26.4"

[[package]]
name = "pydantic"
version = "2.5.3"

[[package]]
name = "pytest"
version = "8.3.0"

[metadata]
content-hash = "{_content_hash(MANIFEST)}"
"""

LOCK_BAD_RANGE = LOCK.replace('version = "1.26.4"', 'version = "3.1.0"')

LOCK_MISSING = LOCK.replace(
    '[[package]]\nname = "pydantic"\nversion = "2.5.3"\n\n',
    "",
)

LOCK_NO_HASH = LOCK.split("[metadata]")[0]


def _size(name: str) -> float:
    return (sum(ord(c) for c in name) % 400 + 100) / 10.0


class IndexDouble:
    """Fake index client: returns a size, rejects a second fetch of one name."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, name: str) -> float:
        if name in self.calls:
            raise AssertionError(f"duplicate index fetch: {name}")
        self.calls.append(name)
        return _size(name)


class CountingStr(str):
    """String that counts every equality/order comparison."""

    __slots__ = ("counter",)

    def __new__(cls, val: str, counter: list[int]) -> CountingStr:
        obj = super().__new__(cls, val)
        obj.counter = counter
        return obj

    def __eq__(self, other: object) -> bool:
        self.counter[0] += 1
        return super().__eq__(other)

    def __lt__(self, other: object) -> bool:
        self.counter[0] += 1
        return str.__lt__(self, str(other))

    def __hash__(self) -> int:
        return super().__hash__()


class TestBronzeExpandConstraint:
    """Bronze: Poetry constraint expansion."""

    @pytest.mark.parametrize(
        ("spec", "expected"),
        [
            ("^1.2.3", (">=1.2.3", "<2.0.0")),
            ("^0.2.3", (">=0.2.3", "<0.3.0")),
            ("^0.0.3", (">=0.0.3", "<0.0.4")),
            ("~1.2.3", (">=1.2.3", "<1.3.0")),
            ("1.2.3", ("==1.2.3", "")),
            ("1.2.*", (">=1.2.0", "<1.3.0")),
            ("~=1.2", (">=1.2.0", "<2.0.0")),
            (">=1.26,<3.0.0", (">=1.26", "<3.0.0")),
            ("", ("", "")),
        ],
    )
    def test_table(self, spec: str, expected: tuple[str, str]) -> None:
        assert mod.expand_constraint(spec) == expected

    def test_rejects_not_equal(self) -> None:
        with pytest.raises(ValueError):
            mod.expand_constraint("!=1.2.3")


def _chain_locked(n: int, counter: list[int]) -> list[dict]:
    """n packages, chain 0 -> 1 -> ... -> n-1, root listed last."""
    rows: list[dict] = []
    for i in range(n):
        deps = [CountingStr(f"pkg{i - 1:05d}", counter)] if i > 0 else []
        rows.append({"name": CountingStr(f"pkg{i:05d}", counter), "dependencies": deps})
    return rows


class TestSilverInstallClosure:
    """Silver: closure walk with a comparison budget."""

    def test_simple(self) -> None:
        locked = [
            {"name": "A", "dependencies": ["B", "C"]},
            {"name": "B", "dependencies": ["D"]},
            {"name": "C", "dependencies": []},
            {"name": "D", "dependencies": []},
        ]
        assert mod.install_closure(locked, ["A"]) == ["A", "B", "C", "D"]

    def test_diamond_visits_shared_node_once(self) -> None:
        locked = [
            {"name": "A", "dependencies": ["B", "C"]},
            {"name": "B", "dependencies": ["D"]},
            {"name": "C", "dependencies": ["D"]},
            {"name": "D", "dependencies": []},
        ]
        assert mod.install_closure(locked, ["A"]) == ["A", "B", "C", "D"]

    def test_root_absent_from_lock_is_kept(self) -> None:
        locked = [{"name": "A", "dependencies": []}]
        assert mod.install_closure(locked, ["A", "ghost"]) == ["A", "ghost"]

    def test_empty_roots(self) -> None:
        assert mod.install_closure([{"name": "A", "dependencies": []}], []) == []

    def test_cycle_terminates(self) -> None:
        locked = [
            {"name": "A", "dependencies": ["B"]},
            {"name": "B", "dependencies": ["A"]},
        ]
        assert mod.install_closure(locked, ["A"]) == ["A", "B"]

    def test_comparison_budget_on_adversarial_chain(self) -> None:
        n = 2000
        counter = [0]
        locked = _chain_locked(n, counter)
        root = f"pkg{n - 1:05d}"
        out = mod.install_closure(locked, [root])
        assert len(out) == n
        assert out[0] == "pkg00000"
        assert counter[0] <= 10 * n, f"{counter[0]} comparisons for n={n}"


class TestGoldAuditManifest:
    """Gold: freshness, group selection, ranges, fetch budget."""

    def test_pristine_manifest_is_fresh(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK, IndexDouble())
        assert out["fresh"] is True
        assert out["unsatisfied"] == []

    def test_ruff_edit_is_not_hashed(self) -> None:
        out = mod.audit_manifest(RUFF_EDITED_MANIFEST, LOCK, IndexDouble())
        assert out["fresh"] is True

    def test_added_dependency_makes_lock_stale(self) -> None:
        out = mod.audit_manifest(STALE_MANIFEST, LOCK, IndexDouble())
        assert out["fresh"] is False

    def test_lock_without_content_hash_is_stale(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK_NO_HASH, IndexDouble())
        assert out["fresh"] is False

    def test_default_groups(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK, IndexDouble())
        assert out["groups"] == ["dev", "main"]

    def test_only_main(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK, IndexDouble(), only=["main"])
        assert out["groups"] == ["main"]

    def test_with_optional_docs(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK, IndexDouble(), with_groups=["docs"])
        assert out["groups"] == ["dev", "docs", "main"]

    def test_without_dev(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK, IndexDouble(), without=["dev"])
        assert out["groups"] == ["main"]

    def test_unknown_group_raises(self) -> None:
        with pytest.raises(ValueError):
            mod.audit_manifest(MANIFEST, LOCK, IndexDouble(), with_groups=["nope"])

    def test_locked_version_outside_range(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK_BAD_RANGE, IndexDouble())
        assert out["unsatisfied"] == ["numpy: 3.1.0 outside >=1.26,<3.0.0"]

    def test_missing_from_lock(self) -> None:
        out = mod.audit_manifest(MANIFEST, LOCK_MISSING, IndexDouble())
        assert out["unsatisfied"] == ["pydantic: missing from lock"]

    def test_sizes_and_fetch_budget(self) -> None:
        fetch = IndexDouble()
        out = mod.audit_manifest(MANIFEST, LOCK, fetch)
        direct = ["numpy", "pydantic", "pytest"]
        all_names = ["mkdocs", "numpy", "pydantic", "pytest"]
        assert out["direct_size_mb"] == pytest.approx(sum(_size(n) for n in direct))
        assert out["total_size_mb"] == pytest.approx(sum(_size(n) for n in all_names))
        assert out["fetches"] == 4
        assert len(fetch.calls) == 4

    def test_only_main_shrinks_direct_size_not_fetches(self) -> None:
        fetch = IndexDouble()
        out = mod.audit_manifest(MANIFEST, LOCK, fetch, only=["main"])
        assert out["direct_size_mb"] == pytest.approx(_size("numpy") + _size("pydantic"))
        assert out["fetches"] == 4

    def test_result_is_deterministic(self) -> None:
        first = mod.audit_manifest(MANIFEST, LOCK, IndexDouble())
        second = mod.audit_manifest(MANIFEST, LOCK, IndexDouble())
        assert first == second
