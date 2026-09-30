# Challenge 38: Test Strategy — The Pipeline Verdict

An Athar ingest pipeline must uphold three promises: text/book/page never get
lost, reruns never duplicate, and known failure cases never return. Each
promise is a different test type. Build all three.

## 🥉 Bronze — Provenance Violations (~15 min)

**Task:** Implement `provenance_violations(before, after)`, the data-test
invariant checker: given source records (list of dicts with `id`, `book`,
`page`, `text`) and the store (dict keyed by `id`), return violation strings
for: lost records (in source, missing from store), phantom records (in store,
never in source), empty stored text, and `source_ref` not carrying `book/page`.

**Signature:**
```python
def provenance_violations(before: list[dict], after: dict[str, dict]) -> list[str]
```

| Input | Expected |
|---|---|
| 1 source record, stored intact | `[]` |
| source record missing from store | `["lost records: ['x']"]` (substring check) |
| store has a record not in source | `["phantom records: ['y']"]` (substring check) |
| stored text is blank | a violation naming the id |

**Constraints:** `n <= 10^4`. Any correct approach passes.

---

## 🥈 Silver — Idempotent Ingest (~35 min)

**Task:** Implement `idempotent_ingest(lines, store)`, parsing JSONL records
(`id`, `book`, `page`, `text`) into the store dict keyed by `id`, inserting
only when absent. Returns `{"imported": N, "skipped_duplicates": M}`.

**Signature:**
```python
def idempotent_ingest(lines: list[str], store: dict) -> dict[str, int]
```

| Input | Expected |
|---|---|
| 3 unique lines | `{"imported": 3, "skipped_duplicates": 0}` |
| same 3 lines again | `{"imported": 0, "skipped_duplicates": 3}` |
| `[]` | `{"imported": 0, "skipped_duplicates": 0}` |

**Constraints:** `n <= 5000`. The tests wrap every record `id` in a
comparison-counting string and assert total equality checks stay under
`3 * n` across BOTH runs — a list-scan dedupe (`any(r["id"] == new for r in
rows)`) is O(n²) comparisons and must fail the budget; dict-keyed insert stays
near O(n). **Adversarial case:** 2000 records sharing one `book` with unique
pages — the list-scan explodes, the dict does not.

---

## 🥇 Gold — The Regression Gate (~75 min)

**Task:** Implement `regression_suite_runner(cases, parser)`, running
known-failure cases `(case_id, input_line, expected)` where `expected` is
`"accept"` or `"reject"`; `parser(line)` returns a dict or raises `ValueError`.
Return the sorted list of **regressed** case ids (outcome mismatched), each id
at most once.

**Signature:**
```python
def regression_suite_runner(cases: list[tuple[str, str, str]], parser) -> list[str]
```

| Input | Expected |
|---|---|
| 20 cases, correct parser | `[]` |
| broken parser (accepts everything) | the 10 reject-case ids |
| duplicate regressed case id | reported once |
| `[]` | `[]` |

**Constraints:** 20 seeded cases (10 must-reject, 10 must-accept). Three
guards: (a) **mutation detection** — a deliberately broken parser (accepts
empty ids) must be reported as regressed on those cases; (b) **call budget** —
the parser is invoked **exactly once per case** (spy counter), so a
double-parse "validate then parse" implementation fails; (c) **dedupe** — each
regressed id appears once even if seeded twice. **Follow-up:** how do you keep
the fixture from drifting? *(Answer: golden files versioned with the case ids —
a case edit is a diff a reviewer sees, never a silent behavior change.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/38-test-strategy-contract-regression/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/38-test-strategy-contract-regression/test_challenge.py -q
```
