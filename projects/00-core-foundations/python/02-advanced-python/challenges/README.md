# 02-advanced-python — Challenge Sets

Practice sets follow [`PRACTICE_SPEC.md`](../../PRACTICE_SPEC.md): Bronze (mechanics)
→ Silver (right structure, measured guard) → Gold (production constraint).

| Challenge | Topic | Skills |
|---|---|---|
| `35-unicode-and-arabic-text/` | [Unicode and Arabic Text](../35-unicode-and-arabic-text/) | normalization, streaming import, located errors |
| `36-separation-of-concerns/` | [Separation of Concerns](../36-separation-of-concerns/) | Protocols, DI, engine-swap invariant |
| `37-code-review-and-refactoring/` | [Code Review and Refactoring](../37-code-review-and-refactoring/) | smell measurement, lock tests, structural budgets |
| `38-test-strategy-contract-regression/` | [Test Strategy](../38-test-strategy-contract-regression/) | provenance, idempotency, regression gate |

## Running

```powershell
python -m pytest 02-advanced-python/challenges/<name>/test_challenge.py -q
# validate the reference solution:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/<name>/test_challenge.py -q
```

Default runs target `starter.py` and fail with `NotImplementedError` until solved.
