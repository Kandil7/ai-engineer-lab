# Poetry - Glossary 39

## Quick Reference Table

| Term | One-Liner |
|------|-----------|
| build backend | The library that turns your source into a wheel; Poetry's is `poetry-core` |
| caret (`^`) | Constraint meaning "compatible within the same leftmost non-zero digit" |
| content hash | SHA-256 of the resolution-relevant part of `pyproject.toml`, stored in the lock |
| dependency group | A named set of development-only dependencies, never shipped |
| extras | Optional dependency sets published inside the package for users |
| lockfile | The resolved, hash-pinned dependency graph (`poetry.lock`) |
| package-mode | Poetry setting marking whether the project itself is installable |
| PEP 508 | The standard grammar for requirement specifiers |
| PEP 621 | The standard `[project]` metadata table in `pyproject.toml` |
| PEP 735 | The standard `[dependency-groups]` table |
| plugin | An add-on providing commands Poetry no longer bundles (`export`, `shell`) |
| resolution | Choosing one version per package that satisfies every constraint at once |
| source | A package index Poetry may install from, with a priority |
| sync | Install the locked graph and remove anything not in it |
| tilde (`~`) | Constraint allowing only the rightmost mentioned digit to grow |
| uv | A Rust dependency manager that also resolves into a lockfile |
| virtualenv | The isolated interpreter environment Poetry creates per project |

## Detailed Definitions

### build backend

The library PEP 517 invokes to build your distribution. Under Poetry it is
`poetry-core`, declared in `[build-system]`:

```toml
[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

PEP 517 says a tool should fall back to `setuptools` when no build system is
declared; Poetry currently warns and still uses `poetry-core`.

### caret

Poetry constraint operator. The leftmost non-zero component may grow by one,
everything after it resets:

```python
expand_constraint("^1.2.3")  # ('>=1.2.3', '<2.0.0')
expand_constraint("^0.2.3")  # ('>=0.2.3', '<0.3.0')
expand_constraint("^0.0.3")  # ('>=0.0.3', '<0.0.4')
```

Caret is rejected inside `[project] dependencies` — that table is PEP 508 only.

### content hash

Digest stored under `[metadata] content-hash` in `poetry.lock`, computed over the
manifest fields that can change resolution — dependency tables, groups,
`requires-python`, sources — and not over unrelated configuration:

```python
import hashlib, json
digest = hashlib.sha256(json.dumps(relevant, sort_keys=True).encode()).hexdigest()
```

`poetry check --lock` recomputes it and fails when the stored value differs.

### dependency group

A named, development-only dependency set. Declared in
`[tool.poetry.group.<name>]` or the PEP 735 `[dependency-groups]` table, never
shipped in the wheel:

```toml
[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = ">=1.6"
```

Non-optional groups install by default; optional ones need `--with`.

### extras

Optional dependency sets that travel *inside* the package, so users can opt in:

```toml
[project.optional-dependencies]
qdrant = ["qdrant-client (>=1.9,<2.0.0)"]
```

```bash
pip install rag-utils[qdrant]     # user side
poetry install -E qdrant          # developer side
```

### lockfile

`poetry.lock`: every package the resolver selected, its exact version, Python
constraint and file hashes:

```toml
[[package]]
name = "numpy"
version = "1.26.4"
files = [{file = "numpy-1.26.4-…whl", hash = "sha256:…"}]
```

It is generated, reviewed in diffs, and committed. Hand-editing it breaks the
content hash and the hashes inside it.

### package-mode

`[tool.poetry] package-mode = false` marks a repository Poetry should manage but
never try to install as a package — services, script collections, monorepo tooling.
It removes the "project cannot be installed" error and pairs with
`poetry install --no-root`.

### PEP 508

The grammar requirement specifiers must follow inside `[project]`:

```toml
dependencies = ["numpy (>=1.26,<3.0.0)", "pydantic>=2.5"]
```

No `^`, no `~`, and a bare `1.2.3` is exact.

### PEP 621

The standard `[project]` table for package metadata. Supported since Poetry 2.0
(2025-01-05), and the layout `poetry init` produces by default:

```toml
[project]
name = "rag-utils"
version = "1.2.0"
requires-python = ">=3.10"
dependencies = ["numpy (>=1.26,<3.0.0)"]
```

### PEP 735

The standard `[dependency-groups]` table, readable by Poetry and other tools:

```toml
[dependency-groups]
lint = ["mypy (>=1.11,<2.0.0)"]
```

Mark a group optional with the companion `[tool.poetry.group.<name>] optional = true`.

### plugin

A separate package adding commands to Poetry. Since 2.0 the core no longer ships
`export` or `shell`:

```bash
poetry self add poetry-plugin-export
poetry self add poetry-plugin-shell
poetry export -f requirements.txt -o requirements.txt
```

A project can declare what it needs:

```toml
[tool.poetry.requires-plugins]
poetry-plugin-export = ">=1.8"
```

### resolution

The solver step: choose one version per package such that every constraint in
the graph holds simultaneously. Its result is written to `poetry.lock`. Re-running
resolution with the same inputs gives the same graph; `poetry lock` keeps existing
versions, `poetry lock --regenerate` starts over.

### source

A package index, declared with a priority:

```toml
[[tool.poetry.source]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
priority = "explicit"
```

`primary` replaces implicit PyPI, `supplemental` is a fallback, `explicit` is
opt-in per dependency, `legacy` is an old-style repository.

### sync

`poetry sync` installs the locked graph and *uninstalls* anything not in it, so an
environment cannot accumulate leftovers from an earlier state:

```bash
poetry sync --only main --no-root
```

It replaced `poetry install --sync` in Poetry 2.0.

### tilde

Poetry constraint operator allowing only the rightmost mentioned component to
grow:

```python
expand_constraint("~1.2.3")  # ('>=1.2.3', '<1.3.0')
expand_constraint("~1.2")    # ('>=1.2.0', '<1.3.0')
expand_constraint("~1")      # ('>=1.0.0', '<2.0.0')
```

### uv

Rust tooling that resolves, locks and installs, and also manages Python versions.
`uv sync` installs from `uv.lock` the way `poetry install` installs from
`poetry.lock`. Much faster; less mature plugin ecosystem. The lockfile, not the
tool, is what provides reproducibility.

### virtualenv

The isolated interpreter environment Poetry creates and caches per project, then
enters with `poetry run`. Configuration such as `virtualenvs.in-project` and
`virtualenvs.path` lives in `poetry.toml` (via `poetry config --local`) or in the
global Poetry config.

## Key Concepts Summary

### Intent Versus Decision

`pyproject.toml` records what you are willing to accept. `poetry.lock` records
what was chosen. Reviewing a dependency change means reviewing the manifest diff;
reproducing a run means pinning the lock.

### Freshness Is a Hash Comparison

A lockfile is stale exactly when its stored content hash no longer matches a
recomputed one. Dependency edits change the hash; tooling config does not. That
is why `poetry check --lock` is a cheap CI gate.

### Groups Are For You, Extras Are For Users

Groups never leave the repository. Extras ship in wheel metadata so downstream
users can opt in. Confusing them produces either a bloated published package or a
development environment missing its test runner.

## Practice Terms

1. What does `dependencies = ["numpy 1.2.3"]` in `[project]` mean compared with
   `tool.poetry.dependencies = {numpy = "1.2.3"}`? (Both are exact: confirm you
   are reading neither as a caret range.)
2. Write the group layout you would use for a repository that has a runtime
   service, a CLI, docs and benchmarks.
3. Which files must change when you add a dependency, and which command proves
   they agree?
4. Name two things that make `poetry check --lock` fail and one that does not.
5. When would you choose `--only main` over `package-mode = false`?
