"""Shared fixtures and the src/ import seam for capstone acceptance tests."""

from __future__ import annotations

import sys
from pathlib import Path

# No packaging in this exercise: make src/ importable for the test session.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

T1 = (
    "العلم نور يهدي العقول إلى الحق وهو أساس النهضة والتقدم "
    "في كل أمة تسعى إلى المعرفة والفهم الصحيح لأمور الدين والدنيا معا"
)
# One-letter realistic variant (teh marbuta -> ha): near-duplicate of T1.
T4 = T1.replace("المعرفة", "المعرفه")
C5 = (
    "Rivers shape valleys over centuries as steady water flow "
    "wears down rock and soil along the banks."
)
C6 = (
    "Electric circuits need a closed loop for current to move "
    "through wires resistors and switches."
)

# Fixture records: passage_id / text / source. c2 shares c1's text under another
# id; c3 repeats c1 fully (id + text); c4 is the near-dupe; c7/c8/c9 are rejects.
CORPUS: list[dict[str, str]] = [
    {"passage_id": "b1:p1:0", "text": T1, "source": "bookA"},
    {"passage_id": "b1:p9:0", "text": T1, "source": "bookB"},
    {"passage_id": "b1:p1:0", "text": T1, "source": "bookA"},
    {"passage_id": "b1:p2:0", "text": T4, "source": "bookA"},
    {"passage_id": "b2:c5:0", "text": C5, "source": "bookB"},
    {"passage_id": "b2:c6:0", "text": C6, "source": "bookB"},
    {"passage_id": "b3:empty:0", "text": "   ", "source": "bookC"},
    {"passage_id": "b3:short:0", "text": "short note", "source": "bookC"},
    {"passage_id": "b3:long:0", "text": "x" * 25000, "source": "bookC"},
]
