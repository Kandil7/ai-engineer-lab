# Qdrant 03: Hybrid Search — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hybrid search | Vector + keyword search fused | semantic + lexical |
| Fusion | Combining two ranked lists into one | RRF |
| RRF | Reciprocal rank fusion | 1/(60 + rank) |
| Weight | The relative strength of each signal | keyword 0.6 |
| Semantic match | Meaning-based similarity | synonyms |
| Lexical match | Exact-term similarity | rare proper noun |
| Golden-set tuning | Weights chosen by measured recall | evidence-based |

---

## Alphabetical Glossary

### Fusion

**Definition:** Combining the vector and keyword ranked lists into one.
The point where the two signals meet.

**Example:**
```python
# merge vector results and keyword results into one ranking
```

**Related concepts:** RRF, Weight

---

### Golden-set tuning

**Definition:** Choosing the hybrid weights by measuring recall@k on the
golden set. Evidence-based, not guessed.

**Example:**
```python
# try weight combinations, keep the best recall@k
```

**Related concepts:** Weight

---

### Hybrid search

**Definition:** Running vector and keyword search on the same query and
fusing the results. Each retriever catches what the other misses.

**Example:**
```python
# vector results + keyword results -> fused ranking
```

**Related concepts:** Fusion, Semantic match

---

### Lexical match

**Definition:** Exact-term similarity. Catches rare proper nouns and
technical terms that embeddings dilute.

**Example:**
```python
# "البخاري" matches only passages containing the exact term
```

**Related concepts:** Semantic match

---

### RRF

**Definition:** Reciprocal rank fusion: each result scores the sum of
1/(60 + rank) across the lists. A result ranked first in both lists wins.

**Example:**
```python
def rrf_score(ranks):
    return sum(1 / (60 + r) for r in ranks)
```

**Related concepts:** Fusion

---

### Semantic match

**Definition:** Meaning-based similarity. Catches paraphrases and synonyms
that keyword search misses.

**Example:**
```python
# "السفر" matches passages about travel
```

**Related concepts:** Lexical match

---

### Weight

**Definition:** The relative strength of each signal in the fusion. Tuned
on the golden set.

**Example:**
```python
# keyword weight 0.6, vector weight 0.4
```

**Related concepts:** Fusion, Golden-set tuning

---

## Related Concepts

- **Vector search**: one half of the hybrid (topic 02)
- **Metadata filtering**: filters apply to both retrievers (topic 04)
- **Reranking**: the fused list is reranked (rag-system 03)

## Key Takeaways

1. Vector captures meaning; keyword captures exact terms.
2. Fusion combines the two ranked lists.
3. Weights are tuned on the golden set.
4. Hybrid rarely loses and often wins.
5. The fusion is evaluated, not guessed.