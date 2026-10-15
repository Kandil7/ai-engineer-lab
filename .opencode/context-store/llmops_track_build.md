---
id: llmops_track_build
reported_by: builder
created_at: 2026-10-14T14:17:21.751Z
---

LLMOps track created 2026-10-14: projects/06-devops/llmops/{lectures/01-llmops-lifecycle-lecture.md (563 ln), lectures/01-llmops-lifecycle-glossary.md (604 ln), quizzes/01-llmops-lifecycle-quiz.md (346 ln), exercises/01-llmops-lifecycle.py (722 ln)}. KEY DISCOVERY: devmate/src/devmate/llm/prompts/ and prompts/registry.py DO NOT EXIST (cited by llmops README + roadmap week-1 but not on disk); only PromptTemplate schema (llm/schemas.py:179), inline RAG_SYSTEM_PROMPT (retrieve/rag.py:45), and golden cases pinned devmate.rag.answer@1.0.0 exist. Lecture documents this gap as FACT. Verified facts: CI gate ci.yml:71-77 Hit@5 1.0/MRR 0.70 offline; ADR-0009 live Hit@5 0.900 vs offline 1.000; cost.py MODEL_PRICES; guardrails.py 7 categories/4 actions; semantic_cache threshold 0.85; failure-modes.md Ollama ctx incident; rag_context_char_budget=8000. Exercise: stdlib auditor PR001-PR004 + COST001/COST002; demo bad=6 findings good=0; false positive fixed: skip-rule now suffix-aware (devmate-README.md was misflagged PR001/PR003, fixed with is_documentation()). All files LF-only, py_compile exit 0.
