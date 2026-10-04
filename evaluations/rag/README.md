# RAG Evaluation Guide

How to evaluate retrieval-augmented generation quality in this workspace.

---

## Why Evaluate RAG?

RAG systems fail silently. A retrieval pipeline can return irrelevant chunks,
a reranker can demote correct results, and a generator can hallucinate despite
having the right context. Evaluation catches these failures before they reach users.

## Datasets

Test datasets live in `datasets/` as JSONL files. Each line is one test case:

```json
{"question": "How does DevMate handle fallback across LLM providers?", "expected_context": ["provider fallback chain", "retry with backoff"], "expected_answer": "DevMate tries the primary provider, then falls back through a cheaper provider to a cached or graceful error path."}
```

### Dataset Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | yes | The user query |
| `expected_context` | string[] | yes | Chunks that should be retrieved (at least 2) |
| `expected_answer` | string | yes | Gold-standard answer the generator should produce |
| `metadata` | object | no | Tags like `difficulty`, `topic`, `phase` |

### Creating a Dataset

1. Identify a topic from the learning source index or project code
2. Write 5-10 questions at varying difficulty
3. For each question, identify the 2-5 chunks that contain the answer
4. Write the expected answer grounded in those chunks
5. Save as `evaluations/rag/datasets/<topic>-v<version>.jsonl`

## Metrics

### Retrieval Metrics

| Metric | Formula | Target | What It Catches |
|--------|---------|--------|-----------------|
| **Recall@5** | relevant_in_top5 / total_relevant | > 0.85 | Missing relevant chunks |
| **Precision@3** | relevant_in_top3 / 3 | > 0.80 | Retrieving junk |
| **MRR** | 1 / rank_of_first_relevant | > 0.70 | Relevant docs ranked too low |

### Generation Metrics

| Metric | Description | Target | What It Catches |
|--------|-------------|--------|-----------------|
| **Faithfulness** | % of claims in answer supported by context | > 0.95 | Hallucination |
| **Answer Relevance** | Cosine similarity of answer embedding to query embedding | > 0.80 | Off-topic answers |
| **Completeness** | % of expected answer points covered | > 0.85 | Incomplete answers |

### Custom Metrics

| Metric | Description | When to Use |
|--------|-------------|-------------|
| **Citation Accuracy** | % of cited sources that actually support the claim | When generating citations |
| **Chunk Overlap** | Average token overlap between retrieved chunks | When tuning chunk size |
| **Latency** | End-to-end retrieval + generation time | When optimizing performance |

## Baselines

Baselines are metric snapshots from a known-good configuration.
They live in `baselines/` and are used to detect regression.

```markdown
# Baseline: 2026-06-26

## Configuration
- Chunk size: 512 tokens
- Overlap: 50 tokens
- Embedding model: text-embedding-3-small
- Reranker: none
- Top-k: 5

## Metrics
- Recall@5: 0.87
- Precision@3: 0.82
- Faithfulness: 0.96
- Answer Relevance: 0.83

## Dataset: rag-basics-v1.jsonl (10 cases)
```

### Creating a Baseline

1. Run evaluation with your current configuration
2. Record all metrics in `baselines/<date>-<config>.md`
3. Commit the baseline as a regression anchor
4. Future evaluations compare against this baseline

## Running Evaluations

### Manual Evaluation

1. Select a dataset from `datasets/`
2. Run your RAG pipeline on each question
3. Compare retrieved chunks against `expected_context`
4. Compare generated answer against `expected_answer`
5. Record metrics in `reports/<date>-report.md`

### Automated Evaluation

```powershell
# Run RAG evaluation (when script is available)
# ./infra/scripts/eval-rag.ps1 --dataset rag-basics-v1.jsonl
```

## Reports

Reports live in `reports/` and follow this format:

```markdown
# RAG Evaluation Report — <date>

## Dataset
- Name: rag-basics-v1.jsonl
- Cases: 10

## Metrics
| Metric | Value | Baseline | Delta |
|--------|-------|----------|-------|
| Recall@5 | 0.88 | 0.87 | +0.01 |
| Precision@3 | 0.81 | 0.82 | -0.01 |
| Faithfulness | 0.97 | 0.96 | +0.01 |
| Answer Relevance | 0.84 | 0.83 | +0.01 |

## Failures
- Q3: Retrieved chunk about HTTP routing instead of goroutine management
  - Root cause: Keyword overlap between "route" and "goroutine"
  - Fix: Add semantic reranking

## Decision
- [ ] Accept (metrics meet or exceed baseline)
- [ ] Reject (metrics below baseline — investigate)
```

## Tuning Guide

| Problem | Likely Cause | Try |
|---------|--------------|-----|
| Low Recall@5 | Chunks too small or overlap too low | Increase chunk size, add overlap |
| Low Precision@3 | Embedding model too general | Switch to domain-specific embedding |
| Low Faithfulness | Context too noisy | Add reranking, reduce top-k |
| Low Answer Relevance | Query too vague | Add query rewriting step |
