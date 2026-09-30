"""
Challenge 01: Component Contracts — Reference Solution
======================================================
"""

from __future__ import annotations


def _optional(semantic: str) -> bool:
    return "optional" in semantic


def classify_change(old: dict, new: dict) -> str:
    """Return 'compatible' | 'needs-migration' | 'breaking'.

    Why this approach: set arithmetic on field names is O(n) and sees every
    direction of change at once — removals and semantic edits are breaking
    because consumers read those fields today; required additions are
    migrations because old producers emit nothing; optional additions are
    ignorable by definition.
    """
    old_req: dict = old.get("required", {})
    new_req: dict = new.get("required", {})
    removed = set(old_req) - set(new_req)
    changed = {f for f in set(old_req) & set(new_req) if old_req[f] != new_req[f]}
    added_required = {f for f in set(new_req) - set(old_req) if not _optional(new_req[f])}
    if removed or changed:
        return "breaking"
    if added_required:
        return "needs-migration"
    return "compatible"


def validate_payload(payload: dict, contract: dict) -> list[str]:
    """Return ALL violations: missing required fields, empty text, broken source_ref.

    Why this approach: collecting every violation in one pass gives the
    operator the complete quarantine list. Fail-fast hides the other two
    problems and forces re-runs to find them.
    """
    problems: list[str] = []
    required: dict = contract.get("required", {})
    for field, semantic in required.items():
        if _optional(semantic):
            continue
        if field not in payload:
            problems.append(f"missing required field: {field}")
    text = str(payload.get("text", ""))
    if not text.strip():
        problems.append("invariant violated: text is empty")
    book = str(payload.get("book", ""))
    page = str(payload.get("page", ""))
    ref = str(payload.get("source_ref", ""))
    expected = f"{book}/p{page}"
    if ref and ref != expected:
        problems.append(f"invariant violated: source_ref {ref!r} != {expected!r}")
    return problems


_MIGRATION_STEPS = ["emit-default", "consumers-tolerate", "backfill", "require"]


def plan_migration(old: dict, new: dict) -> list[str]:
    """Return ordered rolling-upgrade steps for adding a required field.

    Why this approach: the four steps are the only sequence where both the
    old and the new producer coexist at every intermediate state. Each
    step is safe alone; skipping to the end is the 3 a.m. outage.
    """
    if classify_change(old, new) == "needs-migration":
        return list(_MIGRATION_STEPS)
    return []


def _step_accepts(step: str, rec: dict, field: str) -> bool:
    if step == "require":
        return field in rec
    return True


def simulate_migration(plan: list[str], old_rec: dict, new_rec: dict) -> bool:
    """True iff plan is a safe rolling upgrade.

    Why this approach: the invariant is checked step by step — before
    `require` both records must survive (that is the whole point of the
    window), and `require` flips exactly one way. A one-step plan fails
    on the first check because the old record dies immediately.
    """
    if not plan or plan[-1] != "require":
        return False
    field = next((f for f in new_rec if f not in old_rec), None)
    if field is None:
        return False
    # the deprecation window must actually exist: at least one step where
    # the old producer still works, or the rollout is a big-bang cutover
    if not any(_step_accepts(step, old_rec, field) for step in plan[:-1]):
        return False
    for step in plan[:-1]:
        if not _step_accepts(step, old_rec, field):
            return False
        if not _step_accepts(step, new_rec, field):
            return False
    return _step_accepts("require", new_rec, field) and not _step_accepts("require", old_rec, field)
