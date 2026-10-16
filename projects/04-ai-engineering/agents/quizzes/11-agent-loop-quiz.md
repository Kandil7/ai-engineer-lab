# Quiz 11: The Agent Loop

Fifteen questions covering Lecture 11 end to end: the control loop, tool
contracts, state and checkpoints, planning patterns, termination, failure
handling, approvals, frameworks, agent-to-agent calls, and evals. Five Easy,
seven Medium, three Hard. Easy answers earn 1 point, Medium 2, Hard 3.

---

### Question 1: Stages of the loop

Perceive state, plan one action, act through a tool, record the result.
Which ordered list names the four loop stages correctly?

A) Prompt, complete, validate, stop
B) Perceive, plan, act, observe
C) Search, read, test, answer
D) Think, approve, execute, log

**Difficulty:** Easy

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** Perceive summarizes state, plan picks one action, act
validates and dispatches, observe records a structured result. The
distractors name activities, not stages.
</details>

---

### Question 2: Why a control loop

The lecture calls the agent loop a control loop. What does that framing
contribute beyond a new name?

A) It proves agents need no stopping condition
B) It maps agent failures to known control failures like unbounded runs and ignored sensors
C) It shows tools are unnecessary when the model is strong
D) It replaces evals with stability proofs

**Difficulty:** Easy

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** Control theory converts vague worries into a checklist:
no setpoint means hunting forever, broken sensors mean oscillation, silent
actuator faults mean corruption. Each maps to an agent failure with a fix.
</details>

---

### Question 3: DevMate's real bound

In DevMate's `ReActAgent.run()`, what enforces the hard iteration bound,
and what happens when it is reached?

A) A token counter pauses the run for human review
B) `range(self.max_steps)` ends the loop and returns the maximum-steps message
C) The model is instructed to count its own steps
D) The tracer kills the run after a fixed wall-clock time

**Difficulty:** Easy

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** The loop at `agent.py:528` iterates `range(self.max_steps)`
with a default of 10, falling through to the maximum-steps message at
`agent.py:549`. The bound lives in the construct, so it holds when planning fails.
</details>

---

### Question 4: Unknown tools

DevMate's model names a tool outside the registry. What does the real agent
do, and why is that the correct manners for any loop?

A) Raises ValueError and crashes so the bug surfaces loudly
B) Retries the same name once in case of a typo
C) Feeds an Unknown action observation back so the loop can recover
D) Silently skips the step and continues planning

**Difficulty:** Easy

<details><summary>View Answer</summary>
**Correct Answer:** C
**Explanation:** `_note_invalid_action` at `agent.py:611-622` appends the
unknown name plus the available list as an observation. The tool set will
change; the loop must survive the model's stale map of it, not crash on it.
</details>

---

### Question 5: Propose versus apply

`ProposePatchTool` is DevMate's most consequential-looking tool. Why does
the lecture call it safe by construction?

A) It requires two human approvals before running
B) It validates the diff and returns it as text without ever writing a file
C) It runs only inside a sandboxed container
D) It deletes its own output after the run ends

**Difficulty:** Easy

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** The executor at `agent.py:304-331` checks path and diff
shape and returns the proposal as text. Nothing mutates, so there is nothing
to approve or resume from. Structural safety beats gated danger.
</details>

---

### Question 6: Boundary validation

A model emits `search_code` arguments missing the required `query` field.
Where should the loop catch this, and what should the repair say?

A) Inside the tool's try block, returning the raw exception
B) At the loop boundary before dispatch, naming the failed field
C) In the eval harness after the run, as a scored error
D) Nowhere, because the tool handles missing fields gracefully

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** DevMate's `{"raw": text}` fallback at `agent.py:515` lets
malformed input reach `execute` as a surprise. Boundary validation replaces
one expensive wasted round trip with one cheap informed replan.
</details>

---

### Question 7: Stuck detection precision

Steps 4 and 5 call `read_file` on the same locked path with the identical
permission error and no replan step between. Which variation should NOT fire
the stuck detector?

A) Step 5 carries a replan flag with new arguments
B) The repeat is non-adjacent, with other work between
C) A flaky call is retried once with backoff after a timeout
D) All of the above should not fire it

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** D
**Explanation:** The rule is narrow: consecutive identical action-plus-
observation pairs with an unchanged approach. A flagged replan, a gap, and
a backoff retry each differ in exactly the checked dimension.
</details>

---

### Question 8: Checkpoints before, not after

A destructive call is approved and about to run. When is the checkpoint
captured, and what does resume do with it after an interruption?

A) After the call, to record what changed for the audit log
B) Before the call, to restore-then-continue without repeating it blindly
C) Only when the call fails, to preserve the error for debugging
D) Never, because approvals already make the call safe

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** A pre-action snapshot of step index plus state lets resume
verify effects: present means continue, absent means repeat once, partial
means escalate. Approvals authorize; checkpoints recover. Different jobs.
</details>

---

### Question 9: Planning pattern selection

A task decomposes into run tests, read three failing files, propose patches,
and a human wants to review the approach before anything runs. Who wins?

A) ReAct, because interleaving adapts to every surprise
B) Plan-and-execute, because the plan is reviewable once, with plan versioning carrying the weight
C) Reflection, because the critic guarantees patch quality
D) Open-loop scripting, because the steps are already known

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** Separated planning yields one artifact the human approves
once instead of every step. Versioning is load-bearing: every replan must
supersede explicitly or stale steps execute under an approval they never had.
</details>

---

### Question 10: The retry rule

A tool call fails with a field-level validation error. Which response obeys
the lecture's retry discipline?

A) Retry the identical call twice in case the failure was transient
B) Fix the named field, retry once, and state the difference in the thought
C) Switch to an unrelated tool to keep the trajectory varied
D) Escalate immediately, because any failure needs human judgment

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** A retry must differ in arguments, tool, or plan, with the
difference stated beforehand so reviewers can separate persistence from
stuckness. Validation errors carry their own fix: one corrected retry.
</details>

---

### Question 11: Approval theater

A run needs six destructive calls. Which approval design preserves both
safety and autonomy?

A) Ask before every step so nothing ever runs unreviewed
B) Pre-approve all six calls once at run start to avoid interruptions
C) Batch scoped single-use receipts against the plan version with full effect statements
D) Approve the first call and treat the rest as covered by precedent

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** C
**Explanation:** Scoping binds each receipt to one exact call, single-use
stops precedent creep, batching keeps humans responsive, effect statements
keep decisions informed. Per-step asks train blind Allow clicks.
</details>

---

### Question 12: Framework adoption

A hand-rolled loop handles short runs with safe tools, but runs are growing
and resume-after-interruption tops the incident list. What is advised?

A) Rewrite in LangGraph immediately, since graphs are the standard
B) Add role-based agents, because incident classes need specialists
C) Adopt checkpointed graphs now that trajectory evidence names resume as the measured pain
D) Raise max iterations, because longer runs just need bigger bounds

**Difficulty:** Medium

<details><summary>View Answer</summary>
**Correct Answer:** C
**Explanation:** Start raw until limits are measured, then let frameworks
earn their place with numbers. Resume pain is exactly what checkpointed
graphs treat, so adoption follows measurement rather than preceding it.
</details>

---

### Question 13: A2A budget delegation

A caller with 60 seconds invokes a researcher subagent. Which delegation is
correct, and what does the held margin buy?

A) Delegate the full 60 seconds, since the callee does the real work
B) Delegate 30 seconds and hold margin so the caller can handle callee failure and still give up gracefully
C) Delegate no deadline, because researchers need open-ended time
D) Delegate approvals implicitly, since the caller was already authorized

**Difficulty:** Hard

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** Deadlines compose downward with margin held back for
handling timeout, partial results, or refusal. Full delegation turns a callee
hang into a caller hang, and approvals never transfer implicitly.
</details>

---

### Question 14: Reading an eval table

Validation fix: success 0.75 to 0.83, cost unchanged. Critic pass: success
0.83 to 0.92, cost doubled. What ships, and what needs an ADR?

A) Ship both, since every success gain is a win
B) Ship validation as a pure win; record the critic tradeoff in an ADR stating what nine points are worth
C) Ship the critic only, because 0.92 beats 0.83
D) Ship neither, because any cost increase invalidates a success gain

**Difficulty:** Hard

<details><summary>View Answer</summary>
**Correct Answer:** B
**Explanation:** Validation lifts success at unchanged cost: a pure win.
The critic trades nearly double the bill for nine points, which is neither
win nor loss until the product states the exchange rate in writing.
</details>

---

### Question 15: The unsafe success

A trajectory succeeds but trips AGT005: a destructive step ran with no
checkpoint before it. The author calls the finding cosmetic. Correct verdict?

A) Agree, because evals score outcomes and this outcome was success
B) Dismiss it, because checkpoints only matter when runs fail
C) Treat it as unsafe speed: fix the checkpoint gap before celebrating, since success without recovery is luck
D) Suppress AGT005 for successful runs to keep the suite green

**Difficulty:** Hard

<details><summary>View Answer</summary>
**Correct Answer:** C
**Explanation:** Trajectory checks score how the run was conducted, not just
how it ended. An uncheckpointed destructive call survives interruption by
luck, and luck does not generalize. Never tune a rule to flatter a run.
</details>

---

## Score Tracking

| Question | Difficulty | Points | Your answer | Correct |
|----------|------------|--------|-------------|---------|
| 1 | Easy | 1 | | B |
| 2 | Easy | 1 | | B |
| 3 | Easy | 1 | | B |
| 4 | Easy | 1 | | C |
| 5 | Easy | 1 | | B |
| 6 | Medium | 2 | | B |
| 7 | Medium | 2 | | D |
| 8 | Medium | 2 | | B |
| 9 | Medium | 2 | | B |
| 10 | Medium | 2 | | B |
| 11 | Medium | 2 | | C |
| 12 | Medium | 2 | | C |
| 13 | Hard | 3 | | B |
| 14 | Hard | 3 | | B |
| 15 | Hard | 3 | | C |
| **Total** | 5 Easy, 7 Medium, 3 Hard | **28** | | |

**Bands:** 24-28 Agent operator. 17-23 Loop literate. 10-16 Re-read concepts 5-7. Below 10 Restart the lecture.

## Answer Key

| Question | Answer | Concept tested |
|----------|--------|----------------|
| 1 | B | 1. The agent loop |
| 2 | B | 1. Control-loop framing |
| 3 | B | 5. Termination bounds |
| 4 | C | 2. Tool contracts |
| 5 | B | 7. Approvals by construction |
| 6 | B | 2. Argument validation |
| 7 | D | 5. Stuck-loop precision |
| 8 | B | 3. Checkpoints |
| 9 | B | 4. Planning patterns |
| 10 | B | 6. Failure handling |
| 11 | C | 7. Approval design |
| 12 | C | 8. Framework tradeoffs |
| 13 | B | 9. A2A budgets |
| 14 | B | 10. Reading evals |
| 15 | C | 10. Trajectory checks |

*AI Engineer Lab — AI Engineering track, agents lane.*
