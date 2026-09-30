"""
Architecture Decision Records - System Design Exercises
========================================================
Topics: ADR structure, when to write one, decision log, status
lifecycle, recording consequences and alternatives, linking decisions
to code and tests.

Why this matters for AI engineering:
    Six months after someone chose "Postgres is the source of truth,
    the vector index is derived", a new teammate will ask why the index
    is not backed up. The answer must not depend on who is in the room.
    An ADR is the durable artifact: context, decision, alternatives,
    consequences - written at decision time, versioned with the code.
    This file builds the ADR format, validates ADR documents, and
    writes the real Athar decision as a worked example.

Environment note:
    Pure standard library. Runnable offline.

Run:      python 05-architecture-decision-records.py
Verify:   python 05-architecture-decision-records.py --verify
Reference: https://adr.github.io/ (MADR template)
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. What an ADR is (and is not)
# ============================================================
# ADR = Architecture Decision Record: a short, versioned document
# capturing ONE significant decision. It is:
#   - written when the decision is made (not reconstructed later)
#   - immutable in content once accepted (status changes only)
#   - reviewed like code (a PR to docs/decisions/)
# It is NOT: a design doc (that is longer, covers a system), a wiki
# page (rot), or a meeting note (unstructured).

print("1. ADR: one decision, one document, written at decision time")
print("   accepted ADRs are immutable; only status changes")
print()


# ============================================================
# 2. The ADR structure (MADR-informed, minimal)
# ============================================================
#   Title        - short, decision-shaped ("Use Postgres as source of truth")
#   Status       - proposed | accepted | deprecated | superseded by NNNN
#   Context      - forces, constraints, the problem (facts, not opinions)
#   Decision     - the choice, stated as "we will ..."
#   Alternatives - what we considered and why not (the value is HERE)
#   Consequences - what becomes easier / harder / new risks
#   Links        - issues, PRs, tests that enforce the decision


@dataclass
class ADR:
    number: int
    title: str
    status: str
    context: str
    decision: str
    alternatives: list[tuple[str, str]] = field(default_factory=list)
    consequences: tuple[str, ...] = ()
    links: tuple[str, ...] = ()

    def to_markdown(self) -> str:
        lines = [
            f"# ADR {self.number:04d}: {self.title}",
            "",
            f"**Status:** {self.status}",
            "",
            "## Context",
            "",
            self.context,
            "",
            "## Decision",
            "",
            self.decision,
            "",
            "## Alternatives considered",
            "",
        ]
        for name, why_not in self.alternatives:
            lines.append(f"- **{name}** — {why_not}")
        lines += ["", "## Consequences", ""]
        for c in self.consequences:
            lines.append(f"- {c}")
        if self.links:
            lines += ["", "## Links", ""]
            for link in self.links:
                lines.append(f"- {link}")
        return "\n".join(lines)


# ============================================================
# 3. Validation: an ADR is only useful if complete
# ============================================================
# A structural validator turns "we should write ADRs" into "this ADR
# is not acceptable yet". The rules below are the team's contract.


REQUIRED_SECTIONS = ["## Context", "## Decision", "## Alternatives considered", "## Consequences"]


def validate_adr(md: str) -> list[str]:
    """Return problems with an ADR document (empty = acceptable)."""
    problems = []
    for section in REQUIRED_SECTIONS:
        if section not in md:
            problems.append(f"missing section: {section}")
    status = re.search(r"\*\*Status:\*\*\s*(\w+)", md)
    if not status:
        problems.append("missing or malformed Status line")
    elif status.group(1) not in {"proposed", "accepted", "deprecated", "superseded"}:
        problems.append(f"unknown status: {status.group(1)}")
    if md.count("## Alternatives considered") == 1:
        # an empty alternatives list is a review smell: what was rejected?
        after = md.split("## Alternatives considered", 1)[1].split("## Consequences")[0]
        if "-" not in after:
            problems.append("no alternatives recorded (review smell)")
    if "we will" not in md.lower() and "we shall" not in md.lower():
        problems.append("decision not phrased as 'we will ...'")
    return problems


print("3. ADR validation rules")
for rule in [
    "required sections",
    "status in lifecycle",
    "alternatives recorded",
    "decision phrased 'we will'",
]:
    print(f"   - {rule}")
print()


# ============================================================
# 4. The worked example: the Athar source-of-truth decision
# ============================================================

ATHAR_ADR = ADR(
    number=1,
    title="Use PostgreSQL as the source of truth; vector index is derived",
    status="accepted",
    context=(
        "The Athar pipeline stores books, editions, page texts, and permission "
        "records, and serves retrieval through a vector index. Both stores can "
        "write the same facts. We need one authoritative store per fact so that "
        "backup, restore, and index rebuild have a defined recovery path, and so "
        "citations (book/page) cannot silently diverge from the corpus."
    ),
    decision=(
        "We will use PostgreSQL as the single source of truth for all catalog "
        "facts (books, editions, pages, permissions, lineage keys). The vector "
        "index will be treated as a derived store: it stores source_ref keys and "
        "embeddings only, is rebuildable from Postgres at any time, and is not "
        "part of the backup surface. Staleness is measured as drift and recovered "
        "by rebuild."
    ),
    alternatives=[
        (
            "Vector DB as source of truth",
            "rejected: no transactions over citations; rebuild path does not exist; "
            "backup/restore semantics weaker than Postgres.",
        ),
        (
            "Dual-write to both stores",
            "rejected: divergence is inevitable; no single recovery point; "
            "corruption discovered late as wrong citations.",
        ),
        (
            "SQLite as source of truth",
            "rejected: concurrent writer load from ingest workers exceeds "
            "single-writer limits; no PITR story.",
        ),
    ],
    consequences=(
        "Index rebuild is the universal recovery for index problems.",
        "Every derived entry must carry source_ref (lineage key invariant).",
        "Ingest writes go through Postgres first; index updates follow.",
        "Drift monitoring is mandatory (source vs index version stamps).",
    ),
    links=(
        "docs/learning/adr/0001-source-of-truth.md",
        "tests: data_invariants_hold (no-loss, provenance)",
    ),
)

print("4. worked example: ADR-0001")
md = ATHAR_ADR.to_markdown()
print(md)
print()
problems = validate_adr(md)
print(f"   validation problems: {problems or 'none - acceptable'}")
print()


# ============================================================
# 5. The status lifecycle
# ============================================================
#   proposed -> accepted -> superseded by NNNN
#                \-> deprecated (decision withdrawn, no replacement)
# A superseding ADR links back; the old one stays (history matters).
# Never edit the content of an accepted ADR - write a new one.

LIFECYCLE = [
    ("proposed", "written, under review"),
    ("accepted", "merged; the decision is binding"),
    ("deprecated", "withdrawn; no replacement"),
    ("superseded", "replaced by a newer ADR (linked)"),
]

print("5. status lifecycle")
for status, meaning in LIFECYCLE:
    print(f"   {status:12} {meaning}")
print()


# ============================================================
# 6. When to write an ADR (the threshold test)
# ============================================================
# Write one when ALL of these hold:
#   - the choice is hard to reverse OR affects multiple components
#   - reasonable engineers could disagree (real alternatives exist)
#   - future readers will ask "why?"
# Do NOT write one for: style choices (linters own those), routine
# library picks with one obvious answer, or decisions already covered
# by an existing ADR's consequences.

WRITE_ADR_CHECKLIST = [
    ("hard to reverse?", "schema ownership, store selection, auth model"),
    ("cross-component impact?", "affects contracts, tests, ops runbooks"),
    ("real alternatives?", "you can name one you rejected and why"),
    ("future 'why?'", "someone will ask in 6 months"),
]

print("6. when to write an ADR")
for question, example in WRITE_ADR_CHECKLIST:
    print(f"   {question:26} e.g. {example}")
print()


# ============================================================
# 7. ADRs link to enforcement
# ============================================================
# An ADR without an enforcement link is a wish. The pattern:
#   decision -> the test/config/lint that keeps it true
# "index is derived"   -> rebuild test; backup excludes index
# "contracts versioned" -> contract tests in CI
# "lineage immutable"   -> invariant test on source_ref
# The Links section carries these; review checks they exist.

ENFORCEMENT_EXAMPLES = [
    ("Postgres is source of truth", "rebuild-from-source test; backup surface excludes index"),
    ("lineage keys immutable", "data invariant: source_ref carried through pipeline"),
    ("contracts are versioned", "contract tests in producer+consumer CI"),
    ("retries capped", "queue max_attempts + DLQ depth alert"),
]

print("7. decision -> enforcement")
for decision, enforcement in ENFORCEMENT_EXAMPLES:
    print(f"   {decision:32} -> {enforcement}")
print()


# ============================================================
# 8. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []
    md = ATHAR_ADR.to_markdown()

    checks.append(("worked example validates clean", validate_adr(md) == []))

    bad = "# ADR 0002: Something\n\n**Status:** accepted\n\n## Context\n\nx."
    problems = validate_adr(bad)
    checks.append(
        ("incomplete ADR is rejected", any("missing section: ## Decision" in p for p in problems))
    )

    checks.append(
        (
            "unknown status rejected",
            any(
                "unknown status" in p
                for p in validate_adr(md.replace("**Status:** accepted", "**Status:** maybe"))
            ),
        )
    )

    empty_alts = (
        md.split("## Alternatives considered")[0]
        + "## Alternatives considered\n\n## Consequences\n\n- x"
    )
    checks.append(
        (
            "empty alternatives flagged",
            any("no alternatives" in p for p in validate_adr(empty_alts)),
        )
    )

    checks.append(
        (
            "all lifecycle statuses defined",
            {s for s, _ in LIFECYCLE} == {"proposed", "accepted", "deprecated", "superseded"},
        )
    )

    checks.append(("decision phrased as 'we will'", "we will use postgresql" in md.lower()))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 05-architecture-decision-records.py --verify):")
    _verify()
