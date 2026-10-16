# Glossary 01: Agent Loop Terms

Quick-reference table first, detailed definitions after. Every definition is
grounded in DevMate's real agent at
`projects/04-ai-engineering/devmate/src/devmate/agent/agent.py` or names the
repo's gap explicitly.

## Quick Reference (~40 Terms)

| Term | One-line meaning |
|------|------------------|
| Agent loop | Perceive, plan, act, observe, then decide whether to repeat |
| Control loop | A loop that reads back results and corrects; the agent's true shape |
| Open-loop system | Acts without reading results; what an agent must never be |
| Perceive | Build the state summary the planner will actually see |
| Plan | Select exactly one next action from the current state |
| Act | Validate, approve, checkpoint, then dispatch the chosen call |
| Observe | Record a structured result the next plan step can use |
| Termination | The decided ending of a run, never a hoped-for one |
| Max iterations | Hard step bound declared before the run and enforced by the loop |
| Stuck-loop detection | Stop when action plus observation repeat with no replan between |
| Success predicate | Checkable condition evaluated on every observation that ends the run |
| Graceful give-up | Stop with a partial-result report when success is unreachable |
| Partial-result report | What was tried, learned, remaining, and advised for the next run |
| Tool | A named capability with a schema, an executor, and a result shape |
| Tool schema | The JSON Schema contract admitting or rejecting arguments |
| Argument validation | Boundary check before dispatch that names the failed field |
| Tool dispatch | Routing a validated call to its executor and logging it |
| Structured result | Typed success or failure the planner can branch on |
| Tool error | A failure naming the tool, constraint, fix, and leaking nothing |
| Unknown action | A recoverable observation, never a crash, when the name misses |
| Agent state | Everything the next plan step may depend on |
| State schema | Declared keys, types, and writers for agent memory |
| Checkpoint | Step index plus state snapshot taken before a destructive call |
| Resume | Restore-then-continue from a checkpoint after interruption |
| State cap | Maximum state keys before pruning or stopping |
| ReAct | Interleaved reasoning and acting, one model call per step |
| Plan-and-execute | Full plan up front, cheap executor after, replan on surprise |
| Reflection | A bounded critic pass whose verdict feeds the next plan |
| Plan versioning | Explicit superseding of plans so actions stay attributable |
| Golden set | Frozen tasks with reference tool choices scored by hand first |
| Tool-choice accuracy | Fraction of steps matching the reference tool on the golden set |
| Argument validity rate | Fraction of calls passing schema validation on first attempt |
| Trajectory check | Deterministic structural audit of a recorded run |
| Offline eval | Scoring recorded trajectories without running a model |
| Success rate vs cost | Completion plotted against steps, tokens, and time per task |
| Human-in-the-loop | A human decides what the model may never decide alone |
| Approval | Scoped, single-use, replay-denied permission for one exact call |
| Destructive action | An irreversible call that always needs approval and a checkpoint |
| Autonomy | The default of free action inside explicit structural bounds |
| A2A call | One agent invoking another under a typed contract and budget |

## Definitions

### How to navigate this glossary

The forty terms cluster around the lecture's ten concepts. Concepts 1 and 5
own the loop vocabulary: agent loop, control loop, open-loop system,
perceive, plan, act, observe, termination, max iterations, stuck-loop
detection, success predicate, graceful give-up, partial-result report.
Concept 2 owns the contract vocabulary: tool, tool schema, argument
validation, tool dispatch, structured result, tool error, unknown action.
Concept 3 owns memory: agent state, state schema, checkpoint, resume, state
cap. Concept 4 owns planning: ReAct, plan-and-execute, reflection, plan
versioning. Concept 7 owns oversight: human-in-the-loop, approval,
destructive action, autonomy. Concept 9 owns delegation: A2A call. Concept
10 owns measurement: golden set, tool-choice accuracy, argument validity
rate, trajectory check, offline eval, success rate vs cost. Learn the
clusters before the alphabet; terms that fire together belong together.

### Easily confused pairs

**Termination vs success predicate.** Termination is the full four-layer
system that ends runs; the success predicate is one layer inside it, the
checkable condition for a good ending. A run can terminate without
succeeding (bound, stuck, give-up) but should never succeed without the
predicate confirming it.

**Checkpoint vs state schema.** The schema says what memory looks like; the
checkpoint says what memory looked like at a moment worth returning to.
Schema without checkpoints cannot resume; checkpoints without schema cannot
be queried. Rule AGT005 checks the checkpoint; no rule can check a schema
that was never written.

**Approval vs autonomy.** Approval is the exception actuator for irreversible
calls; autonomy is the default of free action inside bounds. Teams that
confuse them either gate everything (a chatbot with latency) or gate nothing
(an open-loop spender). The registry's `destructive` flag is the boundary
made machine-readable.

**Replan vs blind retry.** A replan changes arguments, tool, or plan and
states the difference; a blind retry repeats the identical call and hopes.
Stuck-loop detection cannot see intentions, only pairs — the stated
difference in the thought is what separates persistence from stuckness in
review, even when the detector stays silent.

**Reflection vs trajectory check.** Reflection is a model critic judging
meaning; a trajectory check is a deterministic rule judging structure. Use
checks in CI because they never hallucinate, and use reflection where
judgment is genuinely needed, bounded so it cannot spiral. The AGT rules are
checks, not critics.

**A2A call vs tool call.** A tool executes deterministically under its
schema; a called agent plans under its own loop with opinions about how.
The contract looks similar (envelope, result, budget) but the failure modes
differ: tools fail, agents misunderstand. Never delegate approvals
implicitly across that gap.

### Agent loop

The repeating perceive-plan-act-observe cycle wrapped around a model, ending
only through a decided stop. DevMate implements it as `ReActAgent.run()` at
`agent.py:519-549`: one model call, one parse, one tool dispatch, one
observation appended, around again. Name the loop in every design review;
if you cannot point at the code that repeats, you are describing a pipeline
with ambitions.

### Control loop

A loop that senses its output and corrects its input: thermostats, cruise
control, and — when built right — agents. The framing imports a checklist:
setpoints become success predicates, sensor faults become ignored
observations, actuator faults become unstructured tool errors, oscillation
becomes the stuck loop. It also imports the standard: a controller that
cannot stop is not a controller. See open-loop system for the failure, and
termination for the four mechanisms that prevent it.

### Open-loop system

A system that acts without reading back results — a script wearing an agent
costume. It fails silently on the first input nobody tested, because nothing
in it can notice. The lecture's rule admits no exceptions: there are no
open-loop agents. Any proposal without an observation channel and a stop
condition is a batch job; schedule and monitor it as one instead of calling
it an agent.

### Perceive

Building the state summary the planner sees: goal, history, facts, budget
left. DevMate perceives through `get_history()` at `agent.py:390-402`,
rendering each step as prose truncated to 200 characters per observation.
That truncation bounds context growth and discards detail in the same move,
which is why serious loops pair a prompt summary with a structured store the
planner can query exactly.

### Plan

Selecting exactly one next action — or the decision to stop — from current
state. In ReAct, planning happens fresh every turn from the latest
observation; in plan-and-execute, one planning pass produces a versioned
sequence the executor follows. DevMate plans by parsing `Thought:/Action:/
Input:` text at `agent.py:461-502`. Judge every plan representation by one
test: can an auditor tell which plan version an action served.

### Act

Validating arguments, checking approvals, capturing checkpoints, then
dispatching. DevMate's act stage is `_run_tool` at `agent.py:571-609`: look
up the tool, time the execution, record the step, queue the observation.
Note what it does not do — no argument validation at the boundary, no
approval check, no checkpoint — and treat each absence as a named gap with
an auditor rule, not as a style choice.

### Observe

Recording the result as structure the next plan can branch on. DevMate
converts tool output into `ToolResult` at `agent.py:21-27` and failure into
`Error: {result.error}` at `agent.py:591`, then appends it as the next user
message at `agent.py:603-609`. The observation is the loop's only sensor:
prose-only results blind it, typed results steer it. Budget observation
design like sensor design.

### Termination

The decided ending of a run through four layered mechanisms: a hard
iteration bound, stuck-loop detection, a success predicate, and graceful
give-up with a report. DevMate has layer one (`range(self.max_steps)` at
`agent.py:528`) and a declaration-style exit (`Final Answer:` at
`agent.py:539-540`) that nobody verifies. Layers two through four are this
track's core additions; the exercise proves each one executable.

### Max iterations

A positive integer bound declared before the run, enforced by the loop
construct, and recorded in the trajectory meta so auditors can check it
without reading code. DevMate defaults to 10 at `agent.py:381`. A bound
that lives only in code is a rumor; rule AGT001 flags trajectories whose
meta carries no usable bound. Size the bound from measured step
distributions, not from optimism.

### Stuck-loop detection

Stopping when the same action returns the same observation twice in a row
with no replan step between. The definition is deliberately narrow:
consecutive, identical pair, unchanged approach. Backoff retries of flaky
tools and deliberate verification repeats do not match it. DevMate lacks it —
identical `read_file` failures consume steps until the bound — and rule
AGT002 flags the pattern in recorded trajectories. Implement it before your
first production run, not after your first invoice.

### Success predicate

A checkable condition evaluated on every observation that ends the run the
moment it holds: tests passing as parsed from output, a milestone marker
present in a file, a cited answer matching the required evidence. Contrast
with DevMate's exit, where `Final Answer:` declares success and nothing
verifies it. The upgrade is small: after the declaration, run the predicate;
on failure, feed the miss back as one more observation instead of accepting
the claim.

### Graceful give-up

Stopping with a partial-result report when success is unreachable: plan
exhausted, budget nearly spent, required tool absent. DevMate's
`"Maximum steps reached without completing the task."` at `agent.py:549` is
give-up without the report. Add what was tried, what was learned, what
remains, and what the next run should do differently, and give-up becomes a
feature that makes the next run smarter instead of a silence to debug.

### Partial-result report

The give-up artifact: attempts with outcomes, facts established with
evidence, remaining work itemized, and a concrete recommendation for the
next run. It is also what escalation hands to the human, because the human
becomes the planner and deserves the state the agent had. A run that ends
without one — rule AGT007 — has an unknown ending no eval can score.

### Tool

A named capability exposing a description, a parameters schema, and an
executor returning a structured result. DevMate's `BaseTool` at
`agent.py:38-65` is the local form: `name`, `description`,
`parameters_schema`, async `execute`, `to_schema()` for advertising. Four
real tools are registered at `agent.py:335-340`. New tools enter through the
registry and inherit the loop's validation, approval, and audit discipline;
nothing dispatches outside the registry.

### Tool schema

The JSON Schema contract that admits or rejects arguments before dispatch.
DevMate's `search_code` requires `query` at `agent.py:81-99`; `read_file`
requires `file_path` at `agent.py:160-170`. Schema design is shared with the
MCP track (`projects/06-devops/mcp/`): required fields minimal, types
strict, descriptions choosable. The loop-side rule is that the schema is
enforced at the boundary, not hoped for inside each tool.

### Argument validation

Checking dispatched arguments against the schema in the loop and naming the
failed field in the repair observation. DevMate parses the model's `Input:`
text at `agent.py:485-493` and falls back to `{"raw": text}` on bad JSON at
`agent.py:515`, letting malformed input reach `execute` as a surprise.
Validation moves that failure to before dispatch, where one cheap check
replaces one expensive wasted round trip. Metric: argument validity rate.

### Tool dispatch

Routing a validated call to its executor with logging, timing, and tracing.
DevMate dispatches inside a traced span at `agent.py:584-589`, recording
success and latency. Dispatch is also where approvals are checked and
checkpoints captured — before the tool runs, never after. Unknown names
route to the recovery observation at `agent.py:611-622`, never to an
exception.

### Structured result

A typed outcome — success flag, content, metadata, error — that the planner
can branch on without parsing prose. DevMate's `ToolResult` at
`agent.py:21-27` is the pattern, including `result_count` metadata on search
at `agent.py:139-143`. Design results so the common branches (empty, many,
denied, timed out) are fields, not strings to interpret. Unstructured
results corrupt the plan the way faulty actuators corrupt the plant.

### Tool error

A failure that names the tool and rejected argument, states the violated
constraint, suggests the smallest fix, and leaks no internals. DevMate's
`read_file` guard returning `Path traversal not allowed` at
`agent.py:181-184` is the house example; its `run_tests` timeout message at
`agent.py:267` is another. Good errors make replans informed instead of
superstitious; they are the cheapest planning upgrade available.

### Unknown action

The recovery observation when the model names a tool outside the registry.
DevMate's `_note_invalid_action` at `agent.py:611-622` appends `Unknown
action: {name}. Available: [...]` and continues the loop. This is correct
manners: the tool set will change, and the loop must survive the model's
stale map of it. Log unknowns as data — clusters of them mean the prompt's
tool list is out of date, not that the model is misbehaving.

### Agent state

Everything the next plan step may depend on: goal, step history, accumulated
facts, approvals, budget consumed. DevMate's `AgentContext` at
`agent.py:375-402` holds goal, steps, counters, tools, and metadata. Audit
any state design by asking what survives a crash (here: nothing resumable),
what grows without bound (here: the steps list), and what a later step can
query exactly (here: only prose). The answers dictate the schema work.

### State schema

Declared keys, types, and writers for agent memory: `files_read: list[str]`,
`approvals: dict`, `budget_used: int`, with everything else rejected.
DevMate's metadata dict is untyped, so no consumer can rely on its shape.
Schema the state and two things become possible: exact queries during the
run ("have we read this file") and structural audits after it. Untyped
state is a shared drawer; schemed state is a database.

### Checkpoint

A step index plus state snapshot captured before a destructive call, enabling
restore-then-continue after interruption. DevMate has none — verified by
reading all of `agent.py` — and survives only because `propose_patch`
proposes text instead of mutating at `agent.py:304-331`. Rule AGT005 flags
destructive steps with no immediately preceding checkpoint. Build the
checkpoint path while every tool is still safe.

### Resume

Continuing after interruption from a checkpoint: load the record, verify the
guarded action's effects against the world, continue without repeating it if
present, repeat exactly once if absent and approval holds, escalate if
partial. Resume is why checkpoints precede actions rather than follow them.
Test it with destructive fakes before needing it for real; the exercise
simulator's checkpoint demo is the drill.

### State cap

The maximum state size — 25 keys by default in this track — before pruning
or stopping. Unbounded state is a slow memory leak: context windows fill,
prompts slow, costs climb, and old facts crowd out new evidence. DevMate sets
no cap. Rule AGT006 flags trajectories whose recorded state sizes pass the
cap. Pair the cap with a summarization policy so pruning preserves decisions
and evidence, not just the most recent prose.

### ReAct

Reasoning plus acting interleaved: one thought, one action, one observation
per turn, planned fresh from the latest evidence. DevMate's system prompt at
`agent.py:408-424` is pure ReAct. It wins under uncertainty where each
observation changes what to do next, and it costs one model call per action
with drift risk on long runs. Default to ReAct when the task's shape is
unknown; its failures are visible step by step.

### Plan-and-execute

A full plan produced up front, executed by a cheaper executor, with explicit
replanning when observations disagree. Reviewable before any action runs —
a human approves the plan once, not every step — but fragile when the world
surprises it. The load-bearing detail is plan versioning: every replan
supersedes its predecessor, and each action is attributable to exactly one
version. Without versioning it is ReAct with paperwork.

### Reflection

A bounded critic pass reviewing the trajectory for errors, waste, and
violations, feeding its verdict to the next plan. Wins on quality-sensitive
tasks where a model call is cheaper than a wrong action; costs roughly
double the calls plus the failure mode of a hallucinating critic. Bound it:
veto the next action or request one clarifying step, never rewrite history,
and log verdicts as eval data. The AGT rules are reflection mechanized —
deterministic critics that check structure, never meaning.

### Plan versioning

Numbering each plan so every action points at the plan it served. Replans
supersede explicitly; the audit trail shows which version authorized which
call and which approval batch belongs to which version. This is what makes
plan-and-execute auditable and what makes approval batches meaningful.
Version 1 approved does not authorize version 3's new destructive step.

### Golden set

Frozen tasks with hand-judged reference tool choices and expected outcomes,
the ground truth for tool-choice accuracy and success rate. Build it while
the loop is simple enough to judge by hand — DevMate's four tools make a
crisp early set — and freeze it so loop and prompt changes get
before-and-after tables. A golden set that changes with every experiment
measures nothing.

### Tool-choice accuracy

The fraction of trajectory steps whose chosen tool matches the reference on
the golden set, plus a confusion table of which wrong tools attract which
tasks. It separates choosing badly from executing badly: low accuracy with
high argument validity means the prompt's tool descriptions need work (MCP
track territory); the reverse means the parser or schema needs work here.

### Argument validity rate

The fraction of dispatched calls passing schema validation on the first
attempt, split by missing field, wrong type, and hallucinated parameter.
Every invalid call is a wasted model turn. DevMate's `{"raw": text}`
fallback at `agent.py:515` is exactly the path this metric punishes, which
is why boundary validation that names the failed field is the first fix to
ship when the rate sags.

### Trajectory check

A deterministic structural audit of a recorded run: bound declared, budget
kept, no stuck pairs, approvals present, results referenced, checkpoints
taken, state capped, outcome recorded. The eight AGT rules in
`exercises/11-agent-loop.py` are this track's check suite, and they run
without a model — which means they run in CI on every loop or prompt
change. A success that trips a check is unsafe speed, not a win.

### Offline eval

Scoring recorded trajectories without spending model calls: golden-set
comparisons, rule audits, cost accounting from logs. Offline is what makes
evals cheap enough to run always — in CI, on every change, across the whole
history. Reserve live runs for generating new trajectories and calibrating
judges, never for regression checks a recorded trajectory could answer.

### Success rate vs cost

Task completion over the golden set plotted against mean steps, tokens, and
wall-clock per task. The top-line metric that keeps the other three layers
honest: a change lifting success two points while doubling cost is a
tradeoff for an ADR, not a win to announce. Report all four eval layers
together or do not report at all; any single metric alone optimizes into
absurdity, usually the expensive kind.

### Human-in-the-loop

A human deciding what the model may never decide alone — specifically,
irreversible actions — while autonomy runs everywhere else. DevMate has no
human gate in `agent.py`, safe today only because nothing in its registry
mutates. The boundary belongs in the tool registry as `destructive: true`,
readable by loop, auditor, and evals alike. An agent asking before every
step is a chatbot with latency; approvals are the exception actuator, not
the steering wheel.

### Approval

Scoped, single-use, replay-denied permission for one exact call — tool plus
arguments — requested against a plan version and logged to the audit trail.
The mechanics (binding ids to calls, denying replays) are the MCP track's
subject in `projects/06-devops/mcp/`; the loop-side duties are checking
before dispatch and before checkpointing, treating denial as a replannable
observation, and batching asks so humans stay responsive instead of numb.

### Destructive action

Any call with irreversible effects: writing files, deleting state, sending
messages, spending money, changing permissions. Always needs approval plus a
pre-action checkpoint, and its approval never transfers implicitly to
callees in agent-to-agent calls. DevMate's registry holds no true
destructive tool today — `propose_patch` validates and returns text at
`agent.py:304-331` — which is precisely why the approval path must exist
before the first mutating tool is registered, not after the first incident.

### Autonomy

The default of free action inside explicit structural bounds: validated
schemas, declared budgets, stop conditions, and a destructive registry the
loop enforces without asking. Autonomy is what makes the agent worth
building; bounds are what make it shippable. When in doubt, widen the
bounds by improving validation and evals rather than by adding human gates —
gates scale with staffing, structure scales with software.

### A2A call

One agent invoking another as a tool with opinions, under the same
discipline as tools: a task envelope (goal, format, included context, excluded secrets), a typed result schema, a delegated budget with deadlines
held back in margin, and no implicit transfer of approvals. Keep topologies
boring — one caller, one callee, one contract — until per-edge evals justify
anything fancier. Fan-out multiplies the failure modes of termination and
recovery across a network.

*AI Engineer Lab — AI Engineering track, agents lane.*
