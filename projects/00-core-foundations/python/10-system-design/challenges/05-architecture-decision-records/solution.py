"""
Challenge 05: Architecture Decision Records — Reference Solution
================================================================
"""

from __future__ import annotations

_STATUSES = {"proposed", "accepted", "deprecated", "superseded"}


def render_adr(adr: dict) -> str:
    """Render an ADR dict to the standard markdown layout.

    Why this approach: the layout is fixed so the validator can parse it
    mechanically — a decision ledger only scales if its documents are
    uniform enough for tooling to check.
    """
    lines = [
        f"# ADR {adr['number']:04d}: {adr['title']}",
        "",
        f"**Status:** {adr['status']}",
        "",
        "## Context",
        "",
        adr["context"],
        "",
        "## Decision",
        "",
        adr["decision"],
        "",
        "## Alternatives considered",
        "",
    ]
    for name, why_not in adr.get("alternatives", []):
        lines.append(f"- **{name}** — {why_not}")
    lines += ["", "## Consequences", ""]
    for item in adr.get("consequences", []):
        lines.append(f"- {item}")
    links = adr.get("links", [])
    if links:
        lines += ["", "## Links", ""]
        for link in links:
            lines.append(f"- {link}")
    return "\n".join(lines)


def validate_adr(md: str) -> list[str]:
    """Return ALL completeness problems with an ADR document.

    Why this approach: collecting every defect in one pass turns review
    into a checklist instead of a hunt — the author fixes them all in one
    round instead of one per CI run.
    """
    problems: list[str] = []
    for section in (
        "## Context",
        "## Decision",
        "## Alternatives considered",
        "## Consequences",
    ):
        if section not in md:
            problems.append(f"missing section: {section}")

    status_line = None
    for line in md.splitlines():
        if line.startswith("**Status:**"):
            status_line = line[len("**Status:**") :].strip()
            break
    if status_line is None:
        problems.append("missing or malformed Status line")
    elif status_line not in _STATUSES:
        problems.append(f"unknown status: {status_line}")

    if "## Alternatives considered" in md:
        after = md.split("## Alternatives considered", 1)[1]
        before = after.split("## Consequences")[0] if "## Consequences" in after else after
        if "-" not in before:
            problems.append("no alternatives recorded (review smell)")

    decision_text = ""
    if "## Decision" in md:
        rest = md.split("## Decision", 1)[1]
        for stop in ("## Alternatives considered", "## Consequences", "## Links"):
            if stop in rest:
                rest = rest.split(stop)[0]
                break
        decision_text = rest.lower()
    if decision_text and "we will" not in decision_text and "we shall" not in decision_text:
        problems.append("decision not phrased as 'we will ...'")
    return problems


def manage_lifecycle(ledger: list[dict], action: dict) -> list[dict]:
    """Apply a lifecycle action in place; never rewrite decision text.

    Why this approach: accepted content is immutable — corrections are new
    ADRs, not edits — so the only mutable fields are status and
    superseded_by. That is what keeps the history truthful.
    """
    kind = action["type"]
    if kind == "propose":
        adr = dict(action["adr"])
        adr["status"] = "proposed"
        adr.setdefault("superseded_by", None)
        ledger.append(adr)
    elif kind == "accept":
        for adr in ledger:
            if adr["number"] == action["number"]:
                adr["status"] = "accepted"
    elif kind == "deprecate":
        for adr in ledger:
            if adr["number"] == action["number"]:
                adr["status"] = "deprecated"
    elif kind == "supersede":
        new_adr = dict(action["new_adr"])
        new_adr["status"] = "accepted"
        new_adr.setdefault("superseded_by", None)
        for adr in ledger:
            if adr["number"] == action["number"]:
                adr["status"] = "superseded"
                adr["superseded_by"] = new_adr["number"]
        ledger.append(new_adr)
    else:
        raise ValueError(f"unknown action: {kind}")
    return ledger


def effective_decision(ledger: list[dict], topic: str) -> dict | None:
    """Return the highest-numbered accepted ADR for the topic, or None.

    Why this approach: binding means accepted — proposed is a draft,
    deprecated is withdrawn, superseded is history. Ranking by number (not
    list position) makes the answer independent of how the ledger is
    stored or shuffled.
    """
    binding = [
        adr for adr in ledger if adr.get("topic") == topic and adr.get("status") == "accepted"
    ]
    if not binding:
        return None
    return max(binding, key=lambda a: a["number"])
