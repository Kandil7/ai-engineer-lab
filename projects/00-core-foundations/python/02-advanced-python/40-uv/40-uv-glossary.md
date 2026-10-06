# uv - Glossary 40

## Quick Reference Table

| Term | One-Liner |
|------|-----------|
| abi3 | Wheel ABI tag allowing one binary to serve every later CPython 3.x |
| adverse status | PEP 792 project state (deprecated, archived, quarantined) reported by `uv audit` |
| constraint | A version restriction applied only when the package is requested anyway |
| cooldown | An `exclude-newer` cutoff giving fresh releases a review window |
| dependency group | A named development-only dependency set (PEP 735), never shipped |
| exact sync | `uv sync` default: remove packages the lock does not list |
| extras | Optional dependency sets shipped inside the package for users |
| frozen | Install from the existing lock without resolving (`--frozen`) |
| locked | Fail when syncing would change the lockfile (`--locked`) |
| lockfile | The resolved, hash-pinned, universal dependency graph (`uv.lock`) |
| malware check | Opt-in `UV_MALWARE_CHECK=1` OSV MAL lookup that aborts sync |
| manifest | The `[manifest]` section of `uv.lock` recording direct requirements |
| override | Force a version against declared ranges; last resort |
| PEP 508 | The standard grammar for requirement specifiers |
| PEP 621 | The standard `[project]` metadata table in `pyproject.toml` |
| PEP 735 | The standard `[dependency-groups]` table |
| PEP 751 | The standardized `pylock.toml` resolution format |
| pipreqs | Tool deriving requirements from source imports; run via `uvx` |
| pylock.toml | Tool-agnostic lockfile format uv can export and install |
| resolution | Choosing one version per package satisfying every constraint at once |
| source | A package index uv may install from, optionally `explicit` |
| universal lockfile | One `uv.lock` covering every OS, arch and Python version |
| uv audit | Preview command scanning the lock for vulnerabilities |
| uvx | Alias for `uv tool run`: ephemeral tool environments |
| virtualenv | The `.venv` uv creates next to `pyproject.toml` |
| wheel tag | The `python-abi-platform` suffix selecting installable wheels |

## Detailed Definitions

### abi3

The stable ABI tag. A wheel tagged `cp39-abi3` runs on CPython 3.9 and every
later 3.x, so a universal lockfile can serve new interpreters without a
rebuild:

```python
select_wheels(["x-1.0-cp39-abi3-win_amd64.whl"], "cp312", "win_amd64")
# ['x-1.0-cp39-abi3-win_amd64.whl']
```

### adverse status

A PEP 792 project state on the index: `deprecated`, `archived` or
`quarantined`. `uv audit` reports them alongside vulnerabilities because a
quarantined dependency is an emergency even with no CVE attached.

### constraint

`[tool.uv] constraint-dependencies` restricts the versions a package may
resolve to, without causing it to be installed:

```toml
[tool.uv]
constraint-dependencies = ["grpcio<1.65"]
```

The package must still be requested by a real dependency. Contrast with
override.

### cooldown

The operational name for `exclude-newer`: a resolution-time cutoff that
ignores uploads newer than the date, so fresh releases get a review window
before they can enter your lockfile:

```toml
[tool.uv]
exclude-newer = "2026-06-01T00:00:00Z"
exclude-newer-package = { setuptools = false }   # per-package opt-out
```

It is not a pin; the lockfile is what actually pins.

### dependency group

A named, development-only dependency set in the PEP 735 table, never shipped
in the wheel:

```toml
[dependency-groups]
dev = ["pytest>=8.0"]
lint = ["mypy>=1.11"]
```

`dev` is uv's default group and installs without flags; other groups need
`--group` or `--all-groups`.

### exact sync

`uv sync` removes packages present in `.venv` but absent from the lock, so
drift from earlier experiments cannot survive. `--inexact` opts out. This is
the uv equivalent of `poetry sync`.

### extras

Optional dependency sets that travel *inside* the package, so users can opt
in:

```toml
[project.optional-dependencies]
qdrant = ["qdrant-client>=1.9,<2.0.0"]
```

```bash
pip install rag-utils[qdrant]   # user side
uv sync --extra qdrant          # developer side
```

### frozen

`uv sync --frozen` installs from the existing `uv.lock` without performing
resolution at all. Fast, but it will happily install a lock that no longer
matches the manifest. Contrast with locked.

### locked

`uv sync --locked` / `uv audit --locked` resolve (or audit) and fail when the
result would change `uv.lock`. The CI flag: it proves the lock is fresh.

### lockfile

`uv.lock`: every package the resolver selected, its exact version, source,
and every platform's wheels with sha256 hashes. Generated, reviewed in
diffs, committed. Hand-editing it is always wrong.

### malware check

Opt-in sync-time defense. With `UV_MALWARE_CHECK=1`, every `uv add` / `uv
sync` queries OSV for MAL advisories against the locked resolution and
aborts *before* installing anything with a known-malware match:

```bash
UV_MALWARE_CHECK=1 uv sync
```

Needed because PyPI quarantine removes a distribution from the index but not
from object storage, so a lockfile can still point at it.

### manifest

Two meanings, both in play: the *project manifest* is `pyproject.toml`
(intent); the *lock manifest* is the `[manifest]` section of `uv.lock`
recording the direct requirements the lock was built from. Freshness is
comparing the two.

### override

`[tool.uv] override-dependencies` forces a version even against declared
ranges. Last resort for unfixable transitive conflicts: the resulting graph
may never have been tested upstream.

### PEP 508

The grammar requirement specifiers follow inside `[project]`:

```toml
dependencies = ["numpy>=1.26,<3.0.0"]
```

No `^`, no `~`, and a bare `1.2.3` is exact. uv has no second syntax table.

### PEP 621

The standard `[project]` table for package metadata. uv reads it natively;
`uv init` emits it.

### PEP 735

The standard `[dependency-groups]` table for development-only dependency
sets, shared across tooling.

### PEP 751

The standardized `pylock.toml` resolution format: tool-agnostic, installable
by any compliant tool. uv exports to it and accepts it in the `uv pip`
interface, but keeps the richer `uv.lock` for projects.

### pipreqs

Third-party tool that derives a requirements list from a source tree's
imports — the starting point when a legacy project has no manifest. Run
without installing via uvx:

```bash
uvx pipreqs . --mode no-pin
```

`--mode no-pin` avoids inventing exact pins; `--diff` audits an existing
requirements file against real usage.

### pylock.toml

See PEP 751.

### resolution

The solver step: choose one version per package such that every constraint
in the graph holds simultaneously. Its result is written to `uv.lock`.
`uv lock` keeps existing versions; `uv lock --upgrade` re-resolves upward.

### source

A package index, declared with a name and optionally `explicit`:

```toml
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cpu" }
```

An explicit index serves only dependencies that name it.

### universal lockfile

The defining property of `uv.lock`: one file records the resolution for
every OS, architecture and Python version in `requires-python`. Each
machine selects its own wheels at install time. Poetry locks
per-environment instead.

### uv audit

Preview command scanning the locked resolution against OSV for known
vulnerabilities and adverse project statuses. Exits non-zero on findings,
which makes it a CI gate:

```bash
uv audit --locked --output-format sarif
```

4-10x faster than `pip-audit` on typical projects because it reuses uv's
locked resolution and caching.

### uvx

Alias for `uv tool run`: execute a tool in a cached ephemeral environment
without installing it into any project:

```bash
uvx ruff check .
uvx pipreqs . --mode no-pin
```

### virtualenv

The `.venv` uv creates next to `pyproject.toml` (gitignored automatically).
`uv run` uses it and syncs it first; activation is optional.

### wheel tag

The `python-abi-platform` suffix of a wheel filename that decides whether it
is installable on a given interpreter:

```python
parse_wheel_filename("ruff-0.5.0-py3-none-win_amd64.whl")
# {'name': 'ruff', 'version': '0.5.0', 'python_tag': 'py3',
#  'abi_tag': 'none', 'platform_tag': 'win_amd64'}
```

## Key Concepts Summary

### Intent Versus Decision

`pyproject.toml` records what you are willing to accept. `uv.lock` records
what was chosen, for every platform at once. Reviewing a dependency change
means reviewing the manifest diff; reproducing a run means pinning the lock.

### Freshness Is a Manifest Comparison

A lockfile is stale exactly when its `[manifest] requirements` no longer
match the project's direct dependencies. `uv lock --check` is the CI gate;
`--locked` proves it at sync time; `--frozen` deliberately skips the check.

### Security Is Layered

Hashes catch substituted bytes at install time. `uv audit` catches known
vulnerabilities before deploy. `UV_MALWARE_CHECK` catches known malware
before it executes. `exclude-newer` buys review time for everything not yet
known. No single layer is sufficient.

## Practice Terms

1. What does `uv sync --frozen` do that `uv sync --locked` does not, and
   which one belongs in CI?
2. A dependency is declared in `[dependency-groups]` but never installs.
   Which flag is missing, and which group installs without any flag?
3. Write the `[tool.uv]` block that pins uv itself, applies a cooldown, and
   routes torch to a dedicated index.
4. Name two things `uv audit` reports besides CVEs, and one thing it does
   not cover.
5. When would you reach for `override-dependencies` instead of
   `constraint-dependencies`, and what risk does that choice add?
