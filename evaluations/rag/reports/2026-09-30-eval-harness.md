# DevMate Eval Report — 2026-09-30

- Mode: `offline`
- RAG golden set: `evaluations\rag\datasets\devmate-golden.jsonl` (10 cases)
- Prompt golden set: `evaluations\prompts\golden-cases\devmate.jsonl` (10 cases)

## Metrics

```
Metric                  Value
----------------------  -----
Retrieval cases         10
Hit@1                   0.600 (6/10)
Hit@5                   1.000 (10/10)
Hit@10                  1.000 (10/10)
MRR                     0.742
Answer cases            10
Answer pass rate        1.000 (10/10)
```

## Retrieval detail

| Case | Hit@1 | Hit@5 | Hit@10 | RR | Expected | Top retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| dev-golden-001 | True | True | True | 1.000 | src/devmate/ingest/chunker.py | src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py |
| dev-golden-002 | False | True | True | 0.333 | src/devmate/obs/cost.py | src/devmate/api/main.py, src/devmate/obs/__init__.py, src/devmate/obs/cost.py, src/devmate/llm/client.py, src/devmate/llm/client.py |
| dev-golden-003 | True | True | True | 1.000 | src/devmate/api/main.py | src/devmate/api/main.py, src/devmate/api/main.py, tests/unit/test_api_sse.py, tests/unit/test_api_sse.py, tests/unit/test_api_sse.py |
| dev-golden-004 | False | True | True | 0.250 | pyproject.toml | src/devmate/index/vector_store.py, ai-review.md, src/devmate/config.py, pyproject.toml, ai-review.md |
| dev-golden-005 | True | True | True | 1.000 | src/devmate/ingest/chunker.py | src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py, src/devmate/ingest/chunker.py |
| dev-golden-006 | True | True | True | 1.000 | src/devmate/llm/client.py | src/devmate/llm/client.py, src/devmate/llm/client.py, src/devmate/llm/client.py, src/devmate/retrieve/rag.py, src/devmate/api/main.py |
| dev-golden-007 | False | True | True | 0.500 | src/devmate/guards/guardrails.py | src/devmate.egg-info/top_level.txt, src/devmate/guards/guardrails.py, src/devmate/guards/__init__.py, src/devmate.egg-info/entry_points.txt, README.md |
| dev-golden-008 | True | True | True | 1.000 | src/devmate/retrieve/retriever.py | src/devmate/retrieve/retriever.py, src/devmate/retrieve/retriever.py, src/devmate/retrieve/retriever.py, src/devmate/retrieve/retriever.py, src/devmate/retrieve/rag.py |
| dev-golden-009 | False | True | True | 0.333 | src/devmate/db/models.py | tests/unit/test_db_models.py, tests/unit/test_db_models.py, src/devmate/db/models.py, tests/unit/test_db_models.py, src/devmate/db/models.py |
| dev-golden-010 | True | True | True | 1.000 | src/devmate/mcp/server.py | src/devmate/mcp/server.py, src/devmate/mcp/server.py, src/devmate/mcp/__init__.py, src/devmate.egg-info/top_level.txt, src/devmate/mcp/server.py |

## Answer property detail

| Case | Passed | Checks | Failures |
| --- | --- | --- | --- |
| devmate-ask-001 | True | forbidden_phrases_absent=True, has_citation_signal=True |  |
| devmate-ask-002 | True | has_citation_signal=True |  |
| devmate-ask-003 | True | has_citation_signal=True |  |
| devmate-ask-004 | True | has_citation_signal=True |  |
| devmate-ask-005 | True | has_citation_signal=True |  |
| devmate-ask-006 | True | has_citation_signal=True |  |
| devmate-ask-007 | True | has_citation_signal=True |  |
| devmate-ask-008 | True | has_citation_signal=True |  |
| devmate-ask-009 | True | has_citation_signal=True |  |
| devmate-ask-010 | True | has_citation_signal=True, expected_tool_names_present=True |  |

## Decision

- [ ] Accept (Hit@5 and answer pass rate meet or exceed baseline)
- [ ] Reject (metrics below baseline — investigate before merging prompt/model changes)
