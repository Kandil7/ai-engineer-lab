# Challenge 36: Separation of Concerns — The Swappable Search Engine

An Athar pipeline validates reference records (book/page rules) and searches
them. If the validator and the engine are fused, every retrieval experiment
risks the reference rules. Break the fusion.

## 🥉 Bronze — Wire a Pipeline (~15 min)

**Task:** Implement `wire_pipeline(index, config)`, which builds a pipeline
record from given collaborators: returns `{"index": index, "config": config,
"engine_kind": config["engine"]}`. The point is constructor injection — the
function names no concrete class.

**Signature:**
```python
def wire_pipeline(index, config: dict) -> dict
```

| Input | Expected |
|---|---|
| `(fake, {"engine": "memory"})` | `{"index": fake, "config": ..., "engine_kind": "memory"}` |
| `(fake, {"engine": "prefix"})` | `engine_kind == "prefix"` |

**Constraints:** `config` has at least `"engine"`. Any correct approach passes.

---

## 🥈 Silver — The Engine-Swap Invariant (~35 min)

**Task:** Implement `run_engine_swap_test(pipeline_factory, corpus)`, which runs
the same corpus through pipelines built with two different engines and returns
True iff the validation error lists are **identical** (the mastery invariant).
`pipeline_factory(engine_kind)` returns an object with `ingest(records) -> dict`
including an `"errors"` list.

**Signature:**
```python
def run_engine_swap_test(pipeline_factory, corpus: list[dict]) -> bool
```

| Input | Expected |
|---|---|
| factory + corpus with 2 valid, 1 invalid | `True` (same errors both engines) |
| factory + all-valid corpus | `True` |
| `[]` | `True` |

**Constraints:** `n <= 1000`. The tests use a SpyIndex double counting every
call: the validator path must call the index **exactly 0 times** during
validation, and `normalize_text` (injected, counted) must be called **exactly
once per record** — a fused pipeline that re-normalizes in parse AND validate
fails the call budget. **Adversarial case:** records with diacritics +
presentation forms so double normalization would visibly differ.

---

## 🥇 Gold — Extract a New Engine (~75 min)

**Task:** Implement `build_engine(engine_kind)`, returning a NEW engine
object with `add(record) -> None` and `search(query: str, limit: int) -> list`
that satisfies the same contract as the reference engines — WITHOUT any change
to validation logic. Prove decoupling: the pipeline built with it must produce
identical validation errors on a 1000-record corpus.

**Signature:**
```python
def build_engine(engine_kind: str) -> object
```

| Input | Expected |
|---|---|
| `"prefix"` | object with `add` + `search`; search returns matching records |
| `"keyword"` | object with `add` + `search`; substring matching |

**Constraints:** 1000 records, memory ceiling 12 MB peak (`tracemalloc`) —
loading everything twice blows it. The tests assert `inspect.getsource` of the
module does **not** reference the engine module inside validation helpers
(decoupling proof). **Follow-up:** what breaks when a third engine needs
different config? *(Answer: the composition root grows branches — that is the
seam to parameterize; the validator still never changes.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/36-separation-of-concerns/test_challenge.py -q
# validate the reference:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/36-separation-of-concerns/test_challenge.py -q
```
