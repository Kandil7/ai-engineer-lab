# Arabic NLP 06: ANN Search — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| ANN | Approximate nearest neighbor | pruned search |
| Exact search | Scores every vector | linear latency |
| Recall loss | The true neighbor may be pruned | silent degradation |
| HNSW | A multi-layer graph index | walk toward nearest |
| Connectivity | The graph's branching | memory cost |
| Exploration | The search's thoroughness | speed cost |
| Golden-set tuning | Parameters chosen by measured recall | evidence-based |

---

## Alphabetical Glossary

### ANN

**Definition:** Approximate nearest neighbor: trading a little recall for a
lot of speed by pruning the search space.

**Example:**
```python
# only a fraction of vectors are scored per query
```

**Related concepts:** Exact search, Recall loss

---

### Connectivity

**Definition:** The graph's branching factor in HNSW. Higher builds a
better index but uses more memory.

**Example:**
```python
# M = 16 vs M = 32
```

**Related concepts:** HNSW

---

### Exact search

**Definition:** Computing the distance from the query to every vector.
Latency grows linearly with the corpus.

**Example:**
```python
# a million vectors -> a million distance computations
```

**Related concepts:** ANN

---

### Exploration

**Definition:** The search's thoroughness in HNSW. Higher searches more
thoroughly but slower.

**Example:**
```python
# ef_search = 64 vs ef_search = 128
```

**Related concepts:** HNSW

---

### Golden-set tuning

**Definition:** Choosing the ANN parameters by measuring recall@k and
latency on the golden set. Evidence-based.

**Example:**
```python
# try parameter combinations, keep the best recall@k
```

**Related concepts:** Recall loss

---

### HNSW

**Definition:** Hierarchical navigable small world: a multi-layer graph
index. A query walks the graph toward the nearest vectors.

**Example:**
```python
# build once, search many times
```

**Related concepts:** Connectivity, Exploration

---

### Recall loss

**Definition:** The true nearest neighbor may be pruned by the ANN index.
The cost of the speed.

**Example:**
```python
# recall@10 drops from 1.0 to 0.95 with a faster index
```

**Related concepts:** ANN

---

## Related Concepts

- **Embeddings**: ANN searches the embedding vectors (topic 04)
- **Hybrid search**: ANN is the vector half (topic 05)
- **MRR evaluation**: recall loss is measured with MRR (topic 07)

## Key Takeaways

1. Exact search does not scale to large corpora.
2. ANN trades a little recall for a lot of speed.
3. The index prunes the search space.
4. The parameters are the recall/speed dial.
5. The index is tuned on the golden set.