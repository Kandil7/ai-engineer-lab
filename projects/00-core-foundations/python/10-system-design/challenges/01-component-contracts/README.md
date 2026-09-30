# Challenge 01: Component Contracts — The Record Contract

Two teams share the Athar record shape. Yesterday someone added `edition`. The
consumer broke at 3 a.m. because nobody classified the change. Fix the
machinery so it cannot happen again.

## 🥉 Bronze — Classify the Change (~15 min)

**Task:** Implement `classify_change(old, new)`, given two contract dicts
(`{"required": {field: semantic}}`, where a semantic containing `"optional"`
marks an optional field). Return `"breaking"` if a field was removed or its
semantic changed; `"needs-migration"` if a required field was added;
`"compatible"` otherwise.

**Signature:**
```python
def classify_change(old: dict, new: dict) -> str
```

| Change | Expected |
|---|---|
| add `edition: "str, edition label"` (required) | `"needs-migration"` |
| add `ts: "ts, optional"` | `"compatible"` |
| remove `page` | `"breaking"` |
| change `page`'s semantic | `"breaking"` |
| identical contracts | `"compatible"` |

**Constraints:** any correct rule application passes.

---

## 🥈 Silver — Validate Every Violation (~35 min)

**Task:** Implement `validate_payload(payload, contract)`, returning **all**
violation strings: missing required fields (named), empty `text`, and
`source_ref` not equal to `f"{book}/p{page}"`. Fail-fast-on-first is a
failure here — the operator needs the full list to quarantine properly.

**Signature:**
```python
def validate_payload(payload: dict, contract: dict) -> list[str]
```

| Input | Expected |
|---|---|
| valid payload | `[]` |
| 3 broken rules at once | ≥ 3 violations, each naming its rule |
| empty text + bad ref + missing field | all three reported |

**Constraints:** `n <= 2000` payloads. **Guards:** (a) completeness — a
payload violating 3 rules yields ≥ 3 violations (a fail-fast validator returns
1 and fails); (b) immutability — the payload must be unchanged after the call
(a normalizing validator fails). **Adversarial case:** a payload with every
rule broken at once.

---

## 🥇 Gold — Plan and Simulate the Migration (~75 min)

**Task:** Implement `plan_migration(old, new)` returning the ordered step names
for adding a required field:
`["emit-default", "consumers-tolerate", "backfill", "require"]` (empty list for
compatible or breaking changes), and `simulate_migration(plan, old_rec,
new_rec)` returning True iff the plan is a safe rolling upgrade: at least one
coexistence step exists (the deprecation window), every step before `"require"`
accepts BOTH records, and the `"require"` step accepts only the new record.

**Signature:**
```python
def plan_migration(old: dict, new: dict) -> list[str]
def simulate_migration(plan: list[str], old_rec: dict, new_rec: dict) -> bool
```

| Input | Expected |
|---|---|
| full 4-step plan, old lacks field | `True` |
| one-step `["require"]` | `False` (the naive plan) |
| `[]` | `False` |
| plan without final `require` | `False` |

**Constraints:** 1000-field contracts. **Guard (comparison budget):** the tests
wrap field names in a comparison-counting string and assert total equality
checks stay under `6 * n` — pairwise old×new field comparison is O(n²) and must
fail; set-based diff stays near O(n). **Follow-up:** what breaks when two teams
migrate in opposite order? *(Answer: the plan needs a deprecation window and
dual-write for renames — the contract's `deprecated` list is where that
window lives.)*

---

## Running

```bash
python -m pytest 10-system-design/challenges/01-component-contracts/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 10-system-design/challenges/01-component-contracts/test_challenge.py -q
```
