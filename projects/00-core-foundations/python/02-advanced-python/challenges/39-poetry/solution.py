"""
Challenge 39: Poetry - The CI Dependency Gate - Reference Solution
==================================================================
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable

import tomllib  # type: ignore[import-not-found]

_PROJECT_KEYS = (
    "name",
    "version",
    "description",
    "requires-python",
    "dependencies",
    "optional-dependencies",
)
_POETRY_KEYS = ("source", "extras", "dev-dependencies", "group", "dependencies")
_OPERATOR = re.compile(r"^(>=|<=|==|>|<)")
_SPEC_START = ("<", ">", "=", "!")


def _ints(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in re.findall(r"\d+", version))


def _padded(parts: tuple[int, ...], width: int = 3) -> str:
    padded = parts + (0,) * max(0, width - len(parts))
    return ".".join(str(p) for p in padded[: max(width, len(parts))])


def expand_constraint(spec: str) -> tuple[str, str]:
    """Expand a Poetry constraint into a (lower, upper) PEP 508 pair.

    Why this approach: expand once into numeric bounds and reuse the pair for
    both range checks and messages, instead of calling Poetry's spec parser per
    dependency. Alternative: parse everything through packaging.specifiers -
    accurate but slower and it rejects Poetry's caret/tilde syntax.
    """
    spec = spec.strip()
    if not spec:
        return ("", "")
    if spec.startswith(("!", "===")):
        raise ValueError(f"unsupported operator: {spec}")
    if "," in spec:
        lower = ""
        upper = ""
        for part in (p.strip() for p in spec.split(",")):
            if part.startswith(("!", "===")):
                raise ValueError(f"unsupported operator: {part}")
            if part.startswith("<"):
                upper = upper or part
            elif part.startswith((">", "==")):
                lower = lower or part
            else:
                raise ValueError(f"unsupported clause: {part}")
        return (lower, upper)
    if spec.startswith("^"):
        parts = _ints(spec[1:])
        if not parts:
            raise ValueError(f"bad version: {spec}")
        if parts[0] > 0:
            upper = f"<{parts[0] + 1}.0.0"
        elif len(parts) == 1:
            upper = "<1.0.0"
        elif parts[1] > 0:
            upper = f"<0.{parts[1] + 1}.0"
        else:
            upper = f"<0.0.{parts[2] + 1 if len(parts) > 2 else 1}"
        return (f">={spec[1:]}", upper)
    if spec.startswith("~="):
        parts = _ints(spec[2:])
        if len(parts) < 2:
            raise ValueError(f"bad compatible release: {spec}")
        head = list(parts[:-1])
        head[-1] += 1
        return (f">={_padded(parts)}", f"<{_padded(tuple(head))}")
    if spec.startswith("~"):
        parts = _ints(spec[1:])
        if not parts:
            raise ValueError(f"bad version: {spec}")
        if len(parts) >= 2:
            upper = f"<{parts[0]}.{parts[1] + 1}.0"
        elif len(parts) == 1:
            upper = f"<{parts[0] + 1}.0.0"
        else:
            raise ValueError(f"bad version: {spec}")
        return (f">={spec[1:]}", upper)
    if spec.endswith(".*"):
        parts = _ints(spec[:-2])
        if len(parts) < 2:
            raise ValueError(f"bad wildcard: {spec}")
        return (f">={_padded(parts)}", f"<{parts[0]}.{parts[1] + 1}.0")
    if spec[0] in _SPEC_START:
        if spec.startswith((">=", "<=")):
            return (spec, "") if spec[0] == ">" else ("", spec)
        if spec.startswith("=="):
            return (spec, "")
        if spec.startswith(">"):
            return (spec, "")
        return ("", spec)
    return (f"=={spec}", "")


def _split_dep(dep: str) -> tuple[str, str]:
    text = dep.strip()
    i = 0
    while i < len(text) and (text[i].isalnum() or text[i] in "._-"):
        i += 1
    name = text[:i]
    rest = text[i:].strip()
    if rest.startswith("["):
        rest = rest[rest.index("]") + 1 :].strip()
    if rest.startswith("(") and rest.endswith(")"):
        rest = rest[1:-1].strip()
    if rest and rest[0] not in _SPEC_START:
        raise ValueError(f"bad dependency: {dep}")
    return (name, rest)


def _vtuple(version: str) -> tuple[int, ...]:
    parts = _ints(version)
    return parts or (0,)


def _fits(version: str, lower: str, upper: str) -> bool:
    target = _vtuple(version)
    if lower.startswith("=="):
        bound = _vtuple(_OPERATOR.sub("", lower))
        width = max(len(target), len(bound))
        return _pad(target, width) == _pad(bound, width)
    if lower:
        bound = _vtuple(_OPERATOR.sub("", lower))
        width = max(len(target), len(bound))
        if _pad(target, width) < _pad(bound, width):
            return False
    if upper:
        bound = _vtuple(_OPERATOR.sub("", upper))
        width = max(len(target), len(bound))
        if _pad(target, width) >= _pad(bound, width):
            return False
    return True


def _pad(parts: tuple[int, ...], width: int) -> tuple[int, ...]:
    return parts + (0,) * (width - len(parts))


def install_closure(locked: list[dict], roots: list[str]) -> list[str]:
    """Return every package reachable from roots, sorted ascending.

    Why this approach: hash the package list once, then walk with a seen set -
    O(n) comparisons on a 2000-package chain. Alternative: scan the list for
    each name - simpler but O(n^2) and it blows the test's comparison budget.
    """
    index = {str(p["name"]): p for p in locked}
    seen: set[str] = set()
    order: list[str] = []
    stack = list(roots)
    while stack:
        name = str(stack.pop())
        if name in seen:
            continue
        seen.add(name)
        order.append(name)
        node = index.get(name)
        if node is not None:
            stack.extend(str(d) for d in node.get("dependencies", []))
    return sorted(order)


def _content_hash(manifest: dict) -> str:
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


def _poetry(manifest: dict) -> dict:
    return (manifest.get("tool") or {}).get("poetry") or {}


def _available_groups(manifest: dict) -> set[str]:
    declared = _poetry(manifest).get("group") or {}
    return {"main"} | set(declared) | set(manifest.get("dependency-groups") or {})


def _select_groups(
    manifest: dict,
    only: list[str] | None,
    with_groups: list[str] | None,
    without: list[str] | None,
) -> list[str]:
    available = _available_groups(manifest)
    for names in (only, with_groups, without):
        if names:
            unknown = [n for n in names if n not in available]
            if unknown:
                raise ValueError(f"unknown group(s): {', '.join(sorted(unknown))}")
    if only is not None:
        selected = set(only)
    else:
        declared = _poetry(manifest).get("group") or {}
        selected = {"main"}
        selected |= {n for n, cfg in declared.items() if not (cfg or {}).get("optional")}
        selected |= set(with_groups or ())
        selected -= set(without or ())
    return sorted(selected)


def _direct_entries(manifest: dict, groups: list[str]) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for dep in (manifest.get("project") or {}).get("dependencies", []):
        entries.append(_split_dep(dep))
    declared = _poetry(manifest).get("group") or {}
    for group in groups:
        cfg = declared.get(group) or {}
        for dep, value in (cfg.get("dependencies") or {}).items():
            if isinstance(value, str):
                spec = value
            elif isinstance(value, dict):
                spec = str(value.get("version", ""))
            else:
                spec = ""
            entries.append((_split_dep(dep)[0], spec))
        for dep in (manifest.get("dependency-groups") or {}).get(group) or []:
            if isinstance(dep, str):
                entries.append(_split_dep(dep))
    deduped: dict[str, str] = {}
    for name, spec in entries:
        deduped.setdefault(name, spec)
    return sorted(deduped.items())


def audit_manifest(
    pyproject_text: str,
    lock_text: str,
    fetch_meta: Callable[[str], float],
    *,
    only: list[str] | None = None,
    with_groups: list[str] | None = None,
    without: list[str] | None = None,
) -> dict:
    """Audit manifest against lock: freshness, groups, ranges, size budget.

    Why this approach: fetch every unique size once into a cache, then sum -
    two lookups become one pass. Alternative: sum direct sizes in one loop and
    total sizes in a second - correct, but the fake index rejects the repeated
    fetch and the audit dies before it reports anything.
    """
    manifest = tomllib.loads(pyproject_text)
    lock = tomllib.loads(lock_text)
    groups = _select_groups(manifest, only, with_groups, without)
    locked = {p["name"]: p for p in lock.get("package", [])}
    content_hash = (lock.get("metadata") or {}).get("content-hash")
    fresh = bool(content_hash) and content_hash == _content_hash(manifest)

    entries = _direct_entries(manifest, groups)
    unsatisfied: list[str] = []
    for name, spec in entries:
        if name not in locked:
            unsatisfied.append(f"{name}: missing from lock")
        else:
            lower, upper = expand_constraint(spec)
            version = str(locked[name].get("version", ""))
            if not _fits(version, lower, upper):
                unsatisfied.append(f"{name}: {version} outside {spec}")

    direct = {name for name, _ in entries}
    total = set(locked)
    sizes = {name: float(fetch_meta(name)) for name in sorted(direct | total)}
    return {
        "fresh": fresh,
        "groups": groups,
        "unsatisfied": sorted(unsatisfied),
        "direct_size_mb": sum(sizes[name] for name in sorted(direct)),
        "total_size_mb": sum(sizes[name] for name in sorted(total)),
        "fetches": len(sizes),
    }
