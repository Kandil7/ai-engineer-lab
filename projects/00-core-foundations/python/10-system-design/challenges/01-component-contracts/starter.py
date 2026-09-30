"""
Challenge 01: Component Contracts — Starter Code
=================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations


def classify_change(old: dict, new: dict) -> str:
    """Return 'compatible' | 'needs-migration' | 'breaking' for a contract change."""
    raise NotImplementedError


def validate_payload(payload: dict, contract: dict) -> list[str]:
    """Return ALL violations: missing required fields, empty text, broken source_ref."""
    raise NotImplementedError


def plan_migration(old: dict, new: dict) -> list[str]:
    """Return ordered rolling-upgrade steps for adding a required field."""
    raise NotImplementedError


def simulate_migration(plan: list[str], old_rec: dict, new_rec: dict) -> bool:
    """True iff plan is a safe rolling upgrade (both work early, only new at require)."""
    raise NotImplementedError
