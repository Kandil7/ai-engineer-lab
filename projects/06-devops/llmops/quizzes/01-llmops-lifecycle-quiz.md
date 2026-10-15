# Quiz 01: The LLMOps Lifecycle

## Topic Overview
This quiz covers the nine-phase LLMOps lifecycle grounded in DevMate: prompt registry and versioning, eval-gated releases with real CI floors, trace schemas and PII redaction, guardrails and content safety, deployment gates, monitoring for silent degradation, cost control, incident response with a fixed rollback order, recurring red-team suites, and governance.

---

## Questions

### Question 1
**Why are the nine LLMOps phases taught in dependency order rather than as an independent checklist?**

- A) Each phase costs more than the one before it
- B) Skipping a phase does not remove the work; it converts the work into an incident later
- C) Regulators require the phases to be completed in sequence
- D) The phases can only be tested one at a time

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Each phase assumes the previous ones exist. Without prompt versioning, an incident has no cause to point at. Without evals, quality is invisible. Without tracing, production is undebuggable. Skipping a phase postpones its function into incident response, which is the most expensive place to do it.
</details>

---

### Question 2
**What is the core reason an inline system-prompt string fails the prompt-registry discipline?**

- A) Strings consume more memory than files
- B) The model cannot parse inline prompts
- C) An edit changes production behavior with no version recorded, so no trace can attribute an answer to the text that produced it
- D) Inline strings cannot contain placeholders

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** DevMate's `RAG_SYSTEM_PROMPT` is a working inline constant with no version field. Editing its guidelines changes every `devmate ask` answer, and nothing in a trace records which text version produced a given output. A prompt edit nobody can attribute to a version is an incident without a cause — the exact failure a registry prevents.
</details>

---

### Question 3
**In the DevMate CI eval gate, what happens when the offline harness computes Hit@5 below 1.0?**

- A) A warning is posted but the merge proceeds
- B) The harness exits 1 and the pull request cannot merge
- C) The floor is automatically lowered to the measured value
- D) The golden set is trimmed to exclude the failing cases

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `run_ragas.py` implements `--fail-under-hit-at-5` by exiting 1 when the rate is below the threshold, and CI invokes it with 1.0. Below threshold: no merge, no debates, no subjective reviews. Automatically lowering the floor or trimming cases would delete the evidence — the failure mode ADR-0009 explicitly rejected.
</details>

---

### Question 4
**DevMate's CI runs `python -m devmate.eval.run_ragas --mode offline --no-report --fail-under-hit-at-5 1.0 --fail-under-mrr 0.70`. What does `--mode offline` actually score?**

- A) Live retrieval against the production Qdrant index
- B) Recorded retrieval fixtures and recorded answers — no network, no API key
- C) Freshly generated LLM answers judged by a live model
- D) Only the prompt golden cases, skipping retrieval entirely

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Offline mode scores recorded fixtures: retrieval top-k from a recordings file (or expected-context fixtures) and answers from a recorded JSONL. It never touches the network or a provider key, which is what makes it CI-safe. Live retrieval needs Qdrant plus embeddings and runs in the integration job, not the default gate.
</details>

---

### Question 5
**ADR-0009 measured offline Hit@5 of 1.000 and live Hit@5 of 0.900 on the same golden set. What is the correct engineering conclusion?**

- A) The live harness is buggy and should be fixed to match offline
- B) The offline number was fixture satisfaction, not a measurement of the index; the 0.100 gap exposed real indexing-scope defects
- C) The golden set should drop the two failing cases so both modes agree at 1.000
- D) Hit@5 is the wrong metric and should be replaced with accuracy

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The offline mode labels its own fixture path as "not a live measurement." The live run found `pyproject.toml` absent from the index and `devmate.egg-info/` artifacts polluting the top ranks — two indexing-scope defects no chunker change could fix. The lesson: a gate is only as honest as the thing it measures, and dropping the failing cases would delete the evidence.
</details>

---

### Question 6
**Which field of a production trace schema most directly answers "which instruction text produced this answer?"**

- A) request id
- B) token counts
- C) prompt version
- D) tenant id

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The request id identifies the call, token counts explain the cost, and the tenant identifies the customer — but only `prompt.version` attributes the answer's behavior to a specific state of the instructions. DevMate's golden cases already pin `prompt_version: 1.0.0`; the missing file-based registry is what would stamp it onto every trace.
</details>

---

### Question 7
**Why must PII be redacted at the ingestion boundary rather than scrubbed from the trace store later?**

- A) Redaction at read time is more accurate
- B) Traces are too large to scan for PII after the fact
- C) A trace store that ever held raw values is a breach dossier; retrofitting deletion cannot undo copies, exports, or backups
- D) Redaction filters do not run on stored traces

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** If raw emails or keys land in a trace, they have already been serialized, possibly exported to Langfuse, and possibly backed up. Redacting at the boundary — DevMate's `PIIGuardrail` substitutes `[REDACTED_*]` placeholders before content moves downstream — means the raw value never crosses the line it cannot safely return from.
</details>

---

### Question 8
**In DevMate's guardrail vocabulary, what does the action `redact` mean compared to `block`?**

- A) They are synonyms for refusing the request
- B) `redact` strips or masks the offending content and proceeds; `block` refuses the request outright
- C) `redact` logs the content for later review; `block` deletes it
- D) `redact` is only valid for output guardrails; `block` only for inputs

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The four actions are block, warn, redact, and log. Redaction substitutes placeholders (for example `[REDACTED_EMAIL]`) and lets the request continue — the right response for PII in an otherwise valid prompt. Blocking is the right response for prompt injection or system-prompt extraction, where proceeding with masked content still grants the attacker a foothold.
</details>

---

### Question 9
**Why is caching a raw, unvalidated LLM output in the semantic cache dangerous even when it raises the hit-rate dashboard?**

- A) Cached responses expire too quickly to matter
- B) A malformed or ungrounded answer becomes immortal and serves every future similar query, amplifying one error while the dashboard reports savings
- C) Semantic caches only work on exact string matches
- D) The cache threshold of 0.85 is too low to ever match

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A cache hit skips validation forever after. One ungrounded answer stored during a model hiccup is then served to every query above the 0.85 similarity threshold for the TTL, and the rising hit rate looks like success. Validate and screen refusals before storing — a cache hit must be an answer you would ship again.
</details>

---

### Question 10
**What failure mode do per-query cost budgets catch that quality evals cannot?**

- A) Prompt injection attacks
- B) Retrieval returning the wrong file
- C) A prompt edit that triples output tokens while every faithfulness and recall check still passes
- D) Provider regional outages

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Quality gates measure whether answers are correct and grounded; they do not measure what the answers cost. A prompt edit that doubles context or triples verbosity can pass every quality floor while multiplying the invoice. The per-query budget — the COST001-style gate — fails that change at merge time instead of at billing time.
</details>

---

### Question 11
**A quality regression is traced to a bad prompt merge. According to the DevMate rollback order, what do you do first?**

- A) Fail over the LLM provider to another region
- B) Roll the deployment image tag back to the previous digest
- C) Roll the prompt version back to the previous registry entry
- D) Rebuild the vector index from source

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The rollback order is prompt version first, image tag second, provider region third. A prompt rollback is a registry pointer change — seconds, no rebuild — and prompt edits are the most frequent regression class. Image rollbacks take minutes and reverse code. Region failover is the most disruptive lever and addresses provider-side infra, not your change.
</details>

---

### Question 12
**What distinguishes an alert on silent degradation from a conventional error-rate alert?**

- A) Silent degradation alerts fire only on weekends
- B) It watches quality trendlines (for example faithfulness drifting down over days) at flat error rates, catching wrong answers that never produce a 5xx
- C) It replaces all other alerts once configured
- D) It alerts only when users file complaints

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The dangerous LLM failure class is the silent one: no exception, no failed request, wrong or ungrounded output. Error-rate alerts are blind to it by construction. A silent-degradation alert watches trendlines — faithfulness declining across sampled answers while p95 latency and 5xx rates stay flat — and pages before users notice.
</details>

---

### Question 13
**Why must a prompt-injection red-team suite run on a recurring schedule rather than once?**

- A) Payloads change text every week and stop working
- B) One run is enough to prove the system is permanently safe
- C) New guardrail versions, new model pins, and new tools each change the threat surface; a static one-time suite stops measuring it, and a dropping block-rate on a frozen suite signals suite rot
- D) Recurring runs are required by the OWASP license

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The defense changes over time — every guardrail, model, or tool change reopens the question the suite answers. Run it once in week 7 and forget it, and you are trusting a measurement of a system that no longer exists. Track block-rate over time: a decline on a static suite means the suite rotted or a regression landed; investigate either way.
</details>

---

### Question 14
**An auditor asks: "What prompt and model answered a user's question in March?" What does an audit-ready LLMOps setup resolve this to?**

- A) A support ticket summarizing the conversation
- B) A month of server logs to grep manually
- C) A trace id, which resolves to the model version pin, the prompt version, and the eval snapshot the release met
- D) An apology and a refund

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Governance is the discipline that makes every production answer reconstructible. The trace id is the join key; the prompt registry supplies the instruction text; deployment config pins the model; versioned eval reports in git prove which quality bar the release cleared. Anything less than that chain is storytelling, and March is already gone.
</details>

---

### Question 15
**DevMate's `failure-modes.md` records an incident where long questions caused Ollama HTTP 500s. What was the actual root cause and class of failure?**

- A) A provider outage (transient); the fix was retrying more aggressively
- B) The retrieved-context prompt exceeded the model's context window — a silent-before-fix budget error, fixed with `rag_context_char_budget` and `ollama_num_ctx`
- C) A guardrail over-blocking (partial); the fix was disabling the guardrail
- D) A corrupted vector index (permanent); the fix was re-ingesting everything

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Short questions worked and long ones failed, so it looked like a flaky provider. The real cause was the prompt exceeding `qwen2.5-coder:7b`'s default context window — a budget error the system never checked. The fix was `rag_context_char_budget` (8000 chars) in context assembly plus `ollama_num_ctx` (8192), with regression tests. It is the textbook silent failure: no schema violation, no alert, only user-visible 500s on a subset of traffic.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Hard | | |
| 6 | Medium | | |
| 7 | Medium | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Medium | | |
| 12 | Medium | | |
| 13 | Easy | | |
| 14 | Easy | | |
| 15 | Hard | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 6 | C | 11 | C |
| 2 | C | 7 | C | 12 | B |
| 3 | B | 8 | B | 13 | C |
| 4 | B | 9 | B | 14 | C |
| 5 | B | 10 | C | 15 | B |

---

*Generated for ai-engineer-lab - Quiz 01 of 01*
