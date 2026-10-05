# Advanced Python - 39: Poetry

## Topic Overview

Poetry is a dependency manager and packaging tool for Python. It owns four jobs
that pip, setuptools and venv each used to do separately: resolving a dependency
graph, writing it to a lockfile, creating an isolated environment, and installing
exact wheels into it. The output artifacts are `pyproject.toml` (intent) and
`poetry.lock` (decision).

The distinction between those two files is the whole topic. `pyproject.toml` says
"some compatible range of numpy"; `poetry.lock` says "1.26.4, hash `sha256:…`".
A training run, an eval harness, and a CI job all read the second file, so they
get the same bytes. Without a lockfile every machine resolves independently and
the numbers you compare across runs are not comparable.

This topic stays offline. Poetry itself is a network tool, but everything that
decides *what gets installed* is pure string and dict work: parse the manifest,
expand a constraint, pick the groups, hash the relevant fields, compare versions.
Those are the parts we exercise with `tomllib` and `hashlib`.

## Learning Objectives

- Explain what `poetry.lock` guarantees and what it does not.
- Read a Poetry 2.x `pyproject.toml` and say which table each field belongs to.
- Expand `^`, `~`, `*`, `~=` and bare versions into explicit lower/upper bounds.
- Distinguish dependency groups from extras and predict the install set for a
  given `--with` / `--without` / `--only` combination.
- Recompute a lockfile content hash and decide whether a lockfile is stale.
- Choose between Poetry, uv and pip-tools for a given project.

## Prerequisites

- Topic 27: `pyproject.toml`, specifiers, semver, lockfile concept.
- Topic 28: virtual environments.
- Comfort reading TOML via `tomllib` (Python 3.11+, used here as a parser only).

## 1. What Poetry Actually Owns

Poetry is one program covering a four-stage pipeline:

| Stage | Command | Artifact |
|-------|---------|----------|
| Declare | edit `pyproject.toml` | intent |
| Resolve | `poetry lock` / `poetry add` | `poetry.lock` |
| Isolate | auto-created virtualenv | `.venv` under the platform cache dir |
| Install | `poetry install` | wheels in the virtualenv |

Two properties are worth internalizing:

- **Resolution is a solver, not a loop.** Poetry picks one version per package
  that satisfies *every* constraint in the graph at once. `pip install a && pip
  install b` is sequential and can produce a set neither project asked for.
- **The lockfile is the reproducibility contract.** Commit it. A lockfile in
  `.gitignore` is decoration.

## 2. pyproject.toml Under Poetry 2.x

Poetry 2.0 (2025-01-05) added support for the standard `[project]` table from
PEP 621, and current `poetry init` / `poetry new` emit that layout by default.
`[tool.poetry]` still works and remains the only home for Poetry-specific
features. Both tables in one file is normal:

```toml
[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

[project]                                  # PEP 621: standard metadata
name = "rag-utils"
version = "1.2.0"
requires-python = ">=3.10"
dependencies = [                            # PEP 508 strings only
    "numpy (>=1.26,<3.0.0)",
]

[project.optional-dependencies]            # extras, shipped with the package
qdrant = ["qdrant-client (>=1.9,<2.0.0)"]

[tool.poetry]                              # Poetry-native fields
package-mode = true
requires-poetry = ">=2.0"

[tool.poetry.group.dev.dependencies]       # groups, never shipped
pytest = ">=8.0"
```

Rules that bite people:

- `project.dependencies` accepts **PEP 508 only**. `^1.2.3` is rejected, and a
  bare `"1.2.3"` means *exactly* 1.2.3.
- `tool.poetry.dependencies` accepts Poetry syntax: `^`, `~`, `*`, markers,
  git/path sources, `optional = true` entries. Poetry does not deprecate this
  table because PEP 508 cannot express all of it.
- Declaring the same dependency in both tables produces a warning; the
  `[project]` value wins.
- Many `[tool.poetry]` metadata fields (description, license, authors) are
  deprecated in favour of their `[project]` counterparts. `poetry check` lists
  them.

## 3. Constraint Syntax

The expansion rules, from the official dependency specification:

| Written | Means |
|---------|-------|
| `^1.2.3` | `>=1.2.3,<2.0.0` |
| `^1.2` | `>=1.2.0,<2.0.0` |
| `^1` | `>=1.0.0,<2.0.0` |
| `^0.2.3` | `>=0.2.3,<0.3.0` |
| `^0.0.3` | `>=0.0.3,<0.0.4` |
| `^0.0` | `>=0.0.0,<0.1.0` |
| `^0` | `>=0.0.0,<1.0.0` |
| `~1.2.3` | `>=1.2.3,<1.3.0` |
| `~1.2` | `>=1.2.0,<1.3.0` |
| `~1` | `>=1.0.0,<2.0.0` |
| `1.2.3` | `==1.2.3` (exact, not a range) |
| `*` | `>=0.0.0` |
| `1.2.*` | `>=1.2.0,<1.3.0` |
| `~=1.2.3` | `>=1.2.3,<1.3.0` (PEP 440) |
| `~=1.2` | `>=1.2.0,<2.0.0` (PEP 440) |

The caret rule in one sentence: the leftmost non-zero component may only grow by
one, everything to its right resets to zero. That is why `^0.2.3` is bounded by
`0.3.0` and `^0.0.3` by `0.0.4` — for a `0.x` package the minor digit is already
the breaking-change digit.

`expand_constraint()` in this topic's exercise implements exactly this table and
`_verify()` asserts it row by row.

## 4. Dependency Groups vs Extras

They answer different questions:

| | Extra | Dependency group |
|---|-------|------------------|
| Declared in | `project.optional-dependencies` / `tool.poetry.extras` | `tool.poetry.group.<name>` or `[dependency-groups]` |
| Shipped? | Yes, in wheel metadata as `Requires-Dist` with an extra marker | No |
| Audience | Users of your package | Developers of your package |
| Selected with | `-E name`, `--all-extras` | `--with`, `--without`, `--only` |

A group is installed by default unless it is marked optional:

```toml
[dependency-groups]
dev = ["pytest (>=8.0,<9.0.0)"]
docs = ["Sphinx (>=5.1.1,<6.0.0)"]

[tool.poetry.group.docs]
optional = true          # now requires `poetry install --with docs`
```

`dev` is non-optional, so plain `poetry install` includes it. `docs` is not.
The flag lives in `[tool.poetry.group.<name>]` even when the dependencies come
from the PEP 735 `[dependency-groups]` table — that combination is documented and
intentional.

Group semantics for `groups_to_install()` in the exercise:

- default: every non-optional group plus `main`
- `--with g`: add optional group `g`
- `--without g`: drop non-optional group `g`
- `--only g`: install exactly `g`, ignoring `--with` / `--without`
- `--all-groups`: every declared group

## 5. The Install Flag Surface

```console
poetry install                       # main + all non-optional groups
poetry install --with docs           # add an optional group
poetry install --without lint        # drop a group
poetry install --only main           # runtime deps alone (Docker multi-stage)
poetry install --all-groups          # everything declared
poetry install -E qdrant --all-extras
poetry install --no-root             # skip installing the project itself
poetry sync                          # install + uninstall what is not in the lock
poetry run pytest                    # run inside the project virtualenv
```

`--no-root` is the flag that matters most in CI: without it Poetry also tries to
install your own package, which fails for a project with no buildable package
layout. Pair it with `package-mode = false` for applications and tooling-only
repositories.

## 6. Anatomy of poetry.lock

```toml
# This file is automatically @generated by Poetry 2.5.0 and should not be
# changed by hand.

[[package]]
name = "numpy"
version = "1.26.4"
optional = false
python-versions = ">=3.9"
files = [
    {file = "numpy-1.26.4-cp312-cp312-win_amd64.whl", hash = "sha256:…"},
]

[metadata]
lock-version = "2.1"
python-versions = ">=3.10"
content-hash = "cfba36c4…"
```

What each field buys you:

- `version` — the resolution decision. Not a range.
- `files[].hash` — install-time integrity check. A wheel whose bytes changed is
  rejected even if the version string matches.
- `lock-version` — the lock schema, not your package version.
- `content-hash` — fingerprints the *relevant* part of `pyproject.toml`.

Never hand-edit it. Regenerate with `poetry lock` (keeps existing versions) or
`poetry lock --regenerate` (throws the old resolution away).

## 7. The Content Hash

Poetry hashes a subset of the manifest — the fields that can change resolution —
and stores the digest under `[metadata]`. Dependency tables, `requires-python`,
`dependency-groups` and sources are in. Tool configuration such as `[tool.ruff]`
is out. The algorithm is `sha256(json.dumps(relevant, sort_keys=True))`, where
`relevant` is assembled in `src/poetry/packages/locker.py`.

The consequence is the rule people learn the hard way:

- Adding or bumping a dependency → hash changes → lockfile is **stale**.
- Reformatting, renaming a project, or editing linter config → hash unchanged.

Verification is one command:

```console
poetry check --lock
```

It fails when `poetry.lock` is missing or its `content-hash` no longer matches.
Plain `poetry check` already fails on a *stale* lockfile; the `--lock` flag adds
the missing-lockfile case, which is what CI wants. This is the check to wire into
a pipeline before `poetry install`.

The exercise reproduces the algorithm: `content_hash()` on a parsed manifest,
`lock_is_fresh()` comparing it to the stored digest, and `_verify()` asserting
that a dependency edit flips freshness to `False` while a `[tool.ruff]` edit does
not.

## 8. Sources and Priorities

```toml
[[tool.poetry.source]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
priority = "explicit"
```

| Priority | Meaning |
|----------|---------|
| `primary` | Can satisfy any dependency; declaring one disables implicit PyPI |
| `supplemental` | Tried when the primary sources cannot satisfy a dependency |
| `explicit` | Only used when a dependency names it by `source` |
| `legacy` | Legacy repository (no JSON/simple API), lowest priority |

A dependency pins a source with `pytorch = {version = ">=2.0", source = "pytorch-cpu"}`.
Credentials live outside the file: `poetry config http-basic.<name>`, or
environment variables `POETRY_HTTP_BASIC_<NAME>_USERNAME` / `_PASSWORD`. Never
commit them.

Local configuration goes in `poetry.toml` next to `pyproject.toml` so the whole
team shares it — `poetry config --local virtualenvs.in-project true`.

## 9. What Moved in Poetry 2.0

Things that surprise people coming from Poetry 1.x:

- `poetry export` no longer ships in the core. Install `poetry-plugin-export`
  (`poetry self add poetry-plugin-export`).
- `poetry shell` moved to `poetry-plugin-shell`; `poetry env activate` is the
  built-in replacement.
- `poetry lock` now preserves existing versions by default; `--regenerate` is the
  old behaviour.
- `poetry sync` replaces `poetry install --sync`.
- Plugins a project requires can be declared in `[tool.poetry.requires-plugins]`
  and are installed automatically.
- Python 3.8 support was dropped in 2.0 (3.9 later); current releases target
  3.15.

## 10. Poetry vs uv vs pip-tools

All three solve the same problem with a committed lockfile; they differ in who
does the solving and how fast.

- **Poetry** — mature, batteries included (venv, build, publish, plugins), a
  large ecosystem of tutorials and CI examples. Slower than uv because parts of
  the pipeline still shell out.
- **uv** — Rust, dramatically faster installs, single binary, also does Python
  version management. `uv sync` plays the role of `poetry install`; both install
  from a lockfile.
- **pip-tools** — the minimal option: you keep hand-written `requirements.in`
  files, `pip-compile` emits `requirements.txt`. No venv management, no build.

The lockfile, not the tool, is what makes a run reproducible. Whichever you pick:
commit the lock, cache it by hash in CI, and install with `--frozen`-equivalent
behaviour so the installer cannot silently re-resolve.

## Common Mistakes to Avoid

### Mistake 1: caret syntax in `[project]`

```toml
# WRONG -- PEP 508 rejects '^'; poetry check fails
dependencies = ["requests ^2.31"]

# CORRECT -- PEP 508 range, or use [tool.poetry.dependencies] for '^'
dependencies = ["requests (>=2.31,<3.0.0)"]
```

### Mistake 2: reading a bare version as a range

```python
# WRONG -- '1.2.3' means ==1.2.3, so 1.2.4 is rejected
tool_poetry_deps = {"numpy": "1.2.3"}

# CORRECT -- say what you meant
tool_poetry_deps = {"numpy": "^1.2.3"}   # >=1.2.3,<2.0.0
```

### Mistake 3: gitignoring the lockfile

```bash
# WRONG -- every runner resolves independently
echo "poetry.lock" >> .gitignore

# CORRECT -- commit it; it is the reproducibility contract
git add poetry.lock
```

### Mistake 4: trusting a lockfile nobody checks

```bash
# WRONG -- CI installs without verifying freshness
poetry install --no-root

# CORRECT -- fail fast when pyproject.toml and poetry.lock disagree
poetry check --lock && poetry install --no-root
```

### Mistake 5: expecting the plugin commands to exist

```bash
# WRONG -- not bundled since Poetry 2.0
poetry export -f requirements.txt -o requirements.txt
poetry shell

# CORRECT -- install the plugins, or use the built-in equivalent
poetry self add poetry-plugin-export
poetry env activate
```

## Best Practices

- Commit `poetry.lock`; verify it with `poetry check --lock` in CI.
- Keep runtime dependencies in `[project]`, development tooling in groups.
- Mark anything heavyweight (docs, benchmarks, GPU stacks) as an optional group.
- Use `package-mode = false` for services and scripts you do not publish.
- Pin `requires-poetry` so the team agrees on the tool version.
- Prefer `poetry sync` in Docker/CI: it removes packages the lockfile does not
  list, which catches drift left behind by earlier layers.
- Pin a source with `priority = "explicit"` when only one dependency should come
  from it.

## Complexity and Cost

| Operation | Cost | Note |
|-----------|------|------|
| Constraint expansion | O(1) | String work, no solver |
| Group selection | O(G) | G = declared groups |
| Content hash | O(M) | M = size of relevant manifest |
| Freshness check | O(M) | Compare two 64-char hex strings |
| Version-in-range check | O(1) | Tuple comparison of padded components |
| Full resolution | O(P × C) worst case, solver-bound | P packages, C constraints; usually cached |
| First `poetry install` | Network + disk | Wheel downloads, hash verification |

Offline, everything in this topic is linear-time string and dict work. The solver
is the only expensive step, and the lockfile exists so you pay it once.

## AI Engineering Relevance

- **Experiment reproducibility.** An eval comparing model A and model B must run
  on identical library versions. A committed lockfile is the cheapest guarantee
  you have; `poetry check --lock` is the cheapest way to enforce it.
- **GPU environments.** Torch wheels come from a dedicated index. Configure it as
  an `explicit` source so only `torch` is pulled from it and everything else
  resolves against PyPI.
- **Splitting environments.** `--only main` in a slim inference image,
  `--with train` on the GPU box, one lockfile for both.
- **CI cost.** Cache the virtualenv keyed on the hash of `poetry.lock`. Cache key
  wrong (hashing `pyproject.toml` instead) and you reinstall every run.
- **Supply chain.** The per-file hashes in the lockfile are verified at install
  time; a substituted wheel fails the download rather than silently running.

## Practice Exercises

### Exercise 1: Parse the Manifest (Difficulty: Easy)
Read a `pyproject.toml` with `tomllib` and report which of `[project]`,
`[tool.poetry]`, `[dependency-groups]` are present and where a named dependency
was declared.

### Exercise 2: Constraint Expander (Difficulty: Medium)
Implement `expand_constraint(spec) -> (lower, upper)` for `^`, `~`, `*`, `~=`,
exact and comma-separated ranges. Assert the table in section 3.

### Exercise 3: Group Resolver (Difficulty: Medium)
Given `groups: dict[str, bool]` and the four flag arguments, return the sorted
install set. Raise on unknown group names.

### Exercise 4: Content Hash (Difficulty: Medium)
Reimplement the manifest fingerprint with `hashlib` and `json`, then prove that
editing a dependency changes it while editing `[tool.ruff]` does not.

### Exercise 5: Lock Auditor (Difficulty: Hard)
Given parsed `pyproject.toml` and `poetry.lock`, list direct requirements the
locked versions do not satisfy, with the offending version in the message.

### Exercise 6: Source Validator (Difficulty: Hard)
Validate `[[tool.poetry.source]]` entries: unique names, known priority, and no
dependency referencing an undeclared source.

## Summary

- `pyproject.toml` is intent, `poetry.lock` is the decision; commit the second.
- `[project]` is PEP 621 and PEP 508 only; `^` and `~` live in `[tool.poetry]`.
- A bare `1.2.3` is exact. `^0.x` bounds move on the minor digit.
- Groups are for developers, extras are for users; `--only` overrides everything.
- The content hash covers resolution-relevant fields only, and `poetry check
  --lock` is the CI gate that catches drift.
- Since 2.0, `export` and `shell` are plugins; `sync` and `env activate` are not.

## Quick Reference

| Task | Command |
|------|---------|
| Add a dependency | `poetry add requests` |
| Add to a group | `poetry add --group dev pytest` |
| Install locked graph | `poetry install` |
| Install runtime only | `poetry install --only main --no-root` |
| Verify lock freshness | `poetry check --lock` |
| Refresh lock, keep versions | `poetry lock` |
| Re-resolve from scratch | `poetry lock --regenerate` |
| Remove drift | `poetry sync` |
| Run inside the venv | `poetry run <cmd>` |
| Activate the venv | `poetry env activate` |
| Install a plugin | `poetry self add poetry-plugin-export` |
| Local config | `poetry config --local virtualenvs.in-project true` |
| Require a plugin | `[tool.poetry.requires-plugins]` in `pyproject.toml` |

## Next Steps

- Topic 38: test strategy — run the suite in a locked, `--only main` environment.
- Read `poetry.lock` in a real project: `grep -c "^\[\[package\]\]" poetry.lock`
  tells you how large the transitive graph is.
- Official docs: <https://python-poetry.org/docs/pyproject/> ·
  <https://python-poetry.org/docs/dependency-specification/> ·
  <https://python-poetry.org/docs/managing-dependencies/> ·
  <https://python-poetry.org/docs/cli/>
