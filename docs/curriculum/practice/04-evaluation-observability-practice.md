# Module 4: Evaluation & Observability — Practice Workbook

**Serves:** [`../lectures/04-evaluation-observability.md`](../lectures/04-evaluation-observability.md) | **Protocol:** [`README.md`](README.md) | **Track:** Weeks 2–3 & Week 7 (see [`../../roadmap/active-track-10-week.md`](../../roadmap/active-track-10-week.md)) | **Vehicle:** DevMate (`projects/04-ai-engineering/devmate/`)

> Mastery protocol (from [`README.md`](README.md)): **a topic is mastered when all three levels are done AND verified — not when it feels understood.**
> 🏋️ Level 1 = Drill (20–45 min, deterministic, assertable) · 💻 Level 2 = Applied (1–3 h, real DevMate artifact) · 🚀 Level 3 = Stretch (3–6 h, senior-grade, written decision).
> Interview answers are **spoken aloud, 2 minutes, recorded** (Technical English rule, track §7). When a failure mode hits you, log it in `projects/04-ai-engineering/devmate/mistakes.md`.

## How to work this workbook

1. Read each section's **real-world problem** first — it is the lens for every topic below it. If the problem doesn't hurt, you're reading the wrong problem.
2. Do Level 1 drills until the assertions pass; only then start Level 2. Rule 1 of the protocol: **verify before moving on** — no verified output, no mastery.
3. Level 2 tasks are the **actual week 2–3 and week 7 deliverables** from `docs/roadmap/active-track-10-week.md`: the golden set (`evaluations/rag/datasets/devmate-golden.jsonl`), the harness (`devmate/eval/run_ragas.py`, which `make eval` already targets and which **does not exist yet — that is your task, not a bug**), the regression gate, the traces, the drift detector. Each Level 2 names the exact file to create and a command whose output proves completion.
4. Level 3 tasks are deliberately bigger than the week. Module 2 required two ADRs with results tables (chunking, vector store); Module 4 adds **at least one more** — your choice of the ADR-style justifications flagged here. Use the format in `docs/decisions/0006-adopt-master-ai-engineering-curriculum.md`: Context → Decision Drivers → Options Considered → Decision → Consequences (non-empty) → Links. Number from the next free ID (currently 0007).
5. Track completion in the table below. The module's Definition of Done: **`make eval` prints a metrics table, a regression gate catches an injected bug, every pipeline stage appears in a trace, and cost per eval run < $0.50.**

**Local command note (this workstation):** `make` and `poetry` are not installed here. Wherever a command says `poetry run python ...`, run `& .venv\Scripts\python.exe ...` from `projects/04-ai-engineering/devmate/` instead (see the repo `AGENTS.md`). The `devmate/eval/` folder exists (empty apart from its README) — the harness below is yours to create.

## Completion tracker

| # | Topic | L1 | L2 | L3 | Evidence (file / output) |
|---|-------|----|----|----|---------------------------|
| 4.1a | Golden sets instead of single labels | ☐ | ☐ | ☐ | |
| 4.1b | LLM-as-judge + human evaluation | ☐ | ☐ | ☐ | |
| 4.1c | Regression = golden set + snapshot tests | ☐ | ☐ | ☐ | |
| 4.1d | Drift = query intent distribution | ☐ | ☐ | ☐ | |
| 4.2a | Golden set jsonl structure | ☐ | ☐ | ☐ | |
| 4.2b | Categories & coverage (8/6/4/4/3 = 25) | ☐ | ☐ | ☐ | |
| 4.2c | Quality criteria for golden sets | ☐ | ☐ | ☐ | |
| 4.3a | Context precision@k | ☐ | ☐ | ☐ | |
| 4.3b | Context recall | ☐ | ☐ | ☐ | |
| 4.3c | Faithfulness (hallucination detection) | ☐ | ☐ | ☐ | |
| 4.3d | Answer relevancy | ☐ | ☐ | ☐ | |
| 4.4a | Faithfulness judge | ☐ | ☐ | ☐ | |
| 4.4b | Relevancy judge | ☐ | ☐ | ☐ | |
| 4.4c | Judge pitfalls (stretch) | ☐ | ☐ | ☐ | |
| 4.5a | run_evaluation loop | ☐ | ☐ | ☐ | |
| 4.5b | Report aggregation | ☐ | ☐ | ☐ | |
| 4.6a | Baseline comparison & thresholds | ☐ | ☐ | ☐ | |
| 4.6b | CI integration | ☐ | ☐ | ☐ | |
| 4.7a | What to trace — every stage | ☐ | ☐ | ☐ | |
| 4.7b | Langfuse integration | ☐ | ☐ | ☐ | |
| 4.8a | Centroid shift drift detection | ☐ | ☐ | ☐ | |
| 4.8b | Drift alerting & response | ☐ | ☐ | ☐ | |
| 4.9a | Metric groups & alert thresholds | ☐ | ☐ | ☐ | |
| 4.9b | Grafana/Langfuse panels | ☐ | ☐ | ☐ | |

**Milestone Definition of Done (weeks 2–3 + week 7):** `make eval` prints a metrics table with per-question results · an injected bug (prompt or retriever) makes the regression gate fail · a trace shows all pipeline stages · cost per eval run < $0.50 · a drift alert fires on a synthetic query shift and the response (adding golden examples) is recorded.

---

# 4.1 Why LLM Evaluation Is Different

## Real-world problem: the prompt tweak that shipped a week of silent regressions

"Sana", an e-commerce support copilot, had been live for three months. A junior engineer "simplified" the system prompt one Friday — added "be concise" and reordered the instructions — and merged it. On Monday, answer quality quietly degraded: the copilot started answering from general knowledge instead of the knowledge base, and its answers got shorter but *confidently wrong*. Nothing crashed. Latency went *down*, so the infra dashboards looked better. A full week passed before users complained loudly enough that support tickets surfaced it. The team reverted the prompt and quality came back — but nobody could *prove* the prompt was the cause, and nobody could have caught it on Friday. Meanwhile, the ML team fresh from a classical-ML background proposed the "real" solution: collect 10,000 labeled answers and compute accuracy and F1. Both approaches miss the point.

**The decision you must make:** what measurement system do you build *before* anyone is allowed to touch a prompt again — knowing that (a) there is no single correct answer, (b) you can't afford human review of every change, and (c) the next regression will look exactly like this one: silent, metric-invisible, user-detected. This section gives you the four conceptual shifts (4.1a–4.1d) that make the rest of the module possible.

---

### Topic — No single correct answer → golden sets (4.1a)

**Mastery =** you can explain why exact-match accuracy is meaningless for generative output, encode "multiple valid answers" in a golden-set line, and judge acceptability against a question's *intent* rather than its wording.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

The exact-match trap, computed by hand. Question: *"What is the refund policy?"* Five answers from the same RAG system:

| # | Answer | Ground-truth intent satisfied? |
|---|--------|-------------------------------|
| A1 | "Refunds within 30 days with receipt." | Yes |
| A2 | "You can return items up to 30 days after purchase if you keep the receipt." | Yes |
| A3 | "Full refund within 30 days with receipt." | Yes |
| A4 | "Our policy is 30 days." | Partial (missing receipt condition) |
| A5 | "Refunds are handled by the payment provider." | No |

Hand-compute: exact-match accuracy vs. the reference `"Full refund within 30 days with receipt."` = **1/5 = 0.20**. Semantic acceptability (fully correct) = **3/5 = 0.60**. The same outputs, two conclusions — accuracy *hides* that 3 of 5 answers are correct. *Generative eval scores intent satisfaction, not string equality.*

Then write and run this validator against the lecture's JSONL schema (create the file in a temp dir):

```python
import json

required = {"question", "answer", "contexts", "ground_truth", "category", "difficulty"}

lines = [
    {
        "question": "What is the refund policy?",
        "answer": "Refunds within 30 days with receipt.",
        "contexts": [
            "Refund Policy: Items may be returned within 30 days with receipt."
        ],
        "ground_truth": "Full refund within 30 days with receipt.",
        "category": "policy",
        "difficulty": "easy",
    },
    {
        "question": "What is the refund policy?",
        "answer": "You can return items up to 30 days after purchase if you keep the receipt.",
        "contexts": [
            "Refund Policy: Items may be returned within 30 days with receipt."
        ],
        "ground_truth": "Full refund within 30 days with receipt.",
        "category": "policy",
        "difficulty": "easy",
    },
    {
        "question": "How do I authenticate?",
        "answer": "Use a Bearer token.",
        "contexts": [
            "Authentication: Include Authorization: Bearer <token> in requests."
        ],
        "ground_truth": "API requires Bearer token in Authorization header.",
        "category": "auth",
        "difficulty": "easy",
    },
]
assert all(set(line) == required for line in lines), "schema mismatch"
assert all(isinstance(line["contexts"], list) and line["contexts"] for line in lines), (
    "contexts must be non-empty lists"
)
qs = [l["question"] for l in lines]
assert len(qs) == len(set(qs)), (
    f"duplicate questions: {[q for q in qs if qs.count(q) > 1]}"
)
print("schema OK; lines:", len(lines))
```

Expected: prints `schema OK; lines: 3`. Note line 2: **same question, different (valid) answer** — the golden set must accept paraphrases, which is why `ground_truth` is an intent, not a transcript.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Start the week-2 milestone from the lecture case study: **10 golden questions (smoke test)** over *this* repo, with expected source files (track: "golden set first — 25 questions over this repo with expected source files").

- Create `evaluations/rag/datasets/devmate-golden.jsonl` — 10 lines, lecture schema, covering: retrieval pipeline, chunker, semantic cache, guardrails, cost tracking, CLI. Each line's `contexts` must be **real text taken from the actual DevMate source files** (read them first — e.g. `projects/04-ai-engineering/devmate/src/devmate/obs/cost.py` for cost questions).
- **Deliverable:** the file, plus the L1 validator run against it.
- **Acceptance criteria:** 10 lines; every line passes the L1 schema/duplicate asserts; for each question you can point to the source file(s) that ground the ground truth — put them in a `"metadata": {"expected_source_files": [...]}` field (the `evaluations/rag/README.md` schema permits a `metadata` object).

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Golden-set governance. The dataset is the most valuable asset in your eval stack, and it *rots*: the codebase changes, questions stop being answerable, one person's "easy" is another's "hard", and a dataset written by the same engineer who wrote the code silently encodes their blind spots. Design and implement the governance model:

- Ownership & review: who may add questions, what a review requires (schema + source grounding + difficulty), how a PR looks.
- Contamination guard: golden questions must never be added to the *training* or *index* of the system being tested (if a golden question's answer only exists because it was indexed for eval, the metric is fake).
- Refresh cadence: what triggers a re-audit (new modules, chunker changes, roadmap milestones).
- **Write an ADR-style justification** (docs/decisions/ format): Option A single-owner private file vs. Option B PR-reviewed public dataset vs. Option C automated regeneration. Consequences must include the maintenance cost you accept.

**Verify:** `python -c "import json; lines=[json.loads(l) for l in open(r'evaluations/rag/datasets/devmate-golden.jsonl', encoding='utf-8')]; assert len(lines)==10; print('ok')"` prints `ok`; the ADR exists under `docs/decisions/` (next free number) with a non-empty Consequences section.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Validator passes but file is invalid JSONL | Trailing commas / multiple JSON objects per line | `json.loads` per line, never `json.load` on the whole file; one object per line |
| `assert all(set(line) == required)` fails | Extra or missing fields | The lecture schema is the contract — no `id`; `metadata` is optional |
| Two questions are near-duplicates | No dedupe step | Normalize (lowercase, strip punctuation) before comparing; log duplicates in the QA report |
| Ground truth drifts from sources | Sources changed after writing | Every L2/L3 review re-verifies ground truth against current source files |

**Interview:** *"Why can't you evaluate an LLM system with accuracy and F1?"* Strong answer: names the core property (generative outputs have multiple valid forms → no single label), shows the 0.20 vs 0.60 trap, states what replaces labels (golden sets encoding intent + judges scoring intent satisfaction), and adds the second-order reason: even "correct" is context-dependent, which is why judge/human calibration (4.1b) exists.

---

### Topic — LLM-as-judge + human evaluation (4.1b)

**Mastery =** you can score outputs against a rubric by hand, compute agreement between two evaluators (Cohen's kappa), and explain when an LLM judge can replace a human and when it cannot.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Part 1 — rubric scoring. Given the rubric (lecture §4.4): *5 = perfect, accurate, complete, well-structured; 4 = minor omissions; 3 = partial, some errors; 2 = significant errors; 1 = fail*. Score these three answers to *"How does the semantic cache decide a hit?"* using context from `projects/04-ai-engineering/devmate/src/devmate/cache/semantic_cache.py`:

- B1: "It invalidates when the underlying documents change." → **2** (vague, not grounded in the actual mechanism)
- B2: "The semantic cache compares query embeddings to stored entries and returns a cached answer when similarity exceeds the configured threshold." → **4** (on-topic, minor imprecision)
- B3: (exact mechanism with threshold/similarity details from the real source) → **5**

Write your own score for each and justify in one sentence. Then check: would B1 get a 5 from an LLM judge that rewards length? (Save this thought — 4.4c is exactly this.)

Part 2 — Cohen's kappa by hand. Two judges score 5 DevMate answers as Acceptable (A) or Unacceptable (U):

| Item | Judge 1 | Judge 2 |
|------|---------|---------|
| Q1 | A | A |
| Q2 | A | A |
| Q3 | A | A |
| Q4 | U | U |
| Q5 | A | U |

Observed agreement Po = 4/5 = **0.80**. Expected agreement by chance: P(A) = J1-A marginal (4/5) × J2-A marginal (3/5) = 0.8 × 0.6 = 0.48; P(U) = 0.2 × 0.4 = 0.08; Pe = **0.56**. κ = (Po − Pe)/(1 − Pe) = (0.80 − 0.56)/(1 − 0.56) = 0.24/0.44 = **0.545** (moderate). Now recompute for full agreement (5/5 → κ = 1.0) and for two random judges (Po ≈ Pe → κ ≈ 0). Rule of thumb: κ ≥ 0.6 is usable; below that, the rubric is ambiguous, not the model.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Establish the human baseline for DevMate, because later (4.4c) you will compare the LLM judge against it.

1. Run 5 real questions through the CLI: `cd projects/04-ai-engineering/devmate && poetry run devmate ask "How does FixedSizeChunker split text?"` (use your golden-set questions; needs `make up` for Qdrant, or the in-memory path — see `src/devmate/retrieve/rag.py`).
2. Score the 5 answers with the 5-point rubric on **two separate passes** (e.g., morning and evening; don't re-read your first scores).
3. **Deliverable:** `evaluations/rag/reports/judge-calibration-<date>.md` — the 5 Q/A pairs, both scoring passes, the kappa between pass 1 and pass 2 (self-agreement — your *rubric reliability*), and one sentence per low-agreement item about what the rubric wording missed.
4. **Acceptance criteria:** the report contains a kappa computed by your own formula (write it as a 15-line Python function — do not import sklearn); any item where your two passes disagree is documented with the ambiguity.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Design the human-in-the-loop escalation policy. LLM judges are cheap and always-on; humans are expensive and unreliable at scale — but a judge that never gets checked drifts into confident nonsense. Design and document:

- When humans are pulled in: judge disagreement with itself (temperature>0 runs), judge score in a confidence band (e.g., 3–4 on the 5-scale), random sampling (1–5% of eval runs), and every CI failure.
- Annotation guidelines: one page a new annotator can follow, with 3 worked examples and 3 deliberately ambiguous counter-examples.
- The feedback loop: human corrections become golden cases (see `evaluations/prompts/golden-cases/devmate.jsonl` for the existing prompt-level cases).
- **Write an ADR-style justification:** Option A judge-only eval (fast, biased) vs. Option B human-only (accurate, unscalable) vs. Option C hybrid sampling (chosen). Include a cost estimate: 25-question run × judge cost vs. 25 × 5-min human review.

**Verify:** the calibration report exists with self-agreement kappa; the ADR exists with a cost comparison table (use `MODEL_PRICING` in `src/devmate/obs/cost.py` for judge cost math).

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| κ comes out negative | Judges systematically disagree (one strict, one lenient) | Recalibrate rubric with anchor examples; train both judges on the same 3 anchors before scoring |
| Kappa = 1.0 on first try | Rubric too coarse (everything is 5) | If every score is the top bucket, the rubric cannot distinguish quality — tighten it |
| Human scores drift over a long session | Fatigue | Randomize item order, cap sessions, score in two passes (that's the L2 drill's point) |
| Judge and human agree 95% on easy questions, 40% on hard ones | Easy items dominate agreement | Report kappa *per difficulty band*, not globally |

**Interview:** *"How do you know your LLM judge is any good?"* Strong answer: defines the calibration loop (judge vs. human on a labeled sample → kappa → threshold for trusting the judge), names the failure (high agreement on easy items, low on hard), and states the escalation policy (humans review judge disagreements, low-confidence scores, and CI failures).

---

### Topic — Regression = golden set + snapshot tests, not metric comparison only (4.1c)

**Mastery =** you can explain why metric-only regression misses prompt/content changes, and can write a snapshot test that pins a prompt to a versioned reference.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

The metric-blind change. Two system prompts produce *identical* metrics on a golden set but different production behavior — because metrics measure *output quality*, not *input contract*. Example: weakening `RAG_SYSTEM_PROMPT`'s "Use ONLY the information provided in the context" to "Use the context" keeps faithfulness roughly stable on easy questions (retrieval still works) while quietly permitting more hallucination on hard ones (the grounding guard is weaker).

Write a snapshot test for the current prompt. Read `projects/04-ai-engineering/devmate/src/devmate/retrieve/rag.py` and assert:

```python
import hashlib, sys

sys.path.insert(0, r"projects/04-ai-engineering/devmate/src")
from devmate.retrieve.rag import RAG_SYSTEM_PROMPT

assert "Use ONLY the information provided in the context" in RAG_SYSTEM_PROMPT
assert "[Source" in RAG_SYSTEM_PROMPT  # citation instruction is part of the contract
version = hashlib.sha1(RAG_SYSTEM_PROMPT.encode()).hexdigest()[:10]
print("prompt version:", version)
```

Expected: prints a 10-hex-char version. The point: **a snapshot pins the prompt itself**, so a change that keeps metrics green but alters the contract still fails a test. Explain in one sentence why the snapshot *complements* metric regression (metrics catch quality loss; snapshots catch contract drift).

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `projects/04-ai-engineering/devmate/tests/unit/test_prompt_snapshot.py` containing: (1) the content asserts above (the "ONLY information" clause, citation markers), (2) a version-hash test that pins the *current* hash with a comment explaining what moved the hash last time, (3) a test that `_build_context` output starts with `[Source 1:` for a canned 2-chunk input (read `_build_context` at line 77 of `rag.py` first).
- **Deliverable:** the test file. **Acceptance criteria:** `cd projects/04-ai-engineering/devmate && poetry run pytest -q tests/unit/test_prompt_snapshot.py` → all pass; then deliberately append a space to `RAG_SYSTEM_PROMPT` locally, rerun (hash test must fail), and **revert** — you just proved the test catches prompt edits that metrics would not flag.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Prompt registry design. DevMate has prompts in three places today: `RAG_SYSTEM_PROMPT` in `src/devmate/retrieve/rag.py`, agent prompts in `src/devmate/agent/agent.py`, and golden prompt cases in `evaluations/prompts/golden-cases/` (reviewer/planner/debugger). Scattered snapshot tests don't scale. Design a versioned prompt registry:

- Move prompts to a `src/devmate/llm/prompts/` package with per-prompt version fields, a registry dict, and a snapshot manifest (`evaluations/prompts/prompt-manifest.json`) that CI diffs.
- Snapshot policy: which prompt changes require *human* review vs. only CI (system prompts that touch grounding/safety → human; cosmetic rewording → CI).
- **Write an ADR-style justification:** scattered constants vs. registry + manifest vs. external prompt store (Langfuse prompts / promptfoo). Reference the week-7 case study — the 0.91→0.82 faithfulness regression was a *system prompt* change; the registry exists to make the next one trivially visible.

**Verify:** pytest green; ADR exists with Consequences.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Snapshot test fails on every commit | Prompt hash pinned to volatile content (timestamps, randomness) | Hash only the *stable* prompt text; strip runtime placeholders |
| Snapshot test passes but prompt is broken | Test asserts the wrong surface (e.g., only the first 40 chars) | Assert semantic clauses AND the full-hash version; both move together |
| Everyone ignores the snapshot test | It fails so often it gets deleted | The registry (L3) makes prompt changes a deliberate, reviewed event |
| Metrics say "no regression" but users complain | No snapshot ever existed for the changed prompt | Every prompt gets a snapshot the day it's written, not after the incident |

**Interview:** *"Why is 'metrics didn't change' not proof that a prompt change is safe?"* Strong answer: metrics sample *output quality* on a fixed golden set; a prompt change can alter the *input contract* (grounding clause, citation instruction) in ways that only show up on harder queries or new categories; snapshot tests pin the contract itself; regression detection needs both.

---

### Topic — Drift = query intent distribution, not feature distribution (4.1d)

**Mastery =** you can bucket queries by intent, measure distribution shift between reference and recent periods, and explain why classical feature-distribution drift doesn't apply to free-text queries.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Hand-compute intent drift. Reference period — the golden set's category budget (lecture §4.2): **8 factual, 6 procedural, 4 debugging, 4 architecture, 3 edge = 25 queries** → proportions 32% / 24% / 16% / 16% / 12%.

Recent period — 20 DevMate-ish queries: *6 factual, 4 procedural, 8 debugging, 1 architecture, 1 edge* → proportions 30% / 20% / **40%** / 5% / 5%.

Compute per-category deltas: factual −2 pts, procedural −4, debugging **+24 pts**, architecture −11, edge −7. This mirrors the lecture case study (week 5): *"fix bug in..."* queries grew ~40% relative — debugging intent went from 16% to 40% of traffic. Explain why this is *intent* drift, not feature drift: free-text queries have no fixed feature schema, so there is no feature distribution to monitor; the *distribution of intents* is the invariant you can define and count. Then run:

```python
ref = {"factual": 8, "procedural": 6, "debugging": 4, "architecture": 4, "edge": 3}
recent = {"factual": 6, "procedural": 4, "debugging": 8, "architecture": 1, "edge": 1}
ref_t, rec_t = sum(ref.values()), sum(recent.values())
deltas = {c: recent[c] / rec_t - ref[c] / ref_t for c in ref}
assert abs(deltas["debugging"] - 0.24) < 1e-9, deltas
assert abs(deltas["architecture"] - (-0.11)) < 1e-9
print({c: round(v * 100, 1) for c, v in deltas.items()})
```

Expected: `{'factual': -2.0, 'procedural': -4.0, 'debugging': 24.0, 'architecture': -11.0, 'edge': -7.0}`.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Produce the intent baseline report.

1. Reference distribution: your golden-set categories (from 4.2 once complete; until then use the budget above).
2. Recent sample: write **20 synthetic queries** reflecting *actual* DevMate development tasks in `docs/roadmap/active-track-10-week.md` (e.g., "Why does the semantic cache miss so often?", "How do I add a guardrail?", "What does the MCP server expose?", "fix bug in retriever top_k"). Tag each with an intent category by hand.
3. **Deliverable:** `evaluations/rag/reports/query-intent-baseline-<date>.md` — both distributions, the delta table, the top-3 shifted intents, and a 3-line interpretation (what would you do if debugging really hit 40%?).
4. **Acceptance criteria:** report exists; deltas match hand computation; interpretation names at least one concrete response (add golden examples, add index content, reranker tuning).

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Benign vs. harmful drift. Not every shift is a problem: a product launch adds a feature → "How do I use X?" floods in (benign, expected). But a shift toward *debugging* queries while the debugger agent is broken is harmful. Design the classification:

- Define per-category *expected* shifts (from a product calendar) and *unexpected* triggers.
- Build a simple decision rule: harmful drift = intent shift **and** quality degradation in that same category (faithfulness per intent category).
- **Write an ADR-style justification:** Option A uniform drift score (one number, simple, noisy) vs. Option B per-category drift with quality coupling (chosen — matches the week-5 story where faithfulness recovered only after adding bug-fix golden examples). Include the false-positive math: with 5 categories and a 5% false-alarm rate per category, a uniform alert fires weekly even when nothing is wrong.

**Verify:** report exists; the decision rule documented; ADR with the false-alarm table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| "Drift" fires when nothing changed | Counting raw query text (phrasing changes) instead of intents | Always bucket into a fixed category taxonomy before measuring |
| Real drift invisible | Category taxonomy too coarse (everything is "general") | Taxonomy should match your product's intents; revisit quarterly |
| Team ignores drift reports | No decision attached to the number | Every drift report ends with "if > X, we do Y" — the response playbook (4.8b) |
| Classical-ML mindset applied | Monitoring token/feature distributions | Monitor *intent distribution* + per-intent quality; features are the symptom, intents are the cause |

**Interview:** *"You have a monitoring system for a classical ML model. What breaks when you point it at an LLM copilot?"* Strong answer: feature schemas are fixed in classical ML but free-text queries have no fixed schema; the analog of feature drift is *intent distribution* drift; and quality itself needs a judge, not a label. Bonus: mentions per-intent quality coupling (harmful = shifted + degraded).

---

# 4.2 Golden Dataset Creation

## Real-world problem: perfect metrics, broken product

"DocsAI", a developer-docs assistant, launched with a 25-question golden set written by one engineer — all from the README and the quickstart page. Eval looked great: context precision 0.9, faithfulness 0.95. Users, however, asked the questions the dataset never sampled: *"How do I configure the MCP server?"*, *"Why does the guardrail block my query?"*, *"What happens if the vector DB is down?"* — and the assistant gave confident wrong answers. The team "fixed" it by buying a bigger model; metrics didn't move; users still left. The dataset was the problem: **coverage is the product**, and a golden set that samples only what's easy to write predicts only what's easy to answer.

**The decision you must make:** how to build 25 questions whose coverage *actually* predicts production — schema (4.2a), category budget (4.2b), and quality bar (4.2c) — knowing that every question you don't write is a failure mode you'll meet in production.

---

### Topic — jsonl structure: question/answer/contexts/ground_truth/category/difficulty (4.2a)

**Mastery =** you can write, validate, and extend golden-set lines in the exact lecture schema without corrupting the file, and you can defend each field's purpose.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Write 3 golden lines by hand for DevMate (real content, from real files you read):

1. **Factual/easy:** "What is the default chunk size of the fixed chunker?" — read `src/devmate/ingest/chunker.py` for the true default (do not invent numbers).
2. **Procedural/medium:** "How do I run the DevMate CLI to ask a question?" — ground it in the root `Makefile` (`make cli ARGS="ask '...'"`) and `src/devmate/cli/main.py`.
3. **Architecture/hard:** "What is the role of the reranker in the query pipeline?" — ground it in `src/devmate/retrieve/retriever.py` (`get_reranker`, `NoOpReranker` vs `CohereReranker`).

Each line: `question`, `answer` (2–3 sentences, citing sources `[1]`), `contexts` (2+ strings verbatim from the real files), `ground_truth` (one verifiable sentence), `category`, `difficulty`. Then extend the 4.1a validator to also assert: `contexts` length ≥ 2; every `ground_truth` appears (as a substring or paraphrase you can point to) in some `contexts` entry; `difficulty ∈ {easy, medium, hard}`; `category ∈ {factual, procedural, debugging, architecture, edge}`. Expected output: `schema OK; lines: 3` plus a per-line source file you can name aloud.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Build the validator as a real module and validate your 10-line smoke set from 4.1a.

- Create `projects/04-ai-engineering/devmate/eval/dataset_validate.py` with `validate_dataset(path) -> dict` returning: line count, duplicate questions, missing/invalid fields, per-category counts, per-difficulty counts, and a list of questions whose ground truth is not covered by any context entry (substring match is fine for now).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_dataset_validate.py` with cases: valid file passes; **empty file → error** (edge case: an empty golden set must fail loudly, not silently pass); duplicate question → flagged; ground truth missing from contexts → flagged.
- **Deliverable:** both files. **Acceptance criteria:** `cd projects/04-ai-engineering/devmate && poetry run pytest -q tests/unit/test_dataset_validate.py` green; `poetry run python eval/dataset_validate.py evaluations/rag/datasets/devmate-golden.jsonl` prints the stats table for your 10 lines (run from `projects/04-ai-engineering/devmate` with the repo-relative path, or adjust to the absolute path).

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Schema evolution. The roadmap requires "expected source files" per question (`expected_source_files`); `evaluations/rag/README.md` documents `expected_context`/`expected_answer` (an older schema); the lecture schema has `contexts`/`ground_truth`. Three schemas in one workspace — design the migration:

- Map all three schemas to one canonical JSONL (lecture schema + `expected_source_files` in `metadata`), write a one-way migrator, and update `evaluations/rag/README.md`'s schema table.
- **Write an ADR-style justification:** canonical lecture schema vs. union of all fields vs. per-tool schemas. Consequences must cover: what breaks (existing baselines/reports referencing old fields), what the validator enforces, and the migration test that proves the 10-line dataset survives a round-trip.

**Verify:** migrator round-trips your dataset (validate before == validate after, plus the new field present); ADR exists; README schema table updated (this workbook's file is the only *new* file besides these deliverables — editing README is part of this task).

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Golden file won't parse | Hand-edited JSONL with a stray comma or multi-line string | One object per line; strings escaped; validator as the first gate in CI (4.6b) |
| Contexts don't match the real code | Copy-pasted from an old version | Ground contexts by reading the file at write-time; re-audit on module changes |
| Ground truth not in any context | Question written from memory | If GT isn't derivable from contexts, retrieval can never succeed — the question tests nothing |
| `difficulty` is really `category` | Subjective labels | Define difficulty operationally: easy = answer in 1 chunk; medium = 2–3 chunks; hard = synthesis across modules |

**Interview:** *"Walk me through one line of your golden dataset and justify every field."* Strong answer: question (intent), answer (expected output shape, with citations), contexts (the retrievable evidence — if GT isn't in contexts the test is invalid), ground_truth (the verifiable intent), category + difficulty (coverage budgeting). Bonus: mentions `metadata` for `expected_source_files`, and that the validator runs in CI.

---

### Topic — Categories & coverage: 8 factual + 6 procedural + 4 debugging + 4 architecture + 3 edge = 25 (4.2b)

**Mastery =** you can allocate a question budget across intents, defend the ratio, and prove your dataset covers the modules users actually hit.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Here are 25 proposed DevMate questions (short titles). Assign each a `category` (factual/procedural/debugging/architecture/edge) and a `difficulty` (easy/medium/hard), then verify the budget:

| # | Question (title) | Category | Difficulty |
|---|------------------|----------|------------|
| 1 | What chunk sizes does the fixed chunker support? | factual | easy |
| 2 | What extensions does DocumentLoader skip? | factual | easy |
| 3 | How do I run the CLI `ask` command? | procedural | easy |
| 4 | How does the cost tracker compute USD from tokens? | procedural | medium |
| 5 | Where does `tracer` export spans when Langfuse keys are missing? | factual | easy |
| 6 | How do I enable guardrails in the API? | procedural | medium |
| 7 | Why does the semantic cache miss on paraphrased queries? | debugging | medium |
| 8 | Why is my reranker not affecting results? | debugging | medium |
| 9 | How do I add a new embedding provider? | procedural | hard |
| 10 | What does `retrieve` return when the store is empty? | edge | medium |
| 11 | How does RAGPipeline build citation markers? | architecture | medium |
| 12 | What happens if the LLM API returns a 429? | edge | medium |
| 13 | How does the MCP server expose retrieval tools? | architecture | medium |
| 14 | Why does my guardrail block legitimate queries? | debugging | hard |
| 15 | What is the role of the agent module vs the RAG pipeline? | architecture | hard |
| 16 | How do I run the integration tests? | procedural | easy |
| 17 | What does the CLI `stats` command output? | factual | easy |
| 18 | How does the trace parent-child hierarchy work? | architecture | medium |
| 19 | What happens if two ingests run concurrently? | edge | hard |
| 20 | How do I change the retrieval top-k? | procedural | easy |
| 21 | Why does faithfulness drop when I add more context chunks? | debugging | hard |
| 22 | What is the default reranker and why is it a no-op? | factual | medium |
| 23 | How does the DB layer store eval runs? | procedural | hard |
| 24 | What happens on an empty query string? | edge | easy |
| 25 | How does the cache interact with the guardrails? | architecture | hard |

Check: factual = 8, procedural = 6, debugging = 4, architecture = 4, edge = 3 — **if your assignment doesn't sum, re-bucket and record the final table** (the discipline is the drill). Difficulty: easy = 10, medium = 10, hard = 5 → the 40/40/20 rule (10/25 = 40%, 10/25 = 40%, 5/25 = 20%). Assert the totals:

```python
cats = {}  # fill from your final table
assert cats == {
    "factual": 8,
    "procedural": 6,
    "debugging": 4,
    "architecture": 4,
    "edge": 3,
}
print("category budget OK:", cats)
```

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Complete the golden set: extend `evaluations/rag/datasets/devmate-golden.jsonl` from 10 to **25 questions** hitting the exact budget above. Ground every question in a real file under `projects/04-ai-engineering/devmate/src/` (add `"expected_source_files"` in `metadata`). Then run your validator — it must print category counts **8/6/4/4/3** and difficulty counts **10/10/5**.

- **Deliverable:** the 25-line dataset + validator output pasted into `evaluations/rag/reports/dataset-coverage-<date>.md`.
- **Acceptance criteria:** validator passes (no duplicates, all ground truths covered by contexts); the coverage report maps each category to the modules it exercises (retrieve, guards, cache, obs, llm, ingest, index, agent) and flags any module with **zero** questions.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Module-coverage audit with a decision. Your 25 questions probably leave modules uncovered (the CLI, the MCP server, the DB layer). Write a script `devmate/eval/coverage_audit.py` that maps each golden question's `expected_source_files` to top-level modules and prints a coverage matrix (module × count). Then answer: which uncovered modules are *acceptable* (stable, rarely queried) and which are *risky* (new, user-facing)? Extend the dataset for the risky ones — even if it breaks the 8/6/4/4/3 budget — and **document that decision**.

- **Write an ADR-style justification:** Option A strict budget forever (coverage by intent only) vs. Option B budget + module coverage (chosen — intent coverage predicts *what* users ask, module coverage predicts *whether* the answer exists). Consequences: dataset size grows, eval cost grows, but the DocsAI failure mode (perfect metrics, broken product) is directly addressed.

**Verify:** `poetry run python eval/coverage_audit.py` prints the matrix; ADR exists; dataset still passes `dataset_validate.py` (duplicates/GT checks are hard, the budget check is advisory).

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| All 25 questions are factual | Factual questions are easiest to write | Use the budget as a hard constraint — write the hard categories *first* |
| 25 questions but only 3 modules touched | Questions written from one source area | Run coverage_audit after every addition |
| Difficulty inflation ("everything is hard") | No operational definition | Easy = 1 chunk, medium = 2–3 chunks, hard = cross-module synthesis (write it into the QA report) |
| Dataset passes but production fails | Budget satisfied, coverage wrong | The DocsAI lesson: budget is necessary, module coverage is sufficient |

**Interview:** *"Why 8/6/4/4/3? Why not 25 random questions?"* Strong answer: intent categories map to failure modes (debugging questions catch retrieval/grounding failures, edge questions catch guardrail/handling gaps); the budget forces deliberate sampling; module coverage catches the "all questions from the README" trap.

---

### Topic — Quality criteria: one clear intent, verifiable ground truth, sufficient context, balance, 40/40/20 (4.2c)

**Mastery =** you can audit a golden line against five criteria, identify which production failure each criterion prevents, and run a review process that catches bad lines before they poison the baseline.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Audit these 5 flawed lines. For each, name the violated criterion (one clear intent / verifiable ground truth / sufficient context / balance / difficulty spread) and the production failure it would cause:

- L1: `"How does the cache work and what is the cost of a miss and why is the embedding model slow?"` → **multiple intents** (violates one-clear-intent); eval can't tell which failure caused a low score.
- L2: `"What is the best chunk size?"` with ground_truth `"512 tokens"` but contexts containing no chunk-size discussion → **ground truth not verifiable from contexts**; the test is unanswerable by construction.
- L3: `"How do I add a guardrail?"` with contexts = `["Guardrails exist."]` → **insufficient context**; the answer can't be grounded, so faithfulness is forced down by the dataset, not the model.
- L4: 15 of 25 questions are procedural → **balance violated**; eval averages hide the underrepresented categories.
- L5: 20 easy + 5 medium, zero hard → **difficulty spread violated**; the dataset can't detect regressions on the hard cross-module questions users hit hardest.

Then rewrite L3 properly: read `src/devmate/guards/guardrails.py` (`GuardrailManager`, `enable`, `set_action`) and write question + 2 real contexts + verifiable ground truth. Assert: GT covered by contexts; exactly one interrogative intent.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Run the full QA pass on your 25-question dataset:

1. For every question, fill a checklist: one intent? GT verifiable from sources? contexts sufficient (≥ 2, from real files)? category balanced? difficulty labeled with the operational definition?
2. Fix every question that fails.
3. **Deliverable:** `evaluations/rag/reports/golden-set-qa-<date>.md` — the checklist table (25 rows), issues found and fixes applied, final category/difficulty counts.
4. **Acceptance criteria:** zero "fail" cells except documented exceptions; validator clean; the report states the count of questions rewritten during QA (a real dataset needs 3–6 rewrites on first pass — if you rewrote zero, re-check your standards).

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

The two-reviewer protocol. One person's "one clear intent" is another's compound question. Run the QA as a two-reviewer exercise (grab a human reviewer, or simulate with a second session ≥ 24 h later):

- Both reviewers independently mark each of the 25 questions pass/fail on *one-clear-intent* and *GT-verifiable*.
- Compute Cohen's kappa per criterion (reuse your 4.1b kappa function). κ < 0.6 means the criteria are ambiguous — rewrite the criteria page, not the dataset.
- **Write an ADR-style justification:** single-reviewer QA vs. two-reviewer with kappa gate (chosen for the baseline; relaxed for subsequent edits). Consequences: 2× QA cost, but a baseline built on ambiguous labels teaches the judge the wrong thing — the 4.4c judge-agreement problem starts here.

**Verify:** QA report exists with kappa per criterion; ADR exists; dataset still passes validator.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| QA says pass, a week later a question is obviously broken | Reviewer bias (own dataset) | Two-reviewer protocol; minimum 24 h between writing and reviewing |
| GT "verifiable" but actually loosely paraphrased | Verifiability not checked against source text | GT must be derivable from the listed contexts — mechanically checkable |
| Difficulty labels drift between sessions | No operational definition | Easy/medium/hard definitions written into the QA report header |
| One category silently shrinks after edits | Fixes don't re-check budget | Re-run `dataset_validate.py` after every edit — it prints the budget |

**Interview:** *"Your golden set is done. How do you know it's good?"* Strong answer: five criteria named with the failure each prevents; measurable checks (validator, kappa, budget); and the honest admission that a golden set is a *living artifact* with a review cadence, not a one-time deliverable.

---

# 4.3 RAGAs Metrics Deep Dive

## Real-world problem: the retrieval tuning war

The DevMate team is arguing about chunk size. The retriever person says precision is fine; the generator person says answers are wrong; the PM says users complain about irrelevant citations. Each side has a metric, and each metric is *right about a different thing*: precision@k measures *purity of what you retrieved*, recall measures *whether the right chunk was in reach at all*, faithfulness measures *whether the answer stayed grounded*, and answer relevancy measures *whether the answer addressed the question*. None of them alone explains the failure — and two of them (4.3b, 4.3d) have traps that make them lie exactly when you trust them most.

**The decision you must make:** which metrics to compute per change, what each number means when it moves, and where each metric is too blind to be the only gate. The drills below make you compute all four by hand on tiny examples, so that when the harness prints 0.83 you *know* what it means.

---

### Topic — Context precision@k: math, worked example, top-k vs all (4.3a)

**Mastery =** you can compute precision@k by hand, explain why k and ordering matter, and state when precision hides a retrieval problem.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Worked example 1. Retrieved order: `[A, B, C, D, E]`. Relevant set: `{A, C}`.

- precision@1 = A relevant → **1.0**
- precision@2 = {A, B} → 1 relevant → **0.5**
- precision@3 = {A, B, C} → 2 relevant → **2/3 ≈ 0.667**
- precision@4 = 2/4 = **0.5**; precision@5 = 2/5 = **0.4**

Worked example 2 (ranking matters). Same relevant set, retrieved order `[C, A, B, D, E]`: precision@2 = {C, A} → **1.0** vs. 0.5 in example 1. Same five chunks, different ranking — precision@k at small k exposes it; "precision over all retrieved" = 2/5 = 0.4 in **both** cases and cannot. That is the top-k vs all point: **precision@k is a ranking metric; precision over all retrieved is not.**

```python
def context_precision_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    return sum(1 for c in top_k if c in relevant) / k


r1 = ["A", "B", "C", "D", "E"]
rel = {"A", "C"}
assert context_precision_at_k(r1, rel, 5) == 0.4
assert context_precision_at_k(["C", "A", "B", "D", "E"], rel, 2) == 1.0
assert context_precision_at_k(r1, rel, 3) == 2 / 3
assert context_precision_at_k(r1, rel, 1) == 1.0
print("precision@k OK")
```

Expected: `precision@k OK`. Edge case to decide and defend: `k > len(retrieved)` — divide by k, not by len(retrieved) (RAGAs divides by k).

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Implement the metric in the planned eval module.

- Create `projects/04-ai-engineering/devmate/eval/metrics.py` with `context_precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float` (guard `k <= 0` → error; empty retrieval → 0.0, not crash).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_eval_metrics.py` covering the two worked examples + the empty-retrieval edge case.
- **Deliverable:** both files. **Acceptance criteria:** `cd projects/04-ai-engineering/devmate && poetry run pytest -q tests/unit/test_eval_metrics.py` → all green. The real `RAGResult.contexts` (see `src/devmate/retrieve/rag.py`; `RerankResult` in `retriever.py`) carries chunk ids — your function will receive those ids in 4.5a.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Which retrieval metric gates CI? precision@k (purity), recall@k (coverage), MRR (first-hit rank). The roadmap's harness computes recall@5, recall@10, and MRR — but not precision@k. Analyze: for DevMate (top-k = 5, default reranker is `NoOpReranker` in `get_reranker("none")`), which single metric would have caught the Q6-style failure in `evaluations/rag/reports/2026-06-26-baseline.md` (validator file missing → recall drop, precision unaffected)?

- Build a comparison table on synthetic data: a retrieval change that (a) adds junk at positions 4–5 → precision@5 drops, recall flat; (b) drops a relevant chunk → recall drops, precision may rise; (c) moves the first relevant hit from rank 1 to rank 4 → MRR drops, precision@5 flat.
- **Write an ADR-style justification:** gate on precision@5 vs recall@5 vs MRR vs a composite. Consequences must state which failure mode each choice *cannot see*.

**Verify:** pytest green; comparison table in the ADR; the ADR's Decision names the gate metric(s) for CI and the revisit condition (e.g., when a reranker ships).

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Precision high, users still complain | Precision can't see *missing* chunks (recall's job) | Never gate on precision alone; pair with recall |
| precision@5 = 0.4 but looks "fine" in averages | One hard question dragged it | Per-question results in the report (4.5b), not just the mean |
| Function crashes on empty retrieval | No guard | Empty retrieval → 0.0 with a warning in the report |
| Precision "improved" after a change | Change reduced top-k (fewer chances to be wrong) | Record top-k in the report config; compare like-for-like |

**Interview:** *"What does context precision@5 = 0.83 tell you, and what does it hide?"* Strong answer: on average ~4 of 5 retrieved chunks were relevant; it hides missing chunks (recall), first-hit ranking (MRR), and everything downstream of retrieval (faithfulness).

---

### Topic — Context recall: math, worked example, why it needs the full relevant set (4.3b)

**Mastery =** you can compute recall, and you can explain — with a worked example — why an incomplete `relevant` list silently inflates the score until it is meaningless.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Worked example 1 (complete relevant set). Corpus has 4 relevant chunks `{c1, c2, c3, c4}`. Retrieval returned `[c1, c2, c5, c6]`. recall = |{c1,c2} ∩ {c1,c2,c3,c4}| / 4 = **2/4 = 0.5**.

Worked example 2 (the trap). The "ground truth" relevant list was written by someone who only knew of `{c1}`. Same retrieval → recall = |{c1,c2} ∩ {c1}| / 1 = **1.0**. The retrieval got *worse at nothing* — the *label* got shorter. **Recall without a complete relevant set is a tautology: list one relevant chunk and every retrieval scores 1.0.**

The lesson: recall@5 = 0.79 in the lecture baseline is only meaningful if someone enumerated *all* chunks that answer each question.

```python
def context_recall(retrieved, all_relevant):
    return len(set(retrieved) & set(all_relevant)) / len(all_relevant)


assert context_recall(["c1", "c2", "c5", "c6"], ["c1", "c2", "c3", "c4"]) == 0.5
assert context_recall(["c1", "c2", "c5", "c6"], ["c1"]) == 1.0  # the trap
print("recall OK")
```

Expected: `recall OK`. Write one sentence: *which of the two numbers would you ship in a report, and what footnote would you add?*

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Add `context_recall_at_k(retrieved_ids, relevant_ids, k)` and `mrr(retrieved_ids, relevant_ids)` to `devmate/eval/metrics.py` (recall@5, recall@10, MRR per the roadmap's harness spec).
- Tests in `test_eval_metrics.py`: the two worked examples above, MRR for first-hit-at-rank-3 (→ 1/3) and no-hit (→ 0.0).
- **Deliverable:** metrics + tests. **Acceptance criteria:** pytest green. Note in a docstring: *relevant_ids must be the FULL relevant set — this is a labeling contract, not a code detail.*

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

The relevant-set discovery problem. For DevMate's 25 golden questions, who guarantees `relevant_ids` is complete? Build a discovery workflow:

- Draft: use a stronger retriever (larger top-k, hybrid) + an LLM to propose candidate relevant chunks per question; a human verifies.
- Measure: on 5 questions, compare recall computed with (a) your original list, (b) the expanded list. Expect recall to *drop* when the list grows — that drop is the truth, not a regression.
- **Write an ADR-style justification:** manual relevant-set annotation vs. LLM-assisted discovery vs. "recall only on categories where completeness is cheap" (e.g., code questions where the answer lives in exactly one file). Consequences must include the labeling cost per question and the risk of the 4.3b trap returning.

**Verify:** the 5-question before/after recall table in the ADR; pytest green.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Recall is suspiciously high (0.95+) | Relevant list is a subset of what retrieval returns | Audit completeness with the L3 discovery workflow |
| Recall drops after "improving" the dataset | You added relevant chunks you previously missed | The drop is correct — re-baseline, don't "fix" it |
| Recall and precision move together | Both are sensitive to retrieval size | Report config (top-k) alongside every number |
| recall@5 > recall@10 | Impossible (monotonicity) — means a bug | recall@k must be monotonic in k; assert it in tests |

**Interview:** *"Why does context recall need the full relevant set?"* Strong answer: the denominator is the label; shrink the label and recall inflates to 1.0; recall measures whether the answer was *reachable*, which is meaningless if you only marked chunks you knew were reachable. Bonus: connects to the Q6 story in `2026-06-26-baseline.md` (validator file missing from the index — recall caught it, precision couldn't).

---

### Topic — Faithfulness: claim extraction, supported/total, hallucination detection (4.3c)

**Mastery =** you can split an answer into claims, judge support against context, compute faithfulness, and handle the degenerate cases (zero claims, partial support).

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Answer: *"The semantic cache stores query embeddings and returns cached results when similarity exceeds the threshold. It is the fastest component in the pipeline. It also compresses stored payloads using zlib."* Context (from `src/devmate/cache/semantic_cache.py` — read it): mentions embedding storage and a similarity threshold; nothing about speed; nothing about compression.

Split into claims and mark support:

| Claim | Supported? |
|---|---|
| C1: stores query embeddings | YES |
| C2: returns cached results above a similarity threshold | YES |
| C3: fastest component in the pipeline | NO (opinion, not in context) |
| C4: compresses payloads with zlib | NO (hallucination) |

Faithfulness = supported / total = 2/4 = **0.5**. Grading rule: *partially* supported claims count as unsupported (decide this explicitly — RAGAs treats partial as unsupported). Degenerate case you must define: **zero claims → score 1.0** (nothing to hallucinate; never divide by zero), or skip the question — pick one and write it in your code comment.

```python
def faithfulness(claims):  # claims = list[bool] supported?
    total = len(claims)
    return sum(claims) / total if total else 1.0


assert faithfulness([True, True, False, False]) == 0.5
assert faithfulness([True, True, True]) == 1.0
assert faithfulness([]) == 1.0  # zero-claims rule
assert faithfulness([False]) == 0.0
print("faithfulness OK")
```

Expected: `faithfulness OK`.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Add `parse_faithfulness_claims(text: str) -> list[bool]` to `devmate/eval/metrics.py` parsing the lecture's structured format (`Claim N: [text] - SUPPORTED: YES/NO`). Malformed lines → skip with a warning (the judge's output is untrusted input — see 4.4a).
- Add `faithfulness(supported: list[bool]) -> float` with the zero-claims rule.
- Tests: the 4-claim example (0.5), a malformed line mixed into the text, zero claims.
- **Deliverable:** metrics + tests. **Acceptance criteria:** `poetry run pytest -q tests/unit/test_eval_metrics.py` green.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Claim granularity calibration. An answer's claims can be split coarsely (2 claims) or finely (10 claims). Granularity changes the score: one hallucination buried in a 10-claim answer → 0.9; the same hallucination in a 2-claim answer → 0.5. Both describe the same answer. Calibrate:

- Take 5 real DevMate answers; write claim-splitting rules (one claim per independent assertion; numbers/names are part of the claim, not separate claims); re-split until two independent annotators agree (kappa again).
- Measure score variance across splitting styles; document the rule in the judge prompt (4.4a) so the judge and the evaluator split alike.
- **Write an ADR-style justification:** coarse vs. fine claim granularity, and whether to count "partial" as unsupported. Consequences: judge cost (fine = longer outputs), score stability, and which production failures each choice hides (coarse hides small hallucinations; fine inflates the denominator).

**Verify:** the calibration table (splitting style × score per answer) in the ADR; parser tests green.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Faithfulness always ~1.0 | Judge splits claims to match context (leads the answer) | Judge prompt: extract claims *before* judging; temperature 0 |
| Faithfulness swings wildly between runs | Judge output format varies | Strict parser + fallback; log unparseable judge outputs (4.4a) |
| Zero claims → crash | Division by zero | Zero claims → 1.0 (or skip), never crash; test it |
| Hallucination invisible in averages | One bad answer averaged into 0.95 | Per-question faithfulness in the report; gate on the *minimum*, not the mean (4.6a) |

**Interview:** *"Walk me through computing faithfulness on an answer."* Strong answer: split into claims → each claim marked supported/unsupported against context (partial = unsupported) → supported/total → degenerate cases defined (zero claims, malformed judge output) → and the honesty point: faithfulness is only as good as the claim splitter and the judge (4.4a).

---

### Topic — Answer relevancy: embedding similarity, limitations (short answers game the metric) (4.3d)

**Mastery =** you can compute cosine similarity by hand, and you can demonstrate — with numbers — how a short, low-information answer scores higher than a correct, verbose one.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

2-dimensional toy embeddings (the lecture's `answer_relevancy` is cosine similarity between question and answer embeddings):

- Question q = (1.0, 0.0).
- Answer A (good, detailed): a = (0.8, 0.6) → cos(q, a) = (0.8·1.0 + 0.6·0.0) / (√(0.64+0.36) · √1) = 0.8 / 1.0 = **0.80**.
- Answer B (short, evasive): b = (0.95, 0.05) → cos = 0.95 / √(0.9025 + 0.0025) = 0.95 / 0.9513 ≈ **0.9986**.

**The short answer scores higher (0.9986 > 0.80) while being useless.** Embeddings measure *topical proximity*, not *informativeness* — a one-word answer that mirrors the question's vocabulary gets near-maximum relevance. This is the metric's known gaming failure: it rewards echoing the question.

```python
import math


def cosine(u, v):
    return sum(a * b for a, b in zip(u, v)) / (
        math.sqrt(sum(x * x for x in u)) * math.sqrt(sum(x * x for x in v))
    )


q, good, short = (1.0, 0.0), (0.8, 0.6), (0.95, 0.05)
assert abs(cosine(q, good) - 0.80) < 1e-9
assert abs(cosine(q, short) - 0.9986) < 1e-3  # short beats good
print("relevancy OK — short answer scores", round(cosine(q, short), 4))
```

Expected: `relevancy OK — short answer scores 0.9986`.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Add `answer_relevancy(question: str, answer: str, embed_fn) -> float` to `devmate/eval/metrics.py` (embed_fn injectable — the real one comes from `src/devmate/index/embeddings.py` `EmbeddingService`).
- Tests with a fake `embed_fn` returning the 2-d vectors above: good = 0.80, short = 0.9986, plus a test asserting the gaming property is *observable* (so future readers know the metric lies).
- **Deliverable:** metric + tests. **Acceptance criteria:** pytest green. Add a docstring: *"High score ≠ good answer. Always pair with a judge-based metric (4.4b) or a length-aware check."*

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

The gaming audit. On your 25-question golden set, run answer relevancy on real answers and on *deliberately degraded* answers (prefix "Yes. " to each answer, or replace with the question rephrased). Show that degradation sometimes *increases* the score. Then design the mitigation and decide:

- Option A: hybrid relevance = max(embedding similarity, judge-based relevance) — costlier.
- Option B: relevance only as a *filter* (flag answers scoring > 0.97 with suspiciously low token counts).
- Option C: keep embedding relevance as a secondary dashboard metric, never a gate.
- **Write an ADR-style justification** with your measured before/after table (at least 10 questions × 2 degraded variants). Consequences must include the extra judge cost per eval run and which failure mode remains visible.

**Verify:** the degradation table in the ADR; pytest green.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Relevancy ~1.0 across the board | Answers echo question vocabulary | The gaming audit (L3); replace or de-weight the metric |
| Relevancy drops when answers get *better* | More detailed answers drift topically | Judge-based relevance; never tune against embedding relevance alone |
| "Yes." scores 0.99 | Embedding similarity rewards short topical overlap | Token-count floor or hybrid judge metric |
| Metric green, users confused | Relevancy ≠ correctness | Dashboard grouping: relevancy in "engagement" row, faithfulness in "correctness" row (4.9a) |

**Interview:** *"Why can a short answer game the answer-relevancy metric?"* Strong answer: cosine similarity measures topical overlap, not information content; a one-word echo of the question's vocabulary maximizes overlap; therefore the metric is a dashboard signal, not a gate — and the L3 audit (degraded answers scoring higher) is the proof.

---

# 4.4 LLM-as-Judge Pattern

## Real-world problem: the eval that passed while the judge was biased

A platform team replaced human eval with an LLM judge to save money. The judge was given one sentence of rubric: "score the answer 1–10". It systematically gave **longer answers higher scores** (verbosity bias), preferred answers that **agreed with its own opinions** (self-preference), and when the team tested A/B by swapping answer order, the judge **flipped its preference** (position bias). The eval stayed green while quality rotted, because the *judge* was the weak link — and nobody had calibrated it. The team's mistake: they treated the judge as ground truth instead of as *another system that needs its own eval*.

**The decision you must make:** how to design judge prompts (structured output, temperature 0, rubrics), how to parse and defend against untrusted judge output, and — before trusting it — how to measure the judge's own biases and agreement with humans. This section builds the judges (4.4a, 4.4b) and then attacks them (4.4c).

---

### Topic — Faithfulness judge: prompt, structured claim output, parsing, temperature=0 (4.4a)

**Mastery =** you can write a faithfulness-judge prompt that forces structured output, parse its output robustly (including malformed responses), and justify temperature=0.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Write the faithfulness judge prompt (lecture §4.4 format) for this real DevMate answer, then parse three canned judge responses.

Answer: *"The semantic cache stores query embeddings and returns cached results above a similarity threshold. It is the fastest component. It compresses payloads with zlib."* Context: from `src/devmate/cache/semantic_cache.py` (embedding storage + threshold; **no** claim about speed, **no** compression).

Judge responses to parse:

- R1: `Claim 1: stores query embeddings - SUPPORTED: YES\nClaim 2: returns cached results above a threshold - SUPPORTED: YES\nClaim 3: fastest component - SUPPORTED: NO\nClaim 4: compresses with zlib - SUPPORTED: NO` → faithfulness **0.5**.
- R2 (malformed): `Claim 1: stores query embeddings YES\nClaim 2: compresses payloads - SUPPORTED: NO` → parser must flag line 1 as unparseable, keep line 2 → **0.0** with a warning (never silently drop).
- R3 (empty): `` → zero claims → **1.0** per your 4.3c rule.

```python
import re


def parse_claims(text):
    claims = []
    for line in text.splitlines():
        m = re.match(r"Claim \d+: .+ - SUPPORTED: (YES|NO)", line)
        if not m:
            print("WARN unparseable:", line)
            continue
        claims.append(m.group(1) == "YES")
    return claims


def faithfulness(claims):
    return sum(claims) / len(claims) if claims else 1.0


r1 = "Claim 1: stores query embeddings - SUPPORTED: YES\nClaim 2: returns cached results above a threshold - SUPPORTED: YES\nClaim 3: fastest component - SUPPORTED: NO\nClaim 4: compresses with zlib - SUPPORTED: NO"
r2 = (
    "Claim 1: stores query embeddings YES\nClaim 2: compresses payloads - SUPPORTED: NO"
)
r3 = ""
assert faithfulness(parse_claims(r1)) == 0.5
assert faithfulness(parse_claims(r2)) == 0.0  # malformed line skipped
assert faithfulness(parse_claims(r3)) == 1.0  # zero claims
print("judge parsing OK")
```

Expected output: one WARN line for r2's line 1, then `judge parsing OK`. Also write one sentence justifying **temperature=0** (deterministic claim extraction; the judge must not invent support statuses) and one for why the prompt forbids adding information ("Only use information from the context").

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `projects/04-ai-engineering/devmate/eval/judge.py` with `class LLMJudge`: `judge_faithfulness(question, answer, contexts) -> float` calling `LLMClient` (`src/devmate/llm/client.py`, `get_llm_client()`), `temperature=0.0`, using your prompt, then `parse_claims` (move it from metrics.py into judge.py) and the zero-claims rule. Choose a cheap judge model (e.g., `claude-3-5-haiku-20241022` or `gpt-4o-mini` — see `MODEL_PRICING` in `src/devmate/obs/cost.py`).
- Create `projects/04-ai-engineering/devmate/tests/unit/test_judge.py` with a `FakeClient` (no network!) returning canned responses for R1/R2/R3. **Acceptance criteria:** `poetry run pytest -q tests/unit/test_judge.py` green with no API key configured; the judge always calls with `temperature=0.0` (assert on the FakeClient's received kwargs).
- **Deliverable:** `judge.py`, `test_judge.py`. (This module is what `make eval` will use — 4.5a wires it in.)

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Judge reliability study. Run the faithfulness judge on **50 answers** (your 25 golden questions × 2 answers each: real + one deliberately hallucinated variant), score the same 50 by hand with your rubric, and compute Cohen's kappa (reuse the 4.1b function). Then decide:

- Report per-band kappa (easy vs hard questions) — expect kappa to collapse on hard ones.
- **Write an ADR-style justification:** cheap judge (haiku/mini — high volume, weaker) vs. expensive judge (sonnet — costlier, stronger) vs. ensemble of two judges. Include measured kappa and measured cost per 50 answers using `MODEL_PRICING`. Consequences must state the minimum kappa you require to trust the judge in CI (suggest ≥ 0.6).

**Verify:** `evaluations/rag/reports/judge-kappa-<date>.md` with the per-band kappa table; ADR with cost table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Judge outputs prose, not claims | Prompt not strict enough | "List each claim... Format: Claim N: ..." + few-shot example in the prompt |
| Parser silently drops malformed lines → scores inflated | Lenient parsing | Warn + count skipped lines; fail the eval if > 20% unparseable |
| Faithfulness jumps between runs | temperature > 0 | Assert `temperature=0.0` in the client call (your test does this) |
| Judge "agrees" with every answer | Prompt leads the judge | Judge prompt must extract claims *first*, judge *second*; no example answers in the prompt |

**Interview:** *"Design a faithfulness judge and tell me how you'd know it's trustworthy."* Strong answer: prompt structure (claims before verdicts, structured format, temperature 0), parsing with explicit failure handling, then the calibration step — kappa against humans per difficulty band, with a minimum bar before the judge gates CI.

---

### Topic — Relevancy judge: rubric, 1–10 scale, normalization (4.4b)

**Mastery =** you can write a rubric-grounded 1–10 relevance judge, normalize to 0–1, and handle every non-numeric output a judge can produce.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Write the relevancy judge prompt (lecture format): question, answer, rubric anchors (10 = directly answers, complete, on-topic; 7 = answers but incomplete; 4 = partially on-topic; 1 = irrelevant), "Return only a number 1-10". Hand-score these four answers to *"How do I enable guardrails?"* (context: `src/devmate/guards/guardrails.py`):

- A1: "Set `GuardrailCategory.PROMPT_INJECTION` via `guardrail_manager.enable(...)`." → **9–10**
- A2: "Guardrails are important for safety." → **2** (on-topic word, no mechanism)
- A3: "Use `set_action` to change the block behavior." → **6–7** (correct but partial — doesn't say how to *enable*)
- A4: "The chunker splits documents recursively." → **1** (off-topic)

Normalization: score/10. Parse cases: `"7"` → 0.7; `"8/10"` → strip to 8 → 0.8; `"Good"` → fallback (retry once, then flag + default 0.5 with WARN, never crash):

```python
import re


def parse_score(text):
    m = re.search(r"(\d{1,2})(?:/10)?", text.strip())
    if not m:
        print("WARN non-numeric judge output:", text)
        return 0.5
    return min(max(int(m.group(1)) / 10.0, 0.0), 1.0)  # clamp


assert parse_score("7") == 0.7
assert parse_score("8/10") == 0.8
assert parse_score("Good") == 0.5  # fallback + WARN
assert parse_score("11") == 1.0  # clamp
print("relevancy parsing OK")
```

Expected: one WARN line, then `relevancy parsing OK`.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Add `judge_relevancy(question, answer) -> float` to `devmate/eval/judge.py` (rubric prompt, temperature 0, `parse_score`, clamping).
- Extend `test_judge.py` with the four parse cases + a FakeClient returning "Good" (assert fallback, no exception).
- **Deliverable:** judge + tests. **Acceptance criteria:** pytest green; the normalization rule (score/10, clamp [0,1]) documented in the docstring.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Verbosity-bias experiment on the relevancy judge. Hypothesis: longer answers score higher regardless of content. Design and run it on the real judge:

- Take 10 answers from your golden set; for each, produce a verbose variant (add two irrelevant-but-topic-adjacent sentences) and a terse variant (keep only the first sentence).
- Run `judge_relevancy` on all 30; measure mean score by variant. A mean delta > 0.5/10 between verbose and terse variants on *the same content* is bias.
- **Write an ADR-style justification:** accept the bias (small, cheap to live with) vs. mitigate in the prompt (rubric anchor: "Length is not quality; score content only") vs. add a length-normalization post-pass. Consequences include judge cost and remaining bias after mitigation.

**Verify:** `evaluations/rag/reports/judge-verbosity-<date>.md` with the 30-score table and mean deltas; ADR with the chosen mitigation and a re-run number.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| All relevancy scores are 8–10 | Rubric anchors too vague; judge defaults to praise | Anchor each band with a concrete DevMate example |
| "Good" crashes the eval | Unchecked float() | `parse_score` fallback + WARN; never raise on judge output |
| Scores normalize wrong (0.07 instead of 0.7) | Dividing by 100 instead of 10 | Unit test pins 0.7 for "7" |
| Relevancy and faithfulness both drop together | Judge prompt confusion (relevancy vs groundedness) | Keep judge prompts single-purpose; never combine metrics in one prompt |

**Interview:** *"How do you normalize an LLM judge's 1–10 score, and what can still go wrong?"* Strong answer: score/10 with clamping, rubric anchors per band, fallback for non-numeric output — and the deeper point: normalization only fixes the *scale*, not the *bias*; scale is a parsing problem, bias is a measurement problem (4.4c).

---

### Topic — Judge pitfalls (stretch): position bias, self-preference, verbosity, rubric design, agreement (4.4c)

**Mastery =** you can design experiments that detect each judge bias, measure it, and decide when the judge's agreement with humans is good enough to gate CI.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Design the swap-order experiment on paper. Take answer pair (X, Y) where X is genuinely better. The judge compares two answers and picks a winner. Run the pair twice, once in each order:

| Pair | Order | Winner (unbiased judge) | Winner (position-biased judge) |
|---|---|---|---|
| Pair 1 | X then Y | X | X (first position) |
| Pair 1 | Y then X | X | Y (first position) |

An unbiased judge picks X in **both** orders. A judge with position bias flips with the order. Hand-compute the bias metric: for 10 pairs, count flips; flips/10 = position-bias rate; any rate > 0.2 is a problem. Then define the other biases you'll test: **self-preference** (judge prefers answers matching its own style/opinions — detectable by feeding an answer written in the judge's own voice), **verbosity bias** (longer wins — the 4.4b experiment), **rubric design failure** (anchors ambiguous — detectable by kappa). Write the experiment matrix (bias → setup → metric → threshold) as a table — this table is the deliverable of the drill.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Run the swap-order experiment on the real judge:

- Take 10 golden answers and write a deliberately worse variant for each (drop one key fact).
- Run the comparison judge on all 10 pairs in both orders (20 judge calls).
- **Deliverable:** `evaluations/rag/reports/judge-bias-<date>.md` — per-pair table (winner per order, flip?), the position-bias rate, and one sentence per flip about what the judge was likely reacting to.
- **Acceptance criteria:** the flip rate is computed and interpreted against your 0.2 threshold; if flips > 0.2, state the mitigation (randomize order, anchor rubric) in the report.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

The full judge-agreement study and the gate decision. You now have the tools: kappa (4.1b), faithfulness reliability (4.4a), verbosity (4.4b), position bias (this topic). Run the full battery on 30 samples (10 per difficulty band) and produce one decision:

- **Write an ADR-style justification:** under what conditions the LLM judge *replaces* human eval vs. stays in "suggest" mode. Include the measured battery table (kappa per band, position-bias rate, verbosity delta, judge cost per 30 answers) and a hard rule, e.g.: "judge gates CI only if kappa ≥ 0.6 on easy+medium bands AND position-bias rate ≤ 0.2 AND verbosity delta ≤ 0.5/10; otherwise humans gate."
- Consequences must state what you accept when the judge gates alone (residual bias on hard questions) and the re-calibration cadence (quarterly, or after any judge model change).

**Verify:** the battery table in the ADR; the report files from 4.4a–4.4c all exist; the rule is written as a machine-checkable condition.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Judge always picks answer A | Position bias | Randomize order; run both orders; require agreement across orders |
| Judge flips when you reword the prompt | Rubric ambiguity, not model noise | Anchor examples per band; test prompt stability (same answers, 3 prompt phrasings) |
| Eval green, users angry | No bias battery run | Bias tests are part of the eval harness, not a one-off study |
| Two judges disagree 30% of the time | Judge models differ in style | Pick one judge model and lock it; report the model in every report header |

**Interview:** *"Your LLM judge says everything is fine. Prove it's not lying to you."* Strong answer: the four experiments (position swap, verbosity variants, self-preference probe, human kappa per difficulty band), each with a threshold; and the decision rule that ties them together — the judge gates CI only when the whole battery passes.

---

# 4.5 Automated Evaluation Harness

## Real-world problem: the report that hides the broken question

A startup's eval report prints one line: `faithfulness: 0.94`. The team shipped for two months on that number. Then a user complaint traced to question 17 of the golden set — *the one question that had been scoring 0.3 for six weeks* — invisible because the mean hid it. Meanwhile, eval runs were manual copy-paste: someone ran the pipeline, pasted answers into a spreadsheet, and hand-computed averages. A forgotten dataset version invalidated a whole week of tuning. And every run cost more than it should because no one counted the tokens.

**The decision you must make:** build the harness that (a) runs the full golden set through the real pipeline, (b) computes every metric per question, (c) aggregates honestly (means + percentiles + totals), and (d) saves everything to a versioned report — within the module's hard constraints: **run < 5 minutes, cost < $0.50, no single question can kill the run.** This section builds the loop (4.5a) and the aggregation (4.5b) that everything else (4.6–4.9) consumes.

---

### Topic — run_evaluation loop: load jsonl, run pipeline, compute metrics, collect per-question results (4.5a)

**Mastery =** you can write the full eval loop — load → run → score → collect — with per-question isolation, and defend why per-question results are the minimum honest output.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Write the loop skeleton with a fake pipeline (no network, no store):

```python
import json


def fake_pipeline(question):
    return {
        "answer": f"Answer to: {question}",
        "context_ids": ["c1", "c2"],
        "latency_ms": 100.0,
        "cost_usd": 0.001,
    }


def run_evaluation(dataset, pipeline):
    results = []
    for item in dataset:
        r = pipeline(item["question"])
        results.append(
            {
                "question": item["question"],
                "category": item["category"],
                "answer": r["answer"],
                "context_ids": r["context_ids"],
                "precision_at_5": 0.4,  # placeholder — real metric in 4.3a
                "faithfulness": 0.5,  # placeholder — real judge in 4.4a
                "latency_ms": r["latency_ms"],
                "cost_usd": r["cost_usd"],
            }
        )
    return results


ds = [
    {
        "question": "q1",
        "category": "factual",
        "contexts": ["c1"],
        "ground_truth": "g1",
        "difficulty": "easy",
    },
    {
        "question": "q2",
        "category": "debugging",
        "contexts": ["c2"],
        "ground_truth": "g2",
        "difficulty": "hard",
    },
    {
        "question": "q3",
        "category": "edge",
        "contexts": ["c3"],
        "ground_truth": "g3",
        "difficulty": "medium",
    },
]
results = run_evaluation(ds, fake_pipeline)
assert len(results) == 3
assert all(
    {"question", "category", "answer", "latency_ms", "cost_usd"} <= set(r)
    for r in results
)
assert all(r["latency_ms"] == 100.0 for r in results)
print("loop OK; per-question rows:", len(results))
```

Expected: `loop OK; per-question rows: 3`. Then add one line explaining the **isolation requirement**: one crashing question must not kill the run — wrap per-item work in try/except, record the error in the row, continue. State the design decision: a failed question is a *data point* (error row), not a run failure.

**💻 Level 2 — Applied** (DevMate, 1–3 h) — **the core deliverable of weeks 2–3**

Build the real harness — the file `make eval` already targets:

- Create `projects/04-ai-engineering/devmate/eval/run_ragas.py` that: (1) loads `evaluations/rag/datasets/devmate-golden.jsonl` (path via CLI arg `--dataset`, default the golden set); (2) runs `RAGPipeline.query(RAGRequest(query=item["question"], stream=False))` per question (import from `src/devmate/retrieve/rag.py`); (3) computes: context precision@5, recall@5, recall@10, MRR (your `devmate/eval/metrics.py`), faithfulness + answer relevancy (your `devmate/eval/judge.py`); (4) collects per-question rows (question, category, difficulty, answer, context ids, each score, latency_ms, cost_usd); (5) prints a metrics table to stdout; (6) never dies on a single question (error rows recorded).
- Cost control: reuse `cost_tracker` / `MODEL_PRICING` (`src/devmate/obs/cost.py`); the judge uses your cheap model. Budget check: 25 questions × (1 generation + 1 faithfulness judge + 1 relevancy judge + 1 embedding) at gpt-4o-mini pricing ≈ **$0.02–0.05 total** — the $0.50 budget has huge headroom; verify with the run's reported total.
- **Deliverable:** `run_ragas.py`. **Acceptance criteria:** `cd projects/04-ai-engineering/devmate && poetry run python eval/run_ragas.py --dataset ../../../../evaluations/rag/datasets/devmate-golden.jsonl` (or the root equivalent `make eval` once the path resolves) prints a table with one row per question and a totals row; the run finishes in **< 5 minutes**; total cost reported **< $0.50**; deliberately breaking one question (temporarily) proves the run survives.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Scale the harness to 500 questions without breaking the budget or the wall-clock. DevMate's golden set is 25; production sets grow to hundreds. Design and implement:

- Concurrency: bounded parallel execution of independent questions (e.g., `asyncio.gather` with a semaphore of 5–10), with rate-limit and retry handling for `LLMRateLimitError` (defined in `src/devmate/llm/client.py`).
- Cost shaping: judge-call deduplication (identical question+answer pairs), and a `--sample N` mode that evaluates a random N-question subset with a stated confidence caveat.
- Failure taxonomy: per-question error rows typed (pipeline error vs judge parse error vs timeout), with a summary "3/500 failed (2 timeout, 1 judge)".
- **Write an ADR-style justification:** serial vs bounded-parallel vs fully parallel. Consequences must include cost ceiling math (500 × $0.0015 ≈ $0.75 — over the $0.50 budget! → justify raising the budget or sampling), and the determinism trade-off (parallel judge calls can reorder output, not scores).

**Verify:** 25-question run < 5 min and < $0.50 (printed by the harness); a 500-question synthetic run (duplicate your 25 × 20 with suffix variation) completes under the budget via sampling; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| One bad question kills the whole run | No per-item try/except | Error rows; the run always completes and reports failures |
| `make eval` fails with ModuleNotFoundError | `eval/` has no `__init__.py` or path issues | Run with `poetry run python eval/run_ragas.py` from `projects/04-ai-engineering/devmate`; add `eval/__init__.py` |
| Run takes 30+ minutes | Serial judge calls at full context | Bounded parallelism (L3); or reduce judge context (only pass the top-3 contexts) |
| Cost blows past $0.50 | Using the *generation* model for judging | Judge with the cheap model; assert model names in the report |
| Missing columns in the table | Rows built ad hoc | Fixed row schema (your L1 drill) + the table prints all fields |

**Interview:** *"Walk me through your evaluation harness end to end."* Strong answer: load golden set (with validation) → run the real pipeline per question → compute retrieval metrics + judge metrics per question → isolate failures as error rows → aggregate honestly (means, percentiles, totals) → persist a versioned report; plus the two numbers you guard: wall-clock and dollars.

---

### Topic — Report aggregation: mean scores, p50/p95 latency, total cost, saving JSON reports (4.5b)

**Mastery =** you can aggregate per-question results without lying — means for scores, percentiles for latency, sums for cost — and save a machine-readable report that 4.6's regression checker can consume.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Hand-compute the aggregates for these 5 per-question rows (latency in seconds, cost in USD):

| Q | latency | cost |
|---|---|-------|
| Q1 | 1.0 | 0.01 |
| Q2 | 1.5 | 0.02 |
| Q3 | 2.0 | 0.01 |
| Q4 | 3.0 | 0.03 |
| Q5 | 8.0 | 0.08 |

- mean latency = (1.0+1.5+2.0+3.0+8.0)/5 = **3.1 s**
- p50 latency = **2.0 s** (3rd value of 5 sorted)
- p95 latency (numpy linear interpolation): index = 0.95 × 4 = 3.8 → 3.0 + 0.8 × (8.0 − 3.0) = **7.0 s**
- total cost = **$0.15**; mean cost = **$0.03**

Note the lesson: mean (3.1) is above p50 (2.0) — one outlier pulls it. The report shows *both*. Implement and assert:

```python
import statistics, numpy as np

lat = [1.0, 1.5, 2.0, 3.0, 8.0]
cost = [0.01, 0.02, 0.01, 0.03, 0.08]
assert abs(statistics.mean(lat) - 3.1) < 1e-9
assert np.percentile(lat, 50) == 2.0
assert abs(np.percentile(lat, 95) - 7.0) < 1e-9
assert abs(sum(cost) - 0.15) < 1e-9
report = {
    "num_questions": 5,
    "aggregate": {"latency_p50_s": 2.0, "latency_p95_s": 7.0, "total_cost_usd": 0.15},
}
print("aggregation OK:", report)
```

Expected: `aggregation OK: {'num_questions': 5, 'aggregate': {'latency_p50_s': 2.0, 'latency_p95_s': 7.0, 'total_cost_usd': 0.15}}`. Edge cases to note: **an empty results list must fail loudly** (a report with `num_questions: 0` is a lie); a single-question run has p95 = that question's latency.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Add `aggregate_results(results: list[dict]) -> dict` to `devmate/eval/report.py` (mean per metric, p50/p95 latency, total cost, per-category breakdown, error-row count) and `save_report(report, path)` writing JSON with a UTC ISO timestamp (`datetime.utcnow().isoformat()` — the repo convention in `obs/cost.py`; note the timezone explicitly in the file).
- Wire it into `run_ragas.py`: after the loop, write `evaluations/rag/reports/devmate-<date>.json` and a companion `devmate-<date>.md` table (model, dataset, run timestamp, aggregate table, per-question rows, failures).
- Tests in `test_eval_metrics.py` (or a new `test_report.py`): the 5-row example above (exact numbers), empty-list → raises, single-question p95.
- **Deliverable:** `report.py`, tests, and one real report file from a full run. **Acceptance criteria:** pytest green; `poetry run python eval/run_ragas.py` produces both files; the JSON parses and matches the printed table.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Tiny-set statistics. With 25 questions, one outlier swings the mean (your L1 drill just showed it with 5 rows). Senior move: quantify the uncertainty instead of hiding it.

- Add per-metric standard deviation, min/max, and the **worst-N questions list** (bottom 3 per metric) to the report.
- Add a Monte-Carlo or bootstrap confidence interval for faithfulness (resample questions with replacement, 1000×, report the 95% CI width). If CI width > 0.1 on a 25-question set, the report says so: "faithfulness 0.91 ± 0.12 — do not gate CI on this metric at this dataset size."
- **Write an ADR-style justification:** gate on the mean vs. gate on the worst-N vs. gate on the lower CI bound. Consequences must include dataset-size requirements (how many questions make the CI width < 0.05) and the cost of reaching that size.

**Verify:** the report contains σ, min/max, worst-3, and a bootstrap CI; ADR exists with a size-vs-CI-width table.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Report says 0.94 but question 17 is 0.3 | Mean-only aggregation | Worst-N list + per-question rows in every report |
| Two reports, different aggregates, same data | Percentile method differs (numpy vs linear) | Pin the method in `report.py` and cite it in the report header |
| p95 > max latency | Bug in percentile implementation | Sanity assert: p50 ≤ p95 ≤ max |
| Timestamps in local time → reports misordered | `datetime.now()` vs `utcnow()` | UTC ISO everywhere; the repo convention is `utcnow` (see `obs/cost.py`) |
| Empty run writes a "0 questions" report | No guard | Empty results → raise; never write an empty report |

**Interview:** *"How do you aggregate an eval run so it doesn't lie to you?"* Strong answer: means for scores but always with per-question rows and worst-N; percentiles (p50/p95) for latency, never the mean; sums for cost; UTC timestamps; empty-set guard; and at small N, confidence intervals so you know what you don't know.

---

# 4.6 Regression Testing

## Real-world problem: the faithfulness drop that would have shipped

Week 7 of the track's case study: someone changed the DevMate system prompt — a small wording change to make answers "more direct". The change was *good* in human review. But the golden set caught it: faithfulness dropped **0.91 → 0.82** on the same 25 questions. Without the regression gate, that prompt would have deployed, and the exact failure mode of 4.1's Sana story would repeat: silent, user-detected, weeks-late. The gate exists only because: (a) a baseline was recorded when the system was known-good, (b) a comparison tool knows the thresholds (−0.05 aggregate, −0.1 per question), and (c) CI runs it automatically on every prompt/retrieval change.

**The decision you must make:** what exactly counts as a regression, how strict the gates should be (too strict → noise, too loose → regressions ship), and how to version baselines so comparisons are always honest. This section implements the comparator (4.6a) and the CI gate (4.6b) — and then deliberately tries to break both.

---

### Topic — Baseline comparison: thresholds, per-question regression detection (4.6a)

**Mastery =** you can apply the regression rules (−0.05 aggregate, > +0.02 improvement, −0.1 per question) by hand, implement them, and explain the trade-off in each threshold.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Apply the lecture's rules to three reports. Baseline (week-3 case study): context precision@5 **0.83**, context recall **0.79**, faithfulness **0.91**, answer relevancy **0.88**.

- Report A: precision 0.84, recall 0.80, faithfulness 0.90, relevancy 0.87 → deltas +0.01, +0.01, −0.01, −0.01 → all within ±0.05 → **PASS**.
- Report B: precision 0.83, recall 0.79, faithfulness **0.82**, relevancy 0.88 → faithfulness delta **−0.09 < −0.05** → **FAIL** (this is the week-7 story). Per-question: Q7 faithfulness 0.95 → 0.80 → **−0.15 < −0.1** → question regression logged too.
- Report C: faithfulness **0.94** → delta **+0.03 > +0.02** → improvement logged (not a pass/fail — recorded).

```python
def compare(bl, new, metric_threshold=-0.05, improvement=0.02, per_q=-0.1):
    regressions, improvements, q_regressions = [], [], []
    for m in [
        "context_precision",
        "context_recall",
        "faithfulness",
        "answer_relevancy",
    ]:
        d = new[m] - bl[m]
        if d < metric_threshold:
            regressions.append((m, bl[m], new[m], d))
        elif d > improvement:
            improvements.append((m, bl[m], new[m], d))
    return regressions, improvements, q_regressions


bl = {
    "context_precision": 0.83,
    "context_recall": 0.79,
    "faithfulness": 0.91,
    "answer_relevancy": 0.88,
}
A = {
    "context_precision": 0.84,
    "context_recall": 0.80,
    "faithfulness": 0.90,
    "answer_relevancy": 0.87,
}
B = {
    "context_precision": 0.83,
    "context_recall": 0.79,
    "faithfulness": 0.82,
    "answer_relevancy": 0.88,
}
C = {
    "context_precision": 0.83,
    "context_recall": 0.79,
    "faithfulness": 0.94,
    "answer_relevancy": 0.88,
}
assert compare(bl, A)[0] == []  # PASS
r, i, _ = compare(bl, B)
assert any(m == "faithfulness" for m, _, _, _ in r)  # FAIL: faithfulness -0.09
assert any(m == "faithfulness" for m, _, _, _ in compare(bl, C)[1])  # improvement +0.03
print("regression logic OK")
```

Expected: `regression logic OK`. Also state in one sentence each: why −0.05 and not any drop (judge noise: a ±0.03 swing between identical runs is normal — see 4.5b CI widths), and why per-question −0.1 is stricter (one question can be a canary).

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `projects/04-ai-engineering/devmate/eval/check_regression.py`: `--baseline <json>` + `--new <json>` (or `--report <json>` comparing against the stored baseline); prints a verdict table (metric | baseline | new | delta | verdict) and **exits 1 if any regression or question regression exists**, 0 otherwise. Use your `aggregate_results` JSON from 4.5b as both inputs.
- Establish the baseline: after a green run, copy the report to `evaluations/rag/baselines/devmate-baseline.json` (the `baselines/` folder exists; follow the naming in `evaluations/rag/README.md` §Baselines).
- Tests in `test_eval_metrics.py`: the A/B/C verdicts above, plus an empty-baseline guard (missing file → error, not crash).
- **Deliverable:** `check_regression.py`, baseline file, tests. **Acceptance criteria:** pytest green; unchanged code → exit 0; then the injected-bug drill (below) → exit 1.
- **Injected-bug drill:** introduce a bug in the prompt (weaken the grounding clause in `RAG_SYSTEM_PROMPT`), re-run the eval, run the comparator → it must FAIL; then **revert the bug** and confirm green again. This is the module's central proof: *regression detection catches injected bugs.*

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Threshold statistics, not vibes. The −0.05 threshold is a guess. Make it measured:

- Run the identical eval 3 times on unchanged code; compute the run-to-run noise per metric (std of the deltas). The gate threshold should be ≥ 2× noise, else CI fails randomly (alert fatigue) or passes regressions (false confidence).
- With a 25-question set, faithfulness CI width (your 4.5b bootstrap) may be ±0.1 — quantify the conflict: the gate threshold (−0.05) is *smaller than the measurement noise*. Decide: bigger dataset, or gate on per-question worst-N, or accept noisy gates on some metrics and gate CI only on the stable ones.
- **Write an ADR-style justification:** fixed thresholds vs. noise-derived thresholds vs. per-metric gating (gate faithfulness + per-question canaries; report-only for recall). Consequences must include expected false-fail rate per week (with your measured noise, compute it).

**Verify:** noise table (3 runs × 4 metrics) in the ADR; comparator exit codes proven (0 green, 1 injected bug); ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| CI fails randomly | Threshold smaller than judge noise | Noise-derived thresholds (L3): ≥ 2× run-to-run std |
| CI passes a real regression | Only the mean gated; one question tanked | Per-question −0.1 gate + worst-N list in the report |
| Baseline drift: every run "improves" | Baseline never updated | Freeze baseline; update only via explicit ADR/PR (4.6b L3) |
| Comparator crashes on missing baseline | No guard | Exit with a clear error: "no baseline — run with --establish" |
| Improvement (+0.03) logged as regression | Sign bug | Unit tests pin A/B/C verdicts — never ship the comparator without them |

**Interview:** *"How do you set regression thresholds for an LLM eval without guessing?"* Strong answer: measure run-to-run noise (same code, N runs) → threshold ≥ 2× noise; verify per-question canaries; and be honest that at 25 questions the CI width may exceed the threshold — the answer is dataset size or per-metric gating, not a more aggressive threshold.

---

### Topic — CI integration: eval.yml workflow, paths filter, baseline versioning (4.6b)

**Mastery =** you can write a CI workflow that runs eval only when it should, gates merges on regression, and version baselines so comparisons stay honest.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Write the workflow by hand (lecture §4.6), then answer three questions. The lecture's `eval.yml`:

```yaml
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
          python -m devmate.eval.check_regression --baseline evaluations/rag/baselines/devmate-baseline.json
```

Answer: (1) **When does this run?** Only on PRs touching retrieval or prompt files — a docs-only PR must not burn $0.50. (2) **What are the two gates?** The eval command itself (must exit 0) and the regression check (exits 1 on regression). (3) **What's wrong with the paths here?** This repo's prompt template lives in `projects/04-ai-engineering/devmate/src/devmate/retrieve/rag.py` (`RAG_SYSTEM_PROMPT`), not `llm/prompts/` — a prompt edit in `rag.py` would **not trigger the workflow** (silent gap), and the filter paths must be repo-root-relative (`projects/04-ai-engineering/devmate/src/devmate/retrieve/**`). Write the corrected paths filter as your answer, covering retrieval, prompts, guardrails, and the eval/ folder itself.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `.github/workflows/eval.yml` in this repo: triggers on `pull_request` (paths: `projects/04-ai-engineering/devmate/src/devmate/retrieve/**`, `.../llm/**`, `.../guards/**`, `devmate/eval/**`, `evaluations/rag/datasets/**`) and `workflow_dispatch` (manual re-run); `working-directory: projects/04-ai-engineering/devmate` (mirror `ci.yml`'s setup: setup-python, pipx poetry, `poetry install`); steps run `poetry run python eval/run_ragas.py --dataset <repo-root-relative golden set>` then `poetry run python eval/check_regression.py --baseline ...` — with `ANTHROPIC_API_KEY` from repo secrets (see how `ci.yml` handles env).
- Local proof (you can't run GitHub Actions locally): (1) `poetry run python eval/check_regression.py --baseline evaluations/rag/baselines/devmate-baseline.json --new <latest report>` → exit 0; (2) injected-bug drill from 4.6a → exit 1 → proves the gate logic the workflow will run.
- **Deliverable:** `eval.yml`. **Acceptance criteria:** the file parses as valid YAML (`python -c "import yaml, pathlib; yaml.safe_load(pathlib.Path('.github/workflows/eval.yml').read_text()); print('yaml ok')"`); paths filters correct for this repo layout; the two run steps match your real module names.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Baseline versioning and gate economics. Three problems at once:

- **Versioning:** baselines must be immutable anchors. Design: baseline files named `devmate-baseline-<date>.json`; a `--establish` flag writes a new baseline; updates require a PR that shows the delta table (improvements accepted, regressions rejected). Handle the "improvement drift" failure: after 3 accepted improvements, the baseline is stale — propose the re-baseline cadence.
- **Flakiness:** judge nondeterminism + Qdrant cold starts can flake the gate. Add a retry policy for judge timeouts (`LLMTimeoutError` in `src/devmate/llm/client.py`) and a `--allow-known-flaky` escape hatch that still records the failure in the report (never silent).
- **Economics:** each PR eval costs ~$0.05 and 5 min; at 20 PRs/day that's $1/day and 100 min of runner time. Compute the cost of gating every PR vs. gating only path-filtered PRs vs. nightly full runs + PR smoke (5-question subset). **Write an ADR-style justification** with the three-option cost table and a recommendation.
- Consequences must include: what happens when the golden set changes (the dataset PR itself must not fail the gate — exclude `evaluations/rag/datasets/**` from the regression step or auto-skip with a comment).

**Verify:** yaml parses; exit-code drill green/red as specified; ADR with the cost table exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Workflow never runs | Wrong paths filter (not repo-root-relative, or prompts live elsewhere) | The L1 drill's third answer; test with `workflow_dispatch` |
| CI runs eval on docs PRs | No paths filter / filter too broad | Paths filter; docs-only changes skip eval |
| Gate passes locally, fails in CI | Env differences (API key missing, Qdrant not started) | Mirror `ci.yml`'s setup steps exactly; make Qdrant a service or use in-memory store for eval |
| Baseline silently updated by a failing run | Auto-write on every run | `--establish` is explicit and PR-reviewed; runs never overwrite baselines |
| Dataset PR fails the gate | Gate runs on the dataset change itself | Skip regression step on dataset-only changes (or expect-and-document delta) |

**Interview:** *"How does your eval get into CI, and what could quietly break it?"* Strong answer: path-filtered trigger (cost control), two gates (eval + regression), env parity with the unit-test job; and the failure modes: wrong paths filter (never runs), env drift (passes locally, fails in CI), flaky judge (retry + recorded escape hatch), baseline rot (immutable, PR-reviewed baselines).

---

# 4.7 Observability: Full Pipeline Tracing

## Real-world problem: a $30k/month bill with no visibility

The finance review hits: $30k/month on LLM calls, and nobody can say *why* — which stage costs what, which queries are expensive, whether the semantic cache is even helping. At the same time, support gets "why is it slow?" tickets: the team's only answer is "the LLM takes time". The API trace in `RAGPipeline.query()` today wraps the whole call in a **single span** (`tracer.trace("rag.query", ...)` in `src/devmate/retrieve/rag.py`) — one number for the entire pipeline. A 6-second request could be 5 seconds of embedding, 0.5 of search, 0.5 of generation — or the reverse — and no one can tell. Week 7's production hardening adds cache and guardrails; those stages exist in `src/devmate/cache/semantic_cache.py` and `src/devmate/guards/guardrails.py` but **are not wired into the query path at all**, so they can't be traced either.

**The decision you must make:** instrument every stage with spans (4.7a) and push real metadata — latency, tokens, cost — into Langfuse (4.7b), so the $30k/month question, the latency question, and the cache-effectiveness question all become *queryable* instead of arguable.

---

### Topic — What to trace: every stage from guardrails to response (4.7a)

**Mastery =** you can map the lecture's 9 tracing stages onto DevMate's real code, instrument each with a span, and explain what metadata each span must carry.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Build the trace-map. For each of the 9 stages, name the DevMate file/function that owns it and the metadata the span must carry (write this as a table):

| Stage | DevMate home | Span metadata |
|---|---|---|
| 1. Input guardrails | `src/devmate/guards/guardrails.py` (`GuardrailManager`, `check`-style methods) | guardrail names, action (block/redact/warn) |
| 2. Semantic cache | `src/devmate/cache/semantic_cache.py` | hit/miss, similarity score |
| 3. Query embedding | `RAGPipeline.query()` step 1 (via `EmbeddingService` in `src/devmate/index/embeddings.py`) | model, dimensions, tokens, latency |
| 4. Vector search | `Retriever.retrieve` (`src/devmate/retrieve/retriever.py`) | collection, top_k, num_results |
| 5. Reranking | `get_reranker(...)` in `retriever.py` (default `NoOpReranker`) | reranker name, top scores |
| 6. Prompt construction | `RAGPipeline._build_context` / `_build_messages` (`rag.py`) | template version (hash of `RAG_SYSTEM_PROMPT`), context size in tokens, num chunks |
| 7. LLM generation | `LLMClient.complete` (`src/devmate/llm/client.py`) | model, prompt/completion tokens, temperature, latency, cost |
| 8. Output guardrails | `src/devmate/guards/guardrails.py` | actions applied, schema/PII flags |
| 9. Response | `RAGPipeline.query()` end | total latency, total cost, answer length |

Then verify the current state with code: `cd projects/04-ai-engineering/devmate && poetry run python -c "from devmate.retrieve.rag import RAGPipeline; import inspect; src = inspect.getsource(RAGPipeline.query); print('spans:', src.count('tracer.trace'), 'cache:', 'cache' in src, 'guardrail:', 'guardrail' in src.lower())"` — expect `spans: 1` and `cache: False`, `guardrail: False` (the gap you're about to close). Write one sentence: which two stages are missing from the current query path entirely, and what production question does each span answer?

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Instrument the pipeline. Edit `src/devmate/retrieve/rag.py` `query()` so the existing single span becomes a hierarchy using `tracer.trace_async` (see `src/devmate/obs/tracing.py` — `start_trace`/`start_span`/`end_span`, `trace_async` context manager, spans carry `attributes`):

- Wrap each existing step (embed → retrieve → build context → build messages → generate) in its own named span: `embedding`, `vector_search`, `prompt_construction`, `generation`.
- Add `guardrails_input` / `guardrails_output` spans (even if the checks are currently a no-op passthrough — the span proves the stage was evaluated) and `semantic_cache` (hit/miss).
- Add a `response` span that records total latency and total cost (use `cost_tracker` from `src/devmate/obs/cost.py`).
- Every span carries metadata: `request_id`, model, template version (`hashlib.sha1(RAG_SYSTEM_PROMPT.encode()).hexdigest()[:10]`), num results, latency_ms.
- Create `projects/04-ai-engineering/devmate/tests/unit/test_traces.py`: run one query against a mocked pipeline (FakeRetriever + FakeLLM — no network), then assert `tracer.get_recent_traces()` contains spans named exactly `embedding`, `vector_search`, `prompt_construction`, `generation`, `semantic_cache`, `guardrails_input`, `guardrails_output`, `response` in parent-child order (root = `rag.query`).
- **Deliverable:** instrumented `rag.py` + `test_traces.py`. **Acceptance criteria:** pytest green; the test proves all 9 lecture stages are now visible in traces.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Tracing overhead vs. value. Every span is a cost: attribute serialization, Langfuse API calls, storage. At 1M requests/day, tracing everything is real money. Design the sampling policy:

- Head-based sampling (decide per request: always-trace for sampled traffic, errors, slow requests, and a random 5%) vs. tail-based (buffer and decide after completion — captures slow/error requests precisely).
- Implement a `--trace-sample-rate` config on the tracer (in `src/devmate/config.py` settings, read by `obs/tracing.py`), and prove overhead: measure requests/sec with tracing at 100% vs 5% on a mocked pipeline.
- **Write an ADR-style justification:** always-trace vs. head-sampling vs. tail-sampling. Consequences must include the storage math (spans/day × bytes) and the guarantee that **errors and p95+ requests are always traced** regardless of sampling.

**Verify:** `poetry run pytest -q tests/unit/test_traces.py` green; overhead measurement table (rps at 100% vs 5%) in the ADR.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Trace shows one fat span | Only the outer `rag.query` span existed | The L2 instrumentation — each stage its own span |
| Spans exist but no timing | `end_time` never set | Use `trace_async` context manager (it calls `end_span` in `finally`) |
| Trace is polluted by eval runs | Eval uses the same tracer | Tag traces: `metadata={"purpose": "eval"}` vs "production" |
| Cache spans always "miss" | Cache not actually wired into `query()` | The span records the check result; wiring the cache is a week-7 deliverable — the span makes it visible when it lands |
| Overhead doubles latency | Exporting synchronously | Export async/batched; sample (L3) |

**Interview:** *"What do you trace in a RAG pipeline, and what does each span buy you?"* Strong answer: the 9 stages with their metadata; each span answers a production question (cache effectiveness = hit/miss span; cost = tokens per generation span; slowness = per-stage latency); the tracing hierarchy (root trace, child spans) supports per-stage p95 dashboards (4.9); and the honest cost: sampling policy so tracing doesn't become the bottleneck.

---

### Topic — Langfuse integration: trace + spans, metadata, latency/token/cost capture (4.7b)

**Mastery =** you can map DevMate spans to Langfuse traces/spans, attach cost and token metadata per span, and verify the export end-to-end.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Read `src/devmate/obs/tracing.py` — `_export_span_to_langfuse` already maps: span id → `langfuse_trace.span(id=...)`, attributes → `metadata=span.attributes`, error status → `level="ERROR"`, parent via `parent_span_id`. Now do the mapping exercise by hand. A generation span carries these attributes:

```python
span.attributes = {
    "model": "gpt-4o-mini",
    "prompt_tokens": 800,
    "completion_tokens": 300,
    "total_tokens": 1100,
    "cost_usd": 0.0003,
    "latency_ms": 450.0,
}
```

Write the Langfuse span call this maps to (fields: `id`, `name`, `parent_span_id`, `start_time`, `end_time`, `metadata`, `level`, `status_message`). Then state: which attribute belongs in `metadata` vs. in Langfuse's native usage/cost fields, and why cost *per span* (not just per trace) is required for the $30k/month question (you must see generation vs embedding cost split). One-line answer for each; the drill is the mapping table you write.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Wire real cost metadata into spans and export to Langfuse.

1. In the instrumented `rag.py` from 4.7a, add cost capture: after the generation call, record usage via `cost_tracker.record_usage(provider=..., model=..., usage=..., latency_ms=..., request_id=...)` (`src/devmate/obs/cost.py`) and attach `model`, `prompt_tokens`, `completion_tokens`, `total_tokens`, `cost_usd`, `latency_ms` to the `generation` span (and the embedding tokens to the `embedding` span).
2. Configure Langfuse: set `langfuse_public_key` / `langfuse_secret_key` / `langfuse_host` in `projects/04-ai-engineering/devmate/.env` (see `src/devmate/config.py` settings; self-hosted Langfuse is free — roadmap §reading). With keys set, run 3 real queries: `poetry run devmate ask "How does the semantic cache work?"` (requires `make up` for Qdrant).
3. **Deliverable:** `evaluations/rag/reports/trace-export-<date>.md` — the 3 trace ids, the span tree (parent → children), per-span latency/tokens/cost, and the Langfuse UI screenshots or exported JSON showing the same numbers. **Acceptance criteria:** every span in the trace carries latency; the generation span carries tokens + cost; total cost sums correctly across spans (matches `cost_tracker.get_summary()`); the report records the trace IDs.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Cost attribution correctness. Two production-grade problems:

- **Pricing drift:** `MODEL_PRICING` in `obs/cost.py` is a static dict. Providers change prices; a stale price makes every cost report wrong by a constant factor. Design: pricing config file + a weekly check job that alerts when a tracked model's price changes (diff against a pinned version), and a `cost_accuracy` test that recomputes a known record from raw usage (golden cost value in the test).
- **Attribution:** embedding costs are charged per token but often batched; generation costs depend on retries (a 429-then-retry burns prompt tokens twice — see `LLMTimeoutError`/`LLMRateLimitError` in `src/devmate/llm/client.py`). Design the rule: retries attributed to the request, reported separately as `retry_cost_usd`.
- **Write an ADR-style justification:** static pricing dict vs. config-file pricing with drift check vs. provider-billed-usage API (source of truth, but delayed). Consequences must include the accuracy guarantee per report and the operational cost of each option.

**Verify:** the export report exists with span-level cost; the pricing-drift check job (or script) runs; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Cost is 0 everywhere | `cost_tracking_enabled` false, or `record_usage` never called | Enable in `.env`; assert `cost_tracker.get_summary().total_cost_usd > 0` after a run |
| Langfuse shows traces, no spans | Export called on trace end, spans exported separately and out of order | Export spans on `end_span` (the code already does); flush after the root span |
| Tokens on the trace, not per span | Usage attached to `trace.end` only | Attach usage to the `generation` span; trace-level totals are sums |
| Export crashes the request | Synchronous Langfuse call fails | `_export_span_to_langfuse` already try/excepts — never let tracing fail the query |
| Costs don't match the bill | Static pricing stale | Pricing drift check (L3) |

**Interview:** *"What do you send to Langfuse for each request, and how do you know it's right?"* Strong answer: trace + per-stage spans with latency, tokens, and cost metadata; cost computed at record time from pinned pricing, verified against the provider bill; sampling for scale; and the discipline that tracing failures never fail the request (try/except everywhere).

---

# 4.8 Drift Detection

## Real-world problem: the week-5 query shift that broke faithfulness

The track's case study: in week 5, DevMate's users started asking *"fix bug in..."* questions — 40% more debugging queries than before. The change was invisible to every dashboard: latency flat, cost flat, error rate flat. But faithfulness quietly dropped, because the retriever and the golden set were tuned for factual/procedural queries and had nothing grounding debugging answers. Detection came only from a **centroid-shift measurement**: reference query embeddings vs. recent query embeddings, cosine distance 0.35 > 0.3 → alert → the team added bug-fix examples to the golden set → faithfulness recovered. The alternative (waiting for users to complain) is the Sana story again.

**The decision you must make:** how to detect distribution shift early (4.8a), and what to do when the alert fires — without drowning in false alarms (4.8b). The 0.3 threshold and the response workflow are both decisions, not defaults.

---

### Topic — Centroid shift: reference vs recent embeddings, cosine distance, per-query distances (4.8a)

**Mastery =** you can compute a centroid-shift drift score by hand, implement the detector, and explain per-query distances' role in diagnosing *which* queries moved.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

2-d worked example (lecture §4.8 math, exact numbers). Reference queries (golden-set-like, 3 points): R = [(1.0, 0.0), (0.9, 0.1), (0.95, 0.05)]. Recent queries (debugging-heavy, 3 points): Q = [(0.6, 0.8), (0.5, 0.86), (0.7, 0.7)].

- Reference centroid: mean = ((1.0+0.9+0.95)/3, (0.0+0.1+0.05)/3) = **(0.95, 0.05)**.
- Recent centroid: ((0.6+0.5+0.7)/3, (0.8+0.86+0.7)/3) = **(0.60, 0.7867)**.
- Cosine similarity: dot = 0.95·0.60 + 0.05·0.7867 = 0.57 + 0.0393 = **0.6093**. Norms: ‖ref‖ = √(0.9025 + 0.0025) = √0.905 ≈ 0.9513; ‖rec‖ = √(0.36 + 0.6189) = √0.9789 ≈ 0.9894. cos = 0.6093 / (0.9513 × 0.9894) = 0.6093 / 0.9412 ≈ **0.6474**.
- **Drift score = 1 − cos = 0.3526 > 0.3 → ALERT** — this mirrors the case study's 0.35 almost exactly; you just reproduced the week-5 detection by hand.
- Per-query distance for q1 = (0.6, 0.8): cos(q1, ref_centroid) = (0.6·0.95 + 0.8·0.05) / (1.0 × 0.9513) = 0.61 / 0.9513 ≈ 0.6412 → distance **0.359**.

```python
import math


def cosine(u, v):
    return sum(a * b for a, b in zip(u, v)) / (
        math.sqrt(sum(x * x for x in u)) * math.sqrt(sum(x * x for x in v))
    )


ref = [(1.0, 0.0), (0.9, 0.1), (0.95, 0.05)]
recent = [(0.6, 0.8), (0.5, 0.86), (0.7, 0.7)]
ref_c = tuple(sum(p[i] for p in ref) / len(ref) for i in range(2))
rec_c = tuple(sum(p[i] for p in recent) / len(recent) for i in range(2))
drift = 1 - cosine(ref_c, rec_c)
assert abs(ref_c[0] - 0.95) < 1e-9 and abs(ref_c[1] - 0.05) < 1e-9
assert abs(rec_c[0] - 0.60) < 1e-9
assert abs(drift - 0.3526) < 1e-3 and drift > 0.3
print("centroid shift:", round(drift, 4), "-> ALERT")
```

Expected: `centroid shift: 0.3526 -> ALERT`.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `projects/04-ai-engineering/devmate/obs/drift.py` with `class DriftDetector`: `__init__(embed_fn, reference_queries)` computes and stores the reference centroid; `compute_drift(recent_queries) -> dict` returns `drift_score`, `alert` (score > 0.3), `query_distances` (per-query list), `reference_size`, `recent_size`. Use real embeddings via `EmbeddingService` (`src/devmate/index/embeddings.py`) or a local mock for tests.
- Reference set: your 25 golden questions. Recent set: the 20 synthetic queries from 4.1d (debugging-heavy). Run it and write `evaluations/rag/reports/drift-<date>.md` — drift score, alert verdict, the 5 queries with the highest per-query distance (name the pattern you see: they're the "fix bug in..." ones).
- Tests in `tests/unit/test_drift.py`: the 2-d worked example above (exact numbers), identical sets → drift ≈ 0, empty recent set → error (never divide by zero).
- **Deliverable:** `drift.py`, test, report. **Acceptance criteria:** pytest green; the report reproduces the case study (score > 0.3 on the debugging-heavy set).

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Window design and multi-centroid drift. The single-centroid design has known failure modes: a *balanced* shift (half the queries move to debugging, half to factual) keeps the centroid nearly still — drift hides. And the reference window is a decision: too small → noisy, too large → stale. Design:

- Per-category centroids (factual/procedural/debugging/architecture/edge): compute drift *per centroid* and a combined score (max or weighted mean). Prove on synthetic data that the balanced-shift scenario is invisible to the single centroid but caught per-category.
- Window policy: reference = last 4 weeks vs. fixed golden set vs. quarterly re-anchoring; document the staleness trade-off.
- **Write an ADR-style justification:** single centroid vs. per-category centroids + window policy. Consequences must include the alert-rate math (5 categories × 0.05 false-alarm rate → expected false alerts/month) and a revisit condition.

**Verify:** pytest green; the balanced-shift synthetic case in the ADR shows single-centroid drift < 0.3 but per-category > 0.3.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Drift says 0.9 on day one | Reference and recent sets overlap in time | Reference must be *before* the window; no shared queries |
| Balanced shift invisible | Single centroid cancels opposing moves | Per-category centroids (L3) |
| Distance 0.95 for every query | Different embedding model between reference and recent | Pin the embedding model + version in the detector config |
| Empty recent set → crash | No guard | Error, not crash; the report states "insufficient data" |
| Drift fires on a new user cohort (legit) | Any distribution change alerts | The response workflow (4.8b) distinguishes expected shifts |

**Interview:** *"How do you detect query drift in an LLM system, and what does the number mean?"* Strong answer: reference vs. recent embedding centroids, cosine distance as the score; per-query distances for diagnosis (which queries moved); per-category centroids for balanced shifts; and the honest limit — drift says *the distribution moved*, not *quality broke*; coupling with per-intent faithfulness (4.1d) says whether it matters.

---

### Topic — Alerting: threshold choice (>0.3), avoiding alert fatigue, response workflow (4.8b)

**Mastery =** you can set and defend a drift threshold, compute the false-alarm rate your choice implies, and run the response workflow (alert → diagnose → add golden examples → re-verify).

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Threshold math. The drift score is a sample statistic; a 25-query window has noise. Suppose the true distribution is unchanged, and per-window drift scores (computed on 4 weeks of simulated data) are: 0.11, 0.09, 0.15, 0.21, 0.12, 0.08, 0.14, 0.18, 0.10, 0.13, 0.22, 0.16.

- With threshold 0.30: **0 alerts** in 12 windows (max is 0.22) → false-alarm rate ≈ 0 — safe but possibly blind to smaller real shifts.
- With threshold 0.20: 2 of 12 alert (0.21, 0.22) → false-alarm rate ≈ 17% — one false alert per ~6 weeks.
- With threshold 0.10: 11 of 12 alert → alert fatigue (nobody reads alerts anymore).

Hand-compute and record: for each threshold, alerts/12 and the implied false-alarm rate. Then design the fatigue mitigations: (1) **cooldown** — after an alert, suppress for 7 days; (2) **confirmation** — alert only if 2 consecutive windows exceed the threshold; (3) **severity tiers** — > 0.3 warning, > 0.45 page. Write the final rule you'd ship: *"alert when drift > 0.3 OR (2 consecutive windows > 0.25); page only at > 0.45; max 1 alert/week (cooldown)."* State why the lecture's 0.3 is a good default: it sits above the ~0.22 noise ceiling in this exercise.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

Wire alerting into `devmate/obs/drift.py` and run the response workflow:

1. Add `check(recent_queries, threshold=0.3, cooldown_days=7) -> dict` that returns `alert` and writes `evaluations/rag/reports/drift-alerts-<date>.log`; a CLI entry `poetry run python -m devmate.obs.drift --recent <jsonl>` that **exits 1 when alerting** (CI-usable).
2. Prove both branches: reference-like recent set (your golden questions rephrased) → exit 0; debugging-heavy set (4.1d's 20 queries) → exit 1.
3. **Response workflow (the case-study ending):** add 3 bug-fix golden questions to `evaluations/rag/datasets/devmate-golden.jsonl` (e.g., "Why does the semantic cache return stale results after a file changes?"), re-run the eval, and record in `evaluations/rag/reports/drift-response-<date>.md`: drift score before, alert, actions taken, faithfulness before/after (the lecture's story: faithfulness recovered after adding the examples).
4. **Deliverable:** drift alerting + response report. **Acceptance criteria:** exit codes proven (0/1), the report tells the full story with numbers.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

The alert-to-action loop as a product. Drift alerts are only worth anything if the response is rehearsed. Design and document the runbook:

- Triage: is the shift expected (product launch, docs campaign) or unexpected? (Check the product calendar — 4.1d's benign/harmful classifier.)
- Diagnosis: per-query distances → top patterns → do we lack golden examples (the case-study fix) or lack *index content* (Q6-style missing files) or is it a retriever tuning issue?
- Golden-set expansion policy: who writes the new questions, what budget rule bends (4.2b L3), how the baseline is re-anchored after the dataset changes (4.6b L3).
- **Write an ADR-style justification:** alert-only vs. alert + auto-dataset-expansion vs. alert + on-call runbook (chosen). Consequences must include the response-time SLA (how fast the golden set grows after a confirmed drift) and the false-alert cost of automation.

**Verify:** runbook document exists (in the drift-response report or `evaluations/rag/dashboards/devmate-alerts.md` from 4.9a); exit-code drill green; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Alerts ignored within a month | Threshold too low (0.1) | Noise measurement (L1 exercise); > 0.3 default; cooldown |
| Alert fires once, never again | Nobody acted → team desensitized | The runbook: every alert has an owner and a logged action |
| Golden set grows forever after alerts | Every drift adds questions | Expansion policy with a budget and review (4.2b L3) |
| CI fails on drift randomly | Eval window contains drifted traffic | Don't gate CI on drift; gate on regression (4.6) — drift is a dashboard alert |
| Alert, but quality is fine | Benign shift (new cohort) | The benign/harmful classifier (4.1d L3) |

**Interview:** *"Walk me through what happens when your drift alert fires."* Strong answer: verify it's not noise (consecutive windows, threshold vs. measured noise) → classify benign vs. harmful (calendar + per-intent quality) → diagnose via per-query distances → act (add golden examples / fix index / tune retrieval) → re-run eval to prove recovery → log the whole loop. Bonus: mentions the max-1-alert-per-week design goal to protect the signal.

---

# 4.9 Production Dashboards

## Real-world problem: $30k/month with no dashboard

The finance meeting is tomorrow. The $30k/month LLM bill (the 4.7 story) has one chart: total spend, going up. Nobody can answer: *Is quality dropping? Is the cache helping? Are we slow for some users? Is drift eating us?* The data exists — spans in Langfuse, cost records in `obs/cost.py`, drift scores in reports, error logs in the API — but it's scattered across four systems and zero dashboards. On-call is blind: a quality regression gets discovered by a tweet, not by an alert.

**The decision you must make:** which metric groups to watch (4.9a) and which panels to build first (4.9b) — knowing that a dashboard nobody reads is worse than none, so every panel must map to a decision someone actually makes (stop the rollout / fix the cache / add golden examples).

---

### Topic — Metric groups & alert thresholds: latency, quality, cost, cache, errors, drift (4.9a)

**Mastery =** you can define the six alert rule groups with exact expressions, thresholds, severities, and actions — and defend each threshold against the noise math you did in 4.6a/4.8b.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Write the alert spec table (this is the deliverable of the drill) for all six groups from the lecture:

| Group | Rule (expression) | Threshold | Severity | Action |
|---|---|---|---|---|
| Latency | `histogram_quantile(0.95, rate(rag_latency_seconds_bucket[5m]))` | > 5 s | P1 | Rollback recent deploy / check stage spans |
| Quality | `avg_over_time(rag_faithfulness[7d])` | < 0.8 | P1 | Add golden examples / revert prompt |
| Cost | `sum(rate(rag_cost_usd_total[1h]))` daily projection | > daily budget | P2 | Cache tuning, model downgrade |
| Cache | `rag_cache_hits_total / (rag_cache_hits_total + rag_cache_misses_total)` | < 0.20 | P2 | Investigate query diversity / threshold |
| Errors | `sum(rate(rag_errors_total[5m])) / sum(rate(rag_requests_total[5m]))` | > 1% | P1 | Check LLM provider / guardrails |
| Drift | `rag_drift_score` (weekly job) | > 0.3 | P2 | The 4.8b runbook |

For each row, write one sentence interpreting the expression (e.g., latency: "the 95th percentile request over the last 5 minutes must stay under 5 s"; quality: "the 7-day rolling mean faithfulness must stay above 0.8"). Then defend one threshold against noise: quality < 0.8 with the week-7 story (0.91 → 0.82 caught; the gate sat above the regression and below the healthy baseline) — where would you set it if run-to-run noise were ±0.05 (4.6a L3 answer: at least 2× noise above the regression point → 0.82 + 0.10 ≈ 0.85, i.e., the alert must not fire on noise but must fire before 0.82).

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `evaluations/rag/dashboards/devmate-alerts.md`: the six-rule table above completed with *your* numbers (budget = your measured eval-run cost scaled to production, e.g., $/day), a severity taxonomy (P1 = page, P2 = ticket, P3 = log), and the runbook pointer for each group (quality → 4.8b workflow; latency → 4.7a spans).
- Wire what's wireable today: the drift alert exit code from 4.8b, and a `devmate/obs/metrics.py` stub that exposes Prometheus-style counters (`rag_requests_total`, `rag_errors_total`, `rag_cache_hits_total`, `rag_cache_misses_total`, `rag_cost_usd_total`, `rag_latency_seconds_bucket`) — increment them in the instrumented `rag.py` (4.7a) so the dashboard data exists before Grafana does.
- **Deliverable:** alerts spec + metrics stub. **Acceptance criteria:** the spec has all 6 groups with expression/threshold/severity/action; `poetry run pytest -q` still green (metrics stub is covered by a smoke test that calls each counter).

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

Alert tuning as an engineering discipline. Every threshold you wrote in L2 is a guess until measured. Run the tuning study:

- Collect 4 weeks of synthetic production data (simulate: normal weeks, one slow week, one drift week, one cache-degraded week). Compute, per alert rule: true positives, false positives, missed alerts. Tune thresholds until FP/week ≤ 1 per rule.
- Derive an SLO from the latency threshold: p95 < 5 s at 99% of 30-day windows → error budget = 1% of windows — and state what the budget permits (one bad day per ~3 months).
- **Write an ADR-style justification:** fixed thresholds vs. quarterly tuned thresholds vs. auto-thresholding (percentile-based). Consequences must include the tuning cost per quarter and the guarantee that a regression caught by CI (4.6) never needs the dashboard alert (defense in depth, not redundancy).

**Verify:** the tuning table (rule × FP/TP on the synthetic month) in the ADR; alerts spec updated with tuned values.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Every panel is red on day one | Thresholds below normal operating noise | The 4.6a/4.8b noise math applied to every threshold |
| Nobody looks at the dashboard | Panels don't map to decisions | Every panel has an owner + action (the spec's Action column) |
| Alert fires during every deploy | No deploy window / warmup handling | Suppress alerts for 10 min after a deploy event |
| Cost alert always on | Budget set below baseline | Budget = baseline × 1.3, reviewed quarterly |
| Quality alert fires after the damage | Rolling 7d average is slow | Add a faster canary: 1-day faithfulness on a 5-question subset |

**Interview:** *"What are your six dashboard groups, and how do you set thresholds that don't scream?"* Strong answer: latency/quality/cost/cache/errors/drift, each with an expression, a noise-derived threshold, severity, and action; the discipline: thresholds come from measurement (run-to-run noise, FP/FP tuning on synthetic months), not from guesses; and the defense-in-depth point — CI catches regressions before they ship, dashboards catch them after, by design.

---

### Topic — Grafana/Langfuse panels: PromQL expressions, dashboard layout (4.9b)

**Mastery =** you can translate the six alert rules into dashboard panels, write the JSON, and lay out a dashboard that tells the production story at a glance.

**🏋️ Level 1 — Drill** (mechanics, 20–45 min)

Translate the lecture's four expressions into panels, then hand-compute one panel's output on a sample series:

| Panel | Expression | What it shows |
|---|---|---|
| End-to-End Latency | `histogram_quantile(0.95, rate(rag_latency_seconds_bucket[5m]))` | 95th percentile E2E latency over 5 min |
| Faithfulness (7-day avg) | `avg_over_time(rag_faithfulness[7d])` | 7-day rolling mean faithfulness |
| Cost per Query | `sum(rate(rag_cost_usd_total[1h])) / sum(rate(rag_requests_total[1h]))` | USD per request, hourly rate |
| Cache Hit Rate | `rag_cache_hits_total / (rag_cache_hits_total + rag_cache_misses_total)` | Instantaneous cache hit rate |

Hand-compute the cache panel: 5-min sample — hits total = 120, misses total = 30 → hit rate = 120/150 = **0.80**. Now the same with hits = 12, misses = 60 → **0.167 < 0.20 → alert condition visible on the panel**. Then answer: which two panels would you add beyond the lecture's four (suggest: Error Rate and Drift Score), and why the layout order matters (top row = user-facing health: latency + errors; middle = quality; bottom = cost + drift — the "at a glance" scan order). Write the panel list with titles and row assignments — that's the drill's output.

**💻 Level 2 — Applied** (DevMate, 1–3 h)

- Create `evaluations/rag/dashboards/devmate-production-dashboard.json` — a Grafana-importable dashboard (simplified per the lecture's JSON structure) with **six panels**: End-to-End Latency (p95), Faithfulness 7-day avg, Cost per Query, Cache Hit Rate, Error Rate, Drift Score — each with title, the correct expression, a unit, and a threshold line (the values from 4.9a).
- **Deliverable:** the JSON + `evaluations/rag/dashboards/dashboard-readme.md` explaining: which Langfuse/export data each panel reads (traces for latency; `obs/metrics.py` counters for errors/cache/cost; weekly drift report for drift), how to import into Grafana, and a screenshot or export of the Langfuse UI equivalent (Langfuse has built-in trace dashboards — the readme documents what you looked at).
- **Acceptance criteria:** `python -c "import json; json.load(open('evaluations/rag/dashboards/devmate-production-dashboard.json')); print('json ok')"` → `json ok`; exactly 6 panels; every expression matches the 4.9a spec.

**🚀 Level 3 — Stretch** (production-grade, 3–6 h)

From dashboard to decision. A dashboard is an interface to a decision system. Complete the loop:

- **Audience mapping:** who looks at which row (on-call = top row + P1 alerts; eng lead = quality row + CI regression summary; finance = cost panel + weekly cost report from `cost_tracker.get_summary()`). Document the mapping.
- **Anomaly detection:** beyond fixed thresholds, add a 7-day-vs-28-day comparison panel (e.g., `rag_faithfulness[7d]` vs `rag_faithfulness[28d]` delta) — catches gradual decay fixed thresholds miss.
- **Cost anomaly drill:** simulate a pricing/config error (e.g., generation model swapped to opus — `MODEL_PRICING` has it at $15/$75 per M) and show which panel+alert catches it within the hour. Document the drill.
- **Write an ADR-style justification:** fixed-threshold dashboards vs. threshold + anomaly-delta panels vs. ML-based anomaly detection. Consequences must include the operational cost of each and which failure mode each still misses.

**Verify:** the dashboard JSON validates; the readme exists with the audience mapping; the cost-anomaly drill is documented with the panel that catches it; ADR exists.

**Common failure modes:**

| Symptom | Cause | Fix |
|---|---|---|
| Dashboard imports but panels are empty | Metric names don't match the exporter | Panel expressions must match `obs/metrics.py` counter names exactly |
| p95 panel shows spikes that don't match reality | Histogram bucket boundaries too coarse | Buckets at 0.5/1/2/3/5/8/10 s; `histogram_quantile` needs the `_bucket` series |
| Cost panel shows $0 | Rate over `_total` with no samples yet | Use `sum(rate(...))` over a window; verify with the counter smoke test |
| Drift panel is static | Drift computed weekly, not continuously | Panel reads the weekly job's output; annotate alerts on the panel |
| Nobody reads the dashboard | Too many panels | 6 panels max; every panel has an owner and action (4.9a spec) |

**Interview:** *"Design the production dashboard for a RAG system from scratch."* Strong answer: six metric groups mapped to decisions (not vanity panels); layout by scan order (user-facing health on top, cost/drift on bottom); PromQL expressions with the histogram/label gotchas handled; and the closing point — the dashboard is only half the system, the alerts + runbooks (4.9a) are the other half.

---

## Definition of done for this workbook

This workbook is complete when **all** of the following hold (check off as you go):

- [ ] **Golden set:** `evaluations/rag/datasets/devmate-golden.jsonl` exists with 25 questions, lecture schema, exact category budget 8/6/4/4/3, difficulty spread 10/10/5, `expected_source_files` in metadata, and passes `eval/dataset_validate.py` (4.1a, 4.2a, 4.2b, 4.2c).
- [ ] **Metrics:** `devmate/eval/metrics.py` implements context precision@k, recall@5/@10, MRR, faithfulness (with zero-claims rule), answer relevancy — all pytest-verified with the worked numbers from this workbook (4.3a–4.3d).
- [ ] **Judges:** `devmate/eval/judge.py` implements faithfulness + relevancy judges (temperature 0, structured parsing, fallbacks); judge bias/verbosity/agreement reports exist (4.4a–4.4c).
- [ ] **Harness:** `devmate/eval/run_ragas.py` runs the golden set through the real `RAGPipeline`, prints a per-question metrics table, saves JSON + MD reports; `make eval` prints the table (4.5a, 4.5b); run < 5 min, cost < $0.50, proven by the report's numbers.
- [ ] **Regression gate:** `devmate/eval/check_regression.py` + `evaluations/rag/baselines/devmate-baseline.json`; the injected-bug drill fails the gate (exit 1) and reverting passes (exit 0); `.github/workflows/eval.yml` exists with correct repo-relative paths (4.6a, 4.6b).
- [ ] **Tracing:** `RAGPipeline.query()` emits all stage spans (guardrails, cache, embedding, search, rerank, prompt, generation, response) with latency/token/cost metadata; `test_traces.py` asserts the span tree; Langfuse export report exists (4.7a, 4.7b).
- [ ] **Drift:** `devmate/obs/drift.py` detects the debugging-query shift (> 0.3, exit 1), reference-like queries pass (exit 0); the response workflow added bug-fix golden examples and the report shows the recovery (4.8a, 4.8b).
- [ ] **Dashboards:** `evaluations/rag/dashboards/devmate-alerts.md` (6 rules) and `devmate-production-dashboard.json` (6 panels, valid JSON) exist (4.9a, 4.9b).
- [ ] **ADR:** at least one ADR-style justification under `docs/decisions/` (next free number ≥ 0007) with Context / Decision Drivers / Options Considered / Decision / Consequences — citing measured numbers from this workbook.
- [ ] **Mistakes:** every failure mode you actually hit is logged in `projects/04-ai-engineering/devmate/mistakes.md`.
- [ ] **Interviews:** all 24 interview questions answered aloud, 2 minutes each, recorded (Technical English rule, track §7).
- [ ] **Tracking:** every topic row in the completion tracker above has evidence; nothing is marked done on "feels understood".

*Workbook created 2026-08-11 for ADR-0006 (production-focused curriculum anchored to DevMate). Report format follows `evaluations/rag/reports/2026-06-26-baseline.md` and `evaluations/rag/README.md` conventions.*
