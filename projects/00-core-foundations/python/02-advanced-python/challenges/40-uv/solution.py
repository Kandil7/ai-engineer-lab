"""
Challenge 40: uv - The Reproducible Environment - Reference Solution
=====================================================================
Each docstring states WHY the approach wins against the alternative.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def wheel_tags(filename: str) -> dict:
    """Split a wheel filename into its tag components.

    Why this approach: a wheel filename is 'name-version-python-abi-platform'
    with the distribution name normalized to '_', so a plain split on '-'
    is exact and O(1) in the number of tags. Regex would work but adds a
    failure mode (unescaped dots in names) without adding information.
    """
    if not filename.endswith(".whl"):
        raise ValueError(f"not a wheel filename: {filename}")
    stem = filename[:-4]
    parts = stem.split("-")
    if len(parts) < 5:
        raise ValueError(f"not a wheel filename: {filename}")
    name, version = parts[0], parts[1]
    python_tag, abi_tag, platform_tag = parts[-3], parts[-2], parts[-1]
    return {
        "name": name,
        "version": version,
        "python_tag": python_tag,
        "abi_tag": abi_tag,
        "platform_tag": platform_tag,
    }


def _python_ok(python_tag: str, wheel_python: str, wheel_abi: str) -> bool:
    """Interpreter compatibility: exact, pure 'py3', or abi3 from an older CPython.

    Why this approach: abi3 wheels are the reason one universal lockfile can
    serve every interpreter - 'cp39-abi3' promises compatibility with all
    CPython >= 3.9, so the check is a minor-version comparison, not equality.
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
    """ABI compatibility: own tag, abi3, or pure ('none').

    Why this approach: these three cases cover every wheel uv installs in
    practice; full PEP 425 tag expansion adds no decisions here.
    """
    return wheel_abi in ("abi3", "none", python_tag)


def _platform_ok(platform_tag: str, wheel_platform: str) -> bool:
    """Platform compatibility: exact tag or 'any'.

    Why this approach: manylinux glibc-version arithmetic is out of scope
    for the challenge; the lock's recorded tags are matched exactly, which
    is what the installer does after full tag resolution has narrowed the
    candidates.
    """
    return wheel_platform == platform_tag or wheel_platform == "any"


class WheelIndex:
    """Index a universal lock's wheels once, then answer many queries.

    Why this approach: parsing each filename once at construction makes
    every select() a scan over pre-parsed tags - O(W) per query with zero
    re-parsing. Re-parsing per query (the naive shape) costs O(W) parses
    per query; at 200 wheels and 100 queries that is 20,000 parses vs 200.
    """

    def __init__(self, wheels: list[str], parse: Callable[[str], dict]) -> None:
        self._entries: list[tuple[str, dict]] = []
        for filename in wheels:
            self._entries.append((filename, parse(filename)))

    def select(self, python_tag: str, platform_tag: str) -> list[str]:
        picked: list[str] = []
        for filename, tags in self._entries:
            if (
                _python_ok(python_tag, tags["python_tag"], tags["abi_tag"])
                and _abi_ok(python_tag, tags["abi_tag"])
                and _platform_ok(platform_tag, tags["platform_tag"])
            ):
                picked.append(filename)
        return picked


def _vkey(version: str) -> tuple[int, ...]:
    """Comparable tuple for a version string (prerelease suffixes dropped).

    Why this approach: padding to a fixed width makes '2.9' and '2.9.0'
    compare equal and '2.10' compare above '2.9' - the two cases string
    comparison gets wrong.
    """
    core = ""
    for ch in version.strip():
        if ch.isdigit() or ch == ".":
            core += ch
        else:
            break
    parts = [int(p) for p in core.split(".") if p]
    return tuple(parts + [0] * (4 - len(parts)))


def audit_stream(
    packages: Iterable[dict],
    advisories: dict[str, list[dict]],
    ignore: frozenset[str] | set[str] = frozenset(),
) -> list[str]:
    """Audit a lock's packages against advisories without materializing it.

    Why this approach: consuming the iterator one package at a time keeps
    peak memory at O(findings) instead of O(packages). A real uv.lock
    reaches hundreds of thousands of wheel entries; list()-ing it first is
    exactly the memory spike the guard exists to catch. Sorting the small
    findings list at the end is O(F log F), not O(P log P).
    """
    findings: list[str] = []
    for package in packages:
        name = str(package["name"]).lower()
        version = str(package["version"])
        for adv in advisories.get(name, []):
            if adv["id"] in ignore:
                continue
            fixed_in = adv.get("fixed_in")
            if fixed_in is None:
                findings.append(f"{name}=={version} {adv['id']} (no fix available)")
            elif _vkey(version) < _vkey(fixed_in):
                findings.append(f"{name}=={version} {adv['id']} (fixed in {fixed_in})")
    findings.sort()
    return findings


def audit_exit_code(findings: list[str]) -> int:
    """uv audit exits non-zero when findings exist.

    Why this approach: the exit code is the CI contract - a pipeline gates
    on it without parsing output.
    """
    return 1 if findings else 0
