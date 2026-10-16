# Quiz 01: MCP Deep — Protocol, Servers, Security, and Conformance

Fifteen questions covering all ten lecture concepts: architecture and
primitives, tool design, DevMate's real server, resources and prompts,
transports, client behavior, security, reliability, registry, and evals.
Answer from the lecture and the verified repo paths, then check yourself.

**How to use:** cover the answers, pick one option per question, then open
each explanation. Score yourself with the tracking table at the end.

---

### Question 1: Who Decides Policy?

**Difficulty:** Easy

In the host/client/server split, which party enforces approval policy and
keeps the audit log?

- A) The server, because it executes the tools
- B) The client, because it holds the session
- C) The host, because it is the only trusted party
- D) The model, because it chooses the tools

<details><summary>View Answer</summary>

**Correct Answer:** C

**Explanation:** The host creates clients, enforces approvals, and writes
the audit log. Servers are untrusted by design and never grade their own
homework — policy in the server is the lecture's first listed mistake.

</details>

---

### Question 2: Requests Versus Notifications

**Difficulty:** Easy

What distinguishes a JSON-RPC notification from a request?

- A) Notifications carry an id and expect a matching response
- B) Notifications carry a method and params and expect nothing back
- C) Notifications are only used for tool calls
- D) Notifications require human approval first

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Requests carry an id and obligate a response with the same
id; notifications are fire-and-forget. Statelessness is what makes calls
loggable, replayable, and testable in the conformance suite.

</details>

---

### Question 3: Classify the Capability

**Difficulty:** Easy

A server offers "read config value db://limits/max_tokens". Applying the
lecture's decision rule, what primitive is this?

- A) A tool, because the model asked for it
- B) A resource, because it is context read by address
- C) A prompt, because it fills in a value
- D) Sampling, because the server answers back

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** If it acts it is a tool; if it is read by address it is a
resource; if it is a fill-in-the-blanks workflow it is a prompt. A URI-read
with no execution is a resource — and the scheme is what rule MCP004 checks.

</details>

---

### Question 4: DevMate's Real Tools

**Difficulty:** Easy

Which statement about DevMate's real MCP server is FACT?

- A) It exposes five tools including file deletion and sampling
- B) It exposes search_code, read_file, and get_repo_stats, and nothing else
- C) It exposes resources for every repo file plus two prompts
- D) It authenticates clients with per-tool approval ids

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** `server.py:30-77` registers exactly three tools and zero
resources or prompts; there is no auth and no sampling. The lecture records
each absence as a gap rather than inventing capabilities.

</details>

---

### Question 5: The Traversal Guard

**Difficulty:** Easy

What does DevMate's path check at `server.py:155-158` actually do?

- A) Validates the file's contents against the input schema
- B) Confines the resolved path under the repo root via relative_to
- C) Logs the request hash to the audit trail
- D) Enforces a per-tool timeout on the read

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The guard resolves the requested path against the working
root and rejects escapes — one real guard against `..` traversal. The
lecture is explicit that it is not a symlink policy, a size cap, or a log.

</details>

---

### Question 6: Empty Schema

**Difficulty:** Medium

`get_repo_stats` declares `"properties": {}`. Why does the lecture call
this an MCP001-class gap?

- A) Empty schemas crash the JSON-RPC parser on every call
- B) Neither the model nor the server can validate arguments against it
- C) It forces the tool to require human approval
- D) It makes the transport fall back from HTTP to stdio

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The schema is the contract both sides use — the model
shapes calls from it, the server validates against it. An empty schema
reduces both to guessing, which is why the auditor flags it as an error.

</details>

---

### Question 7: Transport Choice

**Difficulty:** Medium

A team wants to expose their MCP server to three client machines on the
office network. What does the lecture prescribe?

- A) Ship stdio, since pipes work across machines by default
- B) Use HTTP only after adding auth, TLS, and request logging
- C) Use HTTP as-is, since observability comes free with ports
- D) Avoid both and paste tool output into prompts by hand

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** stdio is single-machine by shape; anything on a network
moves to HTTP with auth, TLS, and logging built in. DevMate's unauthenticated
port-8001 mode is documented as a local demo transport, not a deployment.

</details>

---

### Question 8: Sampling Must Be Declared

**Difficulty:** Medium

A server starts requesting model completions mid-call without declaring
sampling. How does the lecture classify this?

- A) A transport optimization the host can ignore
- B) A capability lie — model access the host never granted
- C) A retryable transient error under the reliability contract
- D) Valid behavior, since servers are the trusted party

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The manifest is a sworn statement; undeclared sampling
(rule MCP006, critical) gives the server influence over model output outside
its admission. It is refused at runtime, not merely flagged.

</details>

---

### Question 9: Poisoned Descriptions

**Difficulty:** Medium

Why are tool descriptions treated as prompt-injection surface?

- A) They execute as code inside the server process
- B) The model reads them as instruction-adjacent text when choosing tools
- C) They are stored in the audit log alongside secrets
- D) They bypass JSON Schema validation on entry

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Descriptions feed tool choice directly, so imperative
language or URLs inside them can steer the model. Controls: admission lint,
declarative wording, and host-pinned descriptions for high-stakes tools.

</details>

---

### Question 10: Shadowing Resolution

**Difficulty:** Medium

Two admitted servers claim the tool name `read_file`. What is the
lecture's required handling?

- A) Silent first-match — the fastest server wins
- B) Registry-wide uniqueness or explicit precedence plus a visible warning
- C) Merge both implementations and average their outputs
- D) Rename at call time with a random suffix

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Exact-match dispatch on model-produced text misroutes
silently under shadowing. The registry must guarantee uniqueness or
precedence, and the client must warn whenever resolution had competition.

</details>

---

### Question 11: Retry the Write?

**Difficulty:** Medium

A destructive cache-rotation tool times out with an unknown response state.
The client auto-retries with backoff. What is wrong?

- A) Nothing — classified retries apply to every tool equally
- B) Destructive tools never auto-retry; a retry is a second unapproved effect
- C) The retry should have skipped the approval check for speed
- D) Timeouts must be disabled before any retry is attempted

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Retries are for safe tools only. A destructive retry needs
a new approval, and idempotency keys bound to the approval id make a
legitimate repeat perform the effect once. Unknown state routes to the model
as a structured error for replanning.

</details>

---

### Question 12: Replay Denied

**Difficulty:** Medium

An approval id for `wipe_cache` with argument hash `9f2c` is presented,
consumed, and presented again with identical arguments. What happens, and
why is the second outcome correct even though nothing changed?

- A) ALLOW both times — identical arguments need no re-review
- B) DENY the replay — single-use consumption bounds every grant to one effect
- C) AUDIT the replay — repeats of safe calls are only logged
- D) ALLOW once per session — ids reset when the session ends

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Consumption on first presentation is the whole defense:
without it, one reviewed grant becomes unlimited unreviewed effects. The
exercise's `decide_call` proves ALLOW-once then DENY-on-replay, and the
approval-path test automates the proof.

</details>

---

### Question 13: Drift and Rollback

**Difficulty:** Hard

A pinned server at `2.3.1` re-advertises with one new tool and no version
bump. Per the lecture, what is the correct registry behavior?

- A) Accept the tool — capabilities may widen within a pinned version
- B) Refuse the session until re-audit passes, with rollback to 2.3.1 available
- C) Log a warning and continue, since discovery output is trusted
- D) Bump the pin to `latest` so future drift is pre-approved

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Discovery output is untrusted and cached per pinned
version; widening it mid-version speaks outside the admission. The session
is refused until re-audit passes, and the retained prior admission makes
rollback one pointer move. `latest` is never a pin.

</details>

---

### Question 14: Conformance Before Admission

**Difficulty:** Hard

DevMate as shipped is put through the five-test conformance suite. Which
three tests does the lecture say it fails, and what do the failures share?

- A) Schema validity, approval path, timeout — all missing-transport defects
- B) Error shape, timeout, audit log — all absent-contract-machinery defects
- C) Approval path, drift, rollback — all registry-configuration defects
- D) Schema validity, sampling, shadowing — all model-side eval defects

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Plain-text errors fail error-shape, missing per-tool
timeouts fail timeout, and no audit log fails audit-log. Each is absent
machinery with a specified fix — the suite reads as a work list, and all
three gate admission alongside the two it passes.

</details>

---

### Question 15: Server Passes, Model Fails

**Difficulty:** Hard

A server passes all five conformance tests, but golden-set evals show low
tool-choice accuracy on two overlapping tools. Is it shippable, and what
fixes it?

- A) Shippable — conformance is the only gate; evals are advisory
- B) Not shippable — evals gate rollout equally; fix descriptions and overlap
- C) Shippable after pinning `latest` so evals track the newest behavior
- D) Not shippable — delete both tools and expose the data as raw text

<details><summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Shippable means the conformance report plus the model-side
eval report for the pinned version. A conformant server that confuses the
model fails the pair — the fix is sharper descriptions and resolved overlap,
re-scored on the golden set before rollout.

</details>

---

## Score Tracking

| Score | Level | Meaning |
|-------|-------|---------|
| 13–15 | Shippable | You can review an MCP server against this track |
| 10–12 | Staged | Re-read the concepts you missed, then re-take |
| 7–9 | Discovery | Re-read the lecture's Key Concepts 1–10 end to end |
| 0–6 | Undeclared | Start over from the Topic Overview and the glossary |

Record your score and the concepts missed — that list is your re-read plan.

---

## Answer Key

| Question | Answer | Concept |
|----------|--------|---------|
| 1 | C | 1. Architecture |
| 2 | B | 1. Architecture |
| 3 | B | 1. Primitives |
| 4 | B | 3. DevMate server |
| 5 | B | 3. Entry validation |
| 6 | B | 2. Tool design |
| 7 | B | 5. Transports |
| 8 | B | 6. Sampling |
| 9 | B | 7. Poisoned descriptions |
| 10 | B | 7. Tool shadowing |
| 11 | B | 8. Safe-only retries |
| 12 | B | 7. Approval replay |
| 13 | B | 9. Drift and rollback |
| 14 | B | 10. Conformance |
| 15 | B | 10. Evals |

*AI Engineer Lab — DevOps track, MCP lane.*
