# Module 2: RAG Systems - Retrieval Augmented Generation

**Weeks 2-3 of Active Track** | **Duration: 6-8 hours theory + 10-12 hours practice**

> 🏋️ **Practice workbook:** [`../practice/02-rag-systems-practice.md`](../practice/02-rag-systems-practice.md) —
> every section has a real-world problem and every topic has Drill → Applied (DevMate) → Stretch levels with verification.

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Design** end-to-end RAG pipelines from ingestion to generation
2. **Implement** multiple chunking strategies and evaluate their impact
3. **Configure** Qdrant vector database with optimal settings
4. **Build** hybrid search (semantic + keyword) with reranking
5. **Create** evaluation harness with RAGAs metrics
6. **Optimize** retrieval quality through systematic experimentation
7. **Deploy** production RAG with caching, monitoring, and cost control

---

## 📚 Lecture Content

### 2.1 RAG Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INGESTION (offline)           QUERY TIME (online)          │
│  ────────────────────          ─────────────────────         │
│                                                              │
│  Documents ──► Chunker ──► Embedder ──► Qdrant              │
│       │                                                        │
│       ▼                                                        │
│  ┌─────────────────────────────────────────────────────┐      │
│  │                    Query Pipeline                    │      │
│  │                                                      │      │
│  │  User Query ──► Embed ──► Hybrid Search ──► Rerank  │      │
│  │       │              (top-20)          (top-5)       │      │
│  │       ▼                     │              │         │      │
│  │  Prompt Construction ◄──────┴──────────────┘         │      │
│  │       │                                               │      │
│  │       ▼                                               │      │
│  │  LLM Generation (with citations)                      │      │
│  │       │                                               │      │
│  │       ▼                                               │      │
│  │  Cited Answer + Sources                               │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight**: The #1 factor in RAG quality is **chunking strategy**, not model choice.

---

### 2.2 Chunking Strategies

#### Fixed-Size Chunking
```python
class FixedSizeChunker:
    def __init__(self, chunk_size=512, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, metadata: dict) -> List[Document]:
        chunks = []
        start = 0
        position = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Break at word boundary
            if end < len(text):
                last_space = text.rfind(" ", start, end)
                if last_space > start:
                    end = last_space

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    Document(
                        content=chunk_text,
                        metadata={
                            **metadata,
                            "chunk_index": position,
                            "chunker": "fixed",
                        },
                    )
                )
                position += 1

            start = end - self.overlap
            if start >= len(text):
                break

        return chunks
```

**Pros**: Simple, fast, predictable
**Cons**: Splits mid-sentence, loses context
**Use when**: Quick prototyping, uniform documents

---

#### Recursive Text Splitting (LangChain Style)
```python
class RecursiveChunker:
    def __init__(self, chunk_size=512, overlap=50, separators=None):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def chunk(self, text: str, metadata: dict) -> List[Document]:
        chunks = self._split_text(text, self.separators)

        documents = []
        for i, chunk_text in enumerate(chunks):
            if chunk_text.strip():
                documents.append(
                    Document(
                        content=chunk_text.strip(),
                        metadata={**metadata, "chunk_index": i, "chunker": "recursive"},
                    )
                )
        return documents

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        if not separators:
            return [
                text[i : i + self.chunk_size]
                for i in range(0, len(text), self.chunk_size)
            ]

        separator = separators[0]
        splits = text.split(separator)

        if len(splits) == 1 or all(len(s) <= self.chunk_size for s in splits):
            if len(separators) > 1:
                return self._split_text(text, separators[1:])
            return splits

        result = []
        for split in splits:
            if len(split) <= self.chunk_size:
                result.append(split)
            else:
                result.extend(self._split_text(split, separators[1:]))

        return result
```

**Pros**: Respects paragraph/sentence boundaries
**Cons**: May create uneven chunks
**Use when**: General documents, mixed content

---

#### Semantic Chunking
```python
class SemanticChunker:
    def __init__(self, embedding_model, similarity_threshold=0.7):
        self.embedding_model = embedding_model
        self.threshold = similarity_threshold

    def chunk(self, text: str, metadata: dict) -> List[Document]:
        # Split into sentences first
        sentences = self._split_sentences(text)

        # Embed all sentences
        embeddings = self.embedding_model.embed(sentences)

        # Group by semantic similarity
        chunks = []
        current_chunk = [sentences[0]]
        current_embeddings = [embeddings[0]]

        for i in range(1, len(sentences)):
            sim = cosine_similarity(embeddings[i], current_embeddings[-1])

            if sim >= self.threshold:
                current_chunk.append(sentences[i])
                current_embeddings.append(embeddings[i])
            else:
                # Finalize current chunk
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]
                current_embeddings = [embeddings[i]]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return [
            Document(content=c, metadata={**metadata, "chunker": "semantic"})
            for c in chunks
        ]
```

**Pros**: Topic-aware splits, coherent chunks
**Cons**: Requires embedding calls during indexing
**Use when**: Quality matters more than speed

---

#### AST-Aware Chunking (For Code)
```python
class ASTAwareChunker:
    """Chunk code by syntactic boundaries (functions, classes)."""

    def chunk(self, text: str, metadata: dict) -> List[Document]:
        language = metadata.get("language", "").lower()

        if language == "python":
            return self._chunk_python(text, metadata)
        elif language in ("javascript", "typescript"):
            return self._chunk_js_ts(text, metadata)
        else:
            # Fallback
            return RecursiveChunker().chunk(text, metadata)

    def _chunk_python(self, text: str, metadata: dict) -> List[Document]:
        import ast

        try:
            tree = ast.parse(text)
        except SyntaxError:
            return RecursiveChunker().chunk(text, metadata)

        chunks = []
        lines = text.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = node.lineno - 1
                end = getattr(node, "end_lineno", start + 50)

                chunk_content = "\n".join(lines[start:end])

                if len(chunk_content) > 2000:  # Too large
                    continue

                chunk_type = (
                    "function"
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    else "class"
                )

                chunks.append(
                    Document(
                        content=chunk_content,
                        metadata={
                            **metadata,
                            "chunk_type": chunk_type,
                            "name": node.name,
                            "start_line": start + 1,
                            "end_line": end,
                            "chunker": "ast_aware",
                        },
                    )
                )

        return chunks if chunks else RecursiveChunker().chunk(text, metadata)
```

---

### 2.3 Vector Database: Qdrant Deep Dive

#### Collection Configuration
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="code_documents",
    vectors_config=models.VectorParams(
        size=1536,  # text-embedding-3-small dimensions
        distance=models.Distance.COSINE,
        on_disk=True,  # Store vectors on disk for large collections
    ),
    optimizers_config=models.OptimizersConfigDiff(
        indexing_threshold=20000,  # Switch to HNSW after 20K vectors
    ),
    hnsw_config=models.HnswConfigDiff(
        m=16,  # Connections per node (higher = better recall, more memory)
        ef_construct=100,  # Build-time search width
        full_scan_threshold=10000,  # Use exact search below this
    ),
)

# Payload indexes for filtering
for field in ["language", "filename", "chunk_type", "repo_name"]:
    client.create_payload_index(
        collection_name="code_documents",
        field_name=field,
        field_schema="keyword",
    )
```

#### HNSW Parameters Explained
| Parameter | Effect | Trade-off |
|-----------|--------|-----------|
| `m` | Graph connectivity | Higher = better recall, more memory |
| `ef_construct` | Build-time search width | Higher = better index quality, slower build |
| `ef_search` | Query-time search width | Higher = better recall, slower queries |

**Recommended starting values**: `m=16`, `ef_construct=100`, `ef_search=64`

---

### 2.4 Hybrid Search: Semantic + Keyword

#### Why Hybrid?
- **Semantic search** misses exact matches: "QDR-2024", "UserService", "OAuth2"
- **Keyword search** misses synonyms: "refund" vs "money back"
- **Hybrid** = best of both worlds

#### Implementation with Reciprocal Rank Fusion (RRF)
```python
class HybridRetriever:
    def __init__(self, qdrant_client, embedding_model, k=60):
        self.client = qdrant_client
        self.embedder = embedding_model
        self.k = k  # RRF parameter

    async def retrieve(
        self,
        query: str,
        query_vector: List[float],
        limit: int = 20,
        filter: dict = None,
    ) -> List[SearchResult]:

        # 1. Semantic search
        semantic_hits = await self._semantic_search(query_vector, limit * 2, filter)

        # 2. Keyword search (BM25 via payload filter)
        keyword_hits = await self._keyword_search(query, limit * 2, filter)

        # 3. RRF Fusion
        return self._rrf_fusion(semantic_hits, keyword_hits, limit)

    async def _semantic_search(self, vector, limit, filter):
        query_filter = self._build_filter(filter) if filter else None
        hits = self.client.search(
            collection_name="code_documents",
            query_vector=vector,
            limit=limit,
            query_filter=query_filter,
            with_payload=True,
        )
        return [SearchResult.from_hit(h) for h in hits]

    async def _keyword_search(self, query, limit, filter):
        # Use Qdrant's text matching on content field
        # In production, use sparse vectors or external BM25
        query_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="content",
                    match=models.MatchText(text=query),
                )
            ]
            + ([self._build_filter(filter)] if filter else [])
        )

        hits, _ = self.client.scroll(
            collection_name="code_documents",
            scroll_filter=query_filter,
            limit=limit,
            with_payload=True,
        )
        return [SearchResult.from_hit(h, score=1.0) for h in hits]

    def _rrf_fusion(self, semantic, keyword, limit):
        """Reciprocal Rank Fusion: score = 1/(k + rank_semantic) + 1/(k + rank_keyword)"""
        scores = {}
        doc_map = {}

        for rank, doc in enumerate(semantic):
            scores[doc.id] = scores.get(doc.id, 0) + 1 / (self.k + rank + 1)
            doc_map[doc.id] = doc

        for rank, doc in enumerate(keyword):
            scores[doc.id] = scores.get(doc.id, 0) + 1 / (self.k + rank + 1)
            if doc.id not in doc_map:
                doc_map[doc.id] = doc

        # Sort by combined score
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        results = []
        for doc_id in sorted_ids[:limit]:
            doc = doc_map[doc_id]
            doc.score = scores[doc_id]  # Update with fused score
            results.append(doc)

        return results
```

---

### 2.5 Reranking: The Cheap Quality Boost

```
Retrieve top-20 (bi-encoder, ~50ms)
        │
        ▼
Rerank top-20 (cross-encoder, ~100ms)
        │
        ▼
Return top-5 (high precision)
```

#### Cross-Encoder vs Bi-Encoder
| Aspect | Bi-Encoder (Retrieval) | Cross-Encoder (Reranking) |
|--------|------------------------|---------------------------|
| **Architecture** | Separate encoders for query/doc | Joint encoding of query+doc |
| **Speed** | Fast (pre-computed doc vectors) | Slower (must process pairs) |
| **Quality** | Good for recall | Excellent for precision |
| **Use Case** | First-stage retrieval | Second-stage reranking |

#### Cohere Rerank Integration
```python
class CohereReranker:
    def __init__(self, api_key: str, model: str = "rerank-v3.5"):
        self.client = httpx.AsyncClient(
            base_url="https://api.cohere.ai/v1",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0,
        )
        self.model = model

    async def rerank(
        self,
        query: str,
        documents: List[SearchResult],
        top_k: int = 5,
    ) -> List[RerankResult]:

        if not documents:
            return []

        payload = {
            "model": self.model,
            "query": query,
            "documents": [d.content for d in documents],
            "top_n": top_k,
            "return_documents": False,
        }

        response = await self.client.post("/rerank", json=payload)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data["results"]:
            idx = item["index"]
            orig = documents[idx]
            results.append(
                RerankResult(
                    id=orig.id,
                    score=item["relevance_score"],
                    content=orig.content,
                    metadata=orig.metadata,
                    original_score=orig.score,
                )
            )

        return results
```

#### Local Reranker (bge-reranker)
```python
class LocalReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        from sentence_transformers import CrossEncoder

        self.model = CrossEncoder(model_name, max_length=512)

    def rerank(
        self,
        query: str,
        documents: List[SearchResult],
        top_k: int = 5,
    ) -> List[RerankResult]:

        pairs = [(query, doc.content) for doc in documents]
        scores = self.model.predict(pairs)

        reranked = []
        for doc, score in zip(documents, scores):
            reranked.append(
                RerankResult(
                    id=doc.id,
                    score=float(score),
                    content=doc.content,
                    metadata=doc.metadata,
                    original_score=doc.score,
                )
            )

        reranked.sort(key=lambda x: x.score, reverse=True)
        return reranked[:top_k]
```

---

### 2.6 Evaluation Framework: RAGAs Metrics

#### The Four Core Metrics

```python
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)
from ragas import evaluate
from datasets import Dataset

# Evaluation dataset format
eval_data = {
    "question": [
        "What is the refund policy?",
        "How do I authenticate with the API?",
    ],
    "answer": [
        "Refunds are available within 30 days...",
        "Use Bearer token in Authorization header...",
    ],
    "contexts": [
        ["Refund Policy: Items may be returned within 30 days...", "..."],
        ["Authentication: Include Authorization: Bearer <token>...", "..."],
    ],
    "ground_truth": [
        "Full refund within 30 days of purchase with receipt.",
        "API requires Bearer token authentication.",
    ],
}

dataset = Dataset.from_dict(eval_data)

# Run evaluation
results = evaluate(
    dataset,
    metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
)

print(results)
# {
#     'context_precision': 0.85,
#     'context_recall': 0.78,
#     'faithfulness': 0.92,
#     'answer_relevancy': 0.88,
# }
```

#### Metric Definitions

| Metric | Formula | Target | What It Measures |
|--------|---------|--------|------------------|
| **Context Precision** | Relevant chunks in top-k / k | > 0.7 | Are retrieved chunks relevant? |
| **Context Recall** | Relevant chunks retrieved / Total relevant | > 0.7 | Did we find all relevant info? |
| **Faithfulness** | Supported claims / Total claims | > 0.85 | Is answer grounded in context? |
| **Answer Relevancy** | Sim(embedding(answer), embedding(question)) | > 0.8 | Does answer address question? |

#### Custom Evaluation Harness
```python
class RAGEvaluator:
    def __init__(self, rag_pipeline):
        self.pipeline = rag_pipeline

    async def evaluate_dataset(
        self,
        dataset_path: str,
        output_path: str = None,
    ) -> Dict[str, float]:

        # Load golden set
        with open(dataset_path) as f:
            golden_set = [json.loads(line) for line in f]

        results = []

        for item in golden_set:
            # Run RAG pipeline
            rag_result = await self.pipeline.query(
                RAGRequest(
                    query=item["question"],
                    stream=False,
                )
            )

            # Prepare for RAGAs
            eval_item = {
                "question": item["question"],
                "answer": rag_result.answer,
                "contexts": [ctx.content for ctx in rag_result.contexts],
                "ground_truth": item.get("ground_truth", ""),
            }
            results.append(eval_item)

        # Compute metrics
        dataset = Dataset.from_list(results)
        metrics = evaluate(
            dataset,
            metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        )

        # Add custom metrics
        metrics["avg_latency_ms"] = np.mean([r.latency_ms for r in rag_results])
        metrics["avg_cost_usd"] = np.mean([r.usage["total_cost"] for r in rag_results])
        metrics["citation_accuracy"] = self._compute_citation_accuracy(results)

        if output_path:
            with open(output_path, "w") as f:
                json.dump(metrics, f, indent=2)

        return metrics

    def _compute_citation_accuracy(self, results) -> float:
        """Check if citations [1], [2] match actual sources."""
        correct = 0
        total = 0

        for item in results:
            answer = item["answer"]
            contexts = item["contexts"]

            # Extract citations [1], [2], etc.
            citations = re.findall(r"\[(\d+)\]", answer)

            for cite in citations:
                total += 1
                idx = int(cite) - 1
                if 0 <= idx < len(contexts):
                    # Verify the cited context actually supports the claim
                    # Simplified: just check if context exists
                    correct += 1

        return correct / max(total, 1)
```

---

### 2.7 Production RAG Checklist

#### Performance Budgets
```
Query embedding:     < 50ms
Qdrant retrieval:    < 100ms
Reranking:           < 150ms
LLM generation:      < 2000ms (streaming)
Total end-to-end:    < 3000ms
```

#### Cost Optimization
```python
class CostOptimizedRAG:
    def __init__(self):
        self.embedding_cache = LRUCache(maxsize=10000)
        self.retrieval_cache = LRUCache(maxsize=1000)
    
    async def query(self, request: RAGRequest) -> RAGResult:
        # 1. Check semantic cache
        cached = await semantic_cache.get(request.query, query_embedding, model)
        if cached:
            return cached.response
        
        # 2. Use smaller embedding model for non-critical paths
        if request.use_fast_path:
            embedding_model = "text-embedding-3-small"  # Cheaper
        else:
            embedding_model = "text-embedding-3-large"  # Better quality
        
        # 3. Batch embedding calls during indexing (not query time)
        # 4. Cache retrieval results for identical queries (24h TTL)
        # 5. Use cheaper LLM for simple questions (Haiku vs Sonnet)
        
        return await self._execute_query(request)
```

#### Monitoring Dashboard Metrics
- Query latency (p50, p95, p99)
- Retrieval quality (RAGAs scores over time)
- Hallucination rate (sampled)
- Cost per query
- Cache hit rate
- Error rate by type

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **RAG** | Retrieval-Augmented Generation - combining retrieval with LLM generation |
| **Chunking** | Splitting documents into retrieval-sized pieces |
| **Embedding** | Dense vector representation of text meaning |
| **Vector Database** | Database optimized for similarity search (Qdrant, Pinecone, etc.) |
| **Semantic Search** | Finding documents by meaning similarity (cosine similarity) |
| **Keyword Search** | Finding documents by exact term matching (BM25) |
| **Hybrid Search** | Combining semantic + keyword search |
| **Reranking** | Second-pass scoring with cross-encoder for precision |
| **Bi-Encoder** | Separate encoders for query and document (fast) |
| **Cross-Encoder** | Joint encoder for query+document pair (accurate) |
| **RRF** | Reciprocal Rank Fusion - combining ranked lists |
| **Context Precision** | Fraction of retrieved chunks that are relevant |
| **Context Recall** | Fraction of relevant chunks that were retrieved |
| **Faithfulness** | Fraction of answer claims supported by context |
| **Answer Relevancy** | Semantic similarity between answer and question |
| **Golden Set** | Curated Q&A pairs for evaluation |
| **Citation Accuracy** | Whether [1], [2] citations match actual sources |

---

## 🏋️ Exercises

### Exercise 2.1: Chunking Comparison (90 min)
Implement all 4 chunkers and compare on a test corpus:

```python
def compare_chunkers(documents: List[Document]) -> Dict:
    chunkers = {
        "fixed": FixedSizeChunker(512, 50),
        "recursive": RecursiveChunker(512, 50),
        "semantic": SemanticChunker(embedding_model),
        "ast": ASTAwareChunker(),
    }
    
    results = {}
    for name, chunker in chunkers.items():
        all_chunks = []
        for doc in documents:
            all_chunks.extend(chunker.chunk(doc.content, doc.metadata))
        
        results[name] = {
            "num_chunks": len(all_chunks),
            "avg_chunk_size": np.mean([len(c.content) for c in all_chunks]),
            "size_std": np.std([len(c.content) for c in all_chunks]),
        }
    
    return results
```

### Exercise 2.2: Build Hybrid Retriever (90 min)
Combine Qdrant semantic search with BM25 keyword search using RRF.

### Exercise 2.3: Reranker Integration (60 min)
Add Cohere reranker (or local bge-reranker) and measure precision@5 improvement.

### Exercise 2.4: Evaluation Harness (120 min)
Create golden set of 25 questions, run RAGAs evaluation, produce comparison report.

### Exercise 2.5: Production Hardening (90 min)
Add: semantic caching, request deduplication, latency budgets, cost alerts.

---

## ❓ Quiz

### Question 1
What is the #1 factor affecting RAG quality?
- A) LLM model choice
- B) Chunking strategy
- C) Vector database choice
- D) Temperature setting

### Question 2
Which chunking strategy is best for source code?
- A) Fixed-size
- B) Recursive
- C) Semantic
- D) AST-aware

### Question 3
What does RRF (Reciprocal Rank Fusion) do?
- A) Combines multiple ranked lists into one
- B) Reranks using cross-encoder
- C) Filters by metadata
- D) Compresses vectors

### Question 4
What is the difference between bi-encoder and cross-encoder?
- A) Bi-encoder is for reranking, cross-encoder for retrieval
- B) Bi-encoder encodes query/doc separately, cross-encoder jointly
- C) They're the same thing
- D) Cross-encoder is faster

### Question 5
What does RAGAs `faithfulness` measure?
- A) How relevant the answer is to the question
- B) How many relevant chunks were retrieved
- C) Whether answer claims are supported by retrieved context
- D) How fast the system responds

### Question 6
What is a good target for context_precision@5?
- A) > 0.3
- B) > 0.5
- C) > 0.7
- D) > 0.9

### Question 7
Why use hybrid search (semantic + keyword)?
- A) It's faster than semantic alone
- B) Catches exact matches that embeddings miss
- C) Reduces vector database size
- D) Eliminates need for reranking

### Question 8
What does `on_disk=True` do in Qdrant collection config?
- A) Stores vectors on disk instead of RAM
- B) Enables persistent storage
- C) Uses disk-based HNSW index
- D) All of the above

---

## 💻 Code Challenge

### Challenge: Build a Complete RAG System with Evaluation

**Requirements:**
1. **Ingestion Pipeline**: Load repo → chunk (3 strategies) → embed → upsert to Qdrant
2. **Retrieval**: Hybrid search (semantic + keyword) → rerank → top-5
3. **Generation**: LLM with citations, streaming
4. **Evaluation**: 25-question golden set, RAGAs metrics, comparison report
5. **Experimentation**: A/B test chunking strategies, document results in ADR

**Deliverables:**
- Working pipeline with CLI
- Evaluation report with metrics table
- ADR documenting chunking strategy choice with numbers
- Cost/latency analysis

**Evaluation:**
- Context precision > 0.7
- Faithfulness > 0.85
- End-to-end latency < 3s (p95)
- Cost per query < $0.02

---

## 📋 Case Study: DevMate RAG (Weeks 2-3)

**Golden Set Creation:**
- 25 questions over this repository
- Categories: architecture, API, data models, deployment, testing
- Each with expected source files and ground truth

**Chunking Experiment Results:**

| Strategy | Context Precision | Context Recall | Faithfulness | Avg Latency |
|----------|-------------------|----------------|--------------|-------------|
| Fixed (512) | 0.62 | 0.58 | 0.78 | 1.8s |
| Recursive | 0.71 | 0.68 | 0.84 | 1.9s |
| **AST-Aware** | **0.83** | **0.79** | **0.91** | **2.1s** |

**Decision**: AST-aware chunking for code (ADR-006), recursive for docs.

**Vector Store Comparison (ADR-005):**

| DB | Precision | Recall | Latency | Cost | Decision |
|----|-----------|--------|---------|------|----------|
| Qdrant | 0.83 | 0.79 | 85ms | Free (self-host) | ✅ Primary |
| Chroma | 0.79 | 0.74 | 120ms | Free | Fallback |

---

## 🚀 Production Checklist

- [ ] Golden set created (25+ questions)
- [ ] Evaluation harness running RAGAs metrics
- [ ] Chunking strategy chosen with evidence
- [ ] Vector DB configured with HNSW tuning
- [ ] Hybrid search implemented
- [ ] Reranker integrated and measured
- [ ] Citation format enforced in prompts
- [ ] Semantic cache deployed
- [ ] Latency budgets defined and monitored
- [ ] Cost per query tracked
- [ ] Drift detection on question distribution
- [ ] A/B testing framework for prompt/model changes
- [ ] Failure mode documentation
- [ ] Runbook for common issues

---

## 📚 Further Reading

1. **DeepLearning.AI**: "Building and Evaluating Advanced RAG"
2. **RAGAs Docs**: https://docs.ragas.io
3. **Qdrant Docs**: https://qdrant.tech/documentation
4. **Cohere Rerank**: https://docs.cohere.com/docs/reranking
5. **"AI Engineering" by Chip Huyen** - RAG chapter
6. **LangChain Chunking**: https://python.langchain.com/docs/modules/data_connection/document_transformers