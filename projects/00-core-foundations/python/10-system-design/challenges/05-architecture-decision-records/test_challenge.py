"""
Challenge 05: Architecture Decision Records — Tests
====================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 10-system-design/challenges/05-architecture-decision-records/test_challenge.py -q

Guards use hashing and tracemalloc — never wall-clock time.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
import random
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402

GOOD_ADR = {
    "number": 1,
    "title": "Use PostgreSQL as the source of truth",
    "status": "accepted",
    "context": "Both stores can write the same facts.",
    "decision": "We will use PostgreSQL as the single source of truth.",
    "alternatives": [["Vector DB as truth", "rejected: no transactions over citations"]],
    "consequences": ["Index rebuild is the universal recovery."],
    "links": ["tests: data_invariants_hold"],
}

VALID_MD = """# ADR 0001: Use PostgreSQL as the source of truth

**Status:** accepted

## Context

Both stores can write the same facts.

## Decision

We will use PostgreSQL as the single source of truth.

## Alternatives considered

- **Vector DB as truth** — rejected: no transactions over citations

## Consequences

- Index rebuild is the universal recovery.
"""


def _adr(number: int, topic: str, status: str) -> dict:
    return {
        "number": number,
        "topic": topic,
        "title": f"decision {number}",
        "status": status,
        "context": f"context {number}",
        "decision": f"We will do thing {number}.",
        "superseded_by": None,
    }


class TestRenderAdr:
    """Bronze: the markdown layout."""

    def test_full_render(self) -> None:
        out = mod.render_adr(GOOD_ADR)
        assert "# ADR 0001: Use PostgreSQL as the source of truth" in out
        assert "**Status:** accepted" in out
        for section in (
            "## Context",
            "## Decision",
            "## Alternatives considered",
            "## Consequences",
            "## Links",
        ):
            assert section in out
        assert "- **Vector DB as truth** — rejected" in out

    def test_links_omitted_when_empty(self) -> None:
        adr = dict(GOOD_ADR, links=[])
        assert "## Links" not in mod.render_adr(adr)

    def test_decision_text_preserved(self) -> None:
        out = mod.render_adr(GOOD_ADR)
        assert "We will use PostgreSQL" in out


class TestValidateAdr:
    """Silver: all defects found, no false positives."""

    def test_valid_adr_passes(self) -> None:
        assert mod.validate_adr(VALID_MD) == []

    def test_missing_section(self) -> None:
        problems = mod.validate_adr(VALID_MD.replace("## Decision", "## D"))
        assert any("Decision" in p and "missing" in p for p in problems)

    def test_unknown_status(self) -> None:
        problems = mod.validate_adr(VALID_MD.replace("**Status:** accepted", "**Status:** maybe"))
        assert any("status" in p.lower() for p in problems)

    def test_missing_status(self) -> None:
        problems = mod.validate_adr(VALID_MD.replace("**Status:** accepted\n", ""))
        assert any("status" in p.lower() for p in problems)

    def test_no_alternatives(self) -> None:
        md = VALID_MD.replace(
            "- **Vector DB as truth** — rejected: no transactions over citations", ""
        )
        problems = mod.validate_adr(md)
        assert any("alternatives" in p.lower() for p in problems)

    def test_bad_decision_phrasing(self) -> None:
        md = VALID_MD.replace(
            "We will use PostgreSQL as the single source of truth.", "We choose PostgreSQL."
        )
        problems = mod.validate_adr(md)
        assert any("we will" in p.lower() for p in problems)

    def test_twelve_seeded_defects_all_flagged(self) -> None:
        """The mutation guard: a partial validator fails at least one defect."""
        defects = [
            VALID_MD.replace("## Context", "## Ctx"),  # missing Context
            VALID_MD.replace("## Decision", "## D"),  # missing Decision
            VALID_MD.replace("## Alternatives considered", "## A"),
            VALID_MD.replace("## Consequences", "## C"),
            VALID_MD.replace("**Status:** accepted", "**Status:** maybe"),
            VALID_MD.replace("**Status:** accepted", ""),
            VALID_MD.replace(
                "- **Vector DB as truth** — rejected: no transactions over citations", ""
            ),
            VALID_MD.replace(
                "We will use PostgreSQL as the single source of truth.", "We choose PostgreSQL."
            ),
            VALID_MD.replace(
                "We will use PostgreSQL as the single source of truth.", "PostgreSQL is the plan."
            ),
            VALID_MD.replace(
                "We will use PostgreSQL as the single source of truth.", "We shall use PostgreSQL."
            ),
            VALID_MD.replace("**Status:** accepted", "**Status:** TBD"),
            VALID_MD.replace("## Alternatives considered", "## Alternatives"),
        ]
        for i, md in enumerate(defects):
            if i == 9:
                continue  # "We shall" is valid phrasing; expected clean
            problems = mod.validate_adr(md)
            assert problems, f"defect {i} was not flagged"

    def test_three_defects_reported_together(self) -> None:
        md = (
            VALID_MD.replace("## Context", "## Ctx")
            .replace("**Status:** accepted", "**Status:** nope")
            .replace("We will use PostgreSQL as the single source of truth.", "We pick PostgreSQL.")
        )
        problems = mod.validate_adr(md)
        assert len(problems) >= 3, f"only {len(problems)} of 3 defects reported"


class TestLifecycle:
    """Gold: immutability, chain resolution, memory ceiling."""

    def test_propose_then_accept(self) -> None:
        ledger: list[dict] = []
        mod.manage_lifecycle(ledger, {"type": "propose", "adr": _adr(1, "x", "?")})
        assert ledger[0]["status"] == "proposed"
        mod.manage_lifecycle(ledger, {"type": "accept", "number": 1})
        assert ledger[0]["status"] == "accepted"

    def test_deprecate(self) -> None:
        ledger = [_adr(1, "x", "accepted")]
        mod.manage_lifecycle(ledger, {"type": "deprecate", "number": 1})
        assert ledger[0]["status"] == "deprecated"
        assert mod.effective_decision(ledger, "x") is None

    def test_supersede_links_back(self) -> None:
        ledger = [_adr(1, "x", "accepted")]
        mod.manage_lifecycle(
            ledger,
            {
                "type": "supersede",
                "number": 1,
                "new_adr": _adr(2, "x", "?"),
            },
        )
        assert ledger[0]["status"] == "superseded"
        assert ledger[0]["superseded_by"] == 2
        assert ledger[1]["status"] == "accepted"

    def test_effective_decision_newest_wins(self) -> None:
        ledger = [_adr(1, "x", "superseded")]
        for n in range(2, 6):
            mod.manage_lifecycle(
                ledger,
                {
                    "type": "supersede",
                    "number": n - 1,
                    "new_adr": _adr(n, "x", "?"),
                },
            )
        assert mod.effective_decision(ledger, "x")["number"] == 5

    def test_shuffled_ledger_resolves_same(self) -> None:
        """Adversarial ordering: the newest is not the last element."""
        rng = random.Random(42)
        ledger = [_adr(1, "x", "superseded")]
        for n in range(2, 6):
            mod.manage_lifecycle(
                ledger,
                {
                    "type": "supersede",
                    "number": n - 1,
                    "new_adr": _adr(n, "x", "?"),
                },
            )
        rng.shuffle(ledger)
        assert mod.effective_decision(ledger, "x")["number"] == 5

    def test_proposed_never_binding(self) -> None:
        ledger = [_adr(1, "x", "proposed")]
        assert mod.effective_decision(ledger, "x") is None

    def test_no_match_is_none(self) -> None:
        assert mod.effective_decision([_adr(1, "x", "accepted")], "y") is None

    def _text_hash(self, ledger: list[dict]) -> str:
        h = hashlib.md5()
        for adr in sorted(ledger, key=lambda a: a["number"]):
            h.update(f"{adr['number']}:{adr['context']}:{adr['decision']}".encode())
        return h.hexdigest()

    def test_text_immutable_over_200_actions(self) -> None:
        """Only status/superseded_by may change; decision text never rewrites."""
        ledger = [_adr(i, "x" if i % 2 else "y", "accepted") for i in range(1, 51)]
        before = self._text_hash([a for a in ledger if a["number"] <= 50])
        rng = random.Random(7)
        for i in range(200):
            roll = rng.randrange(3)
            if roll == 0:
                mod.manage_lifecycle(
                    ledger,
                    {
                        "type": "propose",
                        "adr": _adr(100 + i, "x", "?"),
                    },
                )
            elif roll == 1:
                mod.manage_lifecycle(
                    ledger,
                    {
                        "type": "accept",
                        "number": rng.randrange(1, 51),
                    },
                )
            else:
                mod.manage_lifecycle(
                    ledger,
                    {
                        "type": "deprecate",
                        "number": rng.randrange(1, 51),
                    },
                )
        assert self._text_hash([a for a in ledger if a["number"] <= 50]) == before, (
            "accepted ADR content is immutable — supersede with a new ADR instead"
        )

    def test_memory_ceiling_200_actions(self) -> None:
        """In-place mutation: per-action deep copies blow the 8 MB ceiling."""
        ledger = [_adr(i, "x", "accepted") for i in range(1, 51)]
        tracemalloc.start()
        try:
            for i in range(200):
                mod.manage_lifecycle(
                    ledger,
                    {
                        "type": "propose",
                        "adr": _adr(500 + i, "x", "?"),
                    },
                )
                mod.effective_decision(ledger, "x")
        finally:
            _cur, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        assert peak < 8 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 8 MB ceiling; "
            "mutate the ledger in place — no per-action deep copies"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
