# Advanced Python Lecture 37: Code Review and Refactoring

## Topic Overview

Code review is the cheapest defect filter a team owns, and refactoring is how the code stays changeable after review approves it. Most reviews fail in the same way: they audit style (a formatter's job) and miss structure (the job that matters). A 87-line endpoint with ten parameters will collect "LGTM" comments while hiding a cache written before authorization — until it does not. This lecture makes review mechanical: a priority-ordered lens, smell *measurement* instead of squinting, refactoring moves locked by tests, and a comment format complete enough to change the code. The end state is the Athar pipeline that can change engines and rules because its structure says exactly where each change lands.

The theme: **review structure, measure smells, lock behavior before moving it.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Review in priority order: correctness, structure, tests, security, style.
2. Measure function smells (lines, params, branches) with `ast` and justify thresholds.
3. Refactor with extract-method and strategy-pattern moves that preserve behavior.
4. Write lock tests (golden-output) before structural changes and interpret their result.
5. Write review comments carrying severity, location, problem, and fix.
6. Compute a structural delta (function count, total lines, max branches) for a change.
7. Spot the five highest-value structural review questions for AI pipelines.

---

## Prerequisites

| Need | Where |
|---|---|
| Separation of concerns | `36-separation-of-concerns-lecture.md` |
| Protocols and DI | `36-separation-of-concerns-lecture.md` |
| Test types | `18-unit-testing-lecture.md`, `38-test-strategy-contract-regression-lecture.md` |
| Exceptions | `47-exceptions-advanced-lecture.md` |

---

## 1. The review lens

Review five things, in this order — stop at the first layer that fails, because lower layers don't matter yet:

1. **Correctness** — does the code do what the requirement says, at the edges? What happens on empty input, a missing field, a concurrent write?
2. **Structure** — one reason to change per unit? Does business logic hold only Protocols, never concrete clients? What is the blast radius of this change?
3. **Tests** — would they fail if the code were wrong? Do they cover the edges the reviewer just thought of? Tautologies (`assert result == result`) and assertions on mock internals are the two recurring failure modes.
4. **Security** — untrusted input reaching a query? A secret in a log line? An endpoint missing an authz check? In AI systems add: prompt-injection surface and unbounded-cost endpoints.
5. **Style** — naming and formatting. Automate it with a formatter and a linter; never spend human minutes on it.

The order is a budget: a PR with a correctness bug does not deserve a naming debate.

## 2. Measure smells; don't opine

"This function is too long" is taste. "87 lines, 10 parameters, 23 branches" is evidence a reviewer can argue with — and CI can enforce. The exercise measures with `ast`: line span, parameter count, and branch count (`if`/`for`/`while`/`except`). A production setup uses **ruff** (lint/format), **radon** (complexity), and **mypy** (types) in CI, with these thresholds as the gate.

| Metric | Threshold | Why |
|---|---|---|
| Function length | ≤ 30 lines | past this, one-reason-to-change is usually false |
| Parameters | ≤ 5 | past this, the function is a subsystem |
| Branch count | ≤ 10 | past this, test combinations explode |
| Complexity (radon) | ≤ B grade | A–B is reviewable, C+ needs splitting |
| File length | ≤ 500 lines | navigability, not dogma |

Thresholds are per-team agreements, not laws — but they must be *checked mechanically*, or they decay into a wiki page nobody reads.

## 3. Refactoring move 1: extract method

The god function in the exercise has three concerns fused: request guarding, page filtering, retrieval. Extract by **responsibility**, not by line count. Each extracted unit gets:

1. A name that states its job (`guard_query`, `filter_rows`).
2. Plain-data inputs and outputs (testable without fakes).
3. Its own tests, written immediately.

The mechanical rule: **behavior-preserving means byte-identical outputs on probe inputs.** Characterize the old function first, extract second. If the extraction changes an edge case silently, it is a rewrite wearing a refactoring's name.

## 4. Refactoring move 2: replace conditional with polymorphism

When you see `if engine == "keyword" ... elif engine == "vector" ... else ...`, the branches are classes waiting to exist. A strategy Protocol (`RetrievalStrategy.retrieve`) plus one class per branch removes the switch from business code entirely. The switching code moves to the composition root, which is the only place allowed to know implementations.

The payoff in an AI pipeline is the same as topic 36's engine-swap test: retrieval experiments become new classes, not edits in shared logic. The gate for accepting the move: every caller that used the conditional now calls `retrieve(strategy, query)` and no behavior differs.

## 5. Lock tests

A refactor claims "structure changed, behavior did not." Only a test can referee that claim. **Lock tests** (also called characterization tests or golden tests) capture current behavior *before* the move:

```python
LOCK_INPUTS = ["  Hello   World  ", "مُحَمَّد", "", "A\tB\n C"]


def lock_behavior() -> bool:
    return all(legacy_normalize(t) == refactored_normalize(t) for t in LOCK_INPUTS)
```

Rules for good locks:

- **Probe edges, not averages**: empty, whitespace-only, unicode, tab/newline mixes, max-length.
- **Byte-identical** comparisons — no "close enough".
- **Quirks are included**: if the legacy function lowercased *and* collapsed whitespace, the lock preserves both, even if you'd design it differently. Behavior changes are product decisions, made separately from structural moves.
- If a lock fails after a "pure refactor", the refactor is not pure — find the drift before merging.

## 6. Writing review comments

A review comment is an engineering artifact with four parts: **severity, location, problem, fix.**

| Severity | Meaning | Merge policy |
|---|---|---|
| BLOCK | correctness bug, security hole, data loss | must fix |
| SHOULD | structural debt that raises future cost | fix now or file an issue |
| NIT | style, naming | optional; formatter owns most |

Format: `[SEVERITY] function - problem - suggested fix`. A comment that says "this is confusing" with no suggestion is incomplete unless it is a genuine question of intent ("was the cache-before-authz ordering deliberate?").

Two habits make reviews worth reading:

- **Comment on structure first** (the lenses' order applies to comments too).
- **Ask for a test that would have caught the issue** — the fix is then locked forever.

## 7. Structural deltas

Track the structural cost of every PR: function count, total lines, max branches. If those numbers grow monotonically, the codebase is rotting at an average rate that no amount of style linting stops. The refactoring example reports `1 -> 2 functions, 36 -> 15 lines, max branches 3` — the function count rose (extraction), the max-branch count collapsed (the switch left). Numbers make the tradeoff visible.

In CI this is a diff-based budget: "no PR may raise max branches in a touched file" is enforceable.

## 8. The five structural questions for AI pipelines

When reviewing a change to a RAG/agent system, ask:

1. **Where does untrusted text enter?** (user query, retrieved document) — and is it treated as data, not instruction?
2. **Which layer owns this decision?** If a retrieval experiment edits validation code, the review stops the merge.
3. **What does this cost at 10x traffic?** (embedder calls, LLM calls, cache writes) — cost is a correctness concern in AI products.
4. **What happens when the dependency fails?** Every outbound call needs a timeout and a defined failure path.
5. **What is the rollback?** (feature flag, config value, previous index) — a model/prompt change with no rollback is an experiment run in production.

## 9. Best-practice checklist

| Practice | Payoff |
|---|---|
| Review in lens order | effort goes to what can kill the system |
| Smell thresholds in CI | structure enforced without taste debates |
| Extract by responsibility | each unit gains one reason to change |
| Strategy over conditional branches | new backends = new classes, not new branches |
| Lock tests before structural moves | refactors are provably behavior-preserving |
| Four-part comments | review threads end in changed code |
| Structural deltas per PR | decay is visible before it is fatal |
| Ask for the missing test | the fixed bug stays fixed |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Review debates naming before bugs | enforce lens order |
| "Too complex" without numbers | measure lines/params/branches first |
| Refactor + behavior change in one PR | split: lock test, refactor, then change |
| Strategy pattern with one implementation | premature — wait for the second |
| Comments like "clean this up" | always attach severity + suggested fix |
| Asserting on mock internals | assert on observable behavior of the unit |
| Skipping security review on prompts | prompt injection is an input-validation bug |
| Big-bang rewrite to "fix structure" | incremental extraction with locks |

---

## Mastery Check

You can claim this topic when you can:

1. Read a new PR and identify a structure defect before any style issue.
2. Run a smell measurement on a god function and get numbers over threshold.
3. Split that function into units with tests and show a passing lock test across the move.
4. Replace an `if/elif` backend switch with a strategy and no behavior change.
5. Write a four-part BLOCK comment that a teammate can action without a discussion thread.

---

## Next Steps

- Lock the layers with the full test taxonomy in `38-test-strategy-contract-regression-lecture.md`.
- Apply the contract discipline at system scale in `10-system-design/01-component-contracts/`.
- Track review findings in the module `ai-review.md` (see `templates/`).
