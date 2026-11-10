# Module 4: Evaluation & Observability - Measuring What Matters

**Weeks 2-3 (RAG) & Week 7 (Production)** | **Duration: 4-6 hours theory + 8-10 hours practice**

> 🏋️ **Practice workbook:** [`../practice/04-evaluation-observability-practice.md`](../practice/04-evaluation-observability-practice.md) —
> every section has a real-world problem and every topic has Drill → Applied (DevMate) → Stretch levels with verification.

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Design** evaluation frameworks for non-deterministic systems
2. **Implement** RAGAs metrics (context precision, recall, faithfulness, relevancy)
3. **Build** golden datasets and regression test harnesses
4. **Instrument** full pipeline tracing with Langfuse
5. **Track** cost, latency, and quality per request
6. **Detect** drift in user queries and model performance
7. **Create** dashboards for production monitoring

---

## 📚 Lecture Content

### 4.1 Why LLM Evaluation Is Different

| Aspect | Classical ML | LLM Systems |
|--------|--------------|-------------|
| **Ground Truth** | Single correct label | Multiple valid answers |
| **Metrics** | Accuracy, F1, AUC | Faithfulness, relevance, precision |
| **Evaluation** | Automated | LLM-as-judge + human |
| **Regression** | Compare metrics | Golden set + snapshot tests |
| **Drift** | Feature distribution | Query intent distribution |

**Core Challenge**: No single correct answer → need **golden sets** and **LLM judges**

---

### 4.2 Golden Dataset Creation

#### Structure
```jsonl
{"question": "What is the refund policy?", "answer": "Refunds within 30 days...", "contexts": ["Refund Policy: Items may be returned within 30 days..."], "ground_truth": "Full refund within 30 days with receipt.", "category": "policy", "difficulty": "easy"}
{"question": "How do I authenticate?", "answer": "Use Bearer token...", "contexts": ["Authentication: Include Authorization: Bearer <token>..."], "ground_truth": "API requires Bearer token in Authorization header.", "category": "auth", "difficulty": "easy"}
{"question": "Why does the cache invalidate on write?", "answer": "The write-through cache...", "contexts": ["Cache invalidation happens in CacheManager.invalidate()..."], "ground_truth": "Write-through pattern invalidates on every write to ensure consistency.", "category": "architecture", "difficulty": "hard"}
```

#### Categories for Coverage
| Category | Examples | Target Count |
|----------|----------|--------------|
| **Factual** | "What is X?" | 8 |
| **Procedural** | "How do I do Y?" | 6 |
| **Debugging** | "Why does Z fail?" | 4 |
| **Architecture** | "How does A connect to B?" | 4 |
| **Edge Cases** | "What happens if...?" | 3 |
| **Total** | | **25** |

#### Quality Criteria for Golden Set
- [ ] Each question has **one clear intent**
- [ ] Ground truth is **verifiable from sources**
- [ ] Contexts contain **sufficient information**
- [ ] Categories are **balanced**
- [ ] Difficulty spread: 40% easy, 40% medium, 20% hard

---

### 4.3 RAGAs Metrics Deep Dive

#### 1. Context Precision@k
```python
def context_precision_at_k(retrieved_chunks, relevant_chunks, k=5):
    """
    Of the top-k retrieved chunks, how many are relevant?
    """
    top_k = retrieved_chunks[:k]
    relevant_in_top_k = sum(1 for c in top_k if c.id in relevant_chunks)
    return relevant_in_top_k / k

# Example
retrieved = [chunk_1, chunk_2, chunk_3, chunk_4, chunk_5]  # IDs: 1,2,3,4,5
relevant = {1, 3, 7}  # Only chunks 1 and 3 are relevant
precision_at_5 = 2/5 = 0.4
```

#### 2. Context Recall
```python
def context_recall(retrieved_chunks, all_relevant_chunks):
    """
    Of all relevant chunks in corpus, how many did we retrieve?
    """
    retrieved_ids = {c.id for c in retrieved_chunks}
    relevant_ids = set(all_relevant_chunks)
    return len(retrieved_ids & relevant_ids) / len(relevant_ids)


# If corpus has 10 relevant chunks, we retrieved 7 → recall = 0.7
```

#### 3. Faithfulness (Hallucination Detection)
```python
FAITHFULNESS_PROMPT = """Given a question, answer, and context, identify claims in the answer that are NOT supported by the context.

Question: {question}
Answer: {answer}
Context: {context}

List each claim in the answer and whether it's supported (YES/NO).
Format:
Claim 1: [claim text] - SUPPORTED: YES/NO
Claim 2: [claim text] - SUPPORTED: YES/NO
...

Only use information from the context."""

# Faithfulness = (supported claims) / (total claims)
```

#### 4. Answer Relevancy
```python
def answer_relevancy(question, answer, embedding_model):
    """
    Semantic similarity between question and answer.
    High = answer addresses the question.
    """
    q_emb = embedding_model.embed([question])[0]
    a_emb = embedding_model.embed([answer])[0]
    return cosine_similarity(q_emb, a_emb)
```

---

### 4.4 LLM-as-Judge Pattern

```python
class LLMJudge:
    def __init__(self, llm_client, model="claude-3-5-sonnet-20241022"):
        self.client = llm_client
        self.model = model

    async def judge_faithfulness(
        self, question: str, answer: str, contexts: List[str]
    ) -> float:
        prompt = FAITHFULNESS_PROMPT.format(
            question=question,
            answer=answer,
            context="\n\n".join(f"[{i + 1}] {c}" for i, c in enumerate(contexts)),
        )

        response = await self.client.complete(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.0,
        )

        # Parse claims
        claims = parse_claims(response.content)
        supported = sum(1 for c in claims if c.supported)
        total = len(claims)

        return supported / max(total, 1)

    async def judge_relevancy(self, question: str, answer: str) -> float:
        prompt = f"""Rate how well the answer addresses the question on a scale of 1-10.

Question: {question}
Answer: {answer}

Consider:
- Does it directly answer the question?
- Is it on-topic?
- Does it avoid irrelevant information?

Return only a number 1-10."""

        response = await self.client.complete(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.0,
        )

        return float(response.content.strip()) / 10.0
```

---

### 4.5 Automated Evaluation Harness

```python
class EvaluationHarness:
    def __init__(self, rag_pipeline, judge: LLMJudge):
        self.pipeline = rag_pipeline
        self.judge = judge

    async def run_evaluation(
        self,
        dataset_path: str,
        output_path: str = None,
    ) -> EvaluationReport:

        # Load golden set
        golden_set = load_jsonl(dataset_path)

        results = []

        for item in golden_set:
            # Run RAG pipeline
            rag_result = await self.pipeline.query(
                RAGRequest(
                    query=item["question"],
                    stream=False,
                )
            )

            # Compute metrics
            context_precision = context_precision_at_k(
                rag_result.contexts, item.get("relevant_chunk_ids", []), k=5
            )

            faithfulness = await self.judge.judge_faithfulness(
                item["question"],
                rag_result.answer,
                [c.content for c in rag_result.contexts],
            )

            answer_relevancy = await self.judge.judge_relevancy(
                item["question"], rag_result.answer
            )

            results.append(
                EvalResult(
                    question=item["question"],
                    answer=rag_result.answer,
                    ground_truth=item.get("ground_truth"),
                    contexts=[c.content for c in rag_result.contexts],
                    scores={
                        "context_precision": context_precision,
                        "faithfulness": faithfulness,
                        "answer_relevancy": answer_relevancy,
                    },
                    latency_ms=rag_result.latency_ms,
                    cost_usd=rag_result.usage.get("total_cost", 0),
                )
            )

        # Aggregate
        report = EvaluationReport(
            dataset=dataset_path,
            timestamp=datetime.utcnow(),
            num_questions=len(results),
            aggregate_scores={
                "context_precision": np.mean(
                    [r.scores["context_precision"] for r in results]
                ),
                "faithfulness": np.mean([r.scores["faithfulness"] for r in results]),
                "answer_relevancy": np.mean(
                    [r.scores["answer_relevancy"] for r in results]
                ),
            },
            per_question=results,
            latency_p50=np.percentile([r.latency_ms for r in results], 50),
            latency_p95=np.percentile([r.latency_ms for r in results], 95),
            total_cost_usd=sum(r.cost_usd for r in results),
        )

        if output_path:
            report.save(output_path)

        return report
```

---

### 4.6 Regression Testing: Prompt/Model Changes

```python
class RegressionTester:
    """Compare new version against baseline."""

    def __init__(self, baseline_report: EvaluationReport):
        self.baseline = baseline_report

    def compare(self, new_report: EvaluationReport) -> RegressionReport:
        """Check for regressions."""
        regressions = []
        improvements = []

        for metric in ["context_precision", "faithfulness", "answer_relevancy"]:
            baseline_score = self.baseline.aggregate_scores[metric]
            new_score = new_report.aggregate_scores[metric]
            diff = new_score - baseline_score

            if diff < -0.05:  # 5% regression threshold
                regressions.append(
                    {
                        "metric": metric,
                        "baseline": baseline_score,
                        "new": new_score,
                        "diff": diff,
                    }
                )
            elif diff > 0.02:
                improvements.append(
                    {
                        "metric": metric,
                        "baseline": baseline_score,
                        "new": new_score,
                        "diff": diff,
                    }
                )

        # Per-question comparison
        question_regressions = []
        for bq, nq in zip(self.baseline.per_question, new_report.per_question):
            for metric in bq.scores:
                if nq.scores[metric] - bq.scores[metric] < -0.1:
                    question_regressions.append(
                        {
                            "question": bq.question,
                            "metric": metric,
                            "baseline": bq.scores[metric],
                            "new": nq.scores[metric],
                        }
                    )

        return RegressionReport(
            passed=len(regressions) == 0,
            regressions=regressions,
            improvements=improvements,
            question_regressions=question_regressions,
        )
```

#### CI Integration
```yaml
# .github/workflows/eval.yml
name: RAG Evaluation

on:
  pull_request:
    paths:
      - 'devmate/src/devmate/retrieve/**'
      - 'devmate/src/devmate/llm/prompts/**'

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run evaluation
        run: |
          python -m devmate.eval.run_ragas --dataset evaluations/rag/datasets/devmate-golden.jsonl
      - name: Check regression
        run: |
          python -m devmate.eval.check_regression --baseline evaluations/rag/reports/baseline.json
```

---

### 4.7 Observability: Full Pipeline Tracing

#### What to Trace
```
User Request
    │
    ├─► Input Guardrails (validation, injection detection)
    │
    ├─► Semantic Cache (hit/miss)
    │
    ├─► Query Embedding (latency, tokens)
    │
    ├─► Vector Search (Qdrant latency, results count)
    │
    ├─► Reranking (model, latency, score changes)
    │
    ├─► Prompt Construction (template version, context size)
    │
    ├─► LLM Generation (model, tokens, latency, streaming)
    │
    ├─► Output Guardrails (PII, schema validation)
    │
    └─► Response (total latency, cost, tokens)
```

#### Langfuse Integration
```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key,
    host=settings.langfuse_host,
)


@traced("rag.query")
async def traced_rag_query(request: RAGRequest):
    trace = langfuse.trace(
        name="rag_query",
        input={"question": request.query},
        metadata={"model": request.model},
    )

    # Embedding
    with trace.span(name="embedding") as span:
        embedding = await embed(request.query)
        span.end(output={"dimensions": len(embedding)})

    # Retrieval
    with trace.span(name="retrieval") as span:
        results = await retrieve(embedding)
        span.end(output={"num_results": len(results)})

    # Reranking
    with trace.span(name="reranking") as span:
        reranked = await rerank(request.query, results)
        span.end(output={"top_scores": [r.score for r in reranked[:3]]})

    # Generation
    with trace.span(name="generation") as span:
        answer = await generate(reranked)
        span.end(output={"answer_length": len(answer)})

    trace.end(output={"answer": answer})
    return answer
```

---

### 4.8 Drift Detection

```python
class DriftDetector:
    """Detect shifts in query distribution."""

    def __init__(self, embedding_model, reference_queries: List[str]):
        self.embedder = embedding_model
        self.reference_embeddings = self.embedder.embed(reference_queries)
        self.reference_centroid = np.mean(self.reference_embeddings, axis=0)

    def compute_drift(self, recent_queries: List[str]) -> DriftReport:
        recent_embeddings = self.embedder.embed(recent_queries)
        recent_centroid = np.mean(recent_embeddings, axis=0)

        # Cosine distance between centroids
        drift_score = 1 - cosine_similarity(self.reference_centroid, recent_centroid)

        # Per-query distances
        query_distances = []
        for q, emb in zip(recent_queries, recent_embeddings):
            dist = 1 - cosine_similarity(emb, self.reference_centroid)
            query_distances.append({"query": q, "distance": dist})

        # Alert if drift > threshold
        alert = drift_score > 0.3  # 30% shift

        return DriftReport(
            drift_score=drift_score,
            alert=alert,
            query_distances=query_distances,
            reference_size=len(self.reference_embeddings),
            recent_size=len(recent_queries),
        )
```

---

### 4.9 Production Dashboards

#### Key Metrics to Display

| Dashboard | Metrics | Alert Threshold |
|-----------|---------|-----------------|
| **Latency** | p50, p95, p99 per stage | p95 > 5s |
| **Quality** | Faithfulness, Precision, Relevancy (7-day rolling) | Faithfulness < 0.8 |
| **Cost** | $/query, $/day, tokens/day | $/day > budget |
| **Cache** | Hit rate, size, evictions | Hit rate < 20% |
| **Errors** | Rate by type (timeout, validation, LLM) | Error rate > 1% |
| **Drift** | Query distribution shift | Drift score > 0.3 |

#### Grafana Dashboard JSON (simplified)
```json
{
  "dashboard": {
    "title": "DevMate RAG Production",
    "panels": [
      {
        "title": "End-to-End Latency",
        "targets": [{"expr": "histogram_quantile(0.95, rate(rag_latency_seconds_bucket[5m]))"}]
      },
      {
        "title": "Faithfulness (7-day avg)",
        "targets": [{"expr": "avg_over_time(rag_faithfulness[7d])"}]
      },
      {
        "title": "Cost per Query",
        "targets": [{"expr": "sum(rate(rag_cost_usd_total[1h])) / sum(rate(rag_requests_total[1h]))"}]
      },
      {
        "title": "Cache Hit Rate",
        "targets": [{"expr": "rag_cache_hits_total / (rag_cache_hits_total + rag_cache_misses_total)"}]
      }
    ]
  }
}
```

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Golden Set** | Curated Q&A pairs with ground truth for evaluation |
| **LLM-as-Judge** | Using an LLM to evaluate another LLM's output |
| **Context Precision** | Fraction of retrieved chunks that are relevant |
| **Context Recall** | Fraction of relevant chunks that were retrieved |
| **Faithfulness** | Fraction of answer claims supported by context |
| **Answer Relevancy** | Semantic similarity between answer and question |
| **Regression Test** | Comparing new version against baseline |
| **Drift Detection** | Monitoring for shifts in input distribution |
| **Span** | Single operation in a trace (e.g., embedding, retrieval) |
| **Trace** | Complete request flow with all spans |
| **Snapshot Test** | Comparing output against saved reference |

---

## 🏋️ Exercises

### Exercise 4.1: Build Golden Set (60 min)
Create 25 Q&A pairs for your repository with contexts and ground truth.

### Exercise 4.2: RAGAs Evaluation (90 min)
Run full RAGAs evaluation on your pipeline, produce report.

### Exercise 4.3: LLM Judge (60 min)
Implement faithfulness and relevancy judges with structured output.

### Exercise 4.4: Regression Harness (60 min)
Build comparison tool that fails CI on metric regression.

### Exercise 4.5: Langfuse Tracing (60 min)
Instrument full pipeline with spans, visualize in Langfuse.

### Exercise 4.6: Drift Detection (45 min)
Implement query drift detector with alerting.

---

## ❓ Quiz

### Question 1
Why can't we use classical ML metrics (accuracy, F1) for LLM evaluation?
- A) LLMs are too slow
- B) No single correct answer for generative tasks
- C) LLMs don't output probabilities
- D) Tokens don't match labels

### Question 2
What does RAGAs `faithfulness` measure?
- A) Answer relevance to question
- B) Whether answer claims are grounded in context
- C) Retrieval quality
- D) Response speed

### Question 3
What is a "golden set"?
- A) Best model checkpoints
- B) Curated Q&A pairs with ground truth
- C) Optimal hyperparameters
- D) High-quality training data

### Question 4
How does LLM-as-judge work?
- A) Human evaluates LLM output
- B) One LLM evaluates another LLM's output
- C) Judge model ranks multiple outputs
- D) Both B and C

### Question 5
What is the purpose of regression testing in LLM systems?
- A) Ensure new prompts/models don't degrade quality
- B) Test model training
- C) Validate data pipeline
- D) Check infrastructure

### Question 6
What should you trace in a RAG pipeline?
- A) Only LLM calls
- B) Every stage: guardrails, cache, embedding, retrieval, rerank, generation
- C) Only errors
- D) Only latency

### Question 7
What indicates query drift?
- A) Increasing latency
- B) Shift in query embedding distribution vs reference
- C) Higher costs
- D) More errors

### Question 8
What's a good regression threshold for faithfulness?
- A) Any decrease
- B) > 5% decrease (0.05 absolute)
- C) > 10% decrease
- D) > 20% decrease

---

## 💻 Code Challenge

### Challenge: Complete Evaluation & Observability Stack

**Requirements:**
1. **Golden Set**: 25 questions for your repo
2. **Evaluation Harness**: Runs RAGAs + custom metrics
3. **LLM Judges**: Faithfulness, relevancy with structured output
4. **Regression Testing**: CI gate that fails on >5% regression
5. **Langfuse Tracing**: Full pipeline with spans
6. **Drift Detection**: Weekly query distribution check
7. **Dashboard**: Grafana/Langfuse with key metrics

**Deliverables:**
- `evaluations/rag/datasets/devmate-golden.jsonl`
- `evaluations/rag/harness/run_ragas.py`
- `evaluations/rag/harness/regression.py`
- Langfuse project with traces
- Grafana dashboard JSON

**Success Criteria:**
- Evaluation runs in < 5 minutes
- Regression detection catches injected bugs
- All pipeline stages visible in traces
- Cost per eval run < $0.50

---

## 📋 Case Study: DevMate Evaluation (Weeks 2-3, 7)

**Golden Set Evolution:**
- Week 2: 10 questions (smoke test)
- Week 3: 25 questions (full coverage)
- Week 7: 50 questions (added edge cases)

**Baseline Metrics (Week 3):**

| Metric | Score | Target |
|--------|-------|--------|
| Context Precision@5 | 0.83 | > 0.7 |
| Context Recall | 0.79 | > 0.7 |
| Faithfulness | 0.91 | > 0.85 |
| Answer Relevancy | 0.88 | > 0.8 |
| Citation Accuracy | 0.94 | > 0.9 |

**Regression Catch (Week 7):**
- Changed system prompt → faithfulness dropped 0.91 → 0.82
- CI failed, prompt reverted
- Without harness: would have deployed regression

**Drift Detection:**
- Week 5: New query pattern "fix bug in..." increased 40%
- Detected via centroid shift (drift score 0.35)
- Added bug-fix examples to golden set
- Faithfulness recovered

---

## 🚀 Production Checklist

- [ ] Golden set created (25+ questions, balanced categories)
- [ ] Evaluation harness runs RAGAs + custom metrics
- [ ] LLM judges implemented for faithfulness/relevancy
- [ ] Regression testing in CI/CD
- [ ] Baseline report saved and versioned
- [ ] Full pipeline traced with Langfuse
- [ ] Spans for: guardrails, cache, embed, retrieve, rerank, generate
- [ ] Cost tracking per request
- [ ] Drift detection on query embeddings
- [ ] Dashboards for latency, quality, cost, cache, errors
- [ ] Alerts configured for thresholds
- [ ] Runbook for quality degradation

---

## 📚 Further Reading

1. **RAGAs Docs**: https://docs.ragas.io
2. **Langfuse Docs**: https://langfuse.com/docs
3. **DeepEval**: https://github.com/confident-ai/deepeval
4. **LLM-as-Judge Paper**: "LLM-as-a-Judge: Rethinking Model Evaluation"
5. **Observability for LLMs**: https://arize.com/blog/llm-observability