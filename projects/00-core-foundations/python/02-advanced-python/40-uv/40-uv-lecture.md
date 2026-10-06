# Advanced Python - 40: uv

## Topic Overview

uv is a single Rust binary that replaces the pip + venv + pip-tools + pyenv
stack: it resolves dependency graphs, writes a lockfile, manages Python
interpreters, runs tools in ephemeral environments, builds and publishes
packages, and — since June 2026 — audits its own lockfile for known
vulnerabilities and malware. The artifacts are the same two files Poetry
produces: `pyproject.toml` (intent) and `uv.lock` (decision).

The mental model from topic 39 carries over unchanged: the manifest says
"some compatible range of numpy", the lockfile says "1.26.4, hash
`sha256:…`". What uv adds is speed (a resolver and installer written in
Rust with aggressive caching), a *universal* lockfile that records the
resolution for every platform at once, and a security layer most Python
stacks never had: `uv audit`, opt-in malware checks at sync time, and
resolution cutoffs that act as dependency cooldowns.

This topic stays offline. uv itself is a network tool, but everything that
decides *what gets installed* is pure string and dict work: classify the
manifest, compare the lock's manifest against the project's, pick the
wheels that match a platform, resolve group flags, verify hashes, apply a
cutoff, and match versions against advisories. Those are the parts the
exercise implements with `tomllib` and `hashlib`.

## Learning Objectives

- Explain what `uv.lock` guarantees and why it is universal (cross-platform).
- Read a uv `pyproject.toml`: `[project]`, `[tool.uv]`, `[dependency-groups]`,
  `[tool.uv.sources]`, `[[tool.uv.index]]`.
- Predict the install set for a given `--group` / `--no-dev` / `--only-group`
  / `--all-groups` combination, and the extras for `--extra` / `--all-extras`.
- Distinguish `--locked` from `--frozen` from `--check`, and know that
  `uv sync` is exact by default.
- Select installable wheels from a universal lock for a given interpreter
  and platform.
- Verify wheel hashes and audit a lock against an advisory database.
- Migrate a requirements.txt or Poetry project to uv.
- Apply supply-chain defenses: `uv audit`, `UV_MALWARE_CHECK`,
  `exclude-newer`, `constraint-dependencies` vs `override-dependencies`.

## Prerequisites

- Topic 27: `pyproject.toml`, specifiers, wheels, entry points.
- Topic 28: virtual environments.
- Topic 39: Poetry — the lockfile concept, groups vs extras, and the
  Poetry-vs-uv comparison (section 10 there) are assumed here.

## 1. What uv Actually Owns

One program covering the whole environment lifecycle:

| Stage | Command | Artifact |
|-------|---------|----------|
| Declare | edit `pyproject.toml` | intent |
| Resolve | `uv lock` / `uv add` | `uv.lock` |
| Isolate | auto-created `.venv` next to `pyproject.toml` | project environment |
| Install | `uv sync` | wheels in `.venv` |
| Run | `uv run CMD` | CMD inside `.venv`, auto-synced first |
| Audit | `uv audit` | findings against the lock |

Three properties worth internalizing:

- **`uv run` syncs first.** Running anything through uv guarantees the
  environment matches the lock before your code executes. This is why
  `uv run pytest` in CI replaces an install step.
- **The lockfile is the reproducibility contract.** Commit it. Same rule as
  Poetry, same reason.
- **Sync is exact by default.** Packages present in `.venv` but absent from
  the lock are *removed*, so drift from earlier experiments cannot survive.
  `--inexact` opts out.

## 2. pyproject.toml Under uv

uv is PEP 621-native — there is no uv-flavored metadata table:

```toml
[build-system]
requires = ["uv_build>=0.7,<1.0"]
build-backend = "uv_build"

[project]                       # PEP 621: the only metadata table uv reads
name = "rag-utils"
version = "1.2.0"
requires-python = ">=3.10"
dependencies = ["numpy>=1.26,<3.0.0"]     # PEP 508 strings only

[project.optional-dependencies] # extras, shipped with the package
qdrant = ["qdrant-client>=1.9,<2.0.0"]

[dependency-groups]             # PEP 735: development-only groups
dev = ["pytest>=8.0"]
lint = ["mypy>=1.11"]

[tool.uv]                       # uv configuration
required-version = ">=0.12"     # pin the tool itself
exclude-newer = "2026-06-01T00:00:00Z"

[[tool.uv.index]]               # named indexes
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]               # per-dependency source pinning
torch = { index = "pytorch-cpu" }
```

Rules that bite people:

- `project.dependencies` is **PEP 508 only**. No `^`, no `~`; a bare
  `"1.2.3"` means *exactly* 1.2.3. There is no second syntax table like
  Poetry's `[tool.poetry.dependencies]` — uv never needed one.
- `[tool.uv]` holds settings; a standalone `uv.toml` (discovered upward from
  the working directory) holds the same settings for projects that should
  not carry uv config in their manifest. Do not mix both in one directory.
- `required-version` pins uv itself, so the whole team resolves with the
  same resolver version.
- `explicit = true` on an index means only dependencies that name it in
  `[tool.uv.sources]` may install from it — the GPU-index pattern from
  topic 39, expressed differently.

## 3. uv.lock: The Universal Lockfile

```toml
version = 1
revision = 3
requires-python = ">=3.10"

[[package]]
name = "numpy"
version = "1.26.4"
source = { registry = "https://pypi.org/simple" }
wheels = [
    { url = "https://files.pythonhosted.org/numpy-1.26.4-cp312-cp312-win_amd64.whl",
      hash = "sha256:…" },
]

[manifest]
requirements = [{ name = "numpy", specifier = ">=1.26,<3.0.0" }]
```

What makes it different from `poetry.lock`:

- **Universal.** One lock records the resolution for *every* combination of
  OS, architecture and Python version in `requires-python`. A Linux CI box
  and a Windows laptop install from the same file; each picks its own
  wheels. Poetry locks per-environment and needs regeneration across
  platforms.
- **Hash-pinned.** Every wheel and sdist carries the sha256 recorded at
  resolution time; the installer re-hashes the downloaded bytes and refuses
  a mismatch.
- **Generated.** Human-readable TOML, managed by uv, never hand-edited.
  The format is uv-specific and not readable by other tools.
- **Committed.** It is the reproducibility contract for the team and for CI.

The standardized alternative is PEP 751's `pylock.toml`: tool-agnostic, so
files generated by uv could be installed by other tools and vice versa. uv
supports it as an export target (`uv export -o pylock.toml`) and as an
input to `uv pip`, but keeps `uv.lock` for the project interface because
some uv features cannot be expressed in the standard format.

## 4. Locking and Syncing

```console
uv lock                 # create/update uv.lock (keeps pinned versions)
uv lock --check         # fail if uv.lock is stale (CI gate)
uv lock --upgrade       # re-resolve, allowing upgrades
uv sync                 # install the locked graph into .venv, exact
uv sync --locked        # fail if syncing would change uv.lock
uv sync --frozen        # install from uv.lock without resolving at all
uv sync --check         # verify the environment matches the lock
uv sync --dry-run       # show what would change, touch nothing
uv run pytest           # auto-sync, then run
```

The flag pair people confuse:

- `--locked` — resolve, then **fail** if the result differs from the
  existing `uv.lock`. Use in CI to prove the lock is fresh.
- `--frozen` — **skip resolution entirely** and install from the existing
  lock. Fast, but it will happily install a lock that no longer matches the
  manifest.

The GitHub Actions pattern from the official integration guide:

```yaml
- run: uv sync --locked --all-extras --dev
- run: uv run pytest tests
```

## 5. Dependency Groups, Extras, and the Flag Surface

Groups answer "what do developers need"; extras answer "what can users opt
into". Same split as topic 39, different flags:

```console
uv sync                          # main + default groups (dev is default)
uv sync --group docs             # add a non-default group
uv sync --no-group lint          # drop a group
uv sync --no-dev                 # drop the dev group
uv sync --no-default-groups      # drop every default group
uv sync --all-groups             # everything declared
uv sync --only-group lint        # exactly that group, main excluded
uv sync --only-dev               # exactly the dev group
uv sync --extra qdrant           # add an extra
uv sync --all-extras             # every extra
uv sync --no-install-project     # deps only, skip the project itself
```

`dev` is the one group uv installs by default (PEP 735's default-group
semantics). Everything else needs `--group` or `--all-groups`. In Docker
multi-stage builds the pattern is `uv sync --no-dev --no-install-project`
for the runtime image.

## 6. Universal Resolution and Wheel Selection

Because the lock is universal, each `[[package]]` records *all* the
platform's wheels, and the installer picks by tag:

```console
numpy-1.26.4-cp312-cp312-win_amd64.whl          # CPython 3.12, Windows
numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl
numpy-1.26.4-cp39-abi3-win_amd64.whl            # abi3: any CPython >= 3.9
numpy-1.26.4-py3-none-any.whl                   # pure Python, any platform
```

The selection rules (full PEP 425 matching is more elaborate; the exercise
implements this subset):

- **Python tag** — exact match (`cp312`), the pure `py3` tag, or an `abi3`
  wheel built for an older CPython of the same implementation
  (`cp39-abi3` runs on 3.9 and everything after).
- **ABI tag** — the interpreter's own (`cp312`), `abi3`, or `none` for
  pure-Python wheels.
- **Platform tag** — exact match (`win_amd64`, `manylinux_2_17_x86_64`) or
  `any`.

This is why one lockfile serves the whole team: the Windows laptop and the
Linux CI runner read the same `[[package]]` and each select their own
wheels, hash-verified.

## 7. Migration

The MLOps MENA community talk this topic is anchored on walks the two
legacy shapes you actually meet: a project with a `venv` and a stale
`requirements.txt`, and a bare source tree with no dependency declaration
at all. The migration path:

**From requirements.txt to a uv project:**

```console
uv init                                        # scaffold pyproject.toml
uv add -r requirements.txt                     # import runtime deps
uv add --dev -r requirements-dev.txt           # import dev deps
uv sync                                        # resolve, lock, install
```

**From a bare source tree (no manifest):** derive the dependency list from
imports, not from the drifted environment. `pipreqs` reads the source tree,
maps imports to distributions, and writes a requirements file; run it
without installing anything via `uvx pipreqs . --mode no-pin`. Then feed
the result to `uv add -r`. (`--mode no-pin` avoids inventing exact pins the
original author never declared; `pipreqs --diff` audits an existing file
against real usage.)

**From Poetry / Pipenv / pip-tools:** the third-party `migrate-to-uv` tool
(`uvx migrate-to-uv`) converts metadata, groups, sources and entry points,
preserves version constraints (translating Poetry's caret syntax to PEP
440), and re-locks to the *same* versions the old lockfile pinned.

**Staying on requirements files:** uv's pip interface compiles and syncs
without adopting the project workflow:

```console
uv pip compile pyproject.toml -o requirements.txt   # pip-tools equivalent
uv pip sync requirements.txt                        # exact install
```

After any migration: commit `uv.lock`, add `uv lock --check` to CI, and
delete the old environment so nothing resolves outside the lock.

## 8. Supply-Chain Security

uv ships a security layer that pip-based stacks assemble from separate
tools. Four mechanisms, in order of how often you should think about them:

**`uv audit` (preview).** Scans the locked resolution against the OSV
database and reports known vulnerabilities plus *adverse project statuses*
(deprecated, archived, quarantined — PEP 792). It is uv-native (no separate
tool install), leverages the lock, and is 4–10x faster than `pip-audit` on
typical projects. Verified against the installed binary:

```console
uv audit --locked                 # assert the lock stays unchanged
uv audit --output-format sarif    # text | json | sarif
uv audit --ignore PYSEC-2026-1    # drop one advisory
uv audit --ignore-until-fixed PYSEC-2026-2   # ignore while no fix exists
```

It exits non-zero when findings exist, which is what makes it a CI gate.
Configuration lives under an `[audit]` section in `uv.toml` /
`pyproject.toml`.

**Malware check at sync time.** `UV_MALWARE_CHECK=1` makes every `uv add` /
`uv sync` query OSV for MAL advisories (known malware) against the locked
resolution and **abort before the malicious code can run**. Opt-in while in
preview; applies to PyPI-sourced packages. The reason this is a separate
mechanism from `uv audit`: PyPI quarantines malware by removing it from the
*index*, but a lockfile points at the underlying object storage, so
index-level removal is invisible at install time — the check must happen
before installation, not after.

**Dependency cooldowns.** `exclude-newer = "2026-06-01T00:00:00Z"` makes
resolution ignore anything uploaded after the cutoff, giving security
researchers a review window before a fresh release can enter your lock.
Per-package opt-out: `exclude-newer-package = { setuptools = false }`;
per-index opt-out for private indexes without upload-time metadata:
`exclude-newer = false` on the `[[tool.uv.index]]` entry.

**Constraints vs overrides.** `constraint-dependencies` restricts the
versions a package may resolve to *if it is requested anyway* (it never
adds a package). `override-dependencies` forces a version even against
declared ranges — a last resort for unfixable transitive conflicts, because
the resulting graph may never have been tested upstream.
`build-constraint-dependencies` applies the same idea to build
dependencies (setuptools, wheel), which run arbitrary code at install time
and are a real supply-chain surface.

What `uv audit` does not cover: file-level yank detection, and malware
advisories for non-PyPI sources. Pair it with Dependabot/Renovate for
ongoing monitoring.

## 9. uv vs Poetry vs pip-tools

Topic 39 section 10 covers the comparison; the uv-side summary:

- **uv** — fastest resolver and installer, single binary, Python version
  management, universal lockfile, built-in audit. Youngest of the three;
  security features are still preview.
- **Poetry** — mature, batteries included, per-platform locks, plugin
  ecosystem. Slower; two syntax tables to learn.
- **pip-tools** — minimal: keep `requirements.in`, compile to
  `requirements.txt`. No venv management, no build, no audit.

The lockfile, not the tool, is what makes a run reproducible. Whichever you
pick: commit the lock, gate CI on lock freshness, and install with
frozen-equivalent behavior.

## Common Mistakes to Avoid

### Mistake 1: hand-editing uv.lock

```bash
# WRONG -- uv rewrites it and your edit is lost
vim uv.lock

# CORRECT -- change the manifest, let uv relock
uv add "numpy>=1.26,<3.0.0"
```

### Mistake 2: gitignoring the lockfile

```bash
# WRONG -- every runner resolves independently
echo "uv.lock" >> .gitignore

# CORRECT -- commit it; it is the reproducibility contract
git add uv.lock
```

### Mistake 3: mutating the project env with uv pip

```bash
# WRONG -- uv sync removes it on the next run
uv pip install rich

# CORRECT -- one-off deps ride on the command
uv run --with rich python script.py
```

### Mistake 4: --frozen where --locked was meant

```bash
# WRONG -- installs a stale lock without complaint
uv sync --frozen

# CORRECT -- fail fast when manifest and lock disagree
uv sync --locked
```

### Mistake 5: caret syntax in [project]

```toml
# WRONG -- PEP 508 rejects '^'
dependencies = ["requests ^2.31"]

# CORRECT
dependencies = ["requests>=2.31,<3.0.0"]
```

### Mistake 6: assuming the malware check is on

```bash
# WRONG -- it is opt-in while in preview
uv sync   # no malware lookup happens

# CORRECT
UV_MALWARE_CHECK=1 uv sync
```

## Best Practices

- Commit `uv.lock`; gate CI with `uv lock --check` and install with
  `uv sync --locked`.
- Pin `required-version` so the team resolves with one uv version.
- Set `exclude-newer` as a rolling cooldown; opt individual packages out
  explicitly when you need a fresh release.
- Run `uv audit` in CI with `--locked`; triage with `--ignore-until-fixed`
  rather than bare `--ignore` so ignored findings resurface when a fix
  lands.
- Enable `UV_MALWARE_CHECK=1` in development environments.
- Keep runtime deps in `[project]`, tooling in `[dependency-groups]`, and
  mark heavyweight groups non-default.
- Use `uvx` for one-shot tools and `uv tool install` for recurring ones;
  never pollute project environments.
- In Docker: `uv sync --locked --no-dev --no-install-project` for the
  runtime stage.

## Complexity and Cost

| Operation | Cost | Note |
|-----------|------|------|
| Manifest classification | O(M) | Dict reads over parsed TOML |
| Lock freshness | O(D) | D = direct dependencies, dict equality |
| Specifier check | O(C) | C = clauses in the specifier |
| Wheel selection | O(W) | W = wheels per package, tag string work |
| Hash verification | O(B) | B = wheel bytes, sha256 is the cost |
| Cooldown pick | O(N) | N = candidate versions, single max scan |
| Lock audit | O(P × A) | P packages × advisories per package |
| Full resolution | solver-bound | paid once; the lock exists so you never pay again |

Offline, everything in this topic is linear-time string and dict work. The
resolver is the only expensive step, and `--frozen` exists so CI never pays
it.

## AI Engineering Relevance

- **Experiment reproducibility.** Same contract as topic 39: an eval
  comparing two models must run on identical library versions. `uv sync
  --locked` + `uv run` is the cheapest way to enforce it.
- **GPU environments.** Torch wheels come from a dedicated index; declare
  it `explicit` and pin `torch` to it in `[tool.uv.sources]` so nothing
  else resolves from it.
- **Splitting environments.** One universal lockfile serves the GPU
  training box, the CPU inference image (`--no-dev --no-install-project`),
  and the Windows laptop you write on.
- **Supply chain.** The lock's per-file hashes are verified at install
  time; `uv audit` catches known CVEs before deploy; `UV_MALWARE_CHECK`
  aborts before known-malicious code executes; `exclude-newer` buys the
  review window that protects against day-zero malware.
- **CI cost.** uv's cache makes cold installs fast enough that teams stop
  skipping them — which is how lockfiles actually end up enforced.

## Practice Exercises

### Exercise 1: Classify the Manifest (Difficulty: Easy)
Parse a uv `pyproject.toml` with `tomllib` and report which tables are
present, the PEP 735 groups, the extras, and which indexes are explicit.

### Exercise 2: Lock Freshness (Difficulty: Medium)
Compare the lock's `[manifest] requirements` against the project's direct
dependencies and report requirements the locked versions do not satisfy.

### Exercise 3: Wheel Selector (Difficulty: Medium)
Given a universal lock's wheel list, a Python tag and a platform tag,
return the installable wheels in listed order. Model the simplified
python/ABI/platform rules from section 6.

### Exercise 4: Group Resolver (Difficulty: Medium)
Given `groups: dict[str, bool]` (name -> is_default) and the uv sync flag
arguments, return the sorted install set. Raise on unknown group names.

### Exercise 5: Hash Verifier (Difficulty: Hard)
Re-hash downloaded wheel bytes against the lock's recorded sha256 values
and report mismatches and missing blobs, sorted.

### Exercise 6: Cooldown Picker (Difficulty: Hard)
Given candidate versions with upload timestamps and a cutoff, return the
highest version old enough to resolve. Raise when nothing qualifies.

### Exercise 7: Lock Auditor (Difficulty: Hard)
Match locked versions against an advisory database, honor `--ignore` ids,
report "no fix available" cases, and derive the exit code.

## Summary

- `pyproject.toml` is intent, `uv.lock` is the decision; commit the second.
- uv reads PEP 621/508/735 only — no caret syntax, no second metadata table.
- `uv.lock` is universal: one file, every platform, hash-pinned wheels.
- `uv sync` is exact by default; `--locked` proves freshness, `--frozen`
  skips resolution, `--check` verifies the environment.
- `dev` is the default group; everything else needs `--group` or
  `--all-groups`; `--only-group` excludes main.
- Security: `uv audit` for vulnerabilities and adverse statuses,
  `UV_MALWARE_CHECK=1` to abort on known malware before install,
  `exclude-newer` as a cooldown, constraints to restrict and overrides to
  force (last resort).
- Migration: `uv add -r requirements.txt`, `uvx pipreqs` for bare source
  trees, `uvx migrate-to-uv` for Poetry/Pipenv/pip-tools.

## Quick Reference

| Task | Command |
|------|---------|
| Scaffold a project | `uv init` |
| Add a dependency | `uv add requests` |
| Import requirements.txt | `uv add -r requirements.txt` |
| Add a dev dependency | `uv add --dev pytest` |
| Install the locked graph | `uv sync` |
| Install runtime only | `uv sync --locked --no-dev --no-install-project` |
| Verify lock freshness | `uv lock --check` |
| Refresh lock, keep versions | `uv lock` |
| Re-resolve with upgrades | `uv lock --upgrade` |
| Run inside the environment | `uv run pytest` |
| One-off dependency | `uv run --with rich python x.py` |
| Run a tool ephemerally | `uvx ruff check` |
| Install an interpreter | `uv python install 3.12` |
| Export the lock | `uv export -o requirements.txt` |
| pip-tools style compile | `uv pip compile pyproject.toml -o req.txt` |
| Audit the lock | `uv audit --locked` |
| Enable malware check | `UV_MALWARE_CHECK=1 uv sync` |
| Cooldown cutoff | `[tool.uv] exclude-newer = "2026-06-01T00:00:00Z"` |
| Pin uv itself | `[tool.uv] required-version = ">=0.12"` |

## Next Steps

- Topic 39: Poetry — the same contract with a different tool; section 10
  there is the comparison table this topic summarizes.
- Topic 38: test strategy — run the suite through `uv run pytest` in a
  `--locked` environment.
- Try the real thing: `uv init demo && uv add ruff && uv audit` in a
  scratch directory, then read the generated `uv.lock` end to end.
- Official docs: <https://docs.astral.sh/uv/> ·
  <https://docs.astral.sh/uv/concepts/projects/layout/> ·
  <https://docs.astral.sh/uv/guides/migration/pip-to-project/> ·
  <https://astral.sh/blog/uv-audit>
