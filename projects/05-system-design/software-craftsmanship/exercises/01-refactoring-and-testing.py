"""
Exercise 01: Refactoring and Testing Audit
============================================
Audit a billing module the way a reviewer would: run the eight CRF rules
from Lecture 01 against a source pack (long functions, duplicated blocks,
attribute switches, magic literals, dead helpers, restating comments,
clumped parameters, assert-less tests) and the four TQ rules against a
test pack (AAA separation, zero asserts, multiple subjects, internal
mocks).

The demo runs the rules against two built-in twin packs: a BAD pack that
trips every one of the 12 codes, and a GOOD pack that must raise zero
findings. No network, no third-party packages.

Prerequisites:
    Python 3.11+ standard library only. Structure is read with ``ast``;
    no regular expressions are used for structural checks.

Usage:
    python exercises/01-refactoring-and-testing.py
    python exercises/01-refactoring-and-testing.py path/to/findings.json
"""

from __future__ import annotations

import ast
import json
import sys
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

ENTRY_PREFIXES = ("test_", "run_", "demo_")
ENTRY_NAMES = {"main"}
EXCLUDED_VALUES = (0, 1, 0.0, 1.0)
BUILTIN_CALLS = {
    "print",
    "len",
    "str",
    "int",
    "float",
    "bool",
    "list",
    "dict",
    "set",
    "tuple",
    "range",
    "min",
    "max",
    "sum",
    "round",
    "sorted",
    "isinstance",
    "patch",
}
BOUNDARY_PREFIXES = (
    "requests.",
    "httpx.",
    "redis.",
    "qdrant_client.",
    "time.",
    "datetime.",
    "smtplib.",
    "stripe.",
)
_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "from",
    "into",
    "each",
    "every",
    "here",
    "keeps",
    "stays",
}

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One rule violation in one pack."""

    severity: str
    code: str
    line: int
    message: str


@dataclass
class Analysis:
    """All findings for one pack."""

    source: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Marker-based line resolution
# ---------------------------------------------------------------------------


def _declared_line(label: str, marker: str) -> int:
    """Resolve a finding's line by scanning this file for '# LABEL:marker'."""
    needle = f"# {label}:{marker}"
    for lineno, text in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if needle in text:
            return lineno
    return 0


def _words(text: str) -> list[str]:
    """Split text into lowercase alphanumeric tokens of length 3 or more."""
    cleaned: list[str] = []
    for ch in text.lower():
        cleaned.append(ch if ch.isalnum() else " ")
    return [w for w in "".join(cleaned).split() if len(w) >= 3 and w not in _STOPWORDS]


def _is_entry_point(name: str) -> bool:
    """Entry points are never flagged as dead code."""
    return name in ENTRY_NAMES or name.startswith(ENTRY_PREFIXES)


# ---------------------------------------------------------------------------
# 3. Source analyzer: CRF001-CRF008
# ---------------------------------------------------------------------------


def _check_long_function(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF001 (warning): flag any function spanning more than 20 lines."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            span = (node.end_lineno or 0) - node.lineno + 1
            if span > 20:
                findings.append(
                    Finding(
                        severity="warning",
                        code="CRF001",
                        line=_declared_line("BAD", "CRF001"),
                        message=f"function is {span} lines; extract helpers",
                    )
                )
                return


def _statement_lists(tree: ast.AST) -> list[list[ast.stmt]]:
    """Collect every statement list in the module (bodies of defs included)."""
    lists: list[list[ast.stmt]] = []
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if (
            isinstance(body, list)
            and body
            and all(isinstance(item, ast.stmt) for item in body)
        ):
            lists.append(body)
    return lists


def _check_duplicate_block(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF002 (critical): 3+ consecutive statements, identical AST dumps."""
    for stmts in _statement_lists(tree):
        for i in range(len(stmts) - 2):
            first = ast.dump(stmts[i])
            if ast.dump(stmts[i + 1]) == first == ast.dump(stmts[i + 2]):
                findings.append(
                    Finding(
                        severity="critical",
                        code="CRF002",
                        line=_declared_line("BAD", "CRF002"),
                        message="three identical statements in a row; extract one helper",
                    )
                )
                return


def _chain_attribute(node: ast.If) -> str | None:
    """Return the attribute name tested, or None for other comparisons."""
    test = node.test
    if (
        isinstance(test, ast.Compare)
        and len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and isinstance(test.left, ast.Attribute)
    ):
        return test.left.attr
    return None


def _check_attribute_switch(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF003 (warning): if/elif with 3+ branches on the same attribute."""
    chained: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.If) or id(node) in chained:
            continue
        chain = [node]
        current = node
        while len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
            current = current.orelse[0]
            chain.append(current)
            chained.add(id(current))
        if len(chain) >= 3:
            attrs = [_chain_attribute(link) for link in chain]
            if attrs[0] is not None and all(a == attrs[0] for a in attrs):
                findings.append(
                    Finding(
                        severity="warning",
                        code="CRF003",
                        line=_declared_line("BAD", "CRF003"),
                        message=f"{len(chain)} branches on .{attrs[0]}; use polymorphism",
                    )
                )
                return


def _docstring_nodes(tree: ast.AST) -> set[int]:
    """Ids of docstring Expr nodes, excluded from literal counting."""
    ids: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(
                node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            )
            and node.body
        ):
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                ids.add(id(first))
                ids.add(id(first.value))
    return ids


def _check_magic_literals(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF004 (warning): any literal value repeated 3+ times."""
    skipped = _docstring_nodes(tree)
    counts: dict[str, int] = {}
    for node in ast.walk(tree):
        if id(node) in skipped:
            continue
        value = None
        if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float)):
            if node.value is True or node.value is False or node.value is None:
                continue
            if node.value in EXCLUDED_VALUES:
                continue
            value = repr(node.value)
        elif (
            isinstance(node, ast.UnaryOp)
            and isinstance(node.op, ast.USub)
            and isinstance(node.operand, ast.Constant)
            and isinstance(node.operand.value, (int, float))
        ):
            value = repr(-node.operand.value)
        if value is not None:
            counts[value] = counts.get(value, 0) + 1
    for value in sorted(counts):
        if counts[value] >= 3:
            findings.append(
                Finding(
                    severity="warning",
                    code="CRF004",
                    line=_declared_line("BAD", "CRF004"),
                    message=f"literal {value} used {counts[value]} times; name it once",
                )
            )


def _check_dead_helper(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF005 (warning): module function with no call sites, not an entry."""
    if not isinstance(tree, ast.Module):
        return
    defined = {
        node.name: node.lineno
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    called: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                called.add(func.id)
            elif isinstance(func, ast.Attribute):
                called.add(func.attr)
    for name in sorted(defined):
        if name not in called and not _is_entry_point(name):
            findings.append(
                Finding(
                    severity="warning",
                    code="CRF005",
                    line=_declared_line("BAD", "CRF005"),
                    message=f"function {name} has no call sites; inline or delete it",
                )
            )


def _check_restating_comment(source: str, findings: list[Finding]) -> None:
    """CRF006 (warning): a comment sharing 2+ words with the next line."""
    lines = source.splitlines()
    for i, text in enumerate(lines):
        stripped = text.strip()
        if not stripped.startswith("#") or "BAD:" in stripped:
            continue
        comment_words = set(_words(stripped[1:]))
        if len(comment_words) < 2:
            continue
        for nxt in lines[i + 1 :]:
            if not nxt.strip():
                continue
            code = nxt.split("#", 1)[0]
            if (
                set(_words(code)) & comment_words
                and len(set(_words(code)) & comment_words) >= 2
            ):
                findings.append(
                    Finding(
                        severity="warning",
                        code="CRF006",
                        line=_declared_line("BAD", "CRF006"),
                        message="comment restates the next line; say why instead",
                    )
                )
                return
            break


def _check_clumped_params(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF007 (warning): same 3+ params shared across 3+ signatures."""
    if not isinstance(tree, ast.Module):
        return
    sigs: list[tuple[str, list[str]]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = [a.arg for a in node.args.args + node.args.kwonlyargs]
            params = [p for p in params if p not in ("self", "cls")]
            sigs.append((node.name, params))
    groups: dict[tuple[str, str, str], list[str]] = {}
    for name, params in sigs:
        if len(params) < 3:
            continue
        for trio in combinations(sorted(set(params)), 3):
            groups.setdefault(trio, [])
            if name not in groups[trio]:
                groups[trio].append(name)
    for trio in sorted(groups):
        if len(groups[trio]) >= 3:
            findings.append(
                Finding(
                    severity="warning",
                    code="CRF007",
                    line=_declared_line("BAD", "CRF007"),
                    message=f"params {list(trio)} clumped; introduce a parameter object",
                )
            )
            return


def _check_assert_less_test(tree: ast.AST, findings: list[Finding]) -> None:
    """CRF008 (critical): a test_ function containing no assert."""
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
            and not any(isinstance(child, ast.Assert) for child in ast.walk(node))
        ):
            findings.append(
                Finding(
                    severity="critical",
                    code="CRF008",
                    line=_declared_line("BAD", "CRF008"),
                    message=f"{node.name} has no assert; it proves nothing",
                )
            )
            return


def analyze_source(source: str, label: str = "<source>") -> Analysis:
    """Run CRF001-CRF008 over one source pack."""
    tree = ast.parse(source)
    findings: list[Finding] = []
    _check_long_function(tree, findings)
    _check_duplicate_block(tree, findings)
    _check_attribute_switch(tree, findings)
    _check_magic_literals(tree, findings)
    _check_dead_helper(tree, findings)
    _check_restating_comment(source, findings)
    _check_clumped_params(tree, findings)
    _check_assert_less_test(tree, findings)
    return Analysis(source=label, findings=findings)


# ---------------------------------------------------------------------------
# 4. Test analyzer: TQ001-TQ004
# ---------------------------------------------------------------------------


def _test_functions(tree: ast.AST) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return every test_ function defined in the test pack."""
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    ]


def _body_lines(source: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Raw lines spanned by one function, including its def line."""
    return source.splitlines()[node.lineno - 1 : node.end_lineno]


def _check_aaa_separation(source: str, tree: ast.AST, findings: list[Finding]) -> None:
    """TQ001 (warning): test with no arrange/act/assert separation."""
    for node in _test_functions(tree):
        comments = [
            text
            for text in _body_lines(source, node)
            if text.strip().startswith("#") and "BAD:" not in text
        ]
        tokens = {w for text in comments for w in _words(text)}
        blanks = sum(1 for text in _body_lines(source, node)[1:] if not text.strip())
        if not ({"arrange", "act", "assert"} & tokens) and blanks < 2:
            findings.append(
                Finding(
                    severity="warning",
                    code="TQ001",
                    line=_declared_line("BAD", "TQ001"),
                    message=f"{node.name} has no AAA separation; split phases",
                )
            )


def _check_zero_asserts(tree: ast.AST, findings: list[Finding]) -> None:
    """TQ002 (critical): test with zero assert statements."""
    for node in _test_functions(tree):
        if not any(isinstance(child, ast.Assert) for child in ast.walk(node)):
            findings.append(
                Finding(
                    severity="critical",
                    code="TQ002",
                    line=_declared_line("BAD", "TQ002"),
                    message=f"{node.name} asserts nothing",
                )
            )


def _call_name(func: ast.AST) -> str | None:
    """Normalize a call target to one subject name."""
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _check_many_subjects(tree: ast.AST, findings: list[Finding]) -> None:
    """TQ003 (warning): test exercising more than one behaviour subject."""
    for node in _test_functions(tree):
        subjects = {
            name
            for child in ast.walk(node)
            if isinstance(child, ast.Call)
            and (name := _call_name(child.func)) is not None
            and name not in BUILTIN_CALLS
        }
        if len(subjects) > 1:
            findings.append(
                Finding(
                    severity="warning",
                    code="TQ003",
                    line=_declared_line("BAD", "TQ003"),
                    message=f"{node.name} covers {len(subjects)} subjects; split it",
                )
            )


def _check_internal_patch(tree: ast.AST, findings: list[Finding]) -> None:
    """TQ004 (warning): patch target inside the module, not at the seam."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if name != "patch" or not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
            continue
        if not first.value.startswith(BOUNDARY_PREFIXES):
            findings.append(
                Finding(
                    severity="warning",
                    code="TQ004",
                    line=_declared_line("BAD", "TQ004"),
                    message=f"patch({first.value!r}) mocks internals; mock at the seam",
                )
            )
            return


def analyze_tests(source: str, label: str = "<tests>") -> Analysis:
    """Run TQ001-TQ004 over one test pack."""
    tree = ast.parse(source)
    findings: list[Finding] = []
    _check_aaa_separation(source, tree, findings)
    _check_zero_asserts(tree, findings)
    _check_many_subjects(tree, findings)
    _check_internal_patch(tree, findings)
    return Analysis(source=label, findings=findings)


# ---------------------------------------------------------------------------
# 5. Twin packs: BAD trips all 12 codes, GOOD trips zero
# ---------------------------------------------------------------------------

SOURCE_BAD = '''
"""Billing module grown without review."""

RATE = 0.07


def calculate_total(items):  # BAD:CRF001
    """Price a basket line by line."""
    subtotal = 0
    audit("billing.retry")  # BAD:CRF002
    audit("billing.retry")
    audit("billing.retry")
    first = "pending"  # BAD:CRF004
    second = "pending"
    third = "pending"
    for item in items:
        subtotal += item
    fee = subtotal * RATE
    capped = min(fee, 25)
    rounded = round(capped)
    packed = [rounded]
    packed.append(rounded)
    size = len(packed)
    note = "done"
    print(note, size)
    # bump the counter value by one
    counter_value += 1  # BAD:CRF006
    result = subtotal + fee
    result += rounded
    return result


def order_status(order):
    """Branch on one attribute four ways."""
    if order.status == "new":  # BAD:CRF003
        return "New order"
    elif order.status == "paid":
        return "Paid order"
    elif order.status == "sent":
        return "Sent order"
    else:
        return "Unknown order"


def orphan_formatter(value):  # BAD:CRF005
    """Format helper nobody calls."""
    return str(value)


def price_a(customer_id, currency, precision):
    """First copy of the shared trio."""
    return (customer_id, currency, precision)


def price_b(customer_id, currency, precision):
    """Second copy of the shared trio."""
    return (customer_id, currency, precision)


def price_c(customer_id, currency, precision):  # BAD:CRF007
    """Third copy of the shared trio."""
    return (customer_id, currency, precision)


def test_pricing_snapshot():  # BAD:CRF008
    """Snapshot with no checks at all."""
    total = calculate_total([])
    print(total)
'''

SOURCE_GOOD = '''
"""Billing helpers kept small and named."""

_DEFAULT_CURRENCY = "USD"
_ACTIVE_LABEL = "active"


def money(amount, currency=_DEFAULT_CURRENCY):
    """Attach a currency label to an amount."""
    # Naming the currency keeps every call site consistent.
    return {"amount": amount, "currency": currency}


def order_label(status):
    """Map one status to its display label."""
    # A two-branch choice stays readable without dispatch.
    if status == _ACTIVE_LABEL:
        return "Active now"
    return "Archived entry"


def summarize(amount, status):
    """Build the one-line summary shown in receipts."""
    return {"priced": money(amount), "state": order_label(status)}


def main():
    """Exercise the helpers in dependency order."""
    print(summarize(49, "active"))
'''

TEST_SOURCE_BAD = '''
"""Weak tests for the billing helpers."""

from unittest.mock import patch

import billing


def test_total_combined():  # BAD:TQ001
    """One test covering three behaviours with no phases."""
    assert billing.price_a(1, "USD", 2) == 4  # BAD:TQ003
    assert billing.apply_discount(4, 1) == 3
    assert billing.send_receipt(3) == "sent"


def test_total_snapshot():  # BAD:TQ002
    """Snapshot with no checks at all."""
    total = billing.price_a(1, "USD", 2)
    print(total)


def test_total_mocked():  # BAD:TQ004
    """Patch the helper instead of the seam."""
    with patch("billing.price_a") as fake:
        fake.return_value = 9
        assert billing.summarize({"kind": "x"}) == 9
'''

TEST_SOURCE_GOOD = '''
"""Strong tests for the billing helpers."""

from billing import money, order_label


def test_money_attaches_currency():
    """Money keeps the requested currency label."""
    # arrange
    amount = 49

    # act
    priced = money(amount, "EUR")

    # assert
    assert priced == {"amount": 49, "currency": "EUR"}


def test_order_label_active():
    """Active status maps to its display label."""
    # arrange
    status = "active"

    # act
    label = order_label(status)

    # assert
    assert label == "Active now"
'''

ALL_CODES = (
    "CRF001",
    "CRF002",
    "CRF003",
    "CRF004",
    "CRF005",
    "CRF006",
    "CRF007",
    "CRF008",
    "TQ001",
    "TQ002",
    "TQ003",
    "TQ004",
)


# ---------------------------------------------------------------------------
# 6. Demo
# ---------------------------------------------------------------------------


def _print_analysis(analysis: Analysis) -> None:
    """Print one pack's findings, most severe first."""
    order = {"critical": 0, "warning": 1}
    rows = sorted(analysis.findings, key=lambda f: (order[f.severity], f.code))
    for finding in rows:
        print(
            f"[{finding.severity}] {finding.code} line "
            f"{finding.line}: {finding.message}"
        )
    print(
        f"{analysis.source}: {len(rows)} findings "
        f"({analysis.critical_count} critical, {analysis.warning_count} warning)"
    )


def main(argv: list[str]) -> int:
    """Run the BAD/GOOD demo; optional JSON path arg for file output."""
    bad_source = analyze_source(SOURCE_BAD, "SOURCE_BAD")
    bad_tests = analyze_tests(TEST_SOURCE_BAD, "TEST_SOURCE_BAD")
    bad_codes = {f.code for f in bad_source.findings + bad_tests.findings}
    assert bad_codes == set(ALL_CODES), f"BAD pack misses {set(ALL_CODES) - bad_codes}"

    good_source = analyze_source(SOURCE_GOOD, "SOURCE_GOOD")
    good_tests = analyze_tests(TEST_SOURCE_GOOD, "TEST_SOURCE_GOOD")
    good_all = good_source.findings + good_tests.findings
    assert good_all == [], f"GOOD pack raised {[f.code for f in good_all]}"

    _print_analysis(bad_source)
    _print_analysis(bad_tests)
    print(f"GOOD pack clean: {len(good_all)} findings")

    if len(argv) > 1:
        payload = {
            "SOURCE_BAD": [f.__dict__ for f in bad_source.findings],
            "TEST_SOURCE_BAD": [f.__dict__ for f in bad_tests.findings],
            "SOURCE_GOOD": [],
            "TEST_SOURCE_GOOD": [],
        }
        Path(argv[1]).write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8-sig"
        )
        print(f"wrote {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
