# Code Intelligence

Multi-layered code intelligence powered by codebase-memory-mcp, code-review-graph,
graphify, and repomix.

## Status

| Layer | Status | Details |
|-------|--------|---------|
| **Structural Graph** | ✅ Refreshed 2026-10-05 | **66,515 nodes, 147,478 edges**, 7 languages (Go removed) |
| **Review Graph** | ✅ Rebuilt 2026-10-05 | 12,904 nodes, 95,167 edges, 23 communities, 1,147 flows; built at `10cc7c9`, `head_matches_build: true` |
| **Multimodal Graph** | ✅ Rebuilt 2026-10-05 | 62,930 nodes, 67,935 edges, 3,785 communities (AST-only, no LLM) |
| **Context Pack** | ✅ Repacked 2026-10-05 | 5,425,989 tokens, 3,435 files (repomix CLI defaults; written outside the repo) |
| **Watcher** | ⏳ Manual | Re-index with `codebase-memory index_repository` after large edits |

**Structural project name:** `D-AI-Projects-fullstack-ai-engineer-lab` — becomes `D-AI-Projects-ai-engineer-lab` after the folder rename + reindex
**Root:** `D:/AI/Projects/fullstack-ai-engineer-lab` · branch `master`

### Refresh notes (2026-10-05)

- **Go + frontend removed** (52 files) and the repo rebranded to "AI Engineer Lab" /
  `ai-engineer-lab`. Full structural reindex: nodes 67,084 → **66,515** (−569),
  edges 148,492 → **147,478** (−1,014). Languages 8 → **7** — `Go` is gone.
- Review graph rebuilt at `10cc7c9` (20 stale files dropped): 12,984 → **12,904**
  nodes, 95,601 → **95,167** edges; communities (23) and flows (1,147) unchanged.
- Graphify forced re-extract: 49,856 → **62,930** nodes, 54,483 → **67,935** edges,
  2,833 → **3,785** communities. 283 community labels were re-derived by hub — run
  `graphify label` with an LLM key to refresh the names.
- The structural graph key is still the old path-derived name until the folder is
  renamed and reindexed.
- Repomix repacked with CLI defaults: **5,425,989 tokens / 3,435 files** (the older
  1,244,995 figure came from the MCP tool's narrower defaults — not comparable).
  Output lives in the OS temp dir, not the repo.

### Refresh notes (2026-10-02)

- Growth from lecture/quiz commits: nodes 60,751 → **67,084** (+6,333),
  edges 141,083 → **148,492** (+7,409).
- `parse_partial`: 7 files (infra sql/conf/ps1, `practice_no_solutions.py`,
  `pytest.ini`). `skipped`: 0.
- Review graph rebuilt same day at `78d12fb`: nodes 11,590 → **12,984**,
  edges 87,721 → **95,601**; files 932 → 1,180. Communities (23) and
  flows (1,147) unchanged.
- Graphify unchanged: 49,856 nodes / 54,483 edges / 2,833 communities.
- Hotspots, boundaries, and clusters re-pulled from `get_architecture`
  (`len` fan-in 1,211 → 1,350; `print` 893 → 1,016; cluster IDs renumbered).

### Reindex notes (2026-09-30)

- Full reindex after DevMate eval package + roadmap docs landed.
- Nodes 60,577 → **60,751**; edges 140,909 → **141,083**.
- `parse_partial`: 7 files (infra sql/conf/ps1 + a few curriculum files) — not DevMate eval.
- `skipped`: 0.
- By-design exclusions include `.venv`, `__pycache__`, `.env`, gitignored assets.
- `evaluations/rag/datasets` is currently in not-indexed dirs — golden JSONL is **not** in
  the graph; read those files from the filesystem.
- Uncommitted work still reports `freshness: metadata_changed` on coverage checks until
  committed and reindexed.

### DevMate call-graph after retrace

| Symbol | Callers | Callees | Notes |
| ------ | ------- | ------- | ----- |
| `get_rag_pipeline` | 8 | 1 | API (`ask`/`ingest`/`lifespan`/`rag_query`) + CLI |
| `RAGPipeline.query` | 5 | 33 | hybrid search, tracer, LLM complete, context builders |
| `Tracer.trace` | 47 | 6 | API, CLI, RAG, agents, guards, embeddings, eval live path |
| `Retriever.retrieve` | 15 | 16 | hybrid_search + RRF + rerank; also `eval.run_ragas` live path |
| `score_retrieval` | 3+ | 4 | `run_offline`, `run_live`, `amain` |
| `LLMClient.complete` | 0 in graph | 3 | Lazy `get_llm_client()` + provider dict — **use source, not inbound CALLS** |
| `run_ragas` | module node | 14 | Indexed as Module 1–386; function-level edges resolve via callees |

### Architecture

```mermaid
graph TD
    subgraph EP["Entry points"]
        EP_DATA["main: data-engineering x15"]:::entry
        EP_DS["main: ds-algo x4"]:::entry
        EP_CLI["devmate cli.ask"]:::entry
        EP_API["devmate api.ask"]:::entry
        MAIN["main() across exercises"]:::god
    end

    subgraph CORE["00-core-foundations"]
        PY_CORE["python core + advanced"]
        PY_LIBS["numpy / pandas / polars"]
        PY_DSA["DSA + hash tables"]
        PY_ML["ML + deep learning"]
        PY_WEB["fastapi web track"]
        REDIS["RedisClient capstone"]:::god
        SESSION["SQLAlchemy Session"]:::god
    end

    subgraph HOT["Hotspots by fan-in"]
        H_LEN["len 1,350"]:::hot
        H_PRINT["print 1,016"]:::hot
        H_APPEND["list.append 586"]:::hot
        H_METHODS["Printable.print 582"]:::hot
    end

    subgraph AI["04-ai-engineering"]
        DEVMATE["devmate rag / llm / eval"]
        OBS["obs.tracing + cost"]
        FASTAI["fastai exercises"]
        ATHAR["athar-lab"]
        SPY["SpyClient mock"]:::god
    end

    EP_DATA --> PY_LIBS
    EP_DS --> PY_DSA
    EP_CLI --> DEVMATE
    EP_API --> DEVMATE
    DEVMATE -.->|"406 calls"| PY_CORE
    PY_CORE -.->|"249 calls"| DEVMATE
    DEVMATE -.->|"Tracer.trace 47 callers"| OBS
    PY_ML --> PY_LIBS
    PY_WEB --> SESSION
    PY_CORE -->|"fan-in 1,350"| H_LEN
    PY_LIBS -->|"fan-in 1,016"| H_PRINT
    PY_CORE -->|"fan-in 586"| H_APPEND
    PY_CORE -->|"fan-in 582"| H_METHODS

    classDef entry fill:#1e6fd9,color:#fff,stroke:#0d47a1
    classDef hot fill:#d93025,color:#fff,stroke:#b71c1c
    classDef god fill:#f2994a,color:#fff,stroke:#e65100
```

### Key Hotspots

| Symbol | Type | Fan-in | Why |
|--------|------|--------|-----|
| `len` | builtin | 1,350 | Most-called function across exercises |
| `print` | builtin | 1,016 | Output everywhere |
| `list.append` | builtin | 586 | Core data-structure operation |
| `Printable.print` | method | 582 | ABC pattern demo in `08-abc` |
| `HashTable.items` | method | 258 | DSA hash-table exercise |
| `FileManager.append` | method | 199 | File-manager capstone |
| `dict.get` | builtin | 190 | Dictionary lookup pattern |
| `AsyncDB.close` | method | 159 | FastAPI async-DB exercise |
| `ConnectionManager.connect` | method | 158 | FastAPI websockets exercise |

### Cross-Package Boundaries

| From | To | Calls |
|------|----|-------|
| 00-core-foundations | builtins (`len`) | 763 |
| 00-core-foundations | builtins (`print`) | 715 |
| 04-ai-engineering | 00-core-foundations | 406 |
| 04-ai-engineering | builtins (`len`) | 406 |
| 00-core-foundations | 04-ai-engineering | 249 |

### Clusters (12 from codebase-memory)

| Cluster | Size | Cohesion | Dominant |
|---------|------|----------|----------|
| 0 | 508 | 0.44 | len, range, _verify, partition, top_k_scores |
| 11 | 477 | 0.52 | print, llm_call, run_communication_demo, run, _verify |
| 1 | 329 | 0.59 | str, read, search, main, trace |
| 50 | 320 | 0.81 | execute, connect, commit, close |
| 14 | 317 | 0.48 | append, pop, analyze, execute_plan, solve_problem |
| 15 | 240 | 0.64 | get, _purge, set, append |
| 8 | 230 | 0.56 | list, keys, _verify, parse_sse_stream |
| 12 | 222 | 0.56 | int, encode, main, decode, _verify |
| 21 | 200 | 0.60 | append, get, insert, main, undo |
| 68 | 194 | 0.75 | Session, add, _exp |
| 16 | 160 | 0.47 | items, get, clear, _verify |
| 6 | 155 | 0.60 | dict, sort, KeyValueStore, _verify |

### Communities (23 from code-review-graph)

| Community | Size | Cohesion | Language |
|-----------|------|----------|----------|
| challenges-demo | 2,232 | 0.23 | Python |
| 10-repository-pattern-verify | 1,252 | 0.24 | Python |
| practice-problem | 1,201 | 0.20 | Python |
| exercises-user | 1,160 | 0.15 | Python |
| 23-ml-visualization-exercise | 1,031 | 0.07 | Python |
| exercises-agent | 605 | 0.31 | Python |
| 04-queues-sort | 577 | 0.27 | Python |
| exercises-demo | 538 | 0.25 | Python |
| exercises-demo-agent | 430 | 0.31 | Python |
| llm-count | 375 | 0.32 | Python |
| practice-problem-agent | 346 | 0.60 | Python |
| 09-genai-verify | 296 | 0.31 | Python |
| 08-mlops-verify | 180 | 0.34 | Python |
| exercises-train | 162 | 0.18 | Python |
| 01-calculator-task | 74 | 0.17 | Python |

### God Nodes (graphify, top 10)

| Node | Edges | What it is |
|------|-------|------------|
| `RedisClient` | 110 | Redis connection wrapper (capstone infra) |
| `main()` | 100 | Entry points across all exercises |
| `Session` | 96 | SQLAlchemy session (database exercises) |
| `SpyClient` | 31 | Testing mock (observability exercises) |
| `Glossary: Data Ethics` | 31 | fast.ai lecture glossary |
| `BST` | 29 | Binary search tree (DSA) |
| `Detailed Definitions` | 29 | fast.ai glossary node |
| `TokenUsage` | 28 | LLM cost tracking (DevMate obs) |
| `Terms - Alphabetical Order` | 28 | fast.ai glossary node |
| `Definitions` | 27 | fast.ai glossary node |

## Quick Reference

| Question | Tool call |
|----------|----------|
| Who calls X? | `codebase-memory_trace_path(function_name="X", direction="inbound")` |
| What does X call? | `codebase-memory_trace_path(function_name="X", direction="outbound")` |
| Find by pattern | `codebase-memory_search_graph(name_pattern=".*X.*")` |
| Dead code | `codebase-memory_search_graph(max_degree=0)` |
| Impact of changes | `codebase-memory_detect_changes(project="D-AI-Projects-fullstack-ai-engineer-lab")` |
| Blast radius | `code-review-graph_detect_changes_tool(detail_level="minimal")` |
| Critical flows | `code-review-graph_list_flows_tool(sort_by="criticality", detail_level="minimal")` |
| Community details | `code-review-graph_get_community_tool(community_name="X")` |
| God nodes | `graphify_god_nodes()` |
| Shortest path | `graphify_shortest_path(from="X", to="Y")` |
| Pack for LLM | `repomix_pack_codebase(path="D:\\AI\\Projects\\fullstack-ai-engineer-lab")` |

## How to re-index

```bash
# Structural graph (codebase-memory-mcp)
codebase-memory index_repository --repo_path D:\AI\Projects\fullstack-ai-engineer-lab --mode full

# Review graph (code-review-graph)
# Built automatically on first query, or trigger manually:
code-review-graph build_or_update_graph_tool

# Multimodal graph (graphify)
graphify update . --force
```

## What it covers

- **Python** (1,146 files in structural graph language counts): core, advanced, libraries,
  databases, web frameworks, DSA, ML, MLOps, GenAI, DevMate package + unit tests
- **Markdown** (extensive): lectures, quizzes, ADRs, roadmaps, learning paths
- **HTML/CSS/JS / YAML / TOML / SQL**: templates, compose, CI, registries, init scripts

## Agent tiers

| Tier | When to use | Tools |
|------|-------------|-------|
| **Scout** | Quick lookup, provisional | graph + repomix tools |
| **Verify** | Task-directed evidence | graph + coverage checks + exact snippets |
| **Auditor** | Full bounded verification | All tools, complete pagination |

*Last updated: 2026-10-05 (all graphs rebuilt + repomix repacked after Go/frontend removal: structural 66,515 nodes / 147,478 edges / 7 languages, review 12,904 / 95,167, graphify 62,930 / 67,935, pack 5,425,989 tokens)*
