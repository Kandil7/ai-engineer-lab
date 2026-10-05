# Challenge 39: Poetry — The CI Dependency Gate

A model-serving repo's CI must answer three questions before it installs
anything: which dependency groups this job needs, whether `poetry.lock` still
matches `pyproject.toml`, and how many index lookups the audit is allowed to
make. Answer all three without touching the network.

## 🥉 Bronze — Constraint Expansion (~15 min)

**Task:** Implement `expand_constraint(spec)` returning a `(lower, upper)` pair
of PEP 508 specifier strings. An empty string means unbounded on that side.

**Signature:**
```python
def expand_constraint(spec: str) -> tuple[str, str]
```

| Input | Expected |
|---|---|
| `"^1.2.3"` | `(">=1.2.3", "<2.0.0")` |
| `"^0.2.3"` | `(">=0.2.3", "<0.3.0")` |
| `"^0.0.3"` | `(">=0.0.3", "<0.0.4")` |
| `"~1.2.3"` | `(">=1.2.3", "<1.3.0")` |
| `"1.2.3"` | `("==1.2.3", "")` (bare version is exact) |
| `"1.2.*"` | `(">=1.2.0", "<1.3.0")` |
| `"~=1.2"` | `(">=1.2.0", "<2.0.0")` |
| `">=1.26,<3.0.0"` | `(">=1.26", "<3.0.0")` |
| `""` | `("", "")` |
| `"!=1.2.3"` | raises `ValueError` |

**Constraints:** the caret rule is "leftmost non-zero digit may grow by one,
everything right of it resets" — which is why `^0.2.3` stops at `0.3.0` while
`^1.2.3` stops at `2.0.0`. Any correct approach passes.

---

## 🥈 Silver — Install Closure (~35 min)

**Task:** Implement `install_closure(locked, roots)`: every package reachable
from `roots` through `dependencies`, roots included, returned sorted ascending.
Names not present in `locked` are still returned (they resolve at install time).

**Signature:**
```python
def install_closure(locked: list[dict], roots: list[str]) -> list[str]
```

| Input | Expected |
|---|---|
| `A -> [B, C]`, `B -> [D]`, roots `["A"]` | `["A", "B", "C", "D"]` |
| roots naming a package absent from `locked` | that name alone |
| roots `[]` | `[]` |
| cycle `A -> [B]`, `B -> [A]` | `["A", "B"]` (must terminate) |
| 2000-package chain, root **last** in the list | all 2000 names, sorted |

**Constraints:** `locked` is `{"name": str, "dependencies": list[str]}`. The
tests wrap every `name` in a string subclass that counts `__eq__` calls and
assert the total stays under `10 * len(locked)` across the whole run. Looking a
package up by scanning the list (`next(p for p in locked if p["name"] == n)`)
is O(n) per node, O(n²) total, and must fail the budget at n=2000 — the
adversarial case is that chain with the root at the **end** of the list, so every
lookup scans the whole thing first. Build an index once instead.

---

## 🥇 Gold — The Audit (~75 min)

**Task:** Implement `audit_manifest(pyproject_text, lock_text, fetch_meta, ...)`
returning one dict:

```python
{
    "fresh": bool,  # lock agrees with the manifest
    "groups": list[str],  # sorted install set for the flags
    "unsatisfied": list[str],  # sorted dependency problems, [] when clean
    "direct_size_mb": float,  # size of direct dependencies
    "total_size_mb": float,  # size of every package in the lock
    "fetches": int,  # calls made to fetch_meta
}
```

**Signature:**
```python
def audit_manifest(
    pyproject_text: str,
    lock_text: str,
    fetch_meta,
    *,
    only: list[str] | None = None,
    with_groups: list[str] | None = None,
    without: list[str] | None = None,
) -> dict
```

Semantics, exactly:

- **`groups`** — `main` plus every non-optional group; `with_groups` adds,
  `without` removes, `only` replaces the whole set. Unknown names raise
  `ValueError`. A group is optional when `[tool.poetry.group.<name>]` sets
  `optional = true`.
- **`fresh`** — `sha256(json.dumps(relevant, sort_keys=True))` over
  `{"project": {name, version, description, requires-python, dependencies,
  optional-dependencies}, "dependency-groups": ..., "tool": {"poetry": {source,
  extras, dev-dependencies, group, dependencies}}}`, skipping empty sections,
  compared with `[metadata] content-hash`. Editing `[tool.ruff]` must **not**
  make it stale.
- **`unsatisfied`** — for every direct dependency and every dependency of the
  selected groups: `"<name>: missing from lock"` when absent, else
  `"<name>: <version> outside <spec>"` when the locked version falls outside
  the expanded constraint. Direct dependencies are PEP 508 strings.
- **`fetch_meta(name) -> float`** returns a package size in MB. It is a fake
  index client that **raises on a second call for the same name**. Call it once
  per unique name across the whole audit (`direct ∪ locked`), never twice.

| Input | Expected |
|---|---|
| pristine manifest + matching lock | `fresh=True`, `unsatisfied=[]` |
| `[tool.ruff] line-length` changed | `fresh=True` (not hashed) |
| a dependency added to `[project]` | `fresh=False` |
| default flags | `groups == ["dev", "main"]` |
| `only=["main"]` | `groups == ["main"]` |
| `with_groups=["docs"]` | `groups == ["dev", "docs", "main"]` |
| locked `numpy` bumped to `3.1.0` | `"numpy: 3.1.0 outside >=1.26,<3.0.0"` |
| any call pattern | `fetches == unique(direct \| locked)` |

**Constraints:** sizes and names are deterministic; sums are taken in sorted
name order so the floats are reproducible. **The guard is the fetch budget** —
a natural implementation that computes `direct_size_mb` in one loop over direct
dependencies and `total_size_mb` in a second loop over the lock fetches every
direct package twice, which the index double rejects. Fetch once into a cache,
then sum. **Follow-up:** at 10^9 index lookups a day, what breaks first?
*(Answer: the round-trip itself — key the size cache on the lock's content hash
for the day. The wheel hashes already live in the lock, so the size lookup only
feeds a budget report.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/39-poetry/test_challenge.py -q
# validate the reference solution:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/39-poetry/test_challenge.py -q
```

## Test File Structure

```
challenges/39-poetry/
├── README.md          # This file
├── starter.py         # Signatures only, bodies raise NotImplementedError
├── solution.py        # Reference implementation
└── test_challenge.py  # Tests (default: run against starter.py)
```
