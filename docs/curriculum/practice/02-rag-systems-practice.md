# Module 2: RAG Systems — Practice Workbook

**Serves:** [`../lectures/02-rag-systems.md`](../lectures/02-rag-systems.md) | **Track:** Weeks 2–3 (see [`../../roadmap/active-track-10-week.md`](../../roadmap/active-track-10-week.md)) | **Vehicle:** DevMate (`projects/04-ai-engineering/devmate/`)

> Mastery protocol (from [`README.md`](README.md)): **a topic is mastered when all three levels are done AND verified — not when it feels understood.**
> Level 1 = Drill (20–45 min, deterministic, assertable) · Level 2 = Applied (1–3 h, real DevMate artifact) · Level 3 = Stretch (3–6 h, senior-grade, written decision).
> Interview answers are **spoken aloud, 2 minutes, recorded** (Technical English rule, track §7). When a failure mode hits you, log it in `projects/04-ai-engineering/devmate/mistakes.md`.

## How to work this workbook

1. Read the section's **real-world problem** first — it is the lens for every topic below it.
2. Do Level 1 drills until the assertions pass; only then start Level 2. Rule 1 of the protocol: **verify before moving on** — no verified output, no mastery.
3. Level 3 tasks are deliberately bigger than the week; pick the one per section that hurts most, do it end-to-end, and write the ADR-style justification. The track requires **two ADRs with results tables** (chunking strategy, vector-store comparison) — the Level 3s of §2.2 and §2.3 are the natural homes.
4. Track your completion in the table below; `make eval` printing a metrics table is the week's Definition of Done.

**Local command note (this workstation):** `make` and `poetry` are not installed here. Wherever a command says `poetry run python ...`, run `& .venv\Scripts\python.exe ...` from `projects/04-ai-engineering/devmate/` instead (see the repo `AGENTS.md`). The `devmate/scripts/` folder exists for the scripts below.

## Completion tracker

| # | Topic | L1 | L2 | L3 | Evidence (file / output) |
|---|-------|----|----|----|---------------------------|
| 2.1a | Ingestion pipeline | ☐ | ☐ | ☐ | |
| 2.1b | Query pipeline | ☐ | ☐ | ☐ | |
| 2.1c | Chunking = #1 quality factor | ☐ | ☐ | ☐ | |
| 2.2a | Fixed-size chunking | ☐ | ☐ | ☐ | |
| 2.2b | Recursive text splitting | ☐ | ☐ | ☐ | |
| 2.2c | Semantic chunking | ☐ | ☐ | ☐ | |
| 2.2d | AST-aware chunking | ☐ | ☐ | ☐ | |
| 2.3a | Collection configuration | ☐ | ☐ | ☐ | |
| 2.3b | HNSW parameters | ☐ | ☐ | ☐ | |
| 2.3c | Payload indexes & filters | ☐ | ☐ | ☐ | |
| 2.4a | Why hybrid | ☐ | ☐ | ☐ | |
| 2.4b | Reciprocal Rank Fusion | ☐ | ☐ | ☐ | |
| 2.5a | Bi- vs cross-encoder | ☐ | ☐ | ☐ | |
| 2.5b | Cohere rerank | ☐ | ☐ | ☐ | |
| 2.5c | Local reranker | ☐ | ☐ | ☐ | |
| 2.6a | Four RAGAs metrics | ☐ | ☐ | ☐ | |
| 2.6b | Custom eval harness | ☐ | ☐ | ☐ | |
| 2.7a | Performance budgets | ☐ | ☐ | ☐ | |
| 2.7b | Cost optimization | ☐ | ☐ | ☐ | |
| 2.7c | Monitoring metrics | ☐ | ☐ | ☐ | |

**Milestone A3 Definition of Done:** `make eval` prints a metrics table · the chunking ADR cites measured numbers, not intuition · you can explain why AST-aware chunking helps on code specifically.

---

# 2.1 RAG Architecture Overview

## Real-world problem: the 50,000-document consulting copilot

A fintech consultancy ships "Lexo", an internal assistant over 50,000 documents (contracts, onboarding guides, internal APIs, past proposals). The first version was built by a contractor who optimized the wrong thing: they upgraded the LLM three times, kept the retrieval pipeline naive, and delivered. Customers report: answers are *fluent but wrong* — the model cites paragraphs that exist but answer a different question, and the same question asked twice retrieves different chunks depending on phrasing.

Your boss asks: "should we buy a bigger model?" The real question is: **which component of the pipeline is producing the failure, and how do we prove it before spending money?** You must map the two pipelines (ingestion, query), name the quality lever with the highest ROI (chunking, not model choice), and build a measurement habit that prevents the contractor's mistake. Everything in §2.2–2.6 is a tool you will need.

---

### Topic — Ingestion Pipeline (documents → chunker → embedder → vector DB)

**Mastery =** you can trace a file from disk to a retrievable vector, explain what each stage can silently lose (content, metadata, meaning), and design a re-ingest that is idempotent.

**Level 1 — Drill** (mechanics, 20–45 min)

Trace the pipeline on a 3-file corpus without any external service. This only uses `devmate.ingest.chunker`, no Qdrant:

```python
import sys

sys.path.insert(0, r"projects/04-ai-engineering/devmate/src")
from devmate.ingest.chunker import DocumentLoader, get_chunker
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    (root / "a.md").write_text(
        "# Title\n\nSome body text for the doc.\n", encoding="utf-8"
    )
    (root / "b.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
    (root / "blob.bin").write_bytes(b"\x00\x01\x02")
    (root / "notes.xyz").write_text("unsupported\n", encoding="utf-8")

    loader = DocumentLoader(chunker=get_chunker("fixed", chunk_size=32, overlap=4))
    docs = list(loader.load_directory(root, recursive=False))
    print("count:", len(docs))
    for d in docs:
        print(
            d.metadata.get("filename"),
            "| chunker:",
            d.metadata.get("chunker"),
            "| id_len:",
            len(d.id),
        )
```

Expected output (assert each): `count: 3` — `a.md` becomes ≥ 2 chunks (body exceeds 32 chars), `b.py` becomes 1 chunk, `blob.bin` is skipped (UnicodeDecodeError path), `notes.xyz` is skipped (not in `DocumentLoader.SUPPORTED_EXTENSIONS`). Every chunk carries `source`, `filename`, `extension`, `size_bytes`, `chunk_index`, `chunker`; every `id` is 32 hex chars (full md5 of `source:position:content[:100]` — see `_generate_id` in `src/devmate/ingest/chunker.py`; a 16-hex prefix is neither an integer nor a UUID, so Qdrant rejects the upsert).

Edge cases you must handle in your mental model (each maps to a code path you just saw): empty/whitespace files → `[]`; binary files → `[]`; unsupported extensions → `[]`; the same file re-loaded → identical ids (deterministic hashing = free idempotency at chunk level).

**Level 2 — Applied** (DevMate, 1–3 h)

Ingest the DevMate repo itself and prove the pipeline end-to-end without a single vector DB call.

- Create `projects/04-ai-engineering/devmate/scripts/ingest_stats.py`: uses `DocumentLoader(chunker=get_chunker("recursive", chunk_size=512, overlap=50))` to `load_repository(Path("projects/04-ai-engineering/devmate"))` and prints a table: files indexed, total chunks, chunks by extension, mean/median chunk length (chars), skipped files count.
- Run it: `cd projects/04-ai-engineering/devmate && poetry run python scripts/ingest_stats.py`.
- **Deliverable:** `evaluations/rag/reports/ingestion-stats-<date>.md` with the printed table plus a 5-line note on what gets lost at each stage (content loss: skip rules; metadata loss: only fields the chunker copies; meaning loss: boundaries).
- **Acceptance criteria:** the report exists; the run completes in < 60 s; chunk counts are deterministic across two runs (same file → same chunks, same ids).

**Level 3 — Stretch** (production-grade, 3–6 h)

Scale to multi-repo + incremental re-ingest. A repo changes daily; a full re-ingest of 50 repos at 40k chunks/repo costs real money in embeddings each time and causes retrieval staleness during the window. Design and implement:

- A `RepoIndexer` that computes a content-hash per file, skips unchanged files, re-embeds only changed files, and removes vectors for deleted files (the store already has `delete(ids)` — see `src/devmate/index/vector_store.py`).
- Gates: (1) two consecutive runs over an unchanged repo upsert 0 new vectors and take < 10% of full-ingest time; (2) changing one file updates exactly that file's chunks and no others; (3) a killed mid-run leaves the index consistent on retry.
- **Write an ADR-style justification** (see `docs/decisions/` format: Context, Decision Drivers, Options Considered, Decision, Consequences — Consequences must be non-empty): incremental-hash vs. full re-ingest vs. event-driven (webhook). Reference measured ingest time and embedding cost for DevMate's ~2–5k chunks.

**Verify:** `poetry run python scripts/ingest_stats.py` prints the table twice with identical numbers; the ADR file exists under `docs/decisions/` (next free number, e.g. 0007) with a results table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Binary file crashes the run | `read_text` raises UnicodeDecodeError | `DocumentLoader` catches it → returns `[]`; never let a file raise into the loop |
| Identical file produces different chunk ids across machines | Windows CRLF vs LF | Hash normalized content (`content.replace("\r\n", "\n")`) — see §2.2b for boundary consequences |
| Re-ingest duplicates everything | Upsert without idempotent ids | Keep deterministic ids; upsert, never append |
| Metadata lost downstream | Chunker creates a fresh dict | `.copy()` metadata before `update()` (the code already does this — your custom chunkers must too) |

**Interview:** *"Walk me through your ingestion pipeline and what can silently go wrong at each stage."* Strong answer: names the stages (read → filter → chunk → embed → upsert), gives a concrete loss at each (encoding, unsupported types, boundary context, truncation, batch failure), and closes with idempotency + re-ingest strategy. Bonus: mentions deterministic ids as the free idempotency trick.

---

### Topic — Query Pipeline (query → embed → hybrid search → rerank → prompt construction → LLM with citations)

**Mastery =** you can name every stage of the online path, the budget of each, and exactly where citations are attached so a hallucinated citation is impossible by construction.

**Level 1 — Drill** (mechanics, 20–45 min)

Reimplement the prompt-construction stage by hand, exactly as `RAGPipeline._build_context` does in `src/devmate/retrieve/rag.py` (source headers `[Source i: filename | chunk_type | name]`). Given:

```python
results = [
    {
        "id": "a1",
        "content": "def parse(): ...",
        "metadata": {
            "filename": "parser.py",
            "chunk_type": "function",
            "name": "parse",
        },
    },
    {
        "id": "b2",
        "content": "OAuth2 flow: authorize at /token",
        "metadata": {"filename": "auth.md"},
    },
]
context = build_context(results)  # you write this
prompt = RAG_SYSTEM_PROMPT.format(context=context)  # import from devmate.retrieve.rag
```

Assert: `context` contains exactly two `[Source i: ...]` headers in order; header 1 includes `| function | parse`, header 2 has no `|` suffix beyond filename; the prompt says "Use ONLY the information provided in the context"; and an answer citing `[2]` maps to `auth.md` (1-based indexing). Then trace the full online path in `RAGPipeline.query()` and write the stage order as a comment list — embed → retrieve → build context → build messages → generate — noting that `use_reranker=True` is the only knob between retrieval and generation.

**Level 2 — Applied** (DevMate, 1–3 h)

Prove the pipeline runs against the real store. With `make up` (starts Qdrant on `localhost:6333`, see `infra/docker/docker-compose.yml` service `qdrant`):

1. Ingest a slice of DevMate `src/` (recursive chunker), embed with `EmbeddingService` (`src/devmate/index/embeddings.py`), upsert via `vector_store.upsert(docs)`.
2. Ask 3 questions (`RAGRequest(query="How does FixedSizeChunker split text?")`) and print `answer`, `len(contexts)`, `latency_ms`, and the citation markers `[1]..[n]` present in the answer.
3. **Deliverable:** `evaluations/rag/reports/query-pipeline-<date>.md` — the 3 Q/A pairs, context counts, latencies, and one sentence per stage explaining what you observed.
4. **Acceptance criteria:** every answer contains ≥ 1 `[n]` citation; every citation index ≤ `len(contexts)`; the pipeline completes in < 10 s per question on the first run (cold Qdrant).

**Level 3 — Stretch** (production-grade, 3–6 h)

Hard problem: citations under streaming + concurrency. `RAGPipeline._query_streaming` yields chunks but the caller never sees contexts; a streamed answer cannot verify its own citations mid-flight. Design and implement:

- A `StreamedRAGResult` that exposes `contexts` and `answer` together with a `citation_ok` check (all `[n]` ≤ len(contexts)) after the stream completes.
- Load test: 50 concurrent questions (`asyncio.gather`), target p95 < 3 s end-to-end and zero citation violations.
- Failure drill: kill the LLM client mid-stream — assert the partial answer is marked `incomplete` and not cached.
- **Write an ADR-style justification:** stream-then-verify vs. buffer-then-stream (first-token latency trade-off) vs. post-hoc citation linting. Gates: p95 < 3 s, citation violation rate = 0 on the 50-query run, partial answers never enter the semantic cache.

**Verify:** the load-test script prints `p95=…s, violations=0, incomplete=…`; the ADR has a results table comparing first-token latency of the three options.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Citation `[3]` points nowhere | 1-based indexing bug when trimming contexts | Validate `idx-1 < len(contexts)` in the evaluator; enforce in prompt |
| Same question, different answer | Context order changes between runs | Sort retrieved results deterministically (by fused score, then id) |
| Slow first answer | Model warm-up + Qdrant cold index | Pre-warm with one dummy query at startup |
| Answers ignore context | Prompt stuffed with history | Keep system prompt + context first; verify with a "context-only" probe question |

**Interview:** *"Describe the query-time pipeline of your RAG system and where you would add a cache."* Strong answer: 5 stages with latency intuition each, explains rerank position (after retrieval, before prompt), explains cache insertion points (semantic cache before embedding; retrieval cache keyed by (query, filter); never cache partial streams), and names the citation contract as part of prompt construction.

---

### Topic — Chunking Is the #1 Quality Factor, Not Model Choice

**Mastery =** you can prove with numbers — not vibes — that retrieval quality (hence answer quality) moves more with chunk boundaries than with the generator model, and you can design the A/B that shows it.

**Level 1 — Drill** (mechanics, 20–45 min)

Pure math: compute retrieval metrics by hand. Ground truth: relevant chunks are `R1, R2, R3`. System A (bad chunks) retrieves top-5 = `[R1, X, R2, Y, Z]`; System B (good chunks) retrieves `[R1, R2, R3, W, V]`. Compute for both:

- `precision@5 = relevant_in_top5 / 5`
- `recall@5 = relevant_in_top5 / total_relevant (3)`
- `MRR = 1 / rank_of_first_relevant`

Expected (verified): A → p@5 = 0.40, r@5 = 0.6667, MRR = 1.0 (first hit at rank 1); B → p@5 = 0.60, r@5 = 1.0, MRR = 1.0. Now the punchline: keep the same retrieval, swap the generator from "weak" to "strong" and measure faithfulness 0.78 → 0.84; swap the chunking (bad → good) with the weak generator and measure precision 0.62 → 0.83 (lecture case-study numbers: Fixed(512) 0.62/0.58/0.78 vs AST-aware 0.83/0.79/0.91). Write the 2×2 table; conclude which lever moved more: chunking moved precision +0.21, the model moved faithfulness +0.06.

**Level 2 — Applied** (DevMate, 1–3 h)

Run the experiment the track demands: **three chunkers, measured on one golden set**. Reuse the golden questions from §2.6a if you have them; otherwise use 10 hand-written questions over `src/devmate/ingest/chunker.py` (e.g., "What happens when AST parsing fails?", "How are chunk ids generated?").

1. Ingest the DevMate `src/` tree three times into three Qdrant collections: `devmate_fixed`, `devmate_recursive`, `devmate_ast` (fixed 512/50, recursive 512/50, ast-aware default).
2. For each collection run the 10 questions through `RAGPipeline.query` and record recall@5 (chunk-level relevance you define), faithfulness (manual or RAGAs), avg latency.
3. **Deliverable:** `evaluations/rag/reports/chunker-comparison-<date>.md` with the metrics table (columns: chunker, #chunks, recall@5, faithfulness, avg latency) and a "why" paragraph.
4. **Acceptance criteria:** the table has all three rows with real numbers; the best chunker is not assumed — if your numbers disagree with the lecture (AST 0.83/0.79/0.91 @ 2.1s), investigate and explain the delta.

**Level 3 — Stretch** (production-grade, 3–6 h)

The decision Lexo's boss actually faces, with money attached: **"should we buy a bigger model or fix chunking?"** Build the ROI ADR:

- Measure both levers on the same 25-question golden set: (a) current pipeline + current model, (b) current pipeline + larger model (if you have API access; otherwise simulate with documented prices), (c) new chunking + current model, (d) both.
- Convert to cost: model upgrade = $/1M tokens × tokens/query × queries/day; chunking fix = one engineer-week. Put both in a table with the quality delta.
- **Write ADR-0007 `docs/decisions/0007-chunking-strategy.md`** (the track's required chunking ADR): problem, options (fixed/recursive/AST/semantic), chosen path with the results table from Level 2, why, revisit conditions (new corpus type, new languages, token-cost changes).
- Gates: every number in the ADR is traceable to a file in `evaluations/rag/reports/`; the ADR's Decision section states one winner per corpus type (code vs. docs), mirroring the lecture's "AST-aware for code, recursive for docs".

**Verify:** `docs/decisions/0007-chunking-strategy.md` exists with a results table and a non-empty Consequences section; `make eval` (once §2.6b exists) reproduces the table from the same golden set.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| "Model is bad" conclusion with unchanged retrieval | Confusing fluency with correctness | Always measure retrieval metrics separately from generation |
| Chunking A/B invalid | Different corpora, different questions per arm | Same golden set, same questions, only the chunker changes |
| Recall identical for all chunkers | Questions too easy (whole-file answers) | Ask questions that live *inside* one function/paragraph |
| Numbers not reproducible | Hand-picked questions | Freeze the golden set file; version it |

**Interview:** *"What is the #1 factor in RAG quality and how do you know?"* Strong answer: chunking; cites the mechanism (retrieval can only return what chunk boundaries allow; context precision/recall bound faithfulness) and gives your own measured delta — "fixed→AST-aware moved precision 0.62→0.83 on our golden set; a model upgrade moved faithfulness 0.78→0.84 — chunking won on both cost and quality."

---

# 2.2 Chunking Strategies

## Real-world problem: the legal-docs assistant that answers with half a clause

A legal-tech startup, "ClauseCheck", reviews supplier contracts. v1 uses naive fixed-size chunking at 512 characters. The support queue fills up: the assistant tells users "termination requires 30 days notice" — but the clause actually continues "unless the parties agree otherwise in writing, in which case notice may be given orally". The chunk boundary cut mid-sentence, the LLM faithfully answered from a truncated clause, and the citation pointed at a real paragraph that didn't say what the answer claimed. Legal review is non-negotiable: **the chunk must never split a contractual unit**, and you must prove your chunker keeps clauses, definitions, and signatures intact — measured, not asserted.

Your job: evaluate the four chunking strategies (§2.2a–d), understand exactly what each one preserves and destroys, and choose per corpus type with numbers. The infinite-loop bug and separator quirks you will find in the repo are real: fixing them IS the work.

---

### Topic — Fixed-Size Chunking with Overlap, Word-Boundary Handling

**Mastery =** you can predict chunk boundaries for any (content, size, overlap) triple, you know the word-boundary and tail-stall failure modes, and you can fix them without breaking determinism.

**Level 1 — Drill** (mechanics, 20–45 min)

Part 1 — predictable behavior. Run the real class:

```python
import sys

sys.path.insert(0, r"projects/04-ai-engineering/devmate/src")
from devmate.ingest.chunker import FixedSizeChunker

content = "word " * 60  # 300 chars
docs = FixedSizeChunker(chunk_size=50, overlap=0).chunk(content, {"source": "t.txt"})
print(len(docs), [len(d.content) for d in docs])
```

Expected (verified): `7` chunks, lengths `[49, 45, 45, 45, 45, 45, 26]`. Trace it: the first cut lands at index 49 (last space before 50 — the boundary is exclusive); every subsequent cut is 45 chars (space at `end-1`); the tail is 26 chars. Explain why the first chunk is 49 not 50.

Part 2 — bug hunt (verified 2026-08-11). `FixedSizeChunker(chunk_size=10, overlap=5).chunk("word " * 60, …)` **never returns**: when a chunk's length equals the overlap, `start = end - overlap` stops advancing and the `while start < len(content)` loop stalls forever. Reproduce it with a watchdog (run the chunker in a subprocess, kill after 3 s), then:

1. Find the exact loop in `src/devmate/ingest/chunker.py` (the `start = end - overlap` line).
2. Fix it with a progress guarantee, e.g. `if end >= len(content): break` after emitting the final chunk, or `start = max(start + 1, end - overlap)`.
3. Assert the fix: `(chunk_size=10, overlap=5)` on the same content returns 60 chunks; `(50, 0)` still returns 7; and the repo's own test input `(100, 10)` on `"word " * 200` terminates with `len(docs) == 12` (chunks advance 85 chars/step after the first — verified by simulation).

Part 3 — word-boundary limits. A 200-char word in a 50-char chunker: `rfind(" ")` returns -1 → the cut stays mid-word. Assert that `FixedSizeChunker(chunk_size=50, overlap=0).chunk("a" * 200, …)` returns 4 chunks of 50 and explain why the word-boundary guard cannot help. Related edge: a chunk boundary splitting mid-signature (e.g., `def create_u` | `ser(api_key)` — no spaces near the cut) produces retrievable fragments that match neither query intent nor the function name; say which strategy fixes this (AST-aware, §2.2d) and which does not.

**Level 2 — Applied** (DevMate, 1–3 h)

You just found that `make test` hangs: `devmate/tests/unit/test_chunker.py::test_fixed_size_chunker_creates_chunks_with_metadata` uses `(100, 10)` on `"word " * 200` — the exact stalled input (verified: the loop repeats `(990, 1000)` forever). Deliverables:

1. Fix the loop in `src/devmate/ingest/chunker.py`.
2. Extend `devmate/tests/unit/test_chunker.py` with `test_fixed_size_chunker_progresses_when_tail_le_overlap` (the (10,5) case) and `test_fixed_size_chunker_repo_input_terminates` (the (100,10) case asserting `len(docs) == 12`), and keep all existing tests green.
3. `cd projects/04-ai-engineering/devmate && poetry run pytest -q tests/unit/test_chunker.py` → **all pass, no hang** (run it with a 60 s timeout to prove it).
4. Log the bug + fix in `projects/04-ai-engineering/devmate/mistakes.md` (symptom → root cause → fix).
5. **Acceptance criteria:** `make test` completes (this was previously impossible); the new tests fail on the pre-fix code (prove it with `git stash` if you like).

**Level 3 — Stretch** (production-grade, 3–6 h)

Fixed-size is ClauseCheck's current production chunker for *contracts*. Quantify the damage and decide the migration:

- Instrument the fixed chunker over 5 real contracts (or `src/devmate/` docs): count chunks that (a) start or end mid-sentence, (b) split a numbered clause ("5.1 … 5.2"), (c) split a signature/DOI-style token.
- Write the migration decision as an ADR-style document: keep fixed (cost zero, recall 0.58 measured) vs. migrate (one sprint, recall 0.68+ measured) — with a results table from your own runs. Reference the lecture numbers (Fixed 0.62/0.58/0.78) as the baseline to beat.
- Gates: the mid-sentence split rate is measured per corpus; the ADR states a numeric migration trigger (e.g., "migrate when mid-sentence split rate > 15%").

**Verify:** pytest output shows the new + existing tests passing in < 5 s; the ADR includes the split-rate table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| `make test` never finishes | Tail chunk ≤ overlap stalls the loop | Progress guarantee (`end >= len(content)` break) |
| Chunks split mid-sentence | Word-boundary guard only handles spaces, not punctuation | Use sentence-aware separators or recursive splitting |
| Overlap duplicates sentences into two chunks | Overlap > sentence length | Keep overlap < 15% of chunk size |
| One chunk contains half a function signature | Fixed windows don't know code | Route code files to the AST chunker (§2.2d) |

**Interview:** *"When would you still choose fixed-size chunking in production?"* Strong answer: prototyping, uniform logs/metrics, embedding-cost sensitivity, and exact-character guarantees (e.g., redaction); lists the three cons (mid-sentence cuts, context loss, no structural awareness) and when you'd move off it (measured recall below target on the golden set).

---

### Topic — Recursive Text Splitting (Separator Hierarchy, Uneven Chunks)

**Mastery =** you can predict the output of the separator cascade on any text, you know this repo's implementation descends the *full* hierarchy (a deviation from LangChain), and you can decide when that matters.

**Level 1 — Drill** (mechanics, 20–45 min)

Trace the hierarchy `["\n\n", "\n", ". ", " ", ""]` by hand on this text (chunk_size=64):

```
Paragraph one with enough words to be its own chunk.

Paragraph two, also long enough to stand alone.

Paragraph three, short.
```

Step 1: split on `\n\n` → 3 pieces, all ≤ 64. LangChain semantics would **return** them (3 chunks). This repo's `RecursiveChunker._split_text` instead recurses with the *next* separator even when everything fits, descending all the way to `""` (character level). Verify the real behavior:

```python
from devmate.ingest.chunker import RecursiveChunker

p1 = "Paragraph one with enough words to be its own chunk."
p2 = "Paragraph two, also long enough to stand alone."
p3 = "Paragraph three, short."
text = p1 + "\n\n" + p2 + "\n\n" + p3
docs = RecursiveChunker(chunk_size=64, overlap=0).chunk(text, {"source": "doc.md"})
print(len(docs), [len(d.content) for d in docs])
```

Expected (verified): **2 chunks of 63 and 62 chars** — the cascade reached character-level splitting. Now run the CRLF variant: `text.replace("\n", "\r\n")` → **3 chunks** (boundaries change!). Write asserts for both; explain in one paragraph why Windows line endings change chunk boundaries and what that means for a golden set built on one OS and evaluated on another (`DocumentLoader` reads with `utf-8` — no newline normalization).

**Level 2 — Applied** (DevMate, 1–3 h)

Decide and document the separator behavior:

1. Add tests to `devmate/tests/unit/test_chunker.py` capturing the current cascade semantics: `test_recursive_descends_full_separator_list` (the 2-chunk expectation above) and `test_recursive_crlf_boundary_shift`.
2. Compare against LangChain's `RecursiveCharacterTextSplitter` on the same text (if available; otherwise against the lecture's pseudocode, which returns early when all pieces fit).
3. **Deliverable:** `evaluations/rag/reports/recursive-behavior-<date>.md`: the trace table (separator level → pieces → outcome) + your recommendation: keep the repo behavior (uniform max chunk size, predictable token budgets) or return early (paragraph-preserving). The recommendation must pick one and name the metric it optimizes (recall vs. token uniformity).
4. **Acceptance criteria:** new tests pass; the report shows the exact 2-chunk and 3-chunk outputs; a sentence states the CRLF/LF drift risk in evaluation.

**Level 3 — Stretch** (production-grade, 3–6 h)

ClauseCheck contracts are dominated by numbered clauses — `\n\n` and `. ` both fail to keep "5.1 Termination. Either party…" intact. Design and validate a **separator hierarchy for legal text** (per-corpus separator sets, or a clause-boundary detector). Requirements:

- Evaluate on 3 corpus types (legal, markdown docs, code-adjacent prose) with 10 golden questions each; report recall@5 per corpus × separator set.
- Handle the uneven-chunk problem: greedy merge of tiny pieces (< 20% of chunk_size) — implement and measure whether it helps recall.
- **Write an ADR-style justification**: per-corpus separator sets (config-driven) vs. one global hierarchy. Gates: recall@5 on the legal corpus ≥ 0.75 (from the ~0.58 fixed baseline); no chunk > 1.5× chunk_size in the output.
- Edge cases: all-caps headings, bullet lists (`. ` never fires inside them), tables, and a clause that is itself > chunk_size (must split on its own sub-sections).

**Verify:** the comparison table shows per-corpus recall; the ADR cites it.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Chunks all ~exactly chunk_size on prose | Cascade descends to character level | Return early when all pieces fit (LangChain semantics) — documented decision |
| Same eval, different results on Windows vs CI | CRLF/LF boundary drift | Normalize newlines at ingestion; note in eval README |
| Tiny orphan chunks ("short.") | Aggressive splits | Greedy merge pass under 20% size |
| Lists split into single bullets | `. ` fires inside "1. item" | Add list-aware separators or guard regex |

**Interview:** *"Explain how recursive splitting works and one trap you found in practice."* Strong answer: separator hierarchy from coarse to fine; the trap should be specific — e.g., "our implementation descended the full hierarchy even when pieces fit, so prose became character-level chunks; we proved it with a test and chose early-return semantics; we also hit CRLF boundary drift between Windows and CI."

---

### Topic — Semantic Chunking (Sentence Embeddings, Similarity Threshold, Indexing Cost)

**Mastery =** you can implement the sentence-grouping algorithm, hand-compute the threshold decision, quantify the extra embedding cost at index time, and argue when the cost is worth it.

**Level 1 — Drill** (mechanics, 20–45 min)

Hand-compute the grouping. Sentences with 2-d vectors (your own toy embedder):

| Sentence | Vector |
|---|---|
| s1 "Open a new account." | [1, 0] |
| s2 "The account application form." | [0.6, 0.8] |
| s3 "Submit the form online." | [0, 1] |
| s4 "Refunds are processed within 30 days." | [-1, 0] |

Algorithm (lecture §2.2): start `current = [s1]`; for each next sentence, `cos(v_i, v_last)`; if `sim >= 0.7` append, else start a new chunk. Compute (verified): `cos(s1,s2) = 0.6`, `cos(s2,s3) = 0.8`, `cos(s3,s4) = 0.0`. Expected output: **3 chunks** — `[s1]`, `[s2, s3]`, `[s4]`. Now rerun with threshold 0.5 → 2 chunks (`[s1,s2,s3]`, `[s4]`); threshold 0.9 → 4 chunks. Write asserts for all three thresholds.

Cost drill: indexing a 10,000-sentence document needs ~10,000 sentence-embedding calls **plus** one embedding per final chunk (~800) — vs. fixed-size which embeds only the ~800 chunks. Compute the extra API calls and cost at `text-embedding-3-small` ($0.02/1M tokens, ~20 tokens/sentence): `10,000 × 20 × $0.02/1M ≈ $0.004` extra per document — cheap for one contract corpus, but × 50,000 documents = $200 — and note the *latency* cost: 10k embedding calls dominate index wall-time. Assert the arithmetic.

**Level 2 — Applied** (DevMate, 1–3 h)

The track plans a `chunkers/` package (`devmate/src/devmate/ingest/chunkers/`); semantic chunking is not yet in the repo. Implement it:

1. `projects/04-ai-engineering/devmate/src/devmate/ingest/chunkers/semantic.py` — `SemanticChunker(BaseChunker)` with `threshold` (default 0.7), sentence splitting (regex on `. ` + newline, keep it simple), embedding via `EmbeddingService` (`src/devmate/index/embeddings.py`), grouping per the lecture algorithm, metadata `chunker="semantic"`, source fields preserved.
2. Register it in the `CHUNKERS` dict / `get_chunker()` in `src/devmate/ingest/chunker.py` (or move the registry into the package — your call, documented).
3. Tests in `devmate/tests/unit/test_semantic_chunker.py` with a **fake embedder** (no network!): a `FakeEmbedder` returning the toy vectors above; assert 3 chunks at 0.7, 2 at 0.5, 4 at 0.9, and that empty text → `[]`.
4. **Deliverable:** the module + tests + one line in `evaluations/rag/reports/` noting the design (or the chunker-comparison report extended with a semantic row, if you have a real embedder and budget).
5. **Acceptance criteria:** `poetry run pytest -q tests/unit/test_semantic_chunker.py` passes offline; `get_chunker("semantic")` returns your class.

**Level 3 — Stretch** (production-grade, 3–6 h)

ClauseCheck wants semantic chunking for contracts, but index cost and threshold sensitivity are the concerns. Run the real experiment:

- Sweep `threshold ∈ {0.5, 0.6, 0.7, 0.8, 0.9}` on a real corpus slice (ingest `src/devmate/` docs + one contract-like doc you write); measure chunk count, avg chunk size, indexing wall-time (embedding calls dominate), and recall@5 on 10 golden questions.
- Find the knee: quality vs. indexing time. Decide the default threshold and the per-corpus override.
- **Write an ADR-style justification** (candidate for the track's second ADR): semantic vs. recursive for the docs corpus. Include the cost table (embedding calls per 10k sentences), latency table, recall table.
- Gates: the ADR cites measured numbers from the sweep; a cost ceiling is stated (e.g., "semantic indexing must stay under 3× recursive indexing wall-time"); revisit conditions (embedding price changes, new languages).

**Verify:** the sweep table is in the ADR/report; the chosen threshold is defended by the knee-plot data.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Semantic chunker hits the network in unit tests | No fake embedder | Inject an embedder; keep unit tests offline |
| Every sentence becomes its own chunk | Threshold too high (0.9) | Sweep; start at 0.7 |
| Giant merged chunks | Threshold too low | Merge guard: hard cap chunk_size |
| Indexing takes hours | Serial per-sentence embedding | Batch embedding (settings `embedding_batch_size=100`) |

**Interview:** *"When is semantic chunking worth its indexing cost?"* Strong answer: when chunk boundaries must follow meaning (prose, contracts, regulations) and recall is the binding constraint; quantifies cost ("10k sentences ≈ 10k extra embedding calls per doc — $0.004 at small-model prices"); says where it's not worth it (code, logs, uniform records) — those go to AST or fixed.

---

### Topic — AST-Aware Chunking for Code (Functions/Classes, Line Ranges, Syntax-Error Fallback)

**Mastery =** you can explain why code must not be chunked like prose, implement the Python AST path and the JS/TS fallback, and prove the fallback never crashes on broken files.

**Level 1 — Drill** (mechanics, 20–45 min)

Run the real class on this file:

```python
import sys

sys.path.insert(0, r"projects/04-ai-engineering/devmate/src")
from devmate.ingest.chunker import ASTAwareChunker

code = """import os


def first():
    return 1


def second():
    return 2


class Thing:
    def method(self):
        return 3
"""
docs = ASTAwareChunker(chunk_size=4096, overlap=0).chunk(
    code, {"source": "x.py", "language": "python"}
)
for d in docs:
    m = d.metadata
    print(
        m.get("name"),
        m.get("chunk_type"),
        "lines",
        m.get("start_line"),
        "-",
        m.get("end_line"),
    )
```

Expected (verified): `first function 4–5`, `second function 8–9`, `Thing class 12–14`, and **also** `method function 13–14` (note: `ast.walk` visits nested functions too — methods become their own chunks *and* sit inside the class chunk; decide whether that duplication is desirable). Edge cases to assert: `chunk("def broken(:", …)` → **falls back to recursive** (`chunker == "recursive"` in metadata, no exception — the `except SyntaxError` path in `_chunk_python`); a 3000-line function with `chunk_size=512` is **skipped** by the `len(chunk_content) > chunk_size * 4` guard (2048 chars default) and the file falls back to recursive (verified: 65 recursive chunks, no `chunk_type` metadata); whitespace-only files → `[]`.

**Level 2 — Applied** (DevMate, 1–3 h)

Harden and prove the real implementation:

1. Chunk DevMate's own `src/devmate/ingest/chunker.py` with `ASTAwareChunker`; print the chunk table (name, type, lines) and assert: every `FunctionDef`/`ClassDef` in the module appears by name; `start_line ≤ end_line` for every chunk; no chunk exceeds `chunk_size * 4` chars.
2. Add regression tests to `devmate/tests/unit/test_chunker.py`: syntax-error fallback (exists — extend it), huge-function skip, nested-method chunking, JS/TS path (`language="javascript"` with a function + class sample → chunks exist with `chunk_type` set).
3. Verify line-range correctness against `ast` directly: for a sample file, assert the chunk content equals `"\n".join(lines[start-1:end])` from the original source.
4. **Deliverable:** updated test file + `evaluations/rag/reports/ast-coverage-<date>.md` (the chunk table for `chunker.py` + counts per `chunk_type`).
5. **Acceptance criteria:** `poetry run pytest -q tests/unit/test_chunker.py` green; report shows `function: N, class: M` for the real module.

**Level 3 — Stretch** (production-grade, 3–6 h)

Multi-language + broken-code reality. DevMate supports ~25 extensions (`DocumentLoader.SUPPORTED_EXTENSIONS`), but AST-aware only handles Python (real `ast`) and JS/TS (regex + brace counting — `_extract_balanced_block` tracks strings, but test it against template literals containing `{`). Scope:

- Stress the JS/TS path: arrow functions, nested template literals, destructuring with braces, comments containing braces. Find the cases that produce wrong blocks; quantify the error rate.
- Evaluate tree-sitter (or language-specific parsers) for the top 5 languages in `SUPPORTED_EXTENSIONS` vs. the current fallback-to-recursive. Metric: retrieval recall@5 on 10 questions per language using a golden set over `src/devmate/` (Python) and one JS/TS repo if available.
- **Write an ADR-style justification:** tree-sitter per language vs. regex/ast hybrid vs. fallback-to-recursive. Include the error-rate table and recall table; name the languages that justify parser investment.
- Gates: no exception escapes the chunker on a full-corpus run (syntax errors included); per-language recall reported; the ADR's Consequences section is non-empty.

**Verify:** the stress test prints the failure inventory; the ADR cites per-language recall.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Chunker crashes on minified/broken JS | Regex assumes balanced braces | Always fall back; never raise (`try/except` + fallback) |
| Huge functions silently vanish | `chunk_size * 4` skip guard drops them | Measure how many chunks are lost per repo; split inside the function instead |
| Duplicated code in chunks | `ast.walk` visits methods inside classes | Decide: class-level vs member-level chunks; filter `node in tree.body` for top-level only |
| Wrong line ranges | `end_lineno` missing on old Python | `getattr(node, 'end_lineno', node.lineno)` — already in code; test it |

**Interview:** *"Why does AST-aware chunking beat fixed-size on code, specifically?"* Strong answer: retrieval units become semantic units (a function is what a question targets); embeddings of a whole function preserve name + signature + docstring together; citations point at exact line ranges; the fallback path guarantees robustness; and the measured proof: 0.83/0.79 vs 0.62/0.58 precision/recall on the golden set, with faithfulness 0.91 vs 0.78.

---

# 2.3 Vector Database: Qdrant

## Real-world problem: 10 million documents and a RAM bill

A data-platform company, "IndexCo", runs a document search service. Their vector DB keeps everything in RAM: 10M vectors × 1536 dims × 4 bytes = ~57 GB, plus the HNSW graph overhead (m=16 adds ~15–25% memory) — a multi-thousand-dollar-per-month dedicated instance, and it still thrashes at p99. Meanwhile a separate pilot for a *tiny* 5,000-chunk repo is mysteriously slow too. The CTO asks for: on-disk storage when it pays, HNSW parameters that meet a p95 < 100 ms budget, payload filtering that doesn't scan everything, and a collection config you can justify in review. ADR-0005 already chose Qdrant over Chroma (`docs/decisions/0005-vector-db-qdrant-over-chromadb.md` — it also mandates the comparison report in `evaluations/rag/reports/`); now you must configure it correctly.

---

### Topic — Collection Configuration (vector size, distance, on_disk, optimizers, indexing_threshold)

**Mastery =** you can write a justified `create_collection` call for any corpus size, compute the memory math, and explain when `on_disk` and `indexing_threshold` flip the cost/quality trade.

**Level 1 — Drill** (mechanics, 20–45 min)

Memory math (pure Python, no Qdrant needed):

- 1536 dims, float32 → `1536 × 4 = 6,144 B/vector ≈ 6 KB`. 10M vectors in RAM = `10,000,000 × 6,144 / 2^30 ≈ 57.2 GB`.
- HNSW `m=16`: each node stores ~m neighbor refs ≈ ~2 KB extra per vector → +20 GB. Total ~77 GB in RAM.
- With `on_disk=True`: RAM holds only the hot graph + memmap'd vectors. Compute RAM ≈ graph only (~20 GB) and state the trade: slower random access on cold vectors (SSD ~50–100 µs vs RAM ~100 ns) but ~4× less RAM.

Then read `VectorStoreConfig` in `src/devmate/index/vector_store.py` and `settings` in `src/devmate/config.py`; write the current defaults from code: `collection="devmate_code"`, `vector_size=1536`, `distance="cosine"`, `on_disk=True`, `hnsw_m=16`, `hnsw_ef_construct=100`. Explain why cosine fits normalized embeddings and what `dot` changes (raw dot product, no normalization). Assert that `_create_collection` maps all three distances (`models.Distance.COSINE / DOT / EUCLID`).

`indexing_threshold` drill: Qdrant switches from exact scan to HNSW once a segment exceeds `indexing_threshold` (lecture default 20,000). Below it, queries are exact — so a tiny 5,000-chunk repo is *always exact* (this is why the pilot feels "slow-looking" but exact: small segments get rebuilt). State in one sentence when you'd raise it (hot small collections, exactness matters) and when you'd lower it (large collection, want HNSW early).

**Level 2 — Applied** (DevMate, 1–3 h)

Configure DevMate's real collection:

1. `make up` (Qdrant on `localhost:6333`, image `qdrant/qdrant:v1.8.0`, healthcheck on `/health`).
2. Write `projects/04-ai-engineering/devmate/scripts/configure_collection.py` that connects via `QdrantVectorStore` (or `QdrantClient` directly) and prints: collection list, the `devmate_code` collection's `vectors` config (size, distance, on_disk), `optimizers_config.indexing_threshold`, `hnsw_config` (m, ef_construct). Create the collection if missing using `VectorStoreConfig`.
3. Verify against the server: `curl -s http://localhost:6333/collections/devmate_code` — expected JSON contains `"status": "green"` and a `"config"` with `"params"` size 1536, distance Cosine.
4. **Deliverable:** the script + a 10-line note in `evaluations/rag/reports/` recording the config you chose and why (corpus size now ~2–5k chunks → justify `indexing_threshold` and `on_disk` for *this* scale, not IndexCo's).
5. **Acceptance criteria:** script and curl agree; `make ps` shows `devmate-qdrant` healthy.

**Level 3 — Stretch** (production-grade, 3–6 h)

IndexCo-scale decision with an A/B:

- Generate or collect ≥ 500k vectors (synthetic embeddings of DevMate chunks are fine — the point is scale behavior) into two collections: `devmate_ram` (`on_disk=False`) and `devmate_disk` (`on_disk=True`), identical otherwise.
- Measure: memory (`docker stats devmate-qdrant`), ingest wall-time, p50/p95 query latency on 1,000 queries, recall@10 vs exact scan (temporarily raise `full_scan_threshold` to force exactness).
- **Write an ADR-style justification** (extends ADR-0005's comparison dimensions — retrieval quality, latency, ingest, ops — with the on-disk dimension): in-RAM vs. on-disk vs. hybrid (hot collection in RAM, cold on disk). Include the measured table; state the memory ceiling per instance and the latency gate (p95 < 100 ms).
- Gates: recall@10 delta between modes reported; the ADR's Consequences covers cost, ops, and failure behavior (disk slowdown vs OOM).

**Verify:** `docker stats` shows the RAM delta; the ADR table has both modes' numbers; the report is linked from `evaluations/rag/README.md`.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| OOM during ingest | Vectors + graph in RAM at scale | `on_disk=True`; watch `docker stats` |
| "My 5k-repo search is slow" | `indexing_threshold` rebuild churn on tiny segments | Batch upserts; lower threshold; measure with `full_scan_threshold` |
| Similarity scores all ~0 | Cosine vs dot mismatch after normalization | Pick one convention; cosine for normalized embeddings |
| Collection config immutable after create | Qdrant locks vectors params | Create once with the right config; use `update_collection` only for HNSW/optimizers diffs |

**Interview:** *"How would you configure Qdrant for a 10M-vector collection?"* Strong answer: vector size from the embedding model, distance matching training (cosine), `on_disk=True` at that scale, `indexing_threshold` rationale (exactness below, HNSW above), payload indexes for filters, and measured HNSW params from a sweep — plus the memory math (6 KB/vector × 10M ≈ 57 GB before graph overhead).

---

### Topic — HNSW Parameters (m, ef_construct, ef_search, full_scan_threshold)

**Mastery =** you can state each parameter's effect on recall/memory/latency, run a sweep that picks values for a latency budget, and explain `full_scan_threshold` behavior on tiny collections.

**Level 1 — Drill** (mechanics, 20–45 min)

Trade-off table drill — complete each row with direction and effect:

| Param | ↑ value → recall | ↑ value → latency | ↑ value → memory |
|---|---|---|---|
| `m` | ↑ (denser graph) | ↑ slightly (more hops) | ↑ (more edges) |
| `ef_construct` | ↑ index quality | ↑ slower *build* | ↑ build memory |
| `ef_search` | ↑ strongly | ↑ slower *queries* | ≈ none |
| `full_scan_threshold` | ↑ exactness below threshold | ↑ exact scans on small sets | — |

Compute the sweep expectation: with N=100k vectors, `m=16, ef_construct=100`, doubling `ef_search` from 32→64→128 costs roughly linear query time; a rule of thumb: recall@10 saturates around `ef_search ≈ 3× top_k` for uniform data (so for top_k=20, start at 64). Write a tiny simulation (or reason it out) showing that `full_scan_threshold=10000` ⇒ any collection with ≤ 10k vectors is searched exactly — and that on DevMate (~2–5k chunks) HNSW *never* activates by default; queries are exact scans. State the practical consequence for the Level 2 sweep: you must lower the threshold or grow the corpus to exercise HNSW.

**Level 2 — Applied** (DevMate, 1–3 h)

Run a real HNSW sweep:

1. Ingest DevMate `src/` (≥ 1,500 chunks; recursive chunker) into `devmate_code`.
2. `poetry run python scripts/hnsw_sweep.py` (write it): for `ef_search ∈ {16, 64, 128, 256}` — set via `client.update_collection(hnsw_config=…)` — run 50 queries, record p50/p95 latency and recall@10 (relevant = 10 hand-labeled nearest chunks per query, or compare against exact-search results with a temporarily high `full_scan_threshold`).
3. **Deliverable:** `evaluations/rag/reports/hnsw-tuning-<date>.md` with the 4-row table (ef_search, recall@10, p50, p95) and a chosen default with justification.
4. **Acceptance criteria:** the table has real numbers; the chosen `ef_search` meets the < 100 ms retrieval budget at p95 while keeping recall@10 ≥ 0.95 of the max observed; the sweep script is committed.

**Level 3 — Stretch** (production-grade, 3–6 h)

IndexCo autotuning under a strict budget:

- Fix the budget: p95 retrieval ≤ 100 ms at 10M vectors, recall@10 ≥ 0.95 relative to exact. Sweep `m ∈ {8, 16, 32, 64}` × `ef_search ∈ {32, 64, 128, 256, 512}` (at 500k synthetic vectors to keep the run tractable) and produce a Pareto table (recall vs p95) plus a memory column estimated from `docker stats`.
- Handle the cold-start/tiny-collection edge: define the `full_scan_threshold` policy so small pilot repos (5k chunks) get exact search, and large ones don't accidentally exact-scan (threshold below expected segment size).
- **Write an ADR-style justification:** the chosen `(m, ef_construct, ef_search, full_scan_threshold, indexing_threshold)` tuple with the Pareto evidence; revisit conditions (data distribution shifts, SSD vs NVMe, RAM price changes).
- Gates: the chosen tuple appears in the ADR with a measured table; the ADR states what p95/recall you gave up and why.

**Verify:** `poetry run pytest -q` still green; ADR table complete; sweep artifacts in `evaluations/rag/reports/`.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Sweep shows no change in recall | Corpus under `full_scan_threshold` (exact anyway) | Lower threshold or grow the corpus before sweeping |
| Recall fine but p95 blows budget | `ef_search` too high / graph too dense | Bisect ef_search; try m=16 first |
| Ingest much slower after tuning | `ef_construct` raised globally | Keep build-time params low; raise `ef_search` only |
| "HNSW not used" behavior | Segments below `indexing_threshold` | Batch upserts to exceed the threshold per segment |

**Interview:** *"Explain HNSW parameters and how you'd tune them."* Strong answer: m (graph degree, memory), ef_construct (build quality), ef_search (query-time beam), full_scan_threshold (exact below N); method = sweep on a real corpus against a latency budget, with recall relative to exact search; mentions the tiny-corpus trap where HNSW never engages.

---

### Topic — Payload Indexes & Filters (language, filename, chunk_type, repo_name)

**Mastery =** you can design payload fields and keyword indexes so that every production filter hits an index, and you can write filter conditions without scanning.

**Level 1 — Drill** (mechanics, 20–45 min)

Write Qdrant `models.Filter` payloads by hand for these queries (no server needed — construct the dicts):

1. `language == "python"` → `{"must": [{"key": "language", "match": {"value": "python"}}]}`
2. `chunk_type == "function" AND repo_name == "devmate"` → two `must` conditions
3. `filename == "chunker.py" OR filename == "retriever.py"` → a `should` with two matches and `minimum_should_match=1`
4. `language == "go"` AND `size_bytes > 5000` → match + `range` condition

Assert each dict is a valid `models.Filter` by importing it: `from qdrant_client import models; models.Filter(**payload)`. Then answer: which of these fields are in the lecture's recommended index list (`language, filename, chunk_type, repo_name`), and what happens to filter latency if `filename` is *not* indexed (Qdrant falls back to a payload scan — fine at 5k chunks, deadly at 10M). State the rule: **any field used in production filters gets a keyword payload index.**

**Level 2 — Applied** (DevMate, 1–3 h)

Index and filter DevMate data:

1. Ingest `src/devmate/` with the AST chunker (so `chunk_type` and `name` exist) into `devmate_code`.
2. Create payload indexes for `language, filename, chunk_type, repo_name` (mirror the lecture's loop using `client.create_payload_index(collection_name, field_name, field_schema="keyword")`); verify with `curl -s http://localhost:6333/collections/devmate_code/indexes`.
3. Integration test `devmate/tests/integration/test_vector_store.py` (mark `@pytest.mark.integration`; needs `make up`): search with filter `{"language": "python", "chunk_type": "function"}` → assert every returned chunk has those payload values; count filtered vs unfiltered results (`make test-int` runs it).
4. **Deliverable:** the integration test + a filter-query snippet in `evaluations/rag/reports/`.
5. **Acceptance criteria:** `make test-int` passes with Qdrant up; the filtered result count is smaller than unfiltered for the same vector; the indexes endpoint lists all four fields.

**Level 3 — Stretch** (production-grade, 3–6 h)

Multi-tenancy + security. DevMate will serve many repos (tenants); filters become a **security boundary**:

- Design: `repo_name` as the tenant key; every query *must* carry it; document the failure mode if a filter is omitted (cross-tenant leakage — you retrieve everything).
- Implement a `require_filter` guard in the retriever (`src/devmate/retrieve/retriever.py`): if the caller's tenant filter is missing, return an error, not results. Add tests proving a missing `repo_name` filter cannot leak data, and that keyword indexes on `repo_name` keep per-tenant queries at p95 < 100 ms.
- Scale check: 200 tenants × 50k chunks; verify per-tenant filters still hit indexes (no scans) — use `scroll` + `count` to prove filter selectivity.
- **Write an ADR-style justification:** tenant-key-as-filter vs. per-tenant collections vs. per-tenant Qdrant instances. Include a cost table (collection count × payload overhead) and the security argument. Gates: the leak test fails without the guard, passes with it; per-tenant p95 measured.

**Verify:** `make test-int` green including the leak test; ADR with the three-options table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Filters work but are slow at scale | Unindexed payload field → full scan | `create_payload_index` for every filtered field |
| Filter returns wrong-language chunks | `language` metadata missing at ingest | Set language in loader metadata; test it |
| Cross-tenant results in staging | Filter optional in the API path | Make the tenant filter required; test the missing-filter case |
| Indexes not applied to new segments | Payload index created after upserts | Create indexes before bulk ingest |

**Interview:** *"How do you design payload schemas and indexes for a multi-repo RAG store?"* Strong answer: fields mirror retrieval needs (language, filename, chunk_type, repo_name, line ranges), keyword indexes on every filtered field, tenant key required at query time (security boundary), filters combined with vector search server-side (no client-side merge), and a selectivity test proving no scan.

---

# 2.4 Hybrid Search: Semantic + Keyword

## Real-world problem: the code-search product that can't find "QDR-2024"

A developer-tools company builds "CodeFind", semantic search over 200 GitHub repos. Users complain: searching `QDR-2024` (a ticket id), `UserService` (a class name), or `OAuth2` (a protocol) returns "related concepts" but never the exact file. The embedding model doesn't know these tokens — it embeds meaning, and "QDR-2024" has no meaning. Meanwhile, a colleague's keyword prototype finds the exact tokens but misses paraphrases ("refund" vs "money back"). The decision: **hybrid retrieval** — two rankers, one fused list — and you must implement the fusion, tune its `k`, and prove recall beats either single system. (ADR-0005 noted Qdrant's native sparse-vector support as a reason it was chosen; you are now exercising that.)

---

### Topic — Why Hybrid: Semantic Misses Exact Tokens, Keyword Misses Synonyms

**Mastery =** you can name the two failure classes with concrete examples, construct a query matrix that exposes both, and explain why neither single system can fix the other's failure.

**Level 1 — Drill** (mechanics, 20–45 min)

Build the failure matrix on a 5-doc toy corpus (pure dicts, no services):

```python
docs = {
    "d1": "Ticket QDR-2024: fix the login redirect bug.",
    "d2": "The UserService class handles user profiles.",
    "d3": "Refunds are processed within 30 days.",
    "d4": "Money back requests go through the billing queue.",
    "d5": "OAuth2 token exchange happens at /token.",
}
semantic_top3 = ["d4", "d3", "d2"]  # fake but plausible for a meaning-embedder
keyword_hits = ["d1", "d5"]  # exact tokens only
```

For query `"QDR-2024"`: semantic misses d1 entirely (recall = 0/1), keyword finds it (1/1). For query `"money back"`: semantic finds d4 (synonym-aware), keyword finds nothing (0/1). Compute recall@5 for each system per query and the union list; assert: hybrid recall ≥ max(semantic, keyword) on every query in your matrix. Then write 10 real queries for DevMate's own corpus that stress each class: exact tokens (`FixedSizeChunker`, `QdrantVectorStore`, `COHERE_API_KEY`, `semantic_cache_threshold`) and paraphrases ("how do I break text into pieces" vs "chunking", "where is the vector database code" vs "vector_store.py").

**Level 2 — Applied** (DevMate, 1–3 h)

Measure the gap on the real system:

1. Ensure §2.3c is done (indexed `devmate_code` with payload indexes).
2. `poetry run python scripts/hybrid_query_matrix.py`: run your 10-query matrix twice — semantic-only (`vector_store.search`) and keyword-only (payload `MatchText` on `content` via `scroll`, as the lecture's `_keyword_search` does) — record recall@5 (your labels) per query.
3. **Deliverable:** `evaluations/rag/reports/hybrid-motivation-<date>.md`: the matrix table (query | semantic r@5 | keyword r@5 | winner) + a count of "semantic wins / keyword wins / tie".
4. **Acceptance criteria:** the report shows ≥ 2 queries where each single system scores 0 and the other scores 1 — the existence proof for hybrid. If your corpus doesn't produce a miss, add queries with rarer identifiers (`get_chunker`, `_split_text`, `QDRANT_COLLECTION`).

**Level 3 — Stretch** (production-grade, 3–6 h)

Design the production hybrid with **sparse vectors** — Qdrant's native BM25-style sparse search (the ADR-0005 reason for Qdrant):

- Implement a sparse vector per chunk (`models.SparseVector` with `indices`/`values` from a BM25-style tokenizer, or Qdrant's built-in sparse/Bm25 options if available in the client version) alongside the dense vector — Qdrant supports multi-vector points.
- Compare on the 10-query matrix: dense-only, sparse-only, Qdrant-side hybrid (e.g., `prefetch`-based multi-vector query) vs. client-side RRF merge (your §2.4b implementation). Metrics: recall@5, latency p50/p95, ingest overhead.
- **Write an ADR-style justification**: native multi-vector hybrid vs. external BM25 (e.g., Tantivy) merged client-side vs. payload-MatchText keyword (current). Gates: hybrid recall@5 ≥ max(single) on every matrix query; p95 added latency ≤ 50 ms; ingest-time delta reported.

**Verify:** the comparison table lives in `evaluations/rag/reports/`; the ADR names the winner and the revisit conditions.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Semantic-only misses tickets/ids | Tokens unknown to the embedder | Add the keyword arm; index identifiers explicitly |
| Keyword-only misses paraphrases | Lexical mismatch | Add the semantic arm — never choose one arm |
| Hybrid returns duplicates | Same chunk in both rank lists | Dedupe by chunk id at fusion |
| Matrix has no misses | Queries too easy | Use exact identifiers + cross-cutting paraphrases |

**Interview:** *"Why can't one retriever do everything?"* Strong answer: embeddings are lossy for rare/exact tokens (QDR-2024, class names, ticket ids) and lexical search is blind to paraphrase; hybrid fuses two orthogonal signals; you prove it with a query matrix showing each system failing where the other wins.

---

### Topic — Reciprocal Rank Fusion (implementation, k sensitivity, combining rank lists)

**Mastery =** you can implement RRF, hand-compute fused scores, explain `k`'s effect on rank dominance, and tune it with measurements.

**Level 1 — Drill** (mechanics, 20–45 min)

Implement and verify by hand. Rank lists (doc ids, best first): semantic `[A, B, C, D, E]`, keyword `[C, A, D, F]`. Fused score for doc `d`: `Σ 1/(k + rank)`, rank starting at 1. Compute for `k=60` (verified): `A = 1/61 + 1/62 = 0.032522`, `C = 1/63 + 1/61 = 0.032266`, `D = 1/64 + 1/63 = 0.031498`, `B = 1/62 = 0.016129`, `F = 1/64 = 0.015625`, `E = 1/65 = 0.015385`. Final order: `A > C > D > B > F > E`; top-5 = `[A, C, D, B, F]`.

```python
def rrf(semantic, keyword, k=60, limit=5):
    scores = {}
    for rank, doc in enumerate(semantic, 1):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
    for rank, doc in enumerate(keyword, 1):
        scores[doc] = scores.get(doc, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)[:limit]


assert rrf(["A", "B", "C", "D", "E"], ["C", "A", "D", "F"], 60, 5) == [
    "A",
    "C",
    "D",
    "B",
    "F",
]
assert rrf(["A", "B", "C", "D", "E"], ["C", "A", "D", "F"], 5, 5) == [
    "A",
    "C",
    "D",
    "B",
    "F",
]
```

k-sensitivity drill (verified): with `k=5`, scores compress — `A = 1/6 + 1/7 = 0.309524`, `C = 1/8 + 1/6 = 0.291667`, `D = 1/9 + 1/8 = 0.236111`, `B = 1/7 = 0.142857`, `F = 1/9 = 0.111111`, `E = 1/10 = 0.1` — order holds but margins change. Explain: small `k` makes top ranks dominate (a rank-10 hit contributes `1/15 ≈ 0.067` vs a rank-1 hit `1/6 ≈ 0.167`); large `k` flattens differences. Note the degenerate case `k → ∞` makes all scores ≈ 0.

**Level 2 — Applied** (DevMate, 1–3 h)

Implement RRF in the real retrieval path:

1. Add `src/devmate/retrieve/rrf.py` with `rrf_fusion(semantic_hits, keyword_hits, k=60, limit=20)` operating on `SearchResult` objects (dedupe by `id`, keep metadata).
2. Unit tests `devmate/tests/unit/test_rrf.py`: the two asserts above + a dedupe test (same doc in both lists appears once) + an empty-arm edge (one arm empty → pure other arm, order preserved).
3. Wire it: extend `Retriever.retrieve` (or add `Retriever.retrieve_hybrid`) in `src/devmate/retrieve/retriever.py` to call semantic search + keyword search (MatchText on `content`) and fuse with `k=settings.rag_rrf_k` (add the setting, default 60).
4. Sweep `k ∈ {5, 30, 60, 100}` on your 10-query matrix (recall@5, MRR); **Deliverable:** `evaluations/rag/reports/rrf-k-sweep-<date>.md` with the 4-row table and a chosen default.
5. **Acceptance criteria:** unit tests green; the sweep table shows the chosen k and its MRR; `make test` still passes.

**Level 3 — Stretch** (production-grade, 3–6 h)

Fusion at production scale — RRF vs. learned/weighted fusion:

- Problem: RRF ignores score *magnitude* (a strong semantic match at rank 3 vs. a weak keyword match at rank 3 are treated identically). Build and compare: (a) RRF (k=60), (b) score-normalized weighted sum `w·norm(sem) + (1−w)·norm(kw)` for w ∈ {0.3, 0.5, 0.7}, (c) RRF with per-arm caps (top-50 from each).
- Metrics on the 25-question golden set: recall@5, recall@10, MRR, and p95 latency of the fused path.
- **Write an ADR-style justification**: RRF vs. weighted-sum vs. capped-RRF; include the parameter table and the failure analysis (which queries each fusion mis-ranks and why). Gates: chosen fusion's MRR ≥ 0.70 (eval README target); no golden-set query regresses more than 1 rank vs. the best single arm.

**Verify:** `poetry run pytest -q tests/unit/test_rrf.py` green; sweep + ADR tables present; `make eval` (once built) uses the chosen fusion.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Fusion order identical regardless of k | Corpus too small / lists too similar | Use queries where arms disagree; check margins, not just order |
| Doc appears twice in output | No dedupe by id | Dedupe before ranking (dict keyed by id) |
| Keyword arm returns thousands | MatchText on whole content too broad | Limit each arm (e.g., 2× final limit); cap in fusion |
| One arm dominates silently | Score scales differ | Use ranks (RRF sidesteps this — say why) |

**Interview:** *"Explain RRF and what k does."* Strong answer: rank-based fusion `Σ 1/(k+rank)` — scale-free, no score normalization needed; k sets how much rank position matters; implementation details (dedupe, 1-based ranks, per-arm caps); tuning method (sweep on the golden set, watch MRR); and the trade-off vs weighted score fusion.

---

# 2.5 Reranking: The Cheap Quality Boost

## Real-world problem: the medical Q&A assistant that must cite correctly

A health-tech startup, "MediAssist", answers patient questions from clinical guidelines. Compliance requires: every answer grounded in retrieved passages, citations that survive audit, and p95 latency under 3 s. Current pipeline: hybrid retrieve top-20, stuff all 20 into the prompt, generate. Problems: (1) the LLM ignores irrelevant chunks and sometimes cites them anyway; (2) prompt cost is high (20 chunks × ~1k tokens); (3) retrieval is recall-optimized but precision is poor — precision@5 of 0.4. The fix: **rerank top-20 → top-5 with a cross-encoder** — but the choice (hosted Cohere API vs. local bge-reranker) has privacy, cost, and latency consequences the CTO will grill you on. §2.5a–c give you the tools; the decision must be measured.

---

### Topic — Bi-Encoder vs Cross-Encoder (architecture, speed, quality, when to use which)

**Mastery =** you can explain the architectural difference, compute the forward-pass economics for any (batch, top_k), and justify the two-stage design.

**Level 1 — Drill** (mechanics, 20–45 min)

Economics drill. First stage: bi-encoder, query embedded once; doc vectors precomputed at index time — forward passes = `1 (query) + 0 (docs, cached)` ≈ 50 ms. Second stage: cross-encoder scores `query ∘ doc_i` jointly — forward passes = `top_k` pairs (no caching possible). Compute for `top_k = 20`: the cross-encoder does 20 pair-encodings; at ~5 ms/pair on GPU → ~100 ms; on CPU → 300–800 ms. Fill the table:

| Aspect | Bi-Encoder (Retrieval) | Cross-Encoder (Reranking) |
|---|---|---|
| Encoding | Query and docs separately | Query+doc pairs jointly |
| Precompute docs? | Yes (index time) | No (query time) |
| Speed at top-20 | ~50 ms | ~100 ms GPU / 300–800 ms CPU |
| Quality | Good recall | Excellent precision |

Then the design drill: given p95 budget 3 s and generation at ~2 s, the headroom is ~1 s for retrieve + rerank → rerank budget ~100–150 ms. Which reranker type fits on CPU? Answer: bi-encoder for stage 1 (recall); cross-encoder for stage 2 only with GPU or small top_k; on CPU, a top-20 local cross-encoder risks the budget — that's exactly the decision MediAssist faces. Write the 3-sentence justification.

**Level 2 — Applied** (DevMate, 1–3 h)

Measure the boost on DevMate (rerank-free vs. rerank):

1. Ingest `src/devmate/` (AST chunker) into `devmate_code`; take 10 golden questions from §2.6a.
2. `poetry run python scripts/rerank_ab.py`: for each question — retrieve top-20, compute precision@5 of raw top-5 vs. after `LocalReranker` (or `NoOpReranker` for the baseline arm) — record latency per arm.
3. **Deliverable:** `evaluations/rag/reports/rerank-ab-<date>.md`: per-question table (raw p@5, reranked p@5, Δlatency) + aggregate mean p@5 and p95.
4. **Acceptance criteria:** the report shows the mean precision@5 delta (expect +0.1–0.3 from the lecture pattern: raw 0.62 → reranked 0.83 in the AST row's neighborhood; your corpus may differ — explain); p95 total stays under 3 s; the reranker arm's added latency is reported per question.

**Level 3 — Stretch** (production-grade, 3–6 h)

The architecture decision MediAssist's CTO forces:

- Evaluate four generator-side configurations on the golden set: no-rerank (20 chunks), cross-encoder top-5, LLM-as-reranker (prompt the generator model to pick the best 5 of 20 — expensive but highest quality), and hybrid (cross-encoder top-10 then LLM pick top-5).
- Metrics: faithfulness, answer_relevancy, citation accuracy, p95 latency, and **cost per query** (tokens × price per model).
- **Write an ADR-style justification**: reranker choice (none/local/cohere/LLM). Include the 4-arm results table and a compliance note on why citations must be re-verified post-generation regardless.
- Gates: chosen arm meets faithfulness ≥ 0.85 and p95 < 3 s; the ADR states the cost ceiling per query and revisit conditions (GPU availability, API price changes).

**Verify:** the 4-arm table is in the report and cited by the ADR; the chosen arm is not "the best quality one" unless it also fits the budget — the write-up must show the trade-off explicitly.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Reranking "does nothing" | Relevance labels too easy / top-20 already perfect | Use harder queries; check precision@5, not recall |
| p95 blows past budget | Cross-encoder on CPU, top_k too high | Reduce to top-10; batch; GPU; or a local quantized model (§2.5c) |
| Reranked order ignores query | Passing the wrong field (doc only, not query∘doc) | Cross-encoder must receive the query; unit-test with a query-swap |
| Cost explosion | Reranking on every query | Rerank only when raw scores are ambiguous (top-20 margin small) |

**Interview:** *"Why rerank, and why a cross-encoder specifically?"* Strong answer: retrieval is recall-optimized; precision comes from a second stage; the cross-encoder sees query+doc jointly so it captures interactions bi-encoders can't; economics (top-20 pairs vs. cached doc vectors); and a measured precision delta from your own A/B.

---

### Topic — Cohere Rerank Integration (API, top_n, mapping results back)

**Mastery =** you can integrate the hosted reranker, map `index` fields back to your documents without mixing them up, and handle API failure gracefully.

**Level 1 — Drill** (mechanics, 20–45 min)

Mapping drill (no network). `CohereReranker.rerank` in `src/devmate/retrieve/retriever.py` sends `documents=[d.content for d in documents]` and receives `results: [{index, relevance_score}, …]`. Given input order `[doc_x, doc_y, doc_z]` and response `[{"index": 2, "relevance_score": 0.92}, {"index": 0, "relevance_score": 0.71}]` with `top_n=2`:

```python
docs = ["doc_x", "doc_y", "doc_z"]
resp = [{"index": 2, "relevance_score": 0.92}, {"index": 0, "relevance_score": 0.71}]
mapped = [
    ("doc_" + chr(ord("x") + r["index"]), r["index"], r["relevance_score"])
    for r in resp
]
print(mapped)  # expect [('doc_z', 2, 0.92), ('doc_x', 0, 0.71)]
```

Assert: `mapped[0][0] == "doc_z"` — the **index is a position in the request array, not the chunk id**; the id must be copied from `documents[idx]`, never from the response. Then the API-shape drill: assert the payload the class sends has `model == "rerank-v3.5"` (the default in `CohereReranker.__init__`), `top_n == top_k`, `return_documents == False`, and that `CohereReranker(api_key=None)` falls back to a passthrough (original scores copied — verified in code). Edge: `top_n > len(documents)` → the API clamps; your code must not crash when `len(results) < top_k` (assert `mapped` length is `min(top_n, len(docs))`).

**Level 2 — Applied** (DevMate, 1–3 h)

Wire and measure the real API:

1. Set `COHERE_API_KEY` in your environment (or `.env` — never commit it). `get_retriever()` already picks the Cohere path when the key exists (`src/devmate/retrieve/retriever.py`).
2. Run 10 golden questions through `RAGPipeline.query` with the Cohere path; record per-question: `len(contexts)` (must be ≤ `rag_rerank_top_k = 5`), `latency_ms`, and whether `contexts[i].metadata` matches the source chunk (spot-check 3).
3. Kill-the-API drill: set a wrong key → assert the pipeline either raises a clean error or falls back (decide which is production-correct — see Level 3) and that no partial/corrupt contexts are returned.
4. **Deliverable:** `evaluations/rag/reports/cohere-rerank-<date>.md` with the latency table (retrieve vs. rerank vs. generate) and the spot-check results.
5. **Acceptance criteria:** contexts ≤ 5 per question; the mapping spot-check passes (ids/contents match the source); the wrong-key run behaves per your documented decision.

**Level 3 — Stretch** (production-grade, 3–6 h)

Hosted-API production hardening — MediAssist's compliance constraints:

- Reliability: implement retry with exponential backoff (timeout 30 s is already set in `httpx.Timeout`), a circuit breaker (3 consecutive failures → 60 s open), and **fallback to the local reranker** (`get_reranker("local")`) when the API is down. Prove the fallback path with a stubbed failing client.
- Cost: cap `top_n` by policy; log cost per rerank (inputs = `top_k × doc tokens`, outputs = `top_n`); assert the cap in a test (top_n never exceeds settings).
- Data privacy: document what leaves the network (full chunk contents) — the compliance note: MediAssist must redact or route patient data away from the hosted API.
- **Write an ADR-style justification**: hosted Cohere vs. local bge (privacy, p95 latency, cost per 1k reranks, ops burden). Include measured numbers from Level 2 + the failure drill. Gates: fallback test passes; cost cap enforced by test; the ADR states the privacy decision explicitly.

**Verify:** stubbed-client tests green; the wrong-key run returns the documented behavior; ADR with the hosted-vs-local table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Results reference the wrong document | Treating response `index` as a chunk id | Map `index → documents[index]`; copy id/metadata from the original |
| Timeout kills the whole query | 30 s httpx timeout, no retry | Retry/backoff + circuit breaker + local fallback |
| Key in git history | Hardcoded or committed `.env` | Env var only; check `.gitignore` |
| PII sent to the API | No routing rule | Tenant/data-class filter before rerank |

**Interview:** *"You integrated a hosted reranker — what can go wrong and how did you handle it?"* Strong answer: the index-mapping pitfall (response indexes are request-array positions), timeouts/rate limits (retry + backoff + circuit breaker), fallback to local, cost caps, and the privacy decision for sensitive data.

---

### Topic — Local Reranker (BAAI/bge-reranker-v2-m3, CrossEncoder, no external API)

**Mastery =** you can run a local cross-encoder, keep the event loop non-blocking, and decide when local beats hosted (privacy, latency, cost) with measurements.

**Level 1 — Drill** (mechanics, 20–45 min)

Deterministic stub drill — verify the class contract without downloading a model. Fake a `CrossEncoder`:

```python
import asyncio, sys

sys.path.insert(0, r"projects/04-ai-engineering/devmate/src")
from devmate.retrieve.retriever import LocalReranker
from devmate.index.vector_store import SearchResult


class FakeModel:
    def predict(self, pairs):  # returns per-pair scores
        return [[0.9 - 0.05 * i] for i in range(len(pairs))]


rk = LocalReranker("fake/model")
rk._model = FakeModel()
docs = [
    SearchResult(id=f"d{i}", score=0.5, content=f"content {i}", metadata={"i": i})
    for i in range(5)
]
res = asyncio.run(rk.rerank("q", docs, top_k=3))
print([(r.id, round(r.score, 3)) for r in res])
```

Expected: ids `["d0", "d1", "d2"]` with scores `[0.9, 0.85, 0.8]` and `original_score` preserved from the input (0.5 each). Assert: order is score-descending; `top_k=3` truncates; `original_score == 0.5`; and that the real class runs `self._model.predict(pairs)` in a thread pool (`run_in_executor`) — explain why (blocking CPU work must not stall the event loop).

**Level 2 — Applied** (DevMate, 1–3 h)

Run the real model locally (first download ~2.2 GB — plan for it):

1. `poetry run python scripts/local_rerank_bench.py`: 10 golden questions; per question: raw top-20 → `LocalReranker("BAAI/bge-reranker-v2-m3").rerank(query, docs, top_k=5)`; record p50/p95 rerank time and precision@5 before/after (same labels as §2.5a).
2. **Deliverable:** `evaluations/rag/reports/local-rerank-<date>.md` with the latency table (p50/p95), the precision table, and one paragraph: does local reranking fit the < 150 ms budget (lecture §2.7) on this machine? (On CPU expect 300–800 ms — that's a finding, not a failure.)
3. **Acceptance criteria:** numbers recorded; the paragraph states whether the rerank budget is met and the mitigation if not (GPU, quantization, smaller top_k, batch).

**Level 3 — Stretch** (production-grade, 3–6 h)

Make local reranking fast enough for MediAssist (p95 rerank < 150 ms on commodity hardware):

- Try, measure, and compare: (a) `max_length=512 → 256` (tokens per pair), (b) quantized variant (INT8 / ONNX export of bge-reranker-v2-m3), (c) top-20 → top-10 input reduction, (d) batching pairs in one predict call.
- Record p50/p95 and precision@5 for each variant on the golden set; verify precision does not drop > 0.02 vs. the unquantized baseline.
- **Write an ADR-style justification**: local-quantized vs. local-full vs. hosted (the three-way decision MediAssist faces); include privacy (data never leaves), cost ($0 marginal per query vs. API $/1k docs), latency, and ops (model hosting, memory footprint) in the table. Gates: chosen variant meets p95 < 150 ms or the ADR documents the accepted trade-off with the measured gap.

**Verify:** variant table in the report; ADR cites it; `make test` green with the new tests from Level 1.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Event loop blocked during rerank | `model.predict` called synchronously | `run_in_executor` (already in the class — keep it) |
| Download at deploy time | Model fetched lazily | Preload at startup; pin the model version |
| GPU memory spike | Model + framework loading | Load once (the class caches `_model`); consider INT8 |
| Predict returns nested list | sentence-transformers batch output | Flatten: `predict(pairs)` → `[float(x) for row in scores]` |

**Interview:** *"Local reranker vs. hosted API — how do you choose?"* Strong answer: three axes — privacy (data residency), latency (CPU vs GPU), cost (fixed vs per-call); measured numbers from your bench; and the hybrid pattern (local default, hosted fallback, or vice versa depending on traffic).

---

# 2.6 Evaluation Framework: RAGAs

## Real-world problem: the regression nobody noticed

MediAssist ships weekly. In March they switched embedding models "to save money" and in April switched the reranker top_k from 5 to 8 "to improve recall". Customer complaints about wrong answers doubled — but no metric changed, because there were no metrics. The lesson: RAG fails silently; the fix is **eval-first** — a golden set and a harness that runs on every change (the track mandates exactly this: golden set FIRST, then harness, then everything else, per `docs/roadmap/active-track-10-week.md` weeks 2–3). You must build the 25-question golden set, wire RAGAs' four metrics, and add custom metrics (citation accuracy, latency, cost) so the next regression is a red CI build, not a support ticket.

---

### Topic — The Four Core Metrics (context_precision, context_recall, faithfulness, answer_relevancy)

**Mastery =** you can define each metric, compute it by hand on a small example, state its target, and explain exactly which failure each one catches.

**Level 1 — Drill** (mechanics, 20–45 min)

Hand-compute all four on one example. Ground truth: relevant chunks `R1, R2, R3`; the system retrieved top-5 `[R1, X, R2, Y, Z]`; the answer makes 4 claims, 3 are supported by the retrieved context; answer embedding vs question embedding cosine = 0.82 (given).

| Metric | Computation | Value |
|---|---|---|
| context_precision | relevant in top-k / k = 2/5 | 0.40 |
| context_recall | retrieved relevant / total relevant = 2/3 | 0.67 |
| faithfulness | supported claims / total claims = 3/4 | 0.75 |
| answer_relevancy | cos(answer_emb, question_emb) | 0.82 |

Now map to failures: precision catches "retrieved junk"; recall catches "missed the right chunk"; faithfulness catches "hallucination despite good retrieval"; relevancy catches "off-topic answer". Targets (lecture vs. `evaluations/rag/README.md` — reconcile them in your answer): lecture says precision > 0.7, recall > 0.7, faithfulness > 0.85, relevancy > 0.8; the eval README targets recall@5 > 0.85, precision@3 > 0.80, MRR > 0.70, faithfulness > 0.95, answer relevance > 0.80. Where they differ, note the difference is measurement (RAGAs vs. manual label) not intent. Write a 4-line "which metric to watch when" cheat sheet.

**Level 2 — Applied** (DevMate, 1–3 h)

Run RAGAs on a small real set:

1. Take 5 golden questions (from §2.6a when built; otherwise hand-write 5 over `src/devmate/ingest/chunker.py`), run them through `RAGPipeline.query`, and build the RAGAs dataset: `{"question", "answer", "contexts": [ctx.content…], "ground_truth"}` — exactly the lecture's `RAGEvaluator` shape.
2. If `ragas` + `datasets` are installed: run `evaluate(dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy])` and print the four numbers. If not installed: implement *proxy* versions yourself — precision/recall by label overlap (your labels), faithfulness by claim-split + substring support check, relevancy by cosine of `EmbeddingService` vectors — and document the proxy-vs-RAGAs difference.
3. **Deliverable:** `evaluations/rag/reports/metrics-sample-<date>.md` with the four numbers, targets, and a verdict line per metric (pass/fail vs. target).
4. **Acceptance criteria:** the report has real numbers from the pipeline; every failing metric has a hypothesized cause (e.g., "recall low because AST chunks are small").

**Level 3 — Stretch** (production-grade, 3–6 h)

Metric trust — the senior problem: RAGAs `faithfulness` and `answer_relevancy` are LLM-as-judge; they can be wrong, slow, and expensive. Design a **metric validation protocol**:

- Sample 20 answers; have a human label faithfulness/claim support; compute agreement (Cohen's κ) with the RAGAs judge; report per-metric agreement.
- Find the judge's failure classes (e.g., it accepts "the docs say X" as grounded when X is wrong; it rejects correct paraphrases). Document 5 failure examples with fixes (better judge prompt, stricter claims splitter).
- Cost/latency: measure judge cost per evaluation run (25 questions × 2 judge calls) and decide eval frequency (per PR vs. nightly).
- **Write an ADR-style justification**: RAGAs-default vs. tuned-judge vs. rule-based proxies for the CI gate; include the κ table and cost table. Gates: the gate metric is chosen by agreement, not convenience; the ADR documents what happens when judge agreement < 0.7.

**Verify:** κ numbers in the report; failure examples documented; ADR cites agreement + cost.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Faithfulness always 1.0 | Judge prompt too permissive / claims too coarse | Split claims per sentence; sample hard cases |
| Metrics fluctuate run-to-run | LLM-as-judge nondeterminism | Judge calls at temperature 0; freeze seeds |
| Precision low but recall fine | Chunks too small → many irrelevant | Rerank top-5 (§2.5), bigger chunks |
| Targets unreachable on code corpus | Lecture targets tuned on prose | Reconcile per corpus; record in eval README |

**Interview:** *"Name RAGAs' four core metrics and what each measures."* Strong answer: context_precision (are retrieved chunks relevant), context_recall (did we find everything relevant), faithfulness (claims grounded in context — hallucination), answer_relevancy (answers the question); targets; which failure each catches; and the caveat that two of them are LLM-judged and need validation.

---

### Topic — Custom Evaluation Harness (golden set loading, pipeline runs, aggregation, citation accuracy)

**Mastery =** you can build the `make eval` harness: JSONL golden set in, metrics table out, baseline-compared, regression-gated.

**Level 1 — Drill** (mechanics, 20–45 min)

Harness math drills (pure Python):

1. Golden set loading: parse JSONL lines `{"question", "expected_context": [...], "expected_answer": ..., "metadata": {...}}` (schema per `evaluations/rag/README.md`); assert: all 25 lines parse; every `question` non-empty; every `expected_context` has ≥ 2 entries; metadata topics ∈ {architecture, api, data_models, deployment, testing} (track categories).
2. Aggregation: given per-item metrics `[0.8, 0.9, 1.0, 0.7, 0.9]`, compute mean = 0.86, min = 0.7, max = 1.0 (assert with `statistics.mean`).
3. Citation accuracy: answer `"A[1] and B[2] and C[3]"` with `len(contexts) == 2` → citations `[1],[2],[3]`, valid = 2/3 = 0.667 (the lecture's `_compute_citation_accuracy`: `idx-1 < len(contexts)`); an answer with no citations → `0 / max(total, 1) = 0`. Assert both.
4. Baseline delta: current recall@5 = 0.80, baseline = 0.85 → delta = −0.05 → **fail the gate** (threshold −0.03); assert the boolean gate result.

**Level 2 — Applied** (DevMate, 1–3 h)

This is the track's headline deliverable — build `make eval`:

1. **Golden set first:** create `evaluations/rag/datasets/devmate-golden.jsonl` with 25 questions over this repo (categories: architecture, API, data models, deployment, testing), each with `expected_context` (2–5 chunks, identified by filename or id) and `expected_answer`. Follow the schema in `evaluations/rag/README.md`. Mark which questions are exact-token-sensitive (feed §2.4) and which are paraphrase-sensitive.
2. **Harness:** create `projects/04-ai-engineering/devmate/eval/run_ragas.py` (the path `make eval` already targets: `cd devmate && poetry run python eval/run_ragas.py`). It must: load the JSONL; run each question through `RAGPipeline.query`; compute recall@5, recall@10, MRR (against `expected_context`), RAGAs (or proxies per §2.6a) faithfulness + answer_relevancy; add citation accuracy, avg latency, avg cost (from `RAGResult.usage` + `CostTracker.estimate_cost`); print a metrics table.
3. Save a baseline snapshot to `evaluations/rag/baselines/<date>-v1.md` (format per eval README) and write the full report to `evaluations/rag/reports/<date>-eval.md`.
4. **Acceptance criteria:** `make eval` prints the table and exits 0; running it twice on the same commit gives identical scores (deterministic seed, temperature 0); the golden set has exactly 25 lines; the report includes per-question failures with root-cause hypotheses.

**Level 3 — Stretch** (production-grade, 3–6 h)

Make the harness a **regression gate**:

- Add `--compare` mode: load the latest baseline, compute deltas, exit 1 when any core metric drops below the gate (`recall@5 ≥ −0.03`, `faithfulness ≥ −0.02`, `citation_accuracy ≥ −0.02`).
- Wire a smoke version into CI: `make ci` already runs `test`; add an `eval-smoke` target (5-question subset, no LLM-judge calls) so PRs fail fast, while full `make eval` runs nightly (document the schedule in the eval README).
- Failure drill: commit a deliberate regression (e.g., flip `rag_top_k` 20 → 3 in `src/devmate/config.py`); show the gate fails with the metric table; revert; show green.
- **Write an ADR-style justification**: gate thresholds (how you chose them — baseline minus noise, not vibes), eval frequency, and what happens on a red build (block merge vs. alert+review). Gates: the deliberate regression produces exit 1 with the offending metric highlighted; the ADR's Consequences section is non-empty.

**Verify:** `make eval` output table (rows: recall@5, recall@10, MRR, faithfulness, answer_relevancy, citation_accuracy, latency, cost); the regression drill exit codes (1 with regression, 0 after revert); ADR present.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| `make eval` fails on missing module | `devmate/eval/` doesn't exist yet | It's your deliverable — create it; don't expect the Makefile to run magic |
| Scores differ across runs | LLM nondeterminism in judge/generator | temperature 0; seed; document in README |
| Golden answers leak into prompts | `expected_answer` shipped in the RAG dataset | Keep expected fields out of `RAGRequest`; test with a probe |
| Gate never fails | Thresholds below the noise floor | Set gates from baseline variance (run eval 3×, take ±2σ) |

**Interview:** *"How did you build evaluation into your RAG project?"* Strong answer: golden set first (25 questions, categorized, with expected contexts), harness with retrieval + generation + custom metrics, baselines committed, gates wired into CI with deltas, and the regression drill as proof — "I flipped top_k and the gate went red."

---

# 2.7 Production RAG

## Real-world problem: the enterprise pilot that failed acceptance

IndexCo's enterprise pilot of an internal docs assistant ("DocPilot") hit acceptance testing and failed on three counts: p95 latency 4.2 s against a 3 s contract; cost $0.04/query against a $0.02 ceiling; and the ops team couldn't answer "what's the error rate today?" — there was no dashboard. The vendor says "upgrade the model" (more money), "buy GPUs" (more money). You know better: **budget the stages, cache what repeats, route cheap, and monitor everything**. The lecture gives the budgets: embed < 50 ms, retrieve < 100 ms, rerank < 150 ms, generate < 2 s, total < 3 s; cost levers: semantic caching, cheap-model routing, batch embedding, retrieval TTL caching; monitoring: p50/p95/p99, RAGAs over time, hallucination rate, cost/query, cache hit rate, error rate.

---

### Topic — Performance Budgets (embed <50ms, retrieve <100ms, rerank <150ms, generate <2s, total <3s)

**Mastery =** you can instrument every stage, produce p50/p95 per stage, find the budget violator, and make a justified trade-off when the budget is impossible.

**Level 1 — Drill** (mechanics, 20–45 min)

Budget math. Given stage measurements (ms): embed `[35, 60]`, retrieve `[70, 140]`, rerank `[90, 180]`, generate `[1800, 2600]` (p50, p95 per stage):

1. Compute total p50 = 35+70+90+1800 = 1995 ms ✓ and total p95 = 60+140+180+2600 = 2980 ms ✓ (< 3000).
2. Now rerank p95 → 250 and generate p95 → 2900: total = 60+140+250+2900 = 3350 ✗. Which lever fixes it within budget? Options: (a) reduce rerank top_k 20→10 (rerank p95 → 140, save 110 ms), (b) cheaper generator (generate p95 → 1900, save 1000 ms), (c) shard Qdrant (retrieve p95 → 90, save 50 ms). Compute the resulting totals: (a) 60+140+140+2900 = 3240 ✗, (b) 60+140+250+1900 = 2350 ✓, (c) 60+90+250+2900 = 3300 ✗ — only the model swap meets budget. State the decision rule: **fix the biggest stage first, then re-measure** (generation dominates; don't tune HNSW to save 10 ms when the model costs 1000).
3. Percentile drill (verified): latencies `[120, 340, 95, 210, 1560, 2300, 480, 760, 990, 1520, 640, 290]` → sorted → p50 = 480, p90 = 1560, p95 = 2300, p99 = 2300 (nearest-rank). Implement a `percentile(sorted_latencies, p)` function; assert those values; explain why p99 = p95 here (small n — say why you'd report p95 for n < 1000).

**Level 2 — Applied** (DevMate, 1–3 h)

Instrument DevMate's real stages:

1. `RAGPipeline.query` already opens `tracer.trace("rag.query", …)` and records total `latency_ms`. Add per-stage timing: wrap embed (`trace("rag.embed")`), retrieve (`retriever.retrieve` already traces `"retrieve"`), rerank (`trace("rerank.local")` / `"rerank.cohere"` exist), and generate — collect stage deltas in `RAGResult.stage_times_ms` (a dict).
2. Run 20 questions (mix of §2.6a), aggregate per-stage p50/p95; **Deliverable:** `evaluations/rag/reports/latency-budget-<date>.md` with the stage table (stage | p50 | p95 | budget | pass/fail) and a verdict on the total.
3. **Acceptance criteria:** the table has every stage row against its lecture budget; the total p95 is reported against 3000 ms; the biggest violator is named with a one-line mitigation.

**Level 3 — Stretch** (production-grade, 3–6 h)

The pilot contract, made real: p95 < 3 s at 50 concurrent users on a large corpus (simulate with synthetic vectors + concurrent `asyncio` load):

- Load test (`scripts/load_test.py`): ramp 1→50 concurrent, measure p50/p95/p99 of total + per stage; find where contention appears (Qdrant connection pool, LLM rate limits, GIL during embedding).
- Identify the top-2 fixes by measured impact (e.g., Qdrant connection pooling, generator streaming with early stop, retrieval cache). Implement at least one and re-run the load test.
- **Write an ADR-style justification**: the latency budget allocation (stage budgets + headroom policy — e.g., "retrieval budget = 3× p50 to absorb bursts") and the chosen fix. Include the before/after load-test table. Gates: p95 < 3 s at 50 concurrent in the after-run (or the ADR documents the accepted miss with a date-bound plan).

**Verify:** before/after load-test tables; ADR with the budget table and revisit conditions (traffic growth, new models).

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Total over budget but every stage "fine" | Budgets set without headroom; stages sum to the ceiling | Allocate 80% of total to stages; keep 20% headroom |
| p95 hidden by averages | Mean-based dashboards | Report p50/p95/p99 per stage |
| Tuning the wrong stage | "It felt slow" | Instrument first; fix the biggest stage first |
| First-query latency spike | Cold caches, model warm-up | Pre-warm; exclude warm-up from the SLA |

**Interview:** *"Give me the latency budget of a production RAG system and how you'd enforce it."* Strong answer: the five numbers (50/100/150/2000/3000), per-stage instrumentation, p50/p95 reporting, the fix-the-biggest-stage-first rule with a worked example, and the headroom policy.

---

### Topic — Cost Optimization (semantic caching, cheap-model routing, batch embedding, retrieval caching with TTL)

**Mastery =** you can compute cost/query, identify the dominant cost, and implement caching/routing that measurably cuts it without hurting quality.

**Level 1 — Drill** (mechanics, 20–45 min)

Cost math. Prices (use these constants): embedding `text-embedding-3-small` $0.02/1M tokens; cheap LLM $0.15/1M in, $0.60/1M out; premium LLM $1.25/1M in, $5.00/1M out.

1. One query: 300 prompt + 200 completion tokens on the cheap model → `300×0.15/1e6 + 200×0.60/1e6 = $0.000045 + $0.00012 = $0.000165` ≈ $0.0002; plus 300 embedding tokens → $0.000006. Total ≈ $0.00017/query. Assert the arithmetic (rounded to 6 decimals).
2. At 10,000 queries/day: ≈ $1.7/day. Semantic cache hit rate 40% (threshold 0.85, TTL 3600 — DevMate's settings): cached queries cost only the embedding (~$0.00001); daily cost = `0.4 × 10k × 0.00001 + 0.6 × 10k × 0.00017` ≈ `$0.04 + $1.02` ≈ $1.06/day — a 38% cut. Assert the math.
3. Routing drill: 30% of queries are "simple" (fact lookup) → route to the cheap model; 70% stay premium. Compute blended cost/query and the saving vs. all-premium (premium alone: `300×1.25/1e6 + 200×5/1e6 = $0.000375 + $0.001 = $0.001375`/query). Blend = `0.7 × 0.001375 + 0.3 × 0.000165` ≈ $0.001012 — 26% cheaper. Assert.
4. Batch embedding: indexing 10k chunks in batches of `embedding_batch_size=100` → 100 API calls vs. 10,000; latency math: `100 × ~300 ms ≈ 30 s` vs. serial `10,000 × 300 ms ≈ 50 min`. State the win.

**Level 2 — Applied** (DevMate, 1–3 h)

Implement and measure the cache:

1. `src/devmate/cache/semantic_cache.py` already exists (`get(query, query_embedding, model)`, `set`, `get_stats`, threshold 0.85 from settings). Wire it into `RAGPipeline.query`: before retrieval, check the cache (note the design decision: DevMate computes the query embedding first, so the cache saves LLM + retrieval cost, not embedding cost — document this); on hit, return the cached response; on miss, run and `set`.
2. Add a retrieval-level cache keyed `(query_text, filter)` with TTL 3600 (`settings.cache_ttl_seconds`) storing the top-5 contexts. Decide: full-response cache vs. context-only cache — document the correctness trade (retrieval cache saves rerank+generate; full cache can serve stale answers).
3. Run 20 queries where 10 are near-duplicates (paraphrases above threshold); record `get_stats()` hit rate and compute cost/query before vs. after using `CostTracker` (`src/devmate/obs/cost.py`).
4. **Deliverable:** `evaluations/rag/reports/cache-cost-<date>.md`: cache stats (hits/misses/evictions), cost/query before/after, and the routing rule you'd add next.
5. **Acceptance criteria:** the near-duplicate run shows hits > 0; the report shows the cost/query delta with real token counts from `RAGResult.usage`.

**Level 3 — Stretch** (production-grade, 3–6 h)

The DocPilot cost contract, with failure modes: $0.02/query ceiling at 50k queries/day, plus correctness requirements:

- Design the full cost stack: semantic cache (threshold sweep 0.80–0.92 — measure the false-hit rate on 20 adversarial paraphrases: two different questions must NOT collide), retrieval TTL cache with **invalidation on re-ingest** (new chunks must invalidate stale cached contexts — hook the `RepoIndexer` from §2.1a L3), cheap-model routing with a quality gate (route only if a confidence heuristic fires; verify routed answers' faithfulness ≥ 0.85 on a sample).
- Attack the failure modes: cache poisoning (an abusive query pattern filling the cache with junk — cap per-tenant entries), TTL staleness (documented stale window), and cost spikes (daily cost budget; alert at 80%).
- **Write an ADR-style justification**: caching/routing architecture (what's cached at which layer, invalidation policy, routing rule, cost ceiling) with the measured cost/query table and the quality-gate results. Gates: cost/query ≤ $0.02 at 50k/day in the model; adversarial-paraphrase false-hit rate < 5%; re-ingest invalidates within the documented window.

**Verify:** the model produces the cost table (before/after); the false-hit and invalidation tests pass; ADR present with the ceiling and revisit conditions.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Cache never hits | Threshold too strict / queries all unique | Lower threshold; log query-similarity distribution |
| Stale answers after re-ingest | No invalidation | Version the corpus; invalidate on index change |
| Cost/query unchanged | Caching after the expensive step | Cache before generation (retrieval cache) — measure the delta |
| "Two questions, one answer" | Semantic threshold too loose | Adversarial paraphrase test; per-tenant caches |

**Interview:** *"Where does the money go in RAG and how do you cut it?"* Strong answer: generation dominates (tokens in = retrieved context); levers in order — retrieval/semantic cache (kills generation for repeats), cheap-model routing for simple queries, batch embedding at index time, top_k discipline; each with measured cost/query numbers and the correctness risks (staleness, false hits).

---

### Topic — Monitoring Metrics (p50/p95/p99, RAGAs over time, hallucination rate, cost/query, cache hit rate, error rate)

**Mastery =** you can define the metric set, aggregate them from real pipeline data, set alert thresholds with a rationale, and run a red/amber/green review of a production snapshot.

**Level 1 — Drill** (mechanics, 20–45 min)

Metrics computation on a 10-query snapshot (all numbers given — compute and assert):

- Latency: use the §2.7a list → p50 = 480, p95 = 2300.
- Error rate: 1 failed query of 10 → 10%.
- Cache hit rate: 4 hits / 10 → 40%.
- Hallucination rate: 3 of 100 sampled answers contain an unsupported claim → 3%.
- Cost/query: total $0.0035 over 10 queries → $0.00035.

Then set thresholds with one-line rationales (DocPilot contract): p95 ≥ 3 s → critical (SLA); error rate ≥ 5% → critical (availability); hallucination ≥ 2% → critical (compliance); cost/query ≥ $0.02 → warning (budget); cache hit rate < 20% → info (tuning signal). Write the alert table and state which two alerts would have caught the pilot failure before acceptance (p95 latency and cost/query — both were over contract).

**Level 2 — Applied** (DevMate, 1–3 h)

Produce a monitoring snapshot from the real pipeline:

1. Run the golden set (§2.6a, 25 questions) twice — first cold, then warm (cache primed) — through `RAGPipeline.query`; collect per-query `latency_ms`, `usage` tokens, errors, cache hits (`SemanticCache.get_stats()`).
2. `poetry run python scripts/monitoring_snapshot.py` → prints the metric table: p50/p95/p99 latency, error count, cache hit rate, mean cost/query (via `CostTracker.estimate_cost`), and RAGAs scores if the harness exists.
3. **Deliverable:** `evaluations/rag/reports/monitoring-<date>.md`: the table + alert-status column (green/amber/red vs. the Level 1 thresholds) + a 3-line summary.
4. **Acceptance criteria:** every row has a real number; the red/amber/green statuses are derived, not hand-waved; the report states which alert would fire first in production.

**Level 3 — Stretch** (production-grade, 3–6 h)

The ops dashboard + drift detection:

- Build a lightweight metrics sink: extend `obs/tracing.py` or add `obs/metrics.py` that records per-query: latency by stage, tokens, cost, cache hit, error class — in a JSONL file under `evaluations/rag/metrics/` (or an in-memory ring buffer + snapshot writer). Provide a `metrics_summary(path)` reader that prints the monitoring table for any date window.
- **RAGAs over time**: nightly `make eval` (from §2.6b L3) appends its scores to `metrics/ragas-trend.jsonl`; implement a trend check: any metric below `baseline − 2σ` (computed over the trailing 7 runs) → alert. Feed it 3 weeks of synthetic scores with one injected dip; assert the detector fires on the dip and not on noise.
- Hallucination sampling: every 10th query's answer goes to a reviewer queue (a JSONL of answers + context ids) — document the sampling protocol and the weekly review step; compute the sampled hallucination rate into the alert table.
- **Write an ADR-style justification**: monitoring architecture (metrics sink, alert thresholds, drift detector, sampling protocol) — and the runbook section: what to do when each alert fires (p95 → check stage budget table; hallucination → quarantine the model/config change and roll back; cost → enforce routing). Gates: drift detector has zero false positives on the synthetic noise window; the runbook lists one action per alert; the ADR's Consequences section is non-empty.

**Verify:** `metrics_summary` prints the table for the recorded window; the drift test shows fire-on-dip, no-fire-on-noise; ADR + runbook exist.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Alerts never fire | Thresholds above observed ranges | Set thresholds from real data: baseline + 2σ, review monthly |
| p99 dominated by one bad query | Sparse sampling | Report p95 for n < 1000; use histograms for skew |
| Hallucination rate unknown | No sampling protocol | Sampled review queue; weekly human review |
| Dashboard shows no trend | Metrics overwritten each run | Append-only JSONL; keep baselines |

**Interview:** *"What would you monitor on a production RAG system, and what are your alert thresholds?"* Strong answer: the six metric families (latency percentiles, RAGAs over time, hallucination rate via sampling, cost/query, cache hit rate, error rate); thresholds tied to the contract (p95 < 3 s, cost < $0.02) plus statistical ones (baseline − 2σ drift); and the runbook — every alert has an owner and a rollback action.

---

# Appendix: Repo facts used in this workbook (verified 2026-08-11)

| Fact | Location |
|---|---|
| DevMate root | `projects/04-ai-engineering/devmate/` |
| Chunkers (real, with the documented bug/quirk) | `src/devmate/ingest/chunker.py` (FixedSizeChunker, RecursiveChunker, ASTAwareChunker, DocumentLoader, `CHUNKERS`, `get_chunker`) |
| Planned chunkers package (semantic goes here) | `devmate/src/devmate/ingest/chunkers/` (per track) |
| Embeddings | `src/devmate/index/embeddings.py` (EmbeddingService, OpenAI/Local providers) |
| Vector store | `src/devmate/index/vector_store.py` (VectorStoreConfig, BaseVectorStore, QdrantVectorStore) |
| Retrieval + rerankers | `src/devmate/retrieve/retriever.py` (CohereReranker, LocalReranker, NoOpReranker, `get_reranker`, Retriever, `get_retriever` reads `COHERE_API_KEY`) |
| RAG pipeline | `src/devmate/retrieve/rag.py` (RAGRequest, RAGResult, RAGPipeline, `RAG_SYSTEM_PROMPT`) |
| Caches & observability | `src/devmate/cache/semantic_cache.py`, `src/devmate/obs/cost.py` (CostTracker), `src/devmate/obs/tracing.py` (tracer) |
| Existing unit tests | `devmate/tests/unit/test_chunker.py` (6 tests; `make test` currently hangs on the fixed-size input — your first fix) |
| Eval targets | `make eval` → `devmate/eval/run_ragas.py` (to be created); schema + baselines format in `evaluations/rag/README.md` |
| Golden set (planned, 25 Qs) | `evaluations/rag/datasets/devmate-golden.jsonl` |
| Baseline + report homes | `evaluations/rag/baselines/`, `evaluations/rag/reports/` |
| Infra | `infra/docker/docker-compose.yml` — service `qdrant` (image `qdrant/qdrant:v1.8.0`, port 6333, healthcheck), `QDRANT_COLLECTION=devmate_code` |
| Settings | `src/devmate/config.py` — `qdrant_collection`, `qdrant_vector_size=1536`, `qdrant_distance=cosine`, `rag_top_k=20`, `rag_rerank_top_k=5`, `rag_chunk_size=512`, `rag_chunk_overlap=50`, `semantic_cache_threshold=0.85`, `cache_ttl_seconds=3600`, `embedding_batch_size=100` |
| Vector DB decision | `docs/decisions/0005-vector-db-qdrant-over-chromadb.md` (Qdrant primary; Chroma comparison time-boxed; report to `evaluations/rag/reports/`) |
| ADR format | `docs/decisions/README.md` — Context, Decision Drivers, Options Considered, Decision, Consequences (required); next free number: 0007 |
| Track weeks 2–3 | `docs/roadmap/active-track-10-week.md` — golden set first, harness, 3 chunkers, VectorStore protocol, Chroma adapter, hybrid + rerank, 2 ADRs with results tables; DoD: `make eval` prints a metrics table |
| Lecture case-study numbers | Fixed(512) 0.62/0.58/0.78 @1.8s · Recursive 0.71/0.68/0.84 @1.9s · AST-aware 0.83/0.79/0.91 @2.1s · Qdrant 85ms vs Chroma 120ms |

## Known repo bugs/quirks discovered while writing this workbook

1. **`FixedSizeChunker` infinite loop** (verified): when a chunk's length ≤ `overlap`, `start = end - overlap` stops advancing → the loop never terminates. The repo's own unit test input `(100, 10)` on `"word " * 200` hangs; `make test` is currently blocked. Fix: progress guarantee. (Level 1 of §2.2a.)
2. **`RecursiveChunker` descends the full separator hierarchy** even when all pieces fit, ending in character-level splitting — different from LangChain's early return. (Level 1 of §2.2b.)
3. **CRLF vs LF changes recursive chunk boundaries** on Windows, which can silently break golden-set reproducibility across machines. (Level 1 of §2.2b.)
4. **`devmate/eval/run_ragas.py` and `devmate-golden.jsonl` do not exist yet** — they are the week's deliverables, and `make eval` will fail until §2.6b is done.

---

*Workbook created 2026-08-11 under ADR-0006 (production-focused curriculum anchored to DevMate). All drill numbers verified against the repo code and Python 3.x on 2026-08-11. Back to the lecture: [`../lectures/02-rag-systems.md`](../lectures/02-rag-systems.md) · Protocol: [`README.md`](README.md).*

