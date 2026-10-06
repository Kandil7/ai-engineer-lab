# Challenge 40: uv — The Reproducible Environment

A universal `uv.lock` records every platform's wheels with sha256 hashes,
and `uv audit` gates CI on what that lock contains. This set builds the
three pieces of that machinery you can exercise offline: wheel-tag
selection, an index that answers many queries without re-parsing, and a
lock auditor that streams instead of materializing.

## Bronze — Wheel Tag Parser (~15 min)

**Task:** Implement `wheel_tags(filename)` splitting
`name-version-pythontag-abitag-platformtag.whl` into its components.
Distribution names are normalized to `_`, so a plain split on `-` is safe.
Anything not ending in `.whl`, or with fewer than 5 dash-separated parts,
raises `ValueError`.

**Signature:**
```python
def wheel_tags(filename: str) -> dict
```

| Input | Expected |
|---|---|
| `"numpy-1.26.4-cp312-cp312-win_amd64.whl"` | `{"name": "numpy", "version": "1.26.4", "python_tag": "cp312", "abi_tag": "cp312", "platform_tag": "win_amd64"}` |
| `"ruff-0.5.0-py3-none-any.whl"` | `{"name": "ruff", "version": "0.5.0", "python_tag": "py3", "abi_tag": "none", "platform_tag": "any"}` |
| `"my_pkg-1.0.0-cp39-abi3-manylinux_2_17_x86_64.whl"` | name `"my_pkg"`, platform `"manylinux_2_17_x86_64"` |
| `"setup.txt"` | `ValueError` |
| `"x-1.0.whl"` | `ValueError` |

**Constraints:** no regex required, no network. Any correct approach
passes — this tier is mechanics.

---

## Silver — Wheel Index (~35 min)

**Task:** Implement `WheelIndex(wheels, parse)` with
`select(python_tag, platform_tag) -> list[str]`. The `parse` callable is
injected so tests can count how often filenames are parsed. The production
rule: **each filename is parsed once for the index's lifetime** — parsing
happens at construction, and every query scans pre-parsed tags.

Selection rules (simplified PEP 425):

- **python:** exact tag match (`cp312`), the pure `py3` tag, or an `abi3`
  wheel built for an older-or-equal CPython of the same implementation
  (`cp39-abi3` runs on `cp312`; `cp313-abi3` does not).
- **abi:** the interpreter's own tag, `abi3`, or `none`.
- **platform:** exact match or `any`.

Matching wheels are returned in the order they were listed.

**Signature:**
```python
class WheelIndex:
    def __init__(self, wheels: list[str], parse: Callable[[str], dict]) -> None: ...
    def select(self, python_tag: str, platform_tag: str) -> list[str]: ...
```

| Input wheels | Query | Expected |
|---|---|---|
| cp312/win, cp39-abi3/win, py3/any, cp312/linux, cp311/win | `("cp312", "win_amd64")` | first three, in order |
| cp39-abi3/win, cp313-abi3/win | `("cp312", "win_amd64")` | only the cp39 wheel |
| `[]` | any | `[]` |
| cp312/win only | `("cp39", "linux_x86_64")` | `[]` |

**Guard (measured):** the test builds 200 wheels and runs 100 `select`
queries through a counting parser. Parsing per query costs about 20,000
parse calls; the budget is `len(wheels) + 5`. Parse once at construction,
not once per query.

---

## Gold — Streaming Lock Auditor (~75 min)

**Task:** Implement `audit_stream(packages, advisories, ignore)` and
`audit_exit_code(findings)`. `packages` is an *iterable* of
`{"name": str, "version": str}` — consume it incrementally. `advisories`
maps package name to a list of `{"id": str, "fixed_in": str | None}`. A
version is vulnerable when it is older than `fixed_in` (numeric component
comparison, so `2.10.0` is not below `2.9.9`); `fixed_in: None` means no
fix is available. Findings are returned sorted, with ids in `ignore`
dropped. `audit_exit_code` returns `1` when findings exist, `0` otherwise —
the CI contract.

Finding format: `"{name}=={version} {id} (fixed in {fixed_in})"` or
`"{name}=={version} {id} (no fix available)"`.

**Signature:**
```python
def audit_stream(
    packages: Iterable[dict],
    advisories: dict[str, list[dict]],
    ignore: frozenset[str] | set[str] = frozenset(),
) -> list[str]: ...


def audit_exit_code(findings: list[str]) -> int: ...
```

| Scenario | Expected |
|---|---|
| version below `fixed_in` | finding `(fixed in X)` |
| version equal to `fixed_in` | no finding |
| `2.10.0` vs `fixed_in 2.9.9` | no finding (numeric, not string, compare) |
| `fixed_in: None` | finding `(no fix available)` |
| advisory id in `ignore` | dropped |
| advisories for a package not in the lock | ignored |
| empty package stream | `[]` |

**Guard (measured):** the test streams 20,000 packages under
`tracemalloc` and asserts peak memory stays under 1 MB. A solution that
does `packages = list(packages)` first holds the whole lock in memory
(about 5 MB of dicts) and fails. Consume one package at a time; sort the
small findings list at the end.

---

## Follow-up

At 10^9 packages, what breaks first: the memory ceiling or the advisory
lookup? Describe the audit policy you would ship (chunked batches?
incremental OSV queries? a persistent findings database?) and what it
costs the night a new advisory lands for a package deep in the lock.
*(Answer sketch: the advisory lookup breaks first — memory can be streamed
away, but a per-package OSV query at that scale is a network problem, not a
compute one. Batch queries by package name with a local advisory cache
keyed by lock hash; the cost of a new advisory is one incremental scan over
the cached names, not a full re-audit.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/40-uv/test_challenge.py -q
# validate the reference solution:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/40-uv/test_challenge.py -q
```

## Test File Structure

```
challenges/40-uv/
├── README.md          # This file
├── starter.py         # Signatures only, bodies raise NotImplementedError
├── solution.py        # Reference implementation
├── quiz.md            # 8 recall questions + answer key
└── test_challenge.py  # Tests (default: run against starter.py)
```
