"""
Code Review and Refactoring - Advanced Python Exercises
========================================================
Topics: review as a quality gate, finding smells by measurement, refactoring
safely (extract method, replace conditionals, remove duplication), red-green
locks for refactors, writing review comments that change the code.

Why this matters for AI engineering:
    Most defects in a RAG system reach main through a review that checked
    style and missed structure. An endpoint that parses, validates,
    embeds, and answers in one 80-line function will pass a "looks fine"
    review and fail the first time a rule changes. This file gives you a
    measurable smell checklist and a refactoring workflow where every
    structural move is locked by a test first - so the Athar pipeline can
    change engines and rules without fear.

Environment note:
    Pure standard library. Every check runs offline.

Run:      python 37-code-review-and-refactoring.py
Verify:   python 37-code-review-and-refactoring.py --verify
Reference: Martin Fowler, "Refactoring" (2nd ed.), chapters 1-3.
"""

from __future__ import annotations

import ast
import inspect
import sys
import textwrap

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. The review lens: correctness, structure, tests, security
# ============================================================
# Style is the LAST lens and the cheapest to automate. The review that
# matters asks, in order:
#   1. Correctness - does it do what the requirement says, at the edges?
#   2. Structure   - one reason to change per unit? contract boundaries held?
#   3. Tests       - do they fail when the code is wrong? cover the edges?
#   4. Security    - untrusted input? secrets? injection? authz gaps?
#   5. Style       - naming, formatting (hand this to a formatter).

REVIEW_LENSES = [
    ("correctness", "behavior matches spec, edge cases explicit"),
    ("structure", "single responsibility, contracts held, blast radius small"),
    ("tests", "falsifiable tests, edge coverage, no tautologies"),
    ("security", "input validation, secrets, authz, injection"),
    ("style", "naming, formatting - automate it, don't review it"),
]
print("1. review lenses in priority order")
for name, why in REVIEW_LENSES:
    print(f"   {name:12} {why}")
print()


# ============================================================
# 2. Smell detection by measurement - count, don't squint
# ============================================================
# "This function is too big" is an opinion. "This function is 87 lines
# with cyclomatic complexity 23 and 6 parameters" is evidence. We use
# ast to measure; a real workflow uses ruff + radon + mypy in CI.


def function_stats(src: str) -> dict[str, dict[str, int]]:
    """Measure size and branching of every function in a source string."""
    tree = ast.parse(textwrap.dedent(src))
    stats: dict[str, dict[str, int]] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            n_params = len(args.args) + len(args.posonlyargs) + len(args.kwonlyargs)
            branches = sum(
                isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler))
                for n in ast.walk(node)
            )
            end = node.end_lineno or node.lineno
            stats[node.name] = {
                "lines": end - node.lineno + 1,
                "params": n_params,
                "branches": branches,
            }
    return stats


SMELL_THRESHOLDS = {"lines": 30, "params": 5, "branches": 10}


def find_smells(src: str) -> list[str]:
    """Return human-readable smell reports for functions over threshold."""
    smells = []
    for name, st in function_stats(src).items():
        for metric, limit in SMELL_THRESHOLDS.items():
            value = st[metric]
            if isinstance(value, int) and value > limit:
                smells.append(f"{name}: {metric}={value} (limit {limit})")
    return smells


# A deliberately smelly function - the shape of a god-endpoint
GOD_FUNCTION_SRC = """
def handle_search_request(raw_query, user, book_filter, page_from, page_to,
                         engine, db, cache, embedder, top_k):
    if not user:
        return None
    if len(raw_query) < 2:
        return None
    if book_filter is None:
        book_filter = ""
    q = raw_query.lower().strip()
    for ch in q:
        if ord(ch) > 0x06FF:
            pass
    if db is None:
        raise RuntimeError("no db")
    rows = []
    if book_filter:
        rows = db.query("book=?", book_filter)
    else:
        rows = db.query_all()
    hits = []
    for row in rows:
        if page_from and row.page < page_from:
            continue
        if page_to and row.page > page_to:
            continue
        hits.append(row)
    try:
        vec = embedder.embed(q)
    except Exception:
        vec = None
    if vec is not None and engine is not None:
        more = engine.search(vec, top_k)
        hits = hits + more
    if cache is not None:
        cache.put(q, hits)
    return hits
"""

print("2. smell detection by measurement")
for smell in find_smells(GOD_FUNCTION_SRC):
    print(f"   [smell] {smell}")
print()


# ============================================================
# 3. Refactoring move 1 - extract method
# ============================================================
# Split by responsibility, not by line count. The god function contains
# at least three concerns: input guarding, filtering, retrieval. Each
# extraction must preserve behavior - that is what the lock test is for.


def filter_rows(rows, page_from=None, page_to=None):
    """Extracted concern: page-range filtering. Pure, testable."""
    out = []
    for row in rows:
        if page_from is not None and row.page < page_from:
            continue
        if page_to is not None and row.page > page_to:
            continue
        out.append(row)
    return out


def guard_query(raw_query, user):
    """Extracted concern: request guards. Returns normalized query or None."""
    if not user or len(raw_query) < 2:
        return None
    return raw_query.lower().strip()


print("3. extract method: guard_query + filter_rows are now unit-testable")
print(f"   guard_query('', 'u') -> {guard_query('', 'u')!r}")
print(
    f"   filter_rows([R(1), R(5)], page_from=2) -> {filter_rows([type('R', (), {'page': 1})(), type('R', (), {'page': 5})()], page_from=2)}"
)
print()


# ============================================================
# 4. Refactoring move 2 - replace conditional with polymorphism
# ============================================================
# Three or more branches selecting behavior (if engine == "x" ... elif
# engine == "y") is a class waiting to exist. Each branch becomes a
# strategy with one method; the switch disappears from business code.


class RetrievalStrategy:
    """Contract for pluggable retrieval backends."""

    def retrieve(self, query: str, top_k: int) -> list[str]:
        raise NotImplementedError


class KeywordRetrieval(RetrievalStrategy):
    def retrieve(self, query: str, top_k: int) -> list[str]:
        return [f"kw:{query}"][:top_k]


class VectorRetrieval(RetrievalStrategy):
    def retrieve(self, query: str, top_k: int) -> list[str]:
        return [f"vec:{query}"][:top_k]


def retrieve(strategy: RetrievalStrategy, query: str, top_k: int = 3) -> list[str]:
    """No branch on backend type - polymorphism owns the switch."""
    return strategy.retrieve(query, top_k)


print("4. strategy replaces conditional branching")
print(f"   retrieve(KeywordRetrieval(), 'q')  -> {retrieve(KeywordRetrieval(), 'q')}")
print(f"   retrieve(VectorRetrieval(), 'q')   -> {retrieve(VectorRetrieval(), 'q')}")
print()


# ============================================================
# 5. Lock tests - the refactor's safety net
# ============================================================
# A refactor changes structure without changing behavior. The proof is
# a characterization test captured BEFORE the change and passing AFTER.
# Golden-output lock: same input, byte-identical output across the move.


def legacy_normalize(text: str) -> str:
    """The behavior we will preserve verbatim (quirks included)."""
    return " ".join(text.lower().split())


def refactored_normalize(text: str) -> str:
    """New structure, identical behavior - the lock test is the referee."""
    tokens = text.lower().split()
    return " ".join(tokens)


LOCK_INPUTS = ["  Hello   World  ", "مُحَمَّد", "", "A\tB\n C"]


def lock_behavior() -> bool:
    """Golden test: both implementations agree on every probe input."""
    return all(legacy_normalize(t) == refactored_normalize(t) for t in LOCK_INPUTS)


print("5. lock tests: behavior preserved across the refactor")
print(f"   golden agreement: {lock_behavior()}")
print()


# ============================================================
# 6. Review comments that change code
# ============================================================
# A review comment is an engineering artifact. Format:
#   [severity] location - what is wrong - what to do instead.
# Severities: BLOCK (bug/security), SHOULD (structure), NIT (style).
# A comment without a suggested fix is incomplete unless it is a
# genuine question about intent.

REVIEW_EXAMPLES = [
    (
        "BLOCK",
        "handle_search_request",
        "cache.put runs before authz is checked; unauthenticated hits are cached",
        "move cache.write behind the permission check",
    ),
    (
        "SHOULD",
        "handle_search_request",
        "10 parameters / 87 lines / 23 branches; one reason to change is false",
        "extract guard_query, filter_rows, retrieve; inject engine+db via constructor",
    ),
    ("NIT", "filter_rows", "lambda key shadowing in comprehension", "rename to row_key"),
]
print("6. review comments: severity, location, problem, fix")
for sev, loc, problem, fix in REVIEW_EXAMPLES:
    print(f"   [{sev}] {loc}: {problem}")
    print(f"        -> {fix}")
print()


# ============================================================
# 7. Review metrics that predict maintenance cost
# ============================================================
# Track these per PR. They are the same numbers the smell checker uses,
# aggregated: if the numbers grow monotonically the codebase is rotting.


def pr_delta(old_src: str, new_src: str) -> dict[str, object]:
    """Summarize the structural cost of a change."""
    old_fns, new_fns = function_stats(old_src), function_stats(new_src)
    old_total = sum(f["lines"] for f in old_fns.values() if isinstance(f["lines"], int))
    new_total = sum(f["lines"] for f in new_fns.values() if isinstance(f["lines"], int))
    return {
        "functions": f"{len(old_fns)} -> {len(new_fns)}",
        "total_lines": f"{old_total} -> {new_total}",
        "max_branches": max(
            (f["branches"] for f in new_fns.values() if isinstance(f["branches"], int)), default=0
        ),
    }


print("7. structural delta of this refactor")
print(
    f"   {pr_delta(GOD_FUNCTION_SRC, inspect.getsource(filter_rows) + inspect.getsource(guard_query))}"
)
print()


# ============================================================
# 8. Self-verification
# ============================================================


class Row:
    def __init__(self, page: int) -> None:
        self.page = page


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []
    smells = find_smells(GOD_FUNCTION_SRC)
    checks.append(("god function smells detected", len(smells) >= 3))
    checks.append(("clean code smells-free", find_smells("def f(a):\n    return a + 1") == []))
    checks.append(
        (
            "filter is pure and correct",
            [r.page for r in filter_rows([Row(1), Row(5), Row(9)], 2, 7)] == [5],
        )
    )
    checks.append(("guards reject missing user", guard_query("query", None) is None))
    checks.append(("strategy polymorphism works", retrieve(VectorRetrieval(), "x") == ["vec:x"]))
    checks.append(("lock test preserves behavior", lock_behavior()))
    checks.append(("review format is complete", all(len(x) == 4 for x in REVIEW_EXAMPLES)))
    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 37-code-review-and-refactoring.py --verify):")
    _verify()
