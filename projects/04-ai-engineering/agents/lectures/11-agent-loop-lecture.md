# Lecture 11: The Agent Loop — Control, Tools, State, and Evals

## Topic Overview

An agent is a loop wrapped around a model: it perceives state, plans one
action, acts through tools, observes the result, and repeats until it should
stop. The moment you see it that way, the whole subject reorganizes itself.
A loop is a control loop, and control loops fail in known ways — unbounded
runs, oscillation, actuator faults, lost state, no stop condition. This
lecture teaches the agent loop with that discipline: tool calls as validated
contracts, state you can checkpoint and resume, planning patterns with stated
costs, termination that is decided rather than hoped for, failure handling
that replans instead of retrying blindly, human approval that composes with
autonomy, honest framework tradeoffs, agent-to-agent contracts, and evals
that run offline against recorded trajectories. Worked examples describe
DevMate's real ReAct agent honestly, gaps included.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Python, JSON Schema basics, LLM fundamentals; the MCP track (`projects/06-devops/mcp/`) for tool contracts, descriptions, and approvals, which this lecture composes per tool rather than restating; the reliability track (`projects/06-devops/reliability/`) for timeouts, retries, and idempotency, which this lecture inherits per tool rather than restating

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Model** any agent as a perceive-plan-act-observe control loop and name the failure mode of each stage
2. **Design** tool schemas and validation so that bad arguments fail before dispatch, not inside the trajectory
3. **Manage** agent state with explicit schemas, pre-action checkpoints, and resume-after-interruption
4. **Select** among ReAct, plan-and-execute, and reflection patterns by stating what each costs and when each wins
5. **Guarantee** termination with iteration bounds, stuck-loop detection, success predicates, and graceful give-up
6. **Handle** mid-trajectory tool errors by replanning, clarifying, or escalating — never by retrying blindly
7. **Place** human approvals so that destructive actions always need one while autonomy survives everywhere else
8. **Compare** hand-rolled loops, LangGraph, and role-based frameworks honestly, starting from the raw loop
9. **Specify** the contract between calling and called agents — task envelope, result schema, passed budget — with timeout and approval discipline
10. **Measure** an agent offline with tool-choice accuracy, argument validity, trajectory checks, and success rate versus cost

---

## Key Concepts

### 1. The Agent Loop Is a Control Loop

Perceive, plan, act, observe. Then decide whether to go around again. That is
the whole machine, and every agent framework is a packaging of it. The
control-loop framing matters because it converts vague worries into a
checklist with a century of engineering behind it. A thermostat without a
setpoint hunts forever; an agent without a stop condition does the same with
your API budget. A controller with a broken sensor oscillates; an agent that
ignores observations repeats the same failing call. An actuator that faults
silently corrupts the plant; a tool that returns unstructured text corrupts
the plan. There are no open-loop agents — a system that acts without reading
back results is a script wearing an agent costume, and it fails the way
scripts fail, silently, at 3 AM, on the one input nobody tested.

DevMate's real agent is this loop in its plainest form. `ReActAgent.run()`
iterates `for step_num in range(self.max_steps)` at
`projects/04-ai-engineering/devmate/src/devmate/agent/agent.py:528`, calls the
model, parses the response, dispatches one tool, appends the observation to
the messages, and goes around again. The worked example to carry through the
rest of this lecture is that loop: honest, readable, bounded by one integer,
and missing four things this lecture adds — stuck detection, approvals,
checkpoints, and a state cap. Each gap gets a rule in the exercise auditor,
so you will see the gap, then see the check that catches it.

The loop stages have crisp responsibilities. Perceive builds the state
summary the planner actually sees — DevMate does this with `get_history()`
at `agent.py:390-402`, which truncates each observation to 200 characters.
That truncation is a design decision with consequences: it bounds context
growth, and it also throws away the detail a later step might need, which is
why concept 3 demands explicit state instead of vibes. Plan selects exactly
one next action; React interleaves planning with acting so every step can
react to fresh evidence. Act validates and dispatches; observe records a
structured result. The loop then asks the only question that matters: stop,
or go around. If nothing in your system can answer that question with
authority, you do not have an agent yet. You have a while loop with a credit
card.

A concrete walkthrough fixes the stages in memory. Goal: find where retries
are configured. Step 1, perceive: the state holds only the goal, so history
reads "No previous steps." Plan: search before reading, because reading needs
a path. Act: `search_code` with `{"query": "retry"}`. Observe: two hits with
scores. Step 2, perceive: state now holds the goal plus one evidence-backed
fact. Plan: read the top hit. Act: `read_file` with its path. Observe: 42
lines including a retry constant. Step 3, perceive: the goal is answerable
from state. Plan: stop. Act: `Final Answer:` with the file and line. Three
turns, two tools, one decision to stop — that is the loop doing its job, and
every later concept in this lecture is a guardrail around one of those
three turns.

### 2. Tool Calling Deep — Schemas as Contracts

A tool is a contract with three clauses: a name the model can choose, a
schema that admits or rejects arguments, and a result shape the planner can
act on. DevMate expresses this with `BaseTool` at `agent.py:38-65`: `name`,
`description`, `parameters_schema`, an async `execute`, and `to_schema()` for
advertising. The four real tools — `search_code`, `read_file`, `run_tests`,
`propose_patch`, registered at `agent.py:335-340` — each declare required
parameters in JSON Schema form, such as `search_code` requiring `query` at
`agent.py:81-99`. The contract is only as good as its enforcement, so the
discipline is: validate arguments before dispatch, in the loop, not inside
each tool's try block. DevMate's `_parse_response` at `agent.py:461-502`
parses `Thought:/Action:/Input:` text and falls back to `{"raw": text}` on
bad JSON at `agent.py:515` — which means malformed input reaches `execute`
as a surprise. A contract-first loop rejects or repairs that input at the
boundary and tells the model exactly which field failed, so the replan is
informed instead of superstitious.

Structured results are the other half of the contract. DevMate's
`ToolResult` at `agent.py:21-27` carries `success`, `content`, `metadata`,
and `error`, and the loop converts failure into `Error: {result.error}` at
`agent.py:591`. That single convention is what makes recovery possible: the
model sees a typed failure, not a stack trace, and can choose a different
tool. A good tool error therefore has four properties: it names the tool and
the rejected argument, it states the constraint that was violated, it
suggests the smallest fix, and it never leaks internals like paths outside
the repo root or credentials. Compare DevMate's `read_file` guard at
`agent.py:181-184`, which returns the clean `Path traversal not allowed`
instead of the raw exception — that is the pattern, applied everywhere.

Descriptions are part of the contract too, and they belong to the MCP
track's territory: how to write a description the model can choose between,
how input schemas get validated, and how approvals gate destructive tools
are taught in `projects/06-devops/mcp/` and composed here, not restated.
The loop-side rule is short: the loop must refuse to dispatch what the
schema rejects, must log every dispatch with its arguments, and must treat
an unknown tool name as a recoverable observation. DevMate does the last
one right — `_note_invalid_action` at `agent.py:611-622` feeds `Unknown
action` back as an observation instead of crashing. Keep that property in
every loop you build. The set of tools will change; the loop's manners must
not.

Consider two dispatches of the same tool. Good: `search_code` with
`{"query": "retry", "top_k": 5}` — required field present, types valid, the
loop dispatches and logs the call. Bad: `search_code` with `{"top_k": 5}` —
`query` missing, so the loop rejects before dispatch and returns "tool
search_code rejected argument: missing required field 'query'; provide a
keyword or natural-language query." The model now has an informed replan in
one turn instead of a wasted tool call plus a confusing empty result. That
is the whole economics of boundary validation: one cheap check replaces one
expensive round trip, multiplied by every step of every run. Apply the same
discipline to results. A search result that carries `result_count` in
metadata lets the planner branch — zero hits means broaden the query, many
hits means read the top one. A result that is only prose forces the planner
to guess, and guessing is where trajectories go to drift.

### 3. State — What the Agent Remembers Between Steps

State is everything the next plan step is allowed to depend on: the goal,
the step history, accumulated facts, approvals granted, budget consumed.
DevMate holds this in `AgentContext` at `agent.py:375-402` — goal, steps,
`max_steps`, a counter, tools, metadata — and appends via `add_step`. That
is honest state, and it has three weaknesses worth studying. First, the only
reader is the prompt: history is rendered as text, truncated, with no
separate structured store, so nothing downstream can query "which files have
we already read" without re-reading prose. Second, nothing is ever
forgotten: the steps list grows monotonically within a run, and there is no
cap on keys or size. Third, nothing survives the process: kill the run and
the trajectory exists only in the trace spans, which cannot resume it.

A production state design answers four questions. What is the schema — which
keys exist, what types they hold, who may write each one. DevMate's metadata
dict is untyped; a schema would say `files_read: list[str]`,
`approvals: dict[action, receipt]`, `budget_used: int`, and reject anything
else. When is state written — after every observation, atomically with the
step record, so a crash between tool return and state write cannot lose the
fact that the tool ran. When is it checkpointed — before every destructive
action, capturing step index plus a snapshot, so resume means restore-then-
continue rather than replay-then-hope. And when is it pruned — a cap on keys
(default 25 in the exercise) with a summarization policy, because unbounded
state is a slow memory leak wearing a trench coat.

Checkpoints deserve emphasis because they are the cheapest reliability
mechanism an agent has. A checkpoint is taken before the action, not after:
it records where you were and what you knew, so that after an interruption
the loop can verify the action's effects and continue instead of repeating a
destructive call. DevMate has no checkpoints — verified by reading all of
`agent.py` — and its `propose_patch` tool shows why the gap is survivable
today: proposing a diff as text at `agent.py:304-331` never mutates
anything, so there is nothing to resume from. The day a tool in that
registry actually writes, deletes, or sends, the checkpoint must already
exist. Build the checkpoint path while all your tools are safe, and test it
with the destructive fakes in the exercise before you need it for real.

A checkpoint record is small on purpose: the step index it precedes, a copy
of the state dict, the action and arguments it guards, and the approval
receipt if one was required. Resume is then a procedure, not a hope. Load
the latest checkpoint. Re-read the current world for the action it guarded —
did the write land, did the delete happen, did the send go out. If the
effect is present, continue from the following step without repeating the
call. If the effect is absent and approval is still valid, repeat exactly
once, then verify again. If the effect is partial, escalate with the
checkpoint attached, because partial application is the one case where
neither blind retry nor silent skipping is safe. Practice this against the
exercise simulator: capture a checkpoint before the fake `delete_cache`,
interrupt the run, and resume from the record. The third time you do it, it
stops feeling like ceremony and starts feeling like the only sane default.

### 4. Planning Patterns — ReAct, Plan-and-Execute, Reflection

Three patterns cover nearly every agent you will meet, and they differ in
when planning happens relative to acting. ReAct interleaves them: reason
about the current state, take one action, observe, repeat. DevMate is a pure
ReAct agent — its system prompt at `agent.py:408-424` instructs exactly
`Thought:/Action:/Input:` per turn with `Final Answer:` as the exit. ReAct
wins when the world is uncertain and each observation genuinely changes what
to do next: debugging, exploration, retrieval where step two depends on step
one. It costs one model call per action, latency grows linearly with steps,
and long trajectories drift because each plan sees only a shrinking window
of why the run started. Mitigate with the goal restated in every perceive
step and a step budget that forces convergence.

Plan-and-execute separates the two phases: produce a full plan up front,
then execute steps with a cheaper executor, replanning only when a step
fails. It wins when the task decomposes cleanly — run tests, read the three
failing files, propose patches — because the plan is reviewable before any
action runs, and a human can approve the plan once instead of every step.
It costs plan fragility: the first surprising observation invalidates steps
the planner already committed to, and naive implementations execute stale
steps anyway. The fix is plan versioning — every replan supersedes the old
plan explicitly, and the audit trail shows which plan each action belonged
to. If you cannot point at the plan version an action served, you have
ReAct with extra paperwork.

Reflection adds a critic pass: after acting, a second prompt reviews the
trajectory for errors, wasted calls, and constraint violations, and its
verdict feeds the next plan. It wins on quality-sensitive tasks — patches,
answers that cite sources — where one more model call is cheaper than one
wrong action. It costs roughly double the model calls and introduces a new
failure mode, the critic that hallucinates problems and sends a good run
into a spiral of self-correction. Bound the critic: it may veto the next
action or request one clarifying step, never rewrite history, and its
verdicts are logged as data for evals rather than trusted blindly. The
exercise auditor's trajectory checks in concept 10 are reflection
mechanized: cheap, deterministic critics that never hallucinate because they
check structure, not meaning.

The cost comparison decides the default. ReAct spends one model call per
action and adapts at every step; a six-step run costs six calls and tolerates
surprise at each one. Plan-and-execute spends one large planning call plus
cheap executor calls; the same task costs fewer, larger calls but pays a full
replan whenever the world disagrees. Reflection adds one critic call per
reviewed segment; quality rises, and the bill roughly doubles. None of these
is the right pattern in general. The right question for your task is which
resource is scarcest — model calls, latency, human review time, or tolerance
for a wrong action — and which pattern spends the scarce one slowest. When
the answer is unclear, ReAct is the default because its failure mode is
visible step by step, while a bad upfront plan fails all at once.

### 5. Termination — Bounds, Stuck Detection, Success, Give-Up

Every loop needs four stop mechanisms, layered so that each catches what the
previous missed. First, max iterations as a hard bound: a positive integer,
declared before the run, enforced by the loop construct itself — DevMate's
`range(self.max_steps)` at `agent.py:528` with `max_steps: int = 10` default
at `agent.py:381`. The bound must live in the trajectory meta, not just in
code, because evals and auditors can only check what is recorded — rule
AGT001 exists for exactly this. A bound that is not written down is a rumor.
Second, stuck-loop detection: the same action with the same observation
twice in a row means the loop has stopped learning, and continuing is
burning budget to re-read the same error. DevMate lacks this — two identical
`read_file` failures will consume steps until the bound — so the exercise
implements it and the auditor flags its absence in recorded trajectories
with AGT002. Note the precision of the definition: same action plus same
observation, consecutive, with no replan step between. Retrying a flaky tool
with backoff is not stuck; repeating a deterministic failure without
changing anything is.

Third, success predicates: a checkable condition that ends the run the
moment it holds, evaluated on every observation. A predicate beats a vibe —
"the tests pass" as parsed from `run_tests` output, "the milestone file
contains TASK-DONE" as in the exercise simulator. DevMate's exit is the
model emitting `Final Answer:` at `agent.py:539-540`, which is a declaration
of success, not a verification of it: nothing checks the answer against the
goal. The upgrade path is small and worth taking — after `Final Answer:`,
run the predicate; if it fails, feed that back as one more observation
instead of accepting the claim. Fourth, graceful give-up: when the plan is
exhausted, the budget is nearly spent, or the tools needed do not exist, the
loop stops and reports partial results — what was tried, what was learned,
what remains, and what the next run should do differently. DevMate's
`"Maximum steps reached without completing the task."` at `agent.py:549` is
give-up without the report; add the report and give-up becomes a feature
instead of a failure mode.

Watch the layers fire in order on a doomed run. Steps 1-3 make progress:
search, read, test. Steps 4-5 repeat `read_file` on a locked path with the
identical permission error — the stuck detector fires at step 5 and stops
the run with a partial report instead of spending steps 6-10 re-reading the
denial. If the detector were missing, the bound still stops the run at step
10, expensively. If the file had unlocked at step 5, the success predicate
— tests passing — would have ended the run early at step 6 with a verified
win. And if the task had needed a tool the registry lacks, the planner
should have given up at step 2 with "no such tool; here is what I found so
far" instead of improvising with the wrong one for eight more steps. Four
layers, each catching what the previous missed, each producing a report
instead of a silence.

### 6. Failure Handling Mid-Trajectory — Replan, Clarify, Escalate

Tools fail mid-run the way dependencies fail in production: wrong arguments,
missing permissions, timeouts, empty results, and the occasional genuine
outage. The loop's job is to convert each failure into the cheapest correct
response, in this order: replan, clarify, escalate. Replan first, because
most failures carry their own fix. A validation error names the bad field —
fix the field and retry once with corrected arguments. A permission error on
one path means a different tool or path, not the same call louder. An empty
search result means a broader query, not the same query again. DevMate models
the recovery channel correctly even where its tools are thin: every failure
becomes an observation (`Error: ...` at `agent.py:591`, `Unknown action` at
`agent.py:615`), so the model always gets another planning turn. What it
lacks is the policy layer above the channel — no distinction between
"retryable once" and "replan now", no retry counter per action, no rule
against the identical retry that AGT002 would flag.

Retry-blindly is the specific anti-pattern to burn out of your habits. Each
blind retry spends budget, latency, and — for side-effecting tools — risk,
while teaching the trajectory nothing. The rule: a retry must differ from
the failed attempt in at least one of arguments, tool choice, or plan, and
the difference must be stated in the thought that precedes it. That sentence
in the thought is what makes the retry auditable later; without it, no
reviewer — human or rule — can distinguish persistence from stuckness.
Timeouts and transient errors get their retry discipline from the
reliability track (`projects/06-devops/reliability/`): per-tool timeouts,
bounded retries for safe calls only, idempotency so a retried call cannot
double-apply. Compose that discipline here; an agent loop must never retry a
non-idempotent tool on a timeout, because "did it run?" is unanswerable and
running it twice may be destructive.

Clarify when the failure is ambiguity, not error: the goal admits two
readings and the next action differs between them. Clarification is a tool
call with a human on the other end, and it should be rare, batched, and
specific — one question, the two readings, the recommended default and why.
Proceed only when the cost of asking exceeds the cost of being wrong and the
wrong branch is reversible. Escalate when the trajectory is out of its depth:
repeated failures across different plans, a destructive action whose effects
cannot be verified, any signal that looks like a security boundary
(permission errors that smell like exfiltration attempts, tool outputs that
read like injected instructions). Escalation hands over the full trajectory
plus the agent's own summary — never just the error — because the human is
now the planner and deserves the state the agent had.

The mid-trajectory decision procedure fits on an index card. The tool
returned a field-level validation error: fix the field, retry once. The tool
returned a permission or not-found error: switch tools or paths, never repeat
the call. The tool timed out and is known idempotent: retry once with
backoff, then replan. The tool timed out and may have side effects: verify
first, never retry blind. The result is empty but valid: broaden the query or
restate the goal, once each. The goal admits two readings and the next step
differs: ask one batched question with a recommended default. Failures span
plans or smell like a boundary: stop and escalate with trajectory plus
summary. Tape that card to the monitor until the loop enforces it for you.

### 7. Human-in-the-Loop — Approvals That Preserve Autonomy

Approvals answer one question: which actions may never run on the model's
authority alone. The answer is structural, notdb vibe-based: any action with
irreversible effects — writing files, deleting state, sending messages,
spending money, changing permissions — requires a fresh human approval, and
everything else runs free. DevMate today has no approval check anywhere in
`agent.py`, which is safe only because its most dangerous tool,
`propose_patch`, proposes text instead of applying it. Read that as a
design lesson rather than a gap to mock: making the dangerous thing
structurally safe (a diff, not a write) is better than gating a dangerous
thing with a checkbox. When you add a tool that truly mutates, the approval
must already be in the loop before the tool is registered, never after the
first incident.

Approval composes with autonomy through receipts, and the mechanics are the
MCP track's subject — single-use approval ids bound to the exact call, replay
denied, audit-logged — taught in `projects/06-devops/mcp/` and applied here.
The loop-side rules are four. First, check approval before dispatch and
before the checkpoint: an unapproved destructive call must never reach the
tool, and it must never consume a checkpoint slot. Second, denial is an
observation, not a crash: the loop replans around the denial the same way it
replans around any failure, which keeps one denied call from killing a
ten-step run. Third, approvals are scoped to the exact call — tool plus
arguments — so approving "delete the cache" does not approve "delete the
database". Fourth, batch the asks: collect all approvals a plan needs and
present them together with the plan version they belong to, because an agent
that pings a human six times per task will be answered the way car alarms
are — by nobody.

The failure mode to fear is approval theater: a human clicking allow on
every prompt because the prompts carry no information. Every approval
request must state the action, the exact arguments, the irreversible effect
in plain words, what was already tried, and what happens if denied. If the
human cannot decide from the request alone, the request is broken, not the
human. And keep the chatbot line clear: an agent that asks before every step
is a chatbot with latency. Autonomy is the default, approval is the
exception, and the boundary between them is written in the tool registry —
`destructive: true` — where auditors, evals, and future tools can all read
it.

A request worth approving reads like this: "Step 4 of plan v2. Action:
delete_cache with target 'retrieval-cache'. Irreversible effect: 37 cached
entries are deleted and must be re-embedded, costing about ten minutes.
Tried already: reading the cache manifest, which shows stale embeddings from
before the reindex. If denied: the run continues with stale results flagged
as stale." A human can decide in seconds because everything needed is
present: what, why, what it costs, what happens otherwise. Compare the
theater version — "Allow delete_cache? [Allow] [Deny]" — which trains the
human to click Allow without reading. The quality of the request is the
quality of the oversight. Write requests you would trust a tired colleague
to approve at midnight, because that is exactly who approves them.

### 8. Framework Tradeoffs, Honestly

Start with the raw loop until its limits are measured. That is the rule, and
DevMate is the worked example of why: roughly 650 lines of readable Python
implement tools, ReAct reasoning, dispatch, recovery-by-observation, and
tracing, with no framework dependency beyond the LLM client. The hand-rolled
loop buys total visibility — every stage is code you can read, log, and
test — and zero abstraction tax. It costs you every feature you have not
built yet: no checkpoints, no approvals, no stuck detection, no plan
versioning, no durable state. Those are not arguments against starting raw;
they are the shopping list you earn the right to prioritize by measuring
which absence actually bites. If your runs never exceed six steps and never
touch anything destructive, a framework buys you ceremony. If they do, the
measurements tell you which framework feature to adopt first.

LangGraph buys structure: the loop becomes a graph of nodes and edges with
named state, and checkpoints plus resume come with the platform instead of
from your backlog. DevMate gestures at this — `LangGraphAgent` at
`agent.py:625-651` detects the library and falls back to ReAct when it is
absent, which today means always ReAct. The honest accounting: LangGraph
pays off when runs are long, resumable, and multi-pathed enough that
hand-managed state becomes the bug farm. It costs a mental model (graphs,
reducers, checkpoint stores), a dependency with its own upgrades, and
debugging through framework internals when the graph does something the raw
loop never would. Adopt it when your trajectory logs show resume and
branching pain, not when a README promises them away.

CrewAI and AutoGen buy roles and handoffs: work splits across named agents
with responsibilities, and the framework routes tasks, manages conversation,
and enforces turn-taking. That wins when the task genuinely needs
specialization — a researcher, a critic, an executor — with different tools
and prompts per role. It costs coordination overhead that is invisible in
demos and dominant in production: handoff protocols, duplicated context
across agents, failure attribution across a conversation instead of a stack,
and evals that must now score a team. The multi-agent lecture nodes
(`agents.multi-agent` in the knowledge registry) go deeper; the loop-level
rule stays simple. One agent with good tools beats three agents with a
protocol, until the day the trajectory evidence says the task no longer fits
in one head. Start raw, measure, and let the framework earn its place with
your numbers, not its marketing.

### 9. Multi-Step Agents and A2A — Contracts Between Minds

When one agent calls another, everything this lecture demands of tools
applies again, because a called agent is a tool with opinions. The contract
has three parts. The task envelope: what to do, in what format, with what
context attached and — critically — what context deliberately excluded, since
every token forwarded is cost and every secret forwarded is liability. The
result schema: typed fields the caller can branch on (status, answer,
evidence ids, cost consumed), never free prose the caller must parse with
hope. And the passed budget: iterations, tokens, wall-clock, and approval
authority delegated to the callee, which the callee must respect and report
against. A caller that hands over an unbounded budget has built the
open-loop system concept 1 forbids, one level up.

Timeout and approval discipline transfers unchanged from the tool boundary,
via the reliability and MCP tracks — compose, do not restate — with two
agent-specific additions. First, approvals do not implicitly delegate: a
human approval granted to the caller covers the caller's action, not
whatever the callee decides to do with it, unless the delegation was
explicit in the envelope. The callee's destructive actions need their own
receipts, requested through the caller, attributable end to end. Second,
deadlines compose downward: if the caller has 60 seconds, the callee gets a
fraction with margin held back for the caller to handle the callee's failure
— timeout, partial result, or refusal — and still produce its own graceful
give-up. An A2A call without a deadline is a distributed hang with extra
steps.

Keep the topology boring until measurement says otherwise. A caller with one
callee and a typed contract — a researcher feeding an executor, a planner
feeding a patch proposer like DevMate's `propose_patch` grown into a real
agent — gets you nearly all the benefit with auditable attribution: every
step belongs to exactly one agent, every result crosses exactly one
contract. Fan-out to many callees, peer negotiation, and recursive
delegation each multiply the failure modes of concepts 5 and 6 across a
network, and they demand the evals of concept 10 per edge, not just per
agent. The registry's multi-agent node points at the orchestration depth;
this lecture's contribution is the constraint: agent-to-agent needs the same
timeout and approval discipline as tools, because to the caller, that is
exactly what the callee is.

An envelope makes the contract tangible. Task: "propose a patch for the
retry default in config.py." Context attached: the failing test output and
the two files already read — not the whole trajectory, not the API keys in
the environment. Result schema: status (success, partial, refused), diff
text, files touched, tests run with pass counts, budget consumed (3 steps,
2k tokens, 40 seconds). Budget delegated: 5 iterations, 4k tokens, 90
seconds, zero destructive authority — the callee may propose, never apply.
Deadline margin: the caller holds back 30 seconds to handle refusal or
timeout and still write its own give-up report. Any callee result missing a
field is rejected like any invalid tool argument: returned with the missing
field named, not parsed with hope. Boring, typed, bounded — and therefore
composable into systems you can actually operate.

### 10. Agent Evals — Score the Trajectory, Not the Vibe

Agent evals run offline against recorded trajectories, and they score four
layers. Tool-choice accuracy on a golden set: for each step, given the state
up to that point, did the agent pick the tool the reference solution picked.
DevMate's four tools make a crisp golden set — a "find the retry helper"
task should choose `search_code` before `read_file`, never `run_tests`
first — and the metric is exact-match rate plus a confusion table showing
which wrong tools attract which tasks. Argument validity rate: what fraction
of dispatched calls passed schema validation on the first attempt, with
failures broken down by missing field, wrong type, and hallucinated
parameter. This metric punishes the `{"raw": text}` fallback path at
`agent.py:515` directly, which is the point: every invalid-argument call is a
wasted model turn that a better prompt or a stricter parser would have
saved.

Trajectory checks are the deterministic critics: did it stop (an outcome
record exists), did it stay in budget (steps within the declared bound), did
it checkpoint before destructive calls, did it ask — clarify or escalate —
when stuck instead of looping. These are the eight AGT rules mechanized, and
they run without a model, which means they run in CI on every change to the
loop or the prompts. A trajectory that succeeds but trips AGT005 did
something unsafe quickly; ship the fix for the unsafety, not congratulations
for the speed. Success rate versus cost per task is the top-line metric that
keeps the other three honest: task completion over the golden set plotted
against mean steps, tokens, and wall-clock per task. A planning change that
lifts success by two points while doubling cost is a tradeoff to record in
an ADR, not a win to announce. Report all four layers together or do not
report at all — any single metric in isolation optimizes into absurdity,
usually the expensive kind.

Build the harness before the loop gets clever. Record every run as a
trajectory from day one — DevMate's trace spans at `agent.py:532-534` and
`agent.py:584-589` are the raw material — and freeze a golden set of tasks
with reference tool choices while the loop is still simple enough to judge
by hand. Then every change (a new tool, a prompt edit, a bigger bound) gets
a before-and-after table across the four layers. That table is the
difference between "the agent feels better" and "the agent is better", and
it is also what justifies framework adoption in concept 8: LangGraph earns
its place when resume-related trajectory checks go from red to green, not
before. Evals are not the tax on building agents. They are how you know you
built one.

A before-and-after table makes evals real. Baseline loop on twelve golden
tasks: tool-choice accuracy 0.83, argument validity 0.91, trajectory checks
11 of 12 clean (one missing checkpoint), success rate 0.75 at 4.2 mean steps
and 9k mean tokens. After adding boundary validation that names the failed
field: validity 1.00, success 0.83, cost unchanged — a pure win, ship it.
After adding a critic pass: success 0.92, cost 7.1 steps and 16k tokens —
nearly double the bill for nine points. That second change is not a win or
a loss until the ADR says what nine points are worth to this product. Tables
like these are the only honest way to adopt complexity. Feelings about the
agent go in the retrospective; numbers about the agent go in the decision.

---

## Common Mistakes to Avoid

1. ❌ Running the loop with no iteration bound because "the model usually stops." ✅ Declare `max_iterations` in the trajectory meta and enforce it in the loop construct.
2. ❌ Retrying the identical call after a deterministic failure. ✅ Change arguments, tool, or plan first, and state the difference in the thought.
3. ❌ Treating `Final Answer:` as proof of success. ✅ Run a success predicate against the goal after the declaration, and replan on failure.
4. ❌ Letting state grow as untyped prose with no cap. ✅ Schema the state, cap its keys, checkpoint before destructive actions.
5. ❌ Adding human approval to every step to feel safe. ✅ Gate only irreversible actions with scoped, single-use receipts; let everything else run.
6. ❌ Adopting a framework before measuring the raw loop's limits. ✅ Start hand-rolled, log trajectories, and let red evals justify each abstraction.
7. ❌ Passing free-prose results between agents with no schema or budget. ✅ Envelope the task, type the result, delegate a bounded budget with deadlines.
8. ❌ Reporting success rate without cost per task. ✅ Report tool-choice accuracy, argument validity, trajectory checks, and success-versus-cost together.

---

## Best Practices

1. Write the stop conditions before the first tool: bound, stuck rule, success predicate, give-up report.
2. Record the iteration bound in the trajectory meta so auditors can check it without reading code.
3. Validate tool arguments at the loop boundary and name the failed field in the repair observation.
4. Keep tool errors structured: tool name, violated constraint, smallest fix, no leaked internals.
5. Feed unknown tools and failed calls back as observations; never crash the loop on a bad action.
6. Schema agent state explicitly and prune it with a stated cap and summarization policy.
7. Checkpoint step index plus state snapshot before every destructive call, and test resume with fakes.
8. Restate the goal in every perceive step so long trajectories cannot drift from their purpose.
9. Version plans explicitly when replanning so each action is attributable to the plan it served.
10. Bound the critic in reflection loops: veto or one clarifying step, never history rewrites.
11. Scope every approval to the exact call and deny replays; batch asks against a plan version.
12. Give every approval request the action, arguments, irreversible effect, alternatives tried, and cost of denial.
13. Pass budgets and deadlines downward in agent-to-agent calls and hold margin for handling callee failure.
14. Run the four-layer eval suite in CI over recorded trajectories before and after every loop or prompt change.

---

## Practice Exercises

1. Trace DevMate's `run()` at `agent.py:519-549` by hand for a two-tool task and mark where stuck detection would trigger if the second tool failed identically twice.
2. Write three invalid `search_code` arguments, predict each `_parse_response` outcome at `agent.py:461-502`, then add boundary validation that names the failed field.
3. Design a state schema for a five-step patch task (files read, test results, approvals, budget) with a 25-key cap and a summarization rule.
4. Run the exercise simulator with a looping script, confirm `stuck_loop_detected`, then add a replan step and confirm success.
5. Build a three-task golden set for DevMate's four tools and score tool-choice accuracy plus argument validity by hand.

---

## Summary

1. An agent is a perceive-plan-act-observe control loop; treat it with control-loop discipline.
2. No open-loop agents: every action must read back a result, and every run must be able to stop.
3. Tools are contracts — name, schema, result shape — validated before dispatch with structured errors.
4. State is explicit, schemed, capped, checkpointed before destructive calls, and resumable.
5. ReAct reacts, plan-and-execute reviews, reflection critiques; each wins somewhere and costs somewhere.
6. Termination is four layers: hard bound, stuck detection, success predicate, graceful give-up with a report.
7. Mid-trajectory failures replan first, clarify rarely, escalate with full state; never retry blindly.
8. Approvals gate irreversible actions with scoped single-use receipts while autonomy runs everywhere else.
9. Start with the raw loop, adopt frameworks on measured evidence, and contract agent-to-agent calls like tools.

**Next lecture:** tool-use depth on golden sets — measuring choice accuracy and argument validity per tool before adding a fifth tool to the registry.
