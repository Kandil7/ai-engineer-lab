# Challenge 35: Unicode and Arabic Text — The Corpus Deduplicator

An Arabic RAG corpus arrives from many sources: some with harakat, some with
lam-alef ligatures, some with Arabic-Indic page numbers. Two records that are
*the same text* must deduplicate; a corpus import must never blow up memory.

## 🥉 Bronze — Normalize a Record (~15 min)

**Task:** Implement `normalize_record(record)`, which returns a new dict with:
`page` folded to an ASCII `int`, `text` NFC-cleaned with harakat stripped and
whitespace collapsed, and `search_key` built with full Arabic folding
(NFKC, strip harakat, unify أ إ آ → ا, ى → ي, ة → ه).

**Signature:**
```python
def normalize_record(record: dict) -> dict
```

| Input | Expected |
|---|---|
| `{"id": "a", "page": "١٢", "text": "مُحَمَّد"}` | `{"id": "a", "page": 12, "text": "محمد", "search_key": "محمد"}` |
| `{"id": "b", "page": "7", "text": "أَحْمَد"}` | `page == 7`, `search_key == "احمد"` |
| `{"id": "c", "page": "۵", "text": "مَدْرَسَة"}` | `page == 5`, `search_key == "مدرسه"` |

**Constraints:** `len(text) <= 10^4`. Any correct approach passes.

---

## 🥈 Silver — Find Duplicates (~35 min)

**Task:** Implement `find_duplicates(records)`, grouping records whose
`search_key` collides. Return groups (size ≥ 2) as lists of original records,
groups ordered by first appearance.

**Signature:**
```python
def find_duplicates(records: list[dict]) -> list[list[dict]]
```

| Input | Expected |
|---|---|
| two records with keys `محمد` / `محمد` | one group of 2 |
| three records, all distinct keys | `[]` |
| `[]` | `[]` |
| four records, keys `a,a,a,b` | one group of 3 |

**Constraints:** `n <= 5000`. The tests wrap every search_key in a
comparison-counting string and assert total `__eq__`/`__lt__` calls stay under
`3 * n` — pairwise comparison of keys is O(n²) and must fail the budget;
`dict.setdefault` grouping stays near O(n). Counting comparisons, never
wall-clock. **Adversarial case:** all records share one base word but differ by
diacritics — the naive pairwise loop explodes, the dict approach does not.

---

## 🥇 Gold — Streaming Import (~75 min)

**Task:** Implement `import_corpus(lines, batch_size, on_error)`, streaming a
JSONL corpus in batches: returns `{"imported": int, "batches": int, "errors": int}`;
`on_error(line_no, message)` is called per broken record (JSON error or missing
`id`/`text` field) with the 1-based line number; valid records import.

**Signature:**
```python
def import_corpus(lines: Iterable[str], batch_size: int, on_error) -> dict
```

| Input | Expected |
|---|---|
| 3 valid lines, batch_size 2 | `{"imported": 3, "batches": 2, "errors": 0}` |
| 1 broken JSON line among 3 valid | `errors == 1`, `on_error` got `line 2` |
| empty corpus | `{"imported": 0, "batches": 0, "errors": 0}` |
| missing `text` field | counted as error, located message |

**Constraints:** 200k lines, memory ceiling 8 MB peak (`tracemalloc`).
Materializing `read().splitlines()` blows the ceiling; batch streaming does not.
**Adversarial case:** one corrupt line at position 123 — must be located exactly.

**Follow-up:** what breaks first at 10^9 lines? *(Answer: the error list grows
without bound and a single machine cannot hold the working set — errors must be
spilled to a dead-letter file and batches must be written to disk, not counted
in memory.)*

---

## Running

```bash
python -m pytest 02-advanced-python/challenges/35-unicode-and-arabic-text/test_challenge.py -q
# validate the reference:
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 02-advanced-python/challenges/35-unicode-and-arabic-text/test_challenge.py -q
```
