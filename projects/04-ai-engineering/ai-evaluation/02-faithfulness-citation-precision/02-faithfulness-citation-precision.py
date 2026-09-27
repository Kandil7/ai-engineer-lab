"""
AI Evaluation — 02: Faithfulness and Citation Precision
========================================================
Topics: claim-level faithfulness, citation validity vs support, and
        citation precision.

Why this matters:
    Retrieval quality is not answer quality. This exercise checks whether
    the answer is supported by the context and whether citations actually
    back their claims.

Run:      python 02-faithfulness-citation-precision.py
Verify:   python 02-faithfulness-citation-precision.py --verify
"""

from __future__ import annotations

import sys


def citation_validity(cited: list[str], context_ids: set[str]) -> bool:
    """Mechanical: every cited id exists in the context."""
    return all(c in context_ids for c in cited)


def citation_precision(supported: list[bool]) -> float:
    """Fraction of citations that support their claim."""
    return sum(supported) / len(supported)


def is_supported(claim: str, context: list[str]) -> bool:
    """Claim-level support: does any context passage back the claim?"""
    terms = set(claim.split())
    return any(all(t in passage for t in terms) for passage in context)


def main() -> None:
    context = [
        "القصر جائز للمسافر في الصلاة",
        "الجمع بين الصلاتين جائز في السفر",
    ]
    context_ids = {"b3:p12:0", "b3:p12:1"}

    # A faithful answer: every claim is supported by the context.
    claims = ["القصر جائز للمسافر", "الجمع جائز في السفر"]
    assert all(is_supported(c, context) for c in claims), "all claims supported"

    # An unsupported claim is a hallucination even if true in the world.
    unsupported = "صيام رمضان واجب"
    assert not is_supported(unsupported, context), "context does not back it"

    # Citation validity is mechanical; support is not.
    cited = ["b3:p12:0", "b3:p12:1"]
    assert citation_validity(cited, context_ids)
    assert not citation_validity(["b9:p99"], context_ids), "fabricated id invalid"

    # Citation precision: 3 of 4 citations support their claims.
    assert abs(citation_precision([True, True, True, False]) - 0.75) < 1e-9

    print("faithful answer: every claim supported by the context")
    print("unsupported claim flagged even though true in the world")
    print("citation validity (id exists) is not citation support")
    print("citation precision = 0.75 for 3-of-4 supporting citations")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
