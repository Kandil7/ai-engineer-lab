# Arabic NLP 06: Approximate Nearest Neighbor (ANN) Search

## 🎯 Topic Overview

Exact nearest-neighbor search scans every vector — too slow for a large
corpus. ANN search trades a little recall for a lot of speed, using an
index that prunes the search space. This lecture covers the ANN index, the
recall/speed tradeoff, and the parameters.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why exact search does not scale
2. Explain the ANN recall/speed tradeoff
3. Choose the index parameters
4. Measure the recall loss
5. Tune the index on the golden set

---

## 1. Why Exact Search Does Not Scale

Exact search computes the distance from the query to every vector. At a
million vectors, every query is a million distance computations. The
latency grows linearly with the corpus. The roadmap's exit test: "ANN
search is used for large corpora."

## 2. The ANN Tradeoff

ANN prunes the search space so only a fraction of vectors are scored. The
cost is recall: the true nearest neighbor may be pruned. The tradeoff is
controlled by the index parameters — more pruning, faster but less
accurate. The roadmap's exit test: "the recall/speed tradeoff is
understood."

## 3. The Index

The ANN index organizes vectors so similar ones are near each other in the
index. HNSW builds a multi-layer graph; a query walks the graph toward the
nearest vectors. The index is built once and searched many times.

## 4. The Parameters

The index has parameters: the graph's connectivity and the search's
exploration. Higher connectivity builds a better index but uses more
memory; higher exploration searches more thoroughly but slower. The
parameters are the recall/speed dial.

## 5. Tuning on the Golden Set

The index is tuned on the golden set: try parameter combinations, measure
recall@k and latency, keep the best. The tuning is evidence-based. The
roadmap's exit test: "the ANN index is tuned on the golden set."

## Common Mistakes

- Exact search on a large corpus (slow).
- Ignoring the recall loss (silent degradation).
- Parameters guessed, not tuned.
- No latency measurement.
- Tuning on the wrong set.

## Key Takeaways

1. Exact search does not scale to large corpora.
2. ANN trades a little recall for a lot of speed.
3. The index prunes the search space.
4. The parameters are the recall/speed dial.
5. The index is tuned on the golden set.