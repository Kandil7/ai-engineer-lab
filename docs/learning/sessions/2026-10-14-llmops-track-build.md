# LLMOps Learning Track Built (4 files) + DevMate Path Reality Check

### Context

Created the full llmops learning track under projects/06-devops/llmops/ (lecture, glossary, quiz, exercise) matching the docker track's gold-standard format. Session discovered and honestly documented a repo gap: paths cited in the track README do not all exist.

### Explanation

Files created:
- projects/06-devops/llmops/lectures/01-llmops-lifecycle-lecture.md (563 lines) — 11 key concepts, 4 code examples, 7 mistake pairs, FACT vs general-practice labeling throughout.
- projects/06-devops/llmops/lectures/01-llmops-lifecycle-glossary.md (604 lines) — 24 quick-ref terms, 24 detailed definitions.
- projects/06-devops/llmops/quizzes/01-llmops-lifecycle-quiz.md (346 lines) — 15 questions, answer key, score table.
- projects/06-devops/llmops/exercises/01-llmops-lifecycle.py (722 lines) — stdlib-only prompt-registry auditor (PR001-PR004) + cost budgeter (COST001/COST002); demo: bad pack 6 findings, good pack 0.

CRITICAL repo fact discovered: projects/04-ai-engineering/devmate/src/devmate/llm/prompts/ and prompts/registry.py DO NOT EXIST despite being cited in projects/06-devops/llmops/README.md and the roadmap week-1 table. What exists: llm/{client,schemas,__init__}.py; PromptTemplate schema at llm/schemas.py:179; inline RAG_SYSTEM_PROMPT constant at retrieve/rag.py:45; 10 golden cases pinned to devmate.rag.answer@1.0.0 in evaluations/prompts/golden-cases/devmate.jsonl. The lecture states this gap explicitly rather than pretending.

Other verified FACTs used: CI eval gate at .github/workflows/ci.yml:71-77 (--fail-under-hit-at-5 1.0 --fail-under-mrr 0.70, offline mode); ADR-0009 live baseline Hit@5 0.900/MRR 0.820 vs offline fixtures 1.000; obs/cost.py MODEL_PRICES; guards/guardrails.py categories+actions; cache/semantic_cache.py threshold 0.85; docs/failure-modes.md taxonomy + Ollama context-window incident; config.py rag_context_char_budget=8000, ollama_num_ctx=8192, max_prompt_length=100000.

Exercise false positive fixed during verification: devmate-README.md (in golden-cases dir) fired PR001+PR003 because the skip rule only matched exact "readme" stems; fixed with suffix-aware is_documentation() (readme/changelog/license/contributing as exact or -/_ suffixed stems). After the fix, auditing evaluations/prompts/golden-cases yields 0 findings; a synthetic dir with registry.json correctly fires PR002+PR004 on an orphan entry. All 4 files verified LF-only (0 CRLF pairs); py_compile exits 0.

### Rationale (Why this?)

Grounding every lecture claim in verified repo paths with explicit FACT labels prevents the documentation rot the task warned about. The honest missing-path statement is itself an LLMOps lesson (governance: a registry is a promise about what exists). Demo samples were designed so each finding code fires exactly once, proving rule specificity rather than rule noise.

### Exercises

To extend: (1) implement the missing llm/prompts/ registry per lecture Example 2 and re-run the exercise auditor against it; (2) add a COST003 rule for unknown models as a first-class Finding instead of an info note; (3) wire the exercise's cost check into a CI job as the prompt-change cost diff leg; (4) run the real-dir auditor against a future prompts/ dir once DevMate week-1 deliverable lands.

### Next Steps

ci-cd, deployment tracks exist as untracked dirs from parallel work; check whether they need the same format treatment. The devmate eval gate and ADR-0009 follow-up (live gate at re-baselined number) are natural next DevMate work items.

---
