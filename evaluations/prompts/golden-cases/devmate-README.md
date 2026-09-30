# DevMate Prompt Golden Cases

**Created:** 2026-09-30 · **Milestone:** A2 (active track week 1)
**Path:** `evaluations/prompts/golden-cases/devmate.jsonl`
**Companion RAG set:** `evaluations/rag/datasets/devmate-golden.jsonl` (retrieval golden set + baseline)

These ten cases are the week-1 prompt golden set for `devmate ask` / the RAG answer path.
Each line is one case: question, expected context, expected answer, and checkable
`expected_properties` for the LLM response.

## Why this file exists

Week 1 of the active track requires 10 golden cases as question → expected properties.
RAG retrieval metrics alone cannot catch a generator that invents APIs, drops citations,
or fails to mention fallback behavior. These cases encode the *answer properties* DevMate
must uphold.

## Schema

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | string | yes | Stable case id (`devmate-ask-001` …) |
| `prompt_id` | string | yes | Prompt under test (`devmate.rag.answer`) |
| `prompt_version` | string | yes | Version pin for rollback comparisons |
| `question` | string | yes | User question to DevMate |
| `category` | string | yes | code_comprehension, api, behavior, architecture, debugging |
| `expected_context` | string[] | yes | Chunks that must appear in retrieval |
| `expected_answer` | string | yes | Gold answer grounded in those chunks |
| `expected_properties` | object | yes | Checkable properties for the model response |
| `metadata` | object | yes | expected_source_files, difficulty, topic, checks |

### `expected_properties` keys

| Key | Type | Check |
| --- | --- | --- |
| `must_be_grounded_in_context` | bool | Answer must not invent facts outside retrieved context |
| `must_cite_sources` | bool | Answer must reference sources / context chunks when the system prompt requires citations |
| `must_not_invent_api` | bool | Must not invent function names not present in context |
| `min_context_sources` | int | Minimum number of retrieved sources expected |
| `must_mention_*` | bool | Case-specific required themes (fallback, streaming, tradeoff, …) |
| `must_not_*` | bool | Forbidden claims (e.g. silent success on total provider failure) |
| `forbidden_phrases` | string[] | Substrings that indicate refusal / generic filler |
| `expected_tool_names` | string[] | Exact tool inventory when the case is about MCP tools |

## Offline validation

```powershell
# Schema validation — no API key, no network
cd projects/04-ai-engineering/devmate
.venv\Scripts\python.exe -m pytest tests/unit/test_prompt_golden.py -q
```

Or run the validator module directly:

```powershell
.venv\Scripts\python.exe -m devmate.eval.validate_prompt_golden
```

Expected: 10 cases load, required keys present, unique ids, `min_context_sources >= 1`.

## Live scoring (later — weeks 2–3 / P1)

Live scoring against a running model is **not** in this file's contract yet. The next
step is `devmate/eval/run_ragas.py` (or successor) that:

1. Loads this JSONL
2. Runs `devmate ask` / RAG pipeline
3. Scores retrieval against `expected_context`
4. Scores answer properties against `expected_properties`
5. Writes a report under `evaluations/prompts/regressions/` or `evaluations/rag/reports/`

Until that harness exists, this file is the **specification** of expected behavior and
the offline schema validator is the gate.

## Relationship to Production AI Systems track

These cases are week-1 A2 evidence, not phase P1. Phase P1 (after A4/A6) promotes this
spec into a CI eval gate with thresholds, judge pinning, and regression blocking.
See [`docs/roadmap/production-ai-systems-engineer.md`](../../../docs/roadmap/production-ai-systems-engineer.md).

## Maintenance rules

- Never edit a case id in place; add a new id and retire the old one.
- When a prompt version changes behavior intentionally, bump `prompt_version` and record
  a regression file under `evaluations/prompts/regressions/`.
- Keep expected answers short and grounded. Long gold answers hide retrieval failures.
