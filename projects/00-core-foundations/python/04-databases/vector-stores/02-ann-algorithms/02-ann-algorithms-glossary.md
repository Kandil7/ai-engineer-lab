# Vector Stores 02: ANN Algorithms — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| ANN | Approximate nearest neighbors: faster than exact, recall < 1 | HNSW at recall@10 = 0.97 |
| HNSW | Layered-graph index with greedy descent + beam search | Qdrant default index |
| M | HNSW neighbors per node (build-time: size/speed) | M = 16 typical |
| ef_construction | HNSW build beam width (build-time: quality) | 200 for high recall |
| ef_search | HNSW query beam width (query-time: recall vs latency) | raise until recall flattens |
| IVF | Partition corpus into buckets, search nearest few | 65k buckets, probe 8 |
| Product quantization | Split vector, replace subspaces with centroid codes | 768 floats → 96 bytes |

---

## Alphabetical Glossary

### ANN

**Definition:** Approximate nearest-neighbor search: indexes that return
nearly the true top-k much faster than brute force. Priced by recall@k.

**Example:**
```python
# brute force: 1.00 recall, 800 ms — HNSW: 0.97 recall, 12 ms
```

**Related concepts:** HNSW, IVF, Recall@k

---

### ef_construction

**Definition:** HNSW beam width used while building the graph. Larger means a
better-connected graph and slower indexing. Baked in at build time.

**Example:**
```python
# ef_construction=200: slower build, higher ceiling for ef_search later
```

**Related concepts:** HNSW, M, ef_search

---

### ef_search

**Definition:** HNSW beam width used per query. The live recall-vs-latency
knob — the only parameter tunable without rebuilding.

**Example:**
```python
# sweep ef_search 16 -> 128, plot recall@10, stop at the knee
```

**Related concepts:** HNSW, ef_construction, Recall@k

---

### HNSW

**Definition:** Hierarchical Navigable Small World: layered graph index.
Greedy descent through sparse upper layers, beam search on the dense base.
Logarithmic query scaling; see Malkov & Yashunin 2016.

**Example:**
```python
# Qdrant collection configured with hnsw(m=16, ef_construct=200)
```

**Related concepts:** ANN, M, ef_search, IVF

---

### IVF

**Definition:** Inverted file index: k-means partitions the corpus into
buckets; queries scan only the nearest buckets. Buckets probed is the dial.

**Example:**
```python
# probe 8 of 65k buckets: ~8000x less scanning than brute force
```

**Related concepts:** ANN, Product quantization

---

### M

**Definition:** HNSW out-degree per node. Larger M means a denser graph:
better recall ceiling, bigger index, slower builds.

**Example:**
```python
# M=16 default; raise for high-recall collections with RAM to spare
```

**Related concepts:** HNSW, ef_construction

---

### Product quantization

**Definition:** Compression that splits each vector into subspaces and stores
only the nearest-centroid code per subspace. Distances come from lookup
tables. Buys RAM at the price of fine-grained distortion.

**Example:**
```python
# 768 x float32 (3 KB) -> 96 codes (96 B): 32x smaller
```

**Related concepts:** IVF, Quantization, Reranking

---

## Related Concepts

- **Quantization (scalar/binary)**: coarser compression dials, covered in topic 04
- **Reranking**: repairs PQ distortion on near-duplicates (DevMate weeks 2–3)
- **Recall@k**: the pricing axis for every approximation (topic 01)

## Key Takeaways

1. Three approximations: graph search, partitioning, compression.
2. ef_search is the only knob that turns without a rebuild.
3. Every speedup is priced in recall@k — measure, don't assume.
