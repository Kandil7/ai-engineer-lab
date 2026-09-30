# Challenge 37: Code Review and Refactoring — The God-Endpoint Split

A single 80-line endpoint in the Athar search service parses, validates,
filters, retrieves, and caches. Review demands a split. Refactor it without
changing behavior — and prove both halves.

## 🥉 Bronze — Measure the Smells (~15 min)

**Task:** Implement `function_stats(src)`, returning per-function metrics from
a source string: `{"name": {"lines": int, "params": int, "branches": int}}` —
line span, parameter count, and branch count (`if`/`for`/`while`/`except`).

**Signature:**
```python
def function_stats(src: str) -> dict[str, dict[str, int]]
```

| Input | Expected |
|---|---|
| `"def f(a, b):\n    return a"` | `{"f": {"lines": 2, "params": 2, "branches": 0}}` |
| nested ifs in one function | `branches == 2` |
| async function | counted like a normal one |

**Constraints:** valid Python source. Any correct approach passes.

---

## 🥈 Silver — Split Without Drift (~35 min)

**Task:** Implement `split_god_function(src) -> str`, refactoring the god
source into extracted functions so **no function exceeds 6 branches**, with
behavior byte-identical on probe inputs.

**Signature:**
```python
def split_god_function(src: str) -> str
```

| Probe input | Must match original |
|---|---|
| empty query | same return value |
| missing user | same return value |
| Arabic query with diacritics | same return value |
| page bounds overlap | same list contents |

**Constraints:** the tests exec both sources and compare outputs on 200 seeded
probe records. **Guard (two parts):** (a) structural — `ast`-parse the output
and assert max branches ≤ 6 (rename-only or unsplit solutions fail);
(b) behavioral — outputs byte-identical on every probe including adversarial
edges. **Adversarial case:** a probe that hits every branch of the original.

---

## 🥇 Gold — Refactor with Locks (~75 min)

**Task:** Implement `refactor_with_locks(src, probes) -> tuple[str, list[dict]]`,
returning the refactored source AND a lock-test report (per-probe
`{"probe": i, "preserved": bool}`), under a structural budget: the **max
branches per function must drop ≥ 40%** vs the original and every lock must
pass.

**Signature:**
```python
def refactor_with_locks(src: str, probes: list[dict]) -> tuple[str, list[dict]]
```

| Input | Expected |
|---|---|
| god src + 50 probes | `(refactored, [{"probe": 0, "preserved": True}, ...])` |
| src with 2 small functions | left as-is (already under budget) |

**Constraints:** branch counting via `ast`, behavior via exec-and-compare —
never wall-clock. The tests assert three things: every lock `preserved` is
True, `max_branches(refactored) <= 6`, and the max-branch drop is ≥ 40% —
plus the refactored module must define ≥ 3 functions (real extraction, not a
rename). **Adversarial case:** a probe with empty query, one with no user, and
one with page bounds outside every record.

**Follow-up:** which refactoring comes next? *(Answer: replace the remaining
engine conditional with the strategy pattern — then the lock probes prove
dispatch equivalence, and the composition root becomes the only branching
site.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/37-code-review-and-refactoring/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/37-code-review-and-refactoring/test_challenge.py -q
```
