"""
Advanced Python - 40: uv
========================
Topics: pyproject.toml under uv; uv.lock anatomy and freshness; universal
        (cross-platform) resolution and wheel-tag selection; dependency groups
        and extras with the uv sync flag surface; exact sync; the --locked vs
        --frozen distinction; supply-chain security (uv audit, malware check,
        exclude-newer cooldowns, constraint vs override); migration from
        requirements.txt / Poetry; uv vs Poetry vs pip-tools.

Why this matters for AI/backend engineering:
    uv is the current default answer to "how do I make this environment
    reproducible". An eval harness that resolves on every machine produces
    numbers you cannot compare; a lockfile produces the same bytes everywhere.
    uv also ships the security layer most Python stacks lack: vulnerability
    audits against the lock, opt-in malware checks at sync time, and date
    cutoffs that act as dependency cooldowns. This file exercises the parts
    you can run offline with the standard library: classify the manifest,
    decide lock freshness, pick wheels for a platform, resolve group flags,
    verify wheel hashes, apply a cooldown, and audit a lock against an
    advisory database.

Run:      python 40-uv.py
Verify:   python 40-uv.py --verify
Reference: https://docs.astral.sh/uv/
           https://docs.astral.sh/uv/concepts/projects/layout/
           https://docs.astral.sh/uv/guides/migration/pip-to-project/
           https://astral.sh/blog/uv-audit
"""

from __future__ import annotations

import copy
import hashlib
import sys

import tomllib  # type: ignore[import-not-found]

# --------------------------------------------------------------------------- #
# Section 1: pyproject.toml under uv
# --------------------------------------------------------------------------- #
# uv is PEP 621-native: [project] is the only metadata table it reads for
# dependencies, and requirement strings are PEP 508 only (no ^, no ~; a bare
# "1.2.3" is exact). uv-specific configuration lives in [tool.uv] (or a
# separate uv.toml). Groups use the PEP 735 [dependency-groups] table.
EXAMPLE_PYPROJECT = """
[build-system]
requires = ["uv_build>=0.7,<1.0"]
build-backend = "uv_build"

[project]
name = "rag-utils"
version = "1.2.0"
description = "Shared retrieval helpers for the RAG services"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.26,<3.0.0",
    "pydantic>=2.5,<3.0.0",
]

[project.optional-dependencies]
qdrant = ["qdrant-client>=1.9,<2.0.0"]

[dependency-groups]
dev = ["pytest>=8.0"]
lint = ["mypy>=1.11"]
docs = ["mkdocs>=1.6"]

[tool.uv]
required-version = ">=0.12"
exclude-newer = "2026-06-01T00:00:00Z"

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cpu" }

[tool.ruff]
line-length = 100
"""


def load_pyproject() -> dict:
    """Parse the example manifest with the stdlib TOML parser (3.11+)."""
    parsed: dict = tomllib.loads(EXAMPLE_PYPROJECT)
    return parsed


def load_lock() -> dict:
    """Parse the example lockfile."""
    parsed: dict = tomllib.loads(EXAMPLE_LOCK)
    return parsed


def classify_manifest(data: dict) -> dict:
    """Report which metadata tables a pyproject.toml uses under uv."""
    project = data.get("project", {})
    tool_uv = data.get("tool", {}).get("uv", {})
    indexes = tool_uv.get("index", [])
    return {
        "uses_pep621": bool(project),
        "uses_tool_uv": bool(tool_uv),
        "pep735_groups": sorted(data.get("dependency-groups", {})),
        "extras": sorted(project.get("optional-dependencies", {})),
        "indexes": [src.get("name", "") for src in indexes],
        "explicit_indexes": [src.get("name", "") for src in indexes if src.get("explicit") is True],
        "pinned_sources": sorted(tool_uv.get("sources", {})),
        "tool_uv_keys": sorted(tool_uv),
    }


# --------------------------------------------------------------------------- #
# Section 2: uv.lock anatomy and freshness
# --------------------------------------------------------------------------- #
# A trimmed uv.lock. Real locks also carry per-package [package.metadata]
# requires-dist entries, dependency-groups, and resolution markers; those are
# elided here because nothing in this exercise reads them. What matters:
#   version/revision  - lock format version, bumped by uv releases
#   requires-python   - the interpreter range the lock was resolved for
#   [[package]]       - one entry per package with exact version and files
#   [manifest]        - the direct requirements the lock was built from
EXAMPLE_LOCK = """
version = 1
revision = 3
requires-python = ">=3.10"

[[package]]
name = "rag-utils"
version = "1.2.0"
source = { editable = "." }

[[package]]
name = "numpy"
version = "1.26.4"
source = { registry = "https://pypi.org/simple" }
wheels = [
    { url = "https://files.pythonhosted.org/numpy-1.26.4-cp312-cp312-win_amd64.whl", hash = "sha256:11111111" },
    { url = "https://files.pythonhosted.org/numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl", hash = "sha256:22222222" },
]

[[package]]
name = "pydantic"
version = "2.9.2"
source = { registry = "https://pypi.org/simple" }
wheels = [
    { url = "https://files.pythonhosted.org/pydantic-2.9.2-py3-none-any.whl", hash = "sha256:33333333" },
]

[[package]]
name = "pytest"
version = "8.3.4"
source = { registry = "https://pypi.org/simple" }
wheels = [
    { url = "https://files.pythonhosted.org/pytest-8.3.4-py3-none-any.whl", hash = "sha256:44444444" },
]

[manifest]
requirements = [
    { name = "numpy", specifier = ">=1.26,<3.0.0" },
    { name = "pydantic", specifier = ">=2.5,<3.0.0" },
]
"""


def parse_requirement(req: str) -> tuple[str, str]:
    """Split a PEP 508 requirement into (name, specifier).

    Accepts 'numpy>=1.26,<3' and 'qdrant-client[async]>=1.9'.
    """
    text = req.strip()
    head = text
    spec = ""
    for i, ch in enumerate(text):
        if ch in "<>!=~@":
            head, spec = text[:i], text[i:]
            break
    if "[" in head:
        head = head.partition("[")[0]
    return (head.strip().lower(), spec.strip())


def manifest_requirements(pyproject: dict) -> dict[str, str]:
    """Direct dependencies declared in [project], name -> specifier."""
    out: dict[str, str] = {}
    for req in pyproject.get("project", {}).get("dependencies", []):
        name, spec = parse_requirement(req)
        out[name] = spec
    return out


def lock_requirements(lock: dict) -> dict[str, str]:
    """Direct requirements recorded under [manifest], name -> specifier."""
    out: dict[str, str] = {}
    for entry in lock.get("manifest", {}).get("requirements", []):
        out[str(entry["name"]).lower()] = str(entry.get("specifier", ""))
    return out


def locked_versions(lock: dict) -> dict[str, str]:
    """Locked version per package name (lowercase)."""
    return {str(p["name"]).lower(): str(p["version"]) for p in lock.get("package", [])}


# --------------------------------------------------------------------------- #
# Section 3: version specifiers (PEP 508 subset)
# --------------------------------------------------------------------------- #
# uv reads PEP 508 only. This teaching checker supports the clauses that appear
# in the example: ==, >=, >, <, <=, != joined by commas.
_OPERATORS = ("===", "==", "!=", ">=", "<=", "~=", ">", "<")


def _split_op(clause: str) -> tuple[str, str]:
    """Split '<operator><version>' into (operator, version)."""
    text = clause.strip()
    for op in _OPERATORS:
        if text.startswith(op):
            return op, text[len(op) :].strip()
    return "", text


def _nums(version: str) -> list[int]:
    """Parse the numeric prefix of a version into ints."""
    core = ""
    for ch in version.strip():
        if ch.isdigit() or ch == ".":
            core += ch
        else:
            break
    return [int(p) for p in core.split(".") if p]


def _pad(parts: list[int], width: int = 4) -> list[int]:
    """Pad a version component list with zeros up to `width`."""
    return parts + [0] * (width - len(parts))


def _vkey(version: str) -> tuple[int, ...]:
    """Comparable tuple for a version string (prerelease suffixes dropped)."""
    return tuple(_pad(_nums(version)))


def version_satisfies(version: str, spec: str) -> bool:
    """True when `version` satisfies a comma-separated PEP 508 specifier."""
    value = _vkey(version)
    for clause in spec.split(","):
        clause = clause.strip()
        if not clause:
            continue
        op, bound = _split_op(clause)
        target = _vkey(bound)
        if op == "==" and value != target:
            return False
        if op == ">=" and not value >= target:
            return False
        if op == ">" and not value > target:
            return False
        if op == "<" and not value < target:
            return False
        if op == "<=" and not value <= target:
            return False
        if op == "!=" and value == target:
            return False
    return True


def unsatisfied_dependencies(pyproject: dict, lock: dict) -> list[str]:
    """Direct requirements the locked versions do not satisfy, sorted."""
    locked = locked_versions(lock)
    problems: list[str] = []
    for name, spec in manifest_requirements(pyproject).items():
        version = locked.get(name)
        if version is None:
            problems.append(f"{name}: missing from uv.lock")
        elif not version_satisfies(version, spec):
            problems.append(f"{name}: {version} outside {spec}")
    return sorted(problems)


def lock_is_fresh(pyproject: dict, lock: dict) -> bool:
    """True when the lock's manifest matches the project's direct deps.

    uv re-checks this on every sync: if the manifest drifted from uv.lock,
    the lock is stale and (without --frozen) uv re-resolves.
    """
    return manifest_requirements(pyproject) == lock_requirements(lock)


# --------------------------------------------------------------------------- #
# Section 4: universal resolution - wheel-tag selection
# --------------------------------------------------------------------------- #


def parse_wheel_filename(filename: str) -> dict:
    """Split 'name-version-pythontag-abitag-platformtag.whl' into parts.

    Simplified: distribution names are normalized to '_' so a plain split on
    '-' is safe, and build tags are not modeled.
    """
    stem = filename.removesuffix(".whl")
    parts = stem.split("-")
    if len(parts) < 5:
        raise ValueError(f"not a wheel filename: {filename}")
    python_tag, abi_tag, platform_tag = parts[-3], parts[-2], parts[-1]
    return {
        "name": parts[0],
        "version": parts[1],
        "python_tag": python_tag,
        "abi_tag": abi_tag,
        "platform_tag": platform_tag,
    }


def _python_ok(python_tag: str, wheel_python: str, wheel_abi: str) -> bool:
    """Simplified interpreter compatibility.

    Exact tag match ('cp312' in 'cp312'), the pure-python 'py3' tag, or an
    abi3 wheel built for an older CPython of the same implementation
    ('cp39-abi3' runs on any CPython >= 3.9).
    """
    if python_tag in wheel_python.split("."):
        return True
    if "py3" in wheel_python.split("."):
        return True
    if wheel_abi == "abi3" and wheel_python.startswith("cp") and python_tag.startswith("cp"):
        try:
            return int(wheel_python[2:]) <= int(python_tag[2:])
        except ValueError:
            return False
    return False


def _abi_ok(python_tag: str, wheel_abi: str) -> bool:
    """Simplified ABI compatibility: own abi, abi3, or pure ('none')."""
    return wheel_abi in ("abi3", "none", python_tag)


def _platform_ok(platform_tag: str, wheel_platform: str) -> bool:
    """Simplified platform compatibility: exact tag or the 'any' tag."""
    return wheel_platform == platform_tag or wheel_platform == "any"


def select_wheels(wheels: list[str], python_tag: str, platform_tag: str) -> list[str]:
    """Wheels installable on (python_tag, platform_tag), in listed order.

    uv.lock is universal: it records every platform's wheels and the
    installer picks the ones matching the running interpreter. The rules
    here are a teaching subset of full PEP 425 tag matching.
    """
    picked: list[str] = []
    for filename in wheels:
        tags = parse_wheel_filename(filename)
        if (
            _python_ok(python_tag, tags["python_tag"], tags["abi_tag"])
            and _abi_ok(python_tag, tags["abi_tag"])
            and _platform_ok(platform_tag, tags["platform_tag"])
        ):
            picked.append(filename)
    return picked


# --------------------------------------------------------------------------- #
# Section 5: dependency groups, extras, and the uv sync flag surface
# --------------------------------------------------------------------------- #
# groups = development-only dependency sets (PEP 735); never shipped.
#          'dev' is uv's default group: installed without any flag.
# extras = optional dependency sets shipped inside the package for users.
#
#   --group g          add group g
#   --no-group g       drop group g
#   --no-dev           drop the default dev group
#   --no-default-groups drop every default group
#   --all-groups       every declared group
#   --only-group g     exactly group g (main dependencies excluded)
#   --extra e          add extra e; --all-extras / --no-extra e
#   --inexact          keep packages the lock does not list (default: remove)
def groups_to_install(
    groups: dict[str, bool],
    *,
    with_groups: list[str] | None = None,
    no_groups: list[str] | None = None,
    only_group: str | None = None,
    all_groups: bool = False,
    no_default_groups: bool = False,
) -> list[str]:
    """Resolve the set of groups `uv sync` would install for a flag combination.

    `groups` maps group name -> is_default. 'main' (the shipped runtime deps)
    is always present and non-default.
    """
    with_groups = list(with_groups or [])
    drop = set(no_groups or [])
    known = set(groups) | {"main"}
    if only_group is not None:
        if only_group not in known:
            raise ValueError(f"unknown group: {only_group}")
        return [only_group]
    if all_groups:
        selected = set(groups) | {"main"}
    else:
        selected = {"main"}
        if not no_default_groups:
            selected.update(g for g, is_default in groups.items() if is_default)
        selected.update(with_groups)
    unknown = (set(with_groups) | drop) - known
    if unknown:
        raise ValueError(f"unknown group(s): {sorted(unknown)}")
    return sorted(selected - drop)


def extras_to_install(
    all_extras: bool,
    with_extra: list[str] | None = None,
    no_extra: list[str] | None = None,
) -> list[str]:
    """Resolve the extras `uv sync` would install."""
    with_extra = list(with_extra or [])
    drop = set(no_extra or [])
    return sorted((set(with_extra) if not all_extras else set(with_extra) | {"*"}) - drop)


# --------------------------------------------------------------------------- #
# Section 6: install-time hash verification
# --------------------------------------------------------------------------- #
# Every file in uv.lock carries a sha256 recorded at resolution time. The
# installer re-hashes the downloaded bytes and refuses a mismatch, so a
# substituted or corrupted wheel fails the install instead of running.
def verify_wheel_hashes(lock: dict, blobs: dict[str, bytes]) -> list[str]:
    """Report wheels whose bytes do not match the recorded hash, sorted.

    `blobs` maps wheel URL -> downloaded bytes. A URL with no bytes is
    reported as missing.
    """
    problems: list[str] = []
    for package in lock.get("package", []):
        for wheel in package.get("wheels", []):
            url = wheel["url"]
            expected = str(wheel.get("hash", "")).removeprefix("sha256:")
            blob = blobs.get(url)
            if blob is None:
                problems.append(f"{package['name']}: missing blob for {url}")
                continue
            actual = hashlib.sha256(blob).hexdigest()
            if actual != expected:
                problems.append(
                    f"{package['name']}: hash mismatch for {url} "
                    f"(expected {expected}, got {actual})"
                )
    return sorted(problems)


# --------------------------------------------------------------------------- #
# Section 7: exclude-newer as a dependency cooldown
# --------------------------------------------------------------------------- #
# [tool.uv] exclude-newer = "2026-06-01T00:00:00Z" makes resolution ignore
# anything uploaded after the cutoff. New releases get a review window before
# they can enter your lockfile - a cooldown against fresh malware and broken
# releases. Per-package opt-out: exclude-newer-package = { setuptools = false }.
def pick_with_cooldown(candidates: dict[str, int], cutoff_ts: int) -> str:
    """Highest version uploaded at or before the cutoff timestamp.

    `candidates` maps version -> upload timestamp (epoch seconds). Raises
    ValueError when nothing is old enough.
    """
    eligible = [v for v, ts in candidates.items() if ts <= cutoff_ts]
    if not eligible:
        raise ValueError(f"no candidate uploaded at or before {cutoff_ts}")
    return max(eligible, key=_vkey)


# --------------------------------------------------------------------------- #
# Section 8: uv audit - vulnerabilities and adverse statuses
# --------------------------------------------------------------------------- #
# `uv audit` (preview) scans the locked resolution against OSV and reports
# known vulnerabilities plus adverse project statuses (deprecated, archived,
# quarantined). It exits non-zero when findings exist, which is what makes it
# a CI gate. Malware is a different threat: UV_MALWARE_CHECK=1 makes every
# sync abort before installing anything with a public OSV MAL advisory.
def audit_lock(
    lock: dict,
    advisories: dict[str, list[dict]],
    ignore: set[str] | None = None,
) -> list[str]:
    """Findings for the locked versions, sorted by (package, id).

    `advisories` maps package name -> list of {"id": str, "fixed_in": str|None}.
    A version is vulnerable when it is older than fixed_in; fixed_in None
    means no fix is available. `ignore` drops findings by advisory id.
    """
    ignore = ignore or set()
    findings: list[str] = []
    for package in lock.get("package", []):
        name = str(package["name"]).lower()
        version = str(package["version"])
        for adv in advisories.get(name, []):
            if adv["id"] in ignore:
                continue
            fixed_in = adv.get("fixed_in")
            if fixed_in is None:
                findings.append(f"{name}=={version} {adv['id']} (no fix available)")
            elif not version_satisfies(version, f">={fixed_in}"):
                findings.append(f"{name}=={version} {adv['id']} (fixed in {fixed_in})")
    return sorted(findings)


def audit_exit_code(findings: list[str]) -> int:
    """uv audit exits non-zero when findings exist - the CI gate."""
    return 1 if findings else 0


# --------------------------------------------------------------------------- #
# Section 9: the command surface (print-only)
# --------------------------------------------------------------------------- #
COMMAND_MAP = {
    "uv init": "scaffold a project (PEP 621 pyproject.toml)",
    "uv add pkg": "add + resolve + lock + sync",
    "uv add -r requirements.txt": "import a requirements file",
    "uv add --dev pkg": "add into the dev group",
    "uv remove pkg": "drop the dependency and relock",
    "uv sync": "install the locked graph, remove extraneous packages",
    "uv sync --locked": "fail if syncing would change uv.lock",
    "uv sync --frozen": "install from uv.lock without re-resolving",
    "uv sync --check": "verify the environment matches the lock",
    "uv lock --check": "fail if uv.lock is stale",
    "uv lock --upgrade": "re-resolve, allowing version upgrades",
    "uv run CMD": "run CMD in the project environment (auto-syncs)",
    "uv run --with pkg CMD": "run with a one-off dependency added",
    "uvx pkg": "run a tool in a cached ephemeral environment",
    "uv tool install pkg": "install a tool with its own isolated env",
    "uv python install 3.12": "download and manage a Python interpreter",
    "uv export -o requirements.txt": "export the lock to requirements format",
    "uv pip compile pyproject.toml -o req.txt": "pip-tools-style compile",
    "uv pip sync requirements.txt": "exact-install from a compiled file",
    "uv build / uv publish": "build sdist+wheel / upload to an index",
    "uv audit": "scan the lock for vulnerabilities (preview)",
    "uv tree": "show the resolved dependency tree",
}


# --------------------------------------------------------------------------- #
# Section 10: common mistakes (reference)
# --------------------------------------------------------------------------- #
# 1. Editing uv.lock by hand. It is generated; uv add / uv lock rewrite it.
# 2. Gitignoring uv.lock. Every machine then resolves independently and the
#    "reproducible" eval is not.
# 3. Using `uv pip install` to change the project environment. uv sync removes
#    what the lock does not list; use uv add for project dependencies.
# 4. Confusing --locked with --frozen: --locked fails when the lock would
#    change; --frozen installs from the existing lock without resolving at
#    all (it will happily install a stale lock).
# 5. Assuming uv syntax allows ^ or ~. [project] dependencies are PEP 508
#    only; a bare "1.2.3" is exact.
# 6. Expecting UV_MALWARE_CHECK to be on. It is opt-in while in preview.
# 7. Treating exclude-newer as a pin. It is a resolution-time cutoff; the
#    lockfile is what actually pins.
# 8. Reaching for override-dependencies to "fix" a conflict. Constraints
#    restrict versions that are requested anyway; overrides force versions
#    against declared ranges and can produce a graph that never worked.


def demo_manifest() -> None:
    report = classify_manifest(load_pyproject())
    print("Manifest tables:")
    print(f"  PEP 621 [project]   : {report['uses_pep621']}")
    print(f"  [tool.uv]           : {report['uses_tool_uv']}")
    print(f"  [dependency-groups] : {report['pep735_groups']}")
    print(f"  extras              : {report['extras']}")
    print(f"  indexes             : {report['indexes']} (explicit: {report['explicit_indexes']})")
    print(f"  pinned sources      : {report['pinned_sources']}")


def demo_freshness() -> None:
    pyproject = load_pyproject()
    lock = load_lock()
    stale = copy.deepcopy(pyproject)
    stale["project"]["dependencies"].append("httpx>=0.27,<1.0.0")
    print("\nLock freshness:")
    print(f"  untouched manifest : {lock_is_fresh(pyproject, lock)}")
    print(f"  added a dependency : {lock_is_fresh(stale, lock)}")
    tool_only = copy.deepcopy(pyproject)
    tool_only["tool"]["ruff"]["line-length"] = 88
    print(f"  changed [tool.ruff]: {lock_is_fresh(tool_only, lock)}")
    print(f"  unsatisfied deps   : {unsatisfied_dependencies(pyproject, lock) or 'none'}")


def demo_wheels() -> None:
    wheels = [
        "numpy-1.26.4-cp312-cp312-win_amd64.whl",
        "numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl",
        "numpy-1.26.4-cp39-abi3-win_amd64.whl",
        "numpy-1.26.4-py3-none-any.whl",
        "numpy-1.26.4-cp312-cp312-linux_x86_64.whl",
    ]
    print("\nWheel selection for cp312 / win_amd64:")
    for filename in select_wheels(wheels, "cp312", "win_amd64"):
        print(f"  {filename}")


def demo_groups() -> None:
    groups = {"dev": True, "lint": False, "docs": False}
    print("\nGroup selection (uv sync):")
    print(f"  default                : {groups_to_install(groups)}")
    print(f"  --group docs           : {groups_to_install(groups, with_groups=['docs'])}")
    print(f"  --no-dev               : {groups_to_install(groups, no_groups=['dev'])}")
    print(f"  --only-group lint      : {groups_to_install(groups, only_group='lint')}")
    print(f"  --all-groups           : {groups_to_install(groups, all_groups=True)}")


def demo_security() -> None:
    lock = load_lock()
    blobs = {
        "https://files.pythonhosted.org/pydantic-2.9.2-py3-none-any.whl": b"clean",
        "https://files.pythonhosted.org/pytest-8.3.4-py3-none-any.whl": b"tampered",
    }
    print("\nHash verification (missing blobs reported):")
    for problem in verify_wheel_hashes(lock, blobs):
        print(f"  {problem}")

    print("\nCooldown (exclude-newer = 2026-06-01):")
    candidates = {"2.9.2": 1_760_000_000, "2.10.0": 1_780_000_000, "2.9.9": 1_750_000_000}
    cutoff = 1_770_000_000
    print(f"  candidates {candidates} -> {pick_with_cooldown(candidates, cutoff)}")

    advisories: dict[str, list[dict]] = {
        "pydantic": [{"id": "PYSEC-2026-1", "fixed_in": "2.10.0"}],
        "numpy": [{"id": "PYSEC-2026-2", "fixed_in": None}],
    }
    findings = audit_lock(lock, advisories)
    print("\nuv audit:")
    for finding in findings:
        print(f"  {finding}")
    print(f"  exit code: {audit_exit_code(findings)}")
    print(f"  ignoring PYSEC-2026-1: {audit_lock(lock, advisories, {'PYSEC-2026-1'})}")


def demo_commands() -> None:
    print("\nCommand map:")
    for cmd, note in COMMAND_MAP.items():
        print(f"  {cmd:<44} {note}")


def _verify() -> None:
    """Self-check. Silent on failure-free completion when run with --verify."""
    # Manifest classification.
    report = classify_manifest(load_pyproject())
    assert report["uses_pep621"] and report["uses_tool_uv"]
    assert report["pep735_groups"] == ["dev", "docs", "lint"]
    assert report["extras"] == ["qdrant"]
    assert report["indexes"] == ["pytorch-cpu"]
    assert report["explicit_indexes"] == ["pytorch-cpu"]
    assert report["pinned_sources"] == ["torch"]

    # Requirement parsing.
    assert parse_requirement("numpy>=1.26,<3.0.0") == ("numpy", ">=1.26,<3.0.0")
    assert parse_requirement("qdrant-client[async]>=1.9") == ("qdrant-client", ">=1.9")
    assert parse_requirement("httpx") == ("httpx", "")

    # Specifier membership.
    assert version_satisfies("1.26.4", ">=1.26,<3.0.0")
    assert not version_satisfies("3.0.0", ">=1.26,<3.0.0")
    assert version_satisfies("2.9.2", ">=2.5,<3.0.0")
    assert not version_satisfies("2.5.0", "!=2.5.0")
    assert version_satisfies("1.2.3", "==1.2.3")

    # Manifest / lock agreement.
    pyproject = load_pyproject()
    lock = load_lock()
    assert manifest_requirements(pyproject) == {
        "numpy": ">=1.26,<3.0.0",
        "pydantic": ">=2.5,<3.0.0",
    }
    assert lock_requirements(lock) == manifest_requirements(pyproject)
    assert lock_is_fresh(pyproject, lock)
    assert unsatisfied_dependencies(pyproject, lock) == []

    stale = copy.deepcopy(pyproject)
    stale["project"]["dependencies"].append("httpx>=0.27,<1.0.0")
    assert not lock_is_fresh(stale, lock)
    assert unsatisfied_dependencies(stale, lock) == ["httpx: missing from uv.lock"]

    drifted = copy.deepcopy(lock)
    for pkg in drifted["package"]:
        if pkg["name"] == "numpy":
            pkg["version"] = "3.1.0"
    assert unsatisfied_dependencies(pyproject, drifted) == ["numpy: 3.1.0 outside >=1.26,<3.0.0"]

    # Wheel selection.
    assert parse_wheel_filename("ruff-0.5.0-py3-none-win_amd64.whl") == {
        "name": "ruff",
        "version": "0.5.0",
        "python_tag": "py3",
        "abi_tag": "none",
        "platform_tag": "win_amd64",
    }
    wheels = [
        "numpy-1.26.4-cp312-cp312-win_amd64.whl",
        "numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl",
        "numpy-1.26.4-cp39-abi3-win_amd64.whl",
        "numpy-1.26.4-py3-none-any.whl",
        "numpy-1.26.4-cp312-cp312-linux_x86_64.whl",
        "numpy-1.26.4-cp311-cp311-win_amd64.whl",
    ]
    assert select_wheels(wheels, "cp312", "win_amd64") == [
        "numpy-1.26.4-cp312-cp312-win_amd64.whl",
        "numpy-1.26.4-cp39-abi3-win_amd64.whl",
        "numpy-1.26.4-py3-none-any.whl",
    ]
    assert select_wheels(wheels, "cp312", "manylinux_2_17_x86_64") == [
        "numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl",
        "numpy-1.26.4-py3-none-any.whl",
    ]
    assert select_wheels(["x-1.0-py3-none-any.whl"], "cp310", "linux_x86_64") == [
        "x-1.0-py3-none-any.whl"
    ]

    # Groups.
    groups = {"dev": True, "lint": False, "docs": False}
    assert groups_to_install(groups) == ["dev", "main"]
    assert groups_to_install(groups, with_groups=["docs"]) == ["dev", "docs", "main"]
    assert groups_to_install(groups, no_groups=["dev"]) == ["main"]
    assert groups_to_install(groups, no_default_groups=True) == ["main"]
    assert groups_to_install(groups, only_group="lint") == ["lint"]
    assert groups_to_install(groups, all_groups=True) == ["dev", "docs", "lint", "main"]
    try:
        groups_to_install(groups, with_groups=["nope"])
        raise AssertionError("unknown group must raise")
    except ValueError:
        pass

    # Extras.
    assert extras_to_install(False, with_extra=["qdrant"]) == ["qdrant"]
    assert extras_to_install(True, no_extra=["qdrant"]) == ["*"]
    assert extras_to_install(False) == []

    # Hash verification.
    blobs = {
        "https://files.pythonhosted.org/pydantic-2.9.2-py3-none-any.whl": b"clean",
        "https://files.pythonhosted.org/pytest-8.3.4-py3-none-any.whl": b"tampered",
    }
    problems = verify_wheel_hashes(load_lock(), blobs)
    assert problems == [
        "numpy: missing blob for "
        "https://files.pythonhosted.org/numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.whl",
        "numpy: missing blob for "
        "https://files.pythonhosted.org/numpy-1.26.4-cp312-cp312-win_amd64.whl",
        "pydantic: hash mismatch for "
        "https://files.pythonhosted.org/pydantic-2.9.2-py3-none-any.whl "
        f"(expected 33333333, got {hashlib.sha256(b'clean').hexdigest()})",
        "pytest: hash mismatch for "
        "https://files.pythonhosted.org/pytest-8.3.4-py3-none-any.whl "
        f"(expected 44444444, got {hashlib.sha256(b'tampered').hexdigest()})",
    ]

    # Cooldown.
    candidates = {"2.9.2": 1_760_000_000, "2.10.0": 1_780_000_000, "2.9.9": 1_750_000_000}
    assert pick_with_cooldown(candidates, 1_770_000_000) == "2.9.9"
    assert pick_with_cooldown(candidates, 1_790_000_000) == "2.10.0"
    assert pick_with_cooldown(candidates, 1_755_000_000) == "2.9.9"
    try:
        pick_with_cooldown(candidates, 0)
        raise AssertionError("empty eligible set must raise")
    except ValueError:
        pass

    # Audit.
    lock = load_lock()
    advisories: dict[str, list[dict]] = {
        "pydantic": [{"id": "PYSEC-2026-1", "fixed_in": "2.10.0"}],
        "numpy": [{"id": "PYSEC-2026-2", "fixed_in": None}],
        "pytest": [{"id": "PYSEC-2026-3", "fixed_in": "8.0.0"}],
    }
    assert audit_lock(lock, advisories) == [
        "numpy==1.26.4 PYSEC-2026-2 (no fix available)",
        "pydantic==2.9.2 PYSEC-2026-1 (fixed in 2.10.0)",
    ]
    assert audit_lock(lock, advisories, {"PYSEC-2026-1"}) == [
        "numpy==1.26.4 PYSEC-2026-2 (no fix available)",
    ]
    assert audit_lock(lock, {}) == []
    assert audit_exit_code([]) == 0
    assert audit_exit_code(["x==1 Y (no fix available)"]) == 1

    print("\n[OK] 40-uv: all checks passed")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        _verify()
    else:
        demo_manifest()
        demo_freshness()
        demo_wheels()
        demo_groups()
        demo_security()
        demo_commands()
        _verify()
