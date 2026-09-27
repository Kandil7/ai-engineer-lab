# Mistakes Log

One entry per failure you hit while working on DevMate. This file is a deliverable, not a diary (Module 1, `docs/curriculum/practice/01-llm-fundamentals-practice.md`).

Format per entry:

```
## <date> — <one-line what broke>
- Symptom: (exact error / wrong output)
- What I tried: (in order)
- Fix: (what actually worked)
- Rule: (the transferable lesson, one sentence)
```

Rules:

- Log the failure when it happens, not at the end of the day.
- The Rule line is the point — a mistake without an extracted rule will repeat.
- Re-read this file before starting any new DevMate milestone.

## 2026-09-26 — devmate ask 500 from Ollama on long questions
- Symptom: LLMError: All providers failed. Last error: 500 Internal Server Error for url 'http://localhost:11434/api/chat' — but only for some questions; short questions worked.
- What I tried: reproduced via the RAG pipeline directly (worked), then compared questions.
- Fix: not a code bug — the retrieved-context prompt exceeded qwen2.5-coder:7b's default context window. Shorter question -> fewer/smaller contexts -> fits.
- Rule: retrieval context size is part of the prompt budget; cap retrieved chunks (or set num_ctx) before blaming the provider. Module 1.1's context-budget lesson, live.

## 2026-09-26 — RESOLVED: Ollama 500 on long questions
- Fix: added ag_context_char_budget (8000 chars) enforced in RAGPipeline._build_context, and ollama_num_ctx (8192) passed as an Ollama 
um_ctx option. Regression tests: 	ests/unit/test_rag_context_budget.py (4 passing).
- Verified live: the previously-failing question now answers correctly.
- Rule: retrieval top_k is a candidate count, not a prompt guarantee — always budget the context you actually paste.
