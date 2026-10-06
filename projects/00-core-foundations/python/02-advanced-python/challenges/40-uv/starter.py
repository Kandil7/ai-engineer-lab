"""
Challenge 40: uv - The Reproducible Environment - Starter Code
===============================================================
Fill in the bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def wheel_tags(filename: str) -> dict:
    """Split a wheel filename into its tag components.

    Returns {"name", "version", "python_tag", "abi_tag", "platform_tag"}.
    Raises ValueError on a non-.whl name or fewer than 5 dash-separated
    parts (name-version-python-abi-platform).
    """
    raise NotImplementedError


class WheelIndex:
    """Index a universal lock's wheels once, then answer many queries.

    The parse callable is injected so tests can count how often filenames
    are parsed. Parsing must happen once per wheel for the index's
    lifetime, not once per query.
    """

    def __init__(self, wheels: list[str], parse: Callable[[str], dict]) -> None:
        raise NotImplementedError

    def select(self, python_tag: str, platform_tag: str) -> list[str]:
        """Wheels installable on (python_tag, platform_tag), in listed order.

        Simplified PEP 425 rules:
        - python: exact tag match, 'py3', or abi3 built for an older
          CPython of the same implementation (cp39-abi3 runs on cp312)
        - abi: the interpreter's own tag, 'abi3', or 'none'
        - platform: exact match or 'any'
        """
        raise NotImplementedError


def audit_stream(
    packages: Iterable[dict],
    advisories: dict[str, list[dict]],
    ignore: frozenset[str] | set[str] = frozenset(),
) -> list[str]:
    """Audit a lock's packages against advisories without materializing it.

    `packages` yields {"name": str, "version": str} dicts. `advisories`
    maps package name -> list of {"id": str, "fixed_in": str | None}.
    A version is vulnerable when it is older than fixed_in; fixed_in None
    means no fix is available. Findings are returned sorted, ignoring
    advisory ids in `ignore`. The iterator must be consumed
    incrementally: holding all packages in memory at once fails the
    memory guard.
    """
    raise NotImplementedError


def audit_exit_code(findings: list[str]) -> int:
    """uv audit exits non-zero when findings exist."""
    raise NotImplementedError
