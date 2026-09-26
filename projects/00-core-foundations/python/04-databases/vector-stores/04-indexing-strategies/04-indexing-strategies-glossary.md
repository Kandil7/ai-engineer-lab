# Vector Stores 04: Indexing Strategies — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Operating point | The (recall, latency) knee chosen for production | recall@10 0.97 at p95 38 ms |
| Grid sweep | Measured M × ef_search matrix with recall + latency per cell | 3×4 sweep table |
| Knee | Curve point where more latency stops buying recall | <0.5pp per 2x latency |
| Scalar quantization | float32 → int8 storage (~4x smaller, ~1pp recall cost) | RAM-fit collections |
| Binary quantization | 1 bit per dimension (~32x smaller, needs re-rank) | first-stage retrieval |
| Shadow collection | Rebuilt index validated before cutover | zero-downtime retune |
| Config record | Parameters + corpus + measurements + owner, versioned | ADR appendix |

---

## Alphabetical Glossary

### Binary quantization

**Definition:** One bit per dimension (~32x compression). Coarse enough to
need exact re-ranking of candidates. First-stage retrieval use.

**Example:**
```python
# binary candidates (fast, rough) -> exact rescore top-100 (slow, true)
```

**Related concepts:** Scalar quantization, Reranking

---

### Config record

**Definition:** The versioned tuple behind an index: parameters, corpus and
query sample ids, recall@k, p95, RAM, date, owner. Makes indexes reproducible.

**Example:**
```python
# (M=16, ef_search=64, recall@10=0.971, p95=38ms, 412MB, 2026-09)
```

**Related concepts:** Grid sweep, Operating point

---

### Grid sweep

**Definition:** Systematic M × ef_search evaluation with recall and latency
recorded per cell. The only honest way to set HNSW parameters.

**Example:**
```python
# 12 cells, 200 queries each: the knee, not an opinion
```

**Related concepts:** Operating point, Knee

---

### Knee

**Definition:** The recall-latency curve point past which doubling latency
buys negligible recall (<0.5pp). The operating point.

**Example:**
```python
# ef_search 64 -> 128: +0.2pp recall, +40ms p95 -> stay at 64
```

**Related concepts:** Grid sweep, Operating point

---

### Operating point

**Definition:** The chosen (recall, latency, RAM) triple for a production
collection, defended by sweep data at a fixed query sample.

**Example:**
```python
# DevMate retrieve budget: recall@10 >= 0.95 at p95 < 100 ms
```

**Related concepts:** Knee, Config record

---

### Scalar quantization

**Definition:** float32 → int8 storage, ~4x smaller, typically ~1pp recall
cost on text workloads. The default first compression step.

**Example:**
```python
# 412 MB -> ~110 MB collection, recall@10 0.971 -> 0.963
```

**Related concepts:** Binary quantization, Product quantization

---

### Shadow collection

**Definition:** A rebuilt index validated (recall gate) before traffic
cutover. Required for any parameter change that needs a rebuild.

**Example:**
```python
# build v2 alongside v1 -> recall@10 gate passes -> swap alias
```

**Related concepts:** Config record, Rebuild vs retune

---

## Related Concepts

- **p95 latency**: the tail metric budgets are written against
- **ADR**: the decision-scale version of the config record (DevMate weeks 2–3)
- **Reranking**: what repairs coarse first-stage retrieval

## Key Takeaways

1. Sweep, don't guess; the knee decides.
2. Quantize from the RAM budget backwards.
3. Record everything or repeat everything.
