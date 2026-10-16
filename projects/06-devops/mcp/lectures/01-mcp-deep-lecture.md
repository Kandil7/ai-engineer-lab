# Lecture 01: MCP Deep — Protocol, Servers, Security, and Conformance

## Topic Overview

Model Context Protocol gives a model a typed, auditable way to reach beyond
its context window: instead of pasting tool output into prompts by hand, a
host application opens sessions to capability servers, and the model calls
their tools, reads their resources, and reuses their prompt templates
through one uniform message format. This lecture teaches the whole stack —
the host/client/server split, stateless JSON-RPC messages, the three
primitives and when each is right, Python server construction mapped step by
step to the real DevMate server in this repository, resources and prompts,
stdio versus Streamable HTTP transports, client discovery and sampling, the
security spine (injection surfaces, shadowing, approvals), reliability
composition inherited from the reliability track, registry admission and
drift detection, and the conformance checklist plus model-side evals that
prove a server is shippable. Worked examples describe DevMate's real server
honestly, gaps included.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Python, JSON Schema basics, HTTP fundamentals; the reliability track (`projects/06-devops/reliability/`) for timeouts, retries, and idempotency, which this lecture applies per tool rather than restating

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Distinguish** host, client, and server responsibilities and explain why policy lives in the host, not the server
2. **Classify** any server capability as a tool, a resource, or a prompt and defend the choice with the decision rule for each
3. **Design** tool input schemas and descriptions that let a model choose correctly and fail in ways the model can act on
4. **Build** a Python MCP server with registration, entry validation, and structured errors, mapping each step to DevMate's real server
5. **Compare** stdio and Streamable HTTP transports and select correctly for local versus remote deployments, including auth and observability consequences
6. **Trace** the client loop from capability discovery through routing to sampling, and state why sampling must be declared
7. **Enumerate** the MCP security surfaces — poisoned descriptions, tool shadowing, destructive tools, replayed approvals, secret leakage — and the control for each
8. **Compose** per-tool timeouts, cancellation, idempotency, and safe-only retries onto any tool using the reliability track's patterns
9. **Operate** a server registry with version pinning, admission checks, drift detection, and rollback
10. **Prove** shippability with the five-test conformance checklist and measure model-side tool use with golden-set evals

---

## Key Concepts

### 1. MCP Architecture — Host, Client, Server

Three roles, three trust levels. The **host** is the application the user
runs — an IDE plugin, a desktop app, an agent loop. It is the only trusted
party: it creates clients, enforces approval policy, and writes the audit
log. The **client** holds exactly one session with one server; it speaks the
protocol, routes model requests to tools, and returns results. The
**server** is untrusted by design: it advertises capabilities and executes
calls, but it never decides policy. A malicious or buggy server can lie in
its advertisements, so every claim it makes is verified elsewhere in this
lecture (concepts 7, 9, 10).

Messages are stateless JSON-RPC: a **request** carries an id, a method, and
params and expects a **response** with the same id; a **notification**
carries a method and params and expects nothing back. Statelessness means
any message can be logged, replayed in a test, or retried without hidden
session state — which is exactly what makes the approval receipts in
concept 7 and the conformance tests in concept 10 possible.

```text
model -> host: "I need the retry code"
host -> client: route to server A, tool read_file
client -> server: {"jsonrpc":"2.0","id":7,"method":"tools/call",
                   "params":{"name":"read_file","arguments":{...}}}
server -> client: {"jsonrpc":"2.0","id":7,"result":{...}}
client -> host: result + receipt (approval id consumed?)
host -> audit log: ALLOW/DENY with request hash
```

The three primitives partition all capabilities. **Tools** are functions the
model calls — they run code and can change the world. **Resources** are
addressable context the model reads — files, rows, configs — identified by
URI, never executed. **Prompts** are reusable templates with validated
arguments — stored workflows the model instantiates, not free text. The
decision rule: if it acts, it is a tool; if it is read by address, it is a
resource; if it is a fill-in-the-blanks workflow, it is a prompt. DevMate's
real server exposes three tools (`search_code`, `read_file`,
`get_repo_stats`) and zero resources or prompts — verified by reading all of
`projects/04-ai-engineering/devmate/src/devmate/mcp/server.py`. That is a
FACT about scope, and a gap this lecture keeps visible: every resource or
prompt example here is general practice, not a claim about DevMate.

Host, client, and server duties side by side:

| Duty | Owner | Why there |
|---|---|---|
| Approve a destructive call | Host | Only the user-facing app can ask the user |
| Validate arguments | Server enforces, client pre-checks | Defense in depth; the server has the final say |
| Keep receipts | Host | Servers must not grade their own homework |
| Advertise capabilities | Server | It knows what it implements |
| Choose the tool | Model, via client routing | Descriptions and schemas are its signal |

A session runs initialize, discover, call, and teardown. Initialization
negotiates versions so a stale client never misreads a new server; discovery
caches the advertisement the auditor already approved; calls carry the ids
that make responses pairable; teardown cancels what is outstanding so no
orphan work survives the session. Statelessness is what lets every one of
these steps be logged and replayed inside a test.

### 2. Tool Design — Schema as Contract, Description as UX

A tool's `inputSchema` is the contract: a JSON Schema object naming every
argument, its type, and which are required. The server validates arguments
against it on entry; the model shapes its calls from it. An empty or missing
schema means neither side can validate — the model's arguments are a guess
and the server's parsing is hope. DevMate's `search_code` declares `query`
required with `language` and `top_k` optional
(`server.py:35-53`); `get_repo_stats` declares `"properties": {}`
(`server.py:69-76`) — a real MCP001-class gap the exercise auditor flags,
honestly recorded.

The `description` is user experience for the model: it is the primary signal
the model uses to choose between tools. A description shorter than a clause
("run it", "search") leaves the model choosing blind; a good description
names what the tool does, what it needs, and what it returns, in one or two
sentences. DevMate's descriptions are single sentences
(`server.py:34,57,71`) — adequate, not generous. Naming follows the same
logic: verbs for actions (`search_code`, `read_file`), nouns for snapshots
(`get_repo_stats`), one consistent casing, no two tools sharing a prefix the
model could confuse.

Error returns are the third design surface, and the one most servers get
wrong. The model can only act on an error it can parse: name what was wrong,
which argument, and what valid looks like. DevMate returns plain-text errors
inside `TextContent` (`Error: query is required` at `server.py:96`) rather
than typed error payloads — a FACT, and a weakness: the model must parse
English strings instead of matching a code. Concept 10 turns this into a
conformance test (the error-shape test), and the exercise's rules treat
error design as shippability, not polish.

Concretely, DevMate's `search_code` schema says: an object, with a string
`query` that is required, an optional string `language`, and an optional
integer `top_k` defaulting to 5 (`server.py:35-53`). A model reading that
schema knows the one call shape that can succeed. Without it, the model
guesses argument names from description prose, the server parses
defensively, and both sides burn turns converging. Naming carries the same
contract weight — `search_code`, `read_file`, `get_repo_stats` share one
verb-phrase casing, which is what the model relies on for first-guess
routing. A fourth tool named `FileReader` or `fetch` would break the pattern;
consistency is a routing feature, not house style.

Error design follows the same principle. `Error: query is required` names
the missing argument but gives no code, no shape, and no hint — the model
must pattern-match English. The conformance target is a payload like
`{"code": "missing_argument", "argument": "query", "hint": "provide a
non-empty search string"}`, which the model can branch on without parsing
prose. Concept 10 tests exactly this upgrade.

### 3. Building a Server in Python — Mapped to DevMate's Real Server

A minimal Python server has five steps, each visible in DevMate's real code:

**Step 1 — create the server object.** `Server("devmate")` at `server.py:23`
names the capability domain. The name is the unit of admission later: the
registry pins and audits servers by name and version (concept 9).

**Step 2 — register tools.** The `list_tools` handler at `server.py:30-77`
returns three `types.Tool` objects, each with name, description, and
inputSchema. Registration is declaration, not implementation: it is the
advertisement the client discovers (concept 6) and the auditor checks
(concept 10). Nothing executes here.

**Step 3 — dispatch calls.** The `call_tool` handler at `server.py:79-87`
routes by name to `_search_code`, `_read_file`, `_get_repo_stats`, and
raises `ValueError` for unknown names at `server.py:87`. Two honest notes:
dispatch is exact-match on a string the model produced, so tool names are a
routing surface (concept 7 covers shadowing); and the unknown-tool error
propagates as an exception rather than a typed protocol error.

**Step 4 — validate on entry.** Each handler checks its required argument
first (`server.py:95-96` for query, `server.py:145-146` for file_path) and
`_read_file` adds a traversal guard resolving the path against the repo root
at `server.py:155-158`, plus existence and is-file checks at `server.py:160-164`.
This is validation in the right place — inside the server, before any work —
but in the weakest shape: hand-written `if` statements returning English
strings, with no schema validator shared between the advertised inputSchema
and the enforcement code. Drift between the two is the exact failure rule
MCP001 exists to catch.

**Step 5 — run and serve.** `run_stdio` at `server.py:193-200` speaks over
standard input/output for local clients; `run_http` at `server.py:202-234`
serves SSE over HTTP via uvicorn with routes `/sse` and `/messages/`;
`main` at `server.py:266-278` selects between them from the command line with
host and port from settings at `server.py:260-263`. FACT: DevMate has no
authentication on either transport, no per-tool timeout, and no audit log —
each gap maps to a rule or test later in this lecture rather than being
papered over here.

Running it looks like this from the repo root:

```powershell
python -m devmate.mcp.server stdio   # local clients connect over pipes
python -m devmate.mcp.server http    # serves SSE on port 8001
```

Validation order inside each handler is load-bearing: required-argument
checks first (fail before spending anything), bounds checks second
(traversal, existence, file-ness), expensive work last (embeddings,
retrieval, vector-store reads). DevMate follows this order in `_read_file`
(`server.py:145-164`) — cheap rejections before filesystem touches, and no
retrieval call until the arguments are known good. The remaining weakness is
shape, not order: hand-written `if` statements instead of one shared schema
validator, so the advertisement and the enforcement can drift apart
unnoticed. Generating both from the same schema object closes that drift.

### 4. Resources and Prompts — Addressable Context, Validated Templates

Resources give the model context by address instead of by procedure call. A
resource has a **URI** (`repo://files/config`, `db://rows/orders/42`) that
names what it is and where it lives, plus a description saying what reading
it returns. The scheme matters: it tells the client which handler and which
permission set applies. A URI without a scheme (`repo/files/config`) is not
addressable — it is a string that only a human can resolve, which is why the
exercise's rule MCP004 rejects it. DevMate exposes no resources (FACT), so
every resource in this track is presented as the pattern to add, with the
admission question attached: which schemes may this server serve, and which
paths inside each scheme are in bounds? The traversal guard in `_read_file`
is the beginning of that answer, not the whole of it.

Prompts are the third primitive and the most misunderstood. A prompt is a
stored template with a declared argument list — `Summarize {text} for
{audience}` with `args=["text", "audience"]` — that the client fills and the
model runs. The rule is absolute: **every placeholder must be listed, and
every listed argument must be validated before interpolation.** An
unlisted placeholder (`{audience}` with `args=["text"]`) is unvalidated
interpolation — caller-controlled text entering a template the model will
treat as instruction. That is the MCP005 defect in the exercise, and it is
also a prompt-injection vector, which connects directly to the security
track's injection lecture at
`projects/04-ai-engineering/security/lectures/01-prompt-injection-lecture.md`:
this track owns the mechanism (validate template arguments), that lecture
owns the adversary (crafted content inside them). Neither duplicates the
other. DevMate exposes no prompts (FACT) — so treat this concept as the
checklist to apply before the first prompt ships, not as a description of
current behavior.

A resource allow-list for a DevMate-like server would read: scheme `repo://`
serves files under the repo root, markdown and code only, 256 KB cap per
read; scheme `stats://` serves collection counts, never document contents.
Each row names the scheme, the root, the type filter, and the size cap — four
columns, no discretion at runtime. Anything outside the table is refused
with the error shape from concept 2, and the refusal itself is audit-logged.
Prompts get the parallel checklist before their first ship: every
placeholder declared, every argument typed and bounded, template text
reviewed for instruction language, and the injection review from the
security track's prompt-injection lecture signed off. A template is code;
review it like code.

### 5. Transports — stdio for Local, Streamable HTTP for Remote

Two transports, chosen by deployment shape. **stdio** spawns the server as a
child process of the client and speaks over pipes: one process pair, no
ports, no network, credentials inherited from the local user. It is the
default for local assistants — DevMate documents it as what local MCP
clients expect (`server.py:266-270`) — and its security posture is the
machine's own: if the user can run the client, they can run the server. The
cost is isolation: a crashed server takes the session with it, and there is
exactly one client.

**Streamable HTTP** (DevMate ships the older SSE variant at
`server.py:202-234`) exposes the server on a port with session management:
many clients, reconnectable sessions, observable traffic. Everything stdio
gives for free must now be built: authentication (DevMate has none — a FACT
and a gap, since port 8001 accepts whoever can reach it), TLS, session
tokens with expiry, per-client rate limits, and request logging that becomes
the audit trail. The selection rule: local single-user work stays on stdio;
anything reachable over a network moves to HTTP **with** auth, TLS, and
logging added — shipping DevMate's HTTP mode as-is onto a network would be a
deployment defect, and saying so is part of this concept.

Observability changes with the transport. On stdio, log to standard error
(never standard output — that pipe carries the protocol) and rely on the
host for retention. On HTTP, log every request with its session id, tool
name, argument hash (never raw arguments — concept 7), decision, and
latency; those logs are the raw material for the tool-choice evals in
concept 10. Either way, the server emits facts and the host keeps them: the
server never grades its own homework.

| Property | stdio | Streamable HTTP |
|---|---|---|
| Clients per server | One | Many |
| Authentication | OS user identity | Must be built: tokens, expiry, scopes |
| Confidentiality | Pipe-local | TLS required |
| Observability | Standard-error logs, host retained | Request logs with session id, hashed args |
| Failure blast radius | Session dies with child | Per-session isolation, server survives |
| When to choose | Local single-user work | Any second client or any network hop |

The row that decides is the last one. Teams reach for HTTP for convenience
and inherit its build list; this lecture's position is that the build list
is the price of admission, not an enhancement backlog. DevMate's SSE mode is
the honest middle: real enough to learn session thinking against, ungated
enough to keep off any network.

### 6. The Client Side — Discovery, Routing, Sampling

The client loop has three phases. **Discovery** starts the session: the
client calls `list_tools` (and the resource/prompt equivalents) and caches
the advertised capabilities. Discovery output is untrusted input — it feeds
routing, so a lying advertisement misroutes the model. The admission checks
in concept 9 exist to make discovery trustworthy: schema lint and capability
audit run before the first session, not after the first incident.

**Routing** maps a model request to one tool on one server. The model
chooses from descriptions and schemas (which is why concept 2 treats them as
UX), and the client enforces the choice: exact-name dispatch, argument
validation against the advertised schema, and — for gated tools — an
approval check before the call leaves the client. When two servers claim
overlapping tools, routing needs a precedence rule (registry order, explicit
priority, or user choice) and a visible warning; silent first-match is how
tool shadowing (concept 7) succeeds.

**Sampling** is the direction reversal: the server asks the model back,
mid-call, for a completion it needs to proceed (disambiguation, a summary, a
judgment). It is powerful and therefore declared: a server must announce
sampling support in its manifest so the host can approve, scope, or refuse
it. An undeclared sampler is a capability lie — the server gains model
access the host never granted — which is why the exercise's rule MCP006
flags `uses_sampling` without `declares_sampling` as critical. DevMate
neither declares nor uses sampling (FACT): its calls flow one way, model to
server to result. Keep it that way until a use case justifies the extra
surface, with the declaration wired before the first sampled call.

When advertisements overlap, the client needs a deterministic precedence —
registry order, an explicit priority field, or a user prompt — applied the
same way on every call, with the losing candidates named in the session log.
Nondeterministic routing is a shadowing vulnerability wearing a
load-balancer costume. Sampling declarations belong in the same manifest the
auditor reads:

```json
{ "name": "summarizer", "version": "1.4.0",
  "declares_sampling": true, "uses_sampling": true }
```

The host matches `uses_sampling` against `declares_sampling` at admission
and refuses the session on mismatch — rule MCP006 as gate logic. A server
that needs sampling later re-admits with the flag set; there is no
mid-session upgrade path, by design.

### 7. Security — The Track's Spine

Seven surfaces, each with its control. They form the spine because every
other concept routes through them: a tool the model cannot trust poisons
discovery, routing, evals, and the audit log at once.

**Poisoned descriptions.** Tool descriptions are prompt-injection surface:
the model reads them as instruction-adjacent text, so a compromised server
(or a compromised dependency of a server) can steer the model with
imperative language inside a description. Control: treat descriptions as
untrusted content at admission (concept 9 lints for imperative verbs and
URLs), keep descriptions declarative, and for high-stakes tools require the
host to pin a reviewed description rather than accepting the advertised one.
Depth on injection mechanics lives in the security track at
`projects/04-ai-engineering/security/lectures/01-prompt-injection-lecture.md`.

**Tool shadowing.** Two servers claiming the same tool name means the
model's call can land on the wrong implementation. Control: registry-wide
name uniqueness or explicit precedence, plus a client warning whenever
resolution had more than one candidate. DevMate's exact-match dispatch
(`server.py:79-87`) resolves correctly only if exactly one server owns each
name — an assumption the registry must guarantee.

**Destructive tools.** Anything that writes, deletes, or reaches the network
requires human approval — `destructive=True` implies `requires_approval=True`
with no exceptions, which is the exercise's rule MCP003 (critical).
DevMate's three tools are all reads (FACT), so the server carries no
destructive surface today; the rule exists so the first write tool ships
gated, not as a follow-up fix.

**Approvals bound to the exact call.** An approval grants one call with one
argument set, identified by the hash of both. It is single-use: presenting
it consumes it, and any replay is denied. A blanket "approve this tool"
grants every future argument set including the attacker's; a reusable id
grants the second call nobody reviewed. The exercise's `decide_call`
implements this — ALLOW with consumption, replay DENIED — and concept 10
tests it end to end.

**Secrets never pass through tool arguments in logs.** Approval receipts,
audit rows, and eval datasets carry the request hash, never raw arguments:
arguments routinely contain file contents, queries with names in them, and
config text. DevMate's HTTP logging surface (concept 5) must hash before it
writes. The output-filtering lecture at
`projects/04-ai-engineering/security/lectures/04-output-filtering-lecture.md`
owns redaction mechanics; this track owns the rule that nothing secret
reaches the log in the first place.

**Undeclared capabilities.** Sampling (concept 6), network egress, or
subprocess execution the manifest does not declare is refused at runtime,
not merely flagged. The manifest is the server's sworn statement; behavior
outside it is a breach of the admission contract.

**Dependency supply chain.** The server's own dependencies are part of the
surface: a compromised SDK or plugin inherits the server's session. Control:
pinned dependencies, admission re-audit on any version change, and rollback
to the last audited version — the subject of concept 9.

| Surface | Control | Enforced where |
|---|---|---|
| Poisoned descriptions | Admission lint + host-pinned text | Concept 9, exercise MCP002 |
| Tool shadowing | Registry uniqueness + resolution warning | Concept 9, client routing |
| Destructive tools | Human approval, no exceptions | Exercise MCP003 (critical) |
| Blanket approvals | Single-use ids bound to argument hash | Exercise `decide_call` |
| Secret leakage | Hash-then-log, raw args never stored | Concept 10 audit-log test |
| Undeclared behavior | Runtime refusal outside the manifest | Exercise MCP006 |
| Supply chain | Pinned deps + re-audit on change | Concept 9 drift detection |

Read the table as a threat model in miniature: each row is one way the
model-to-tool boundary breaks, each control is the cheapest point that stops
it, and each pointer says where the control is enforced. A review that
cannot point at all seven rows for a new server is not finished.

### 8. Reliability Composition — Inherit, Then Apply Per Tool

This concept inherits; it does not restate. Timeouts, classified retries
with jitter, breakers, idempotency, and backpressure are taught at the
service call boundary in `projects/06-devops/reliability/` — the
five-layer dependency contract, the jittered retry at the LLM client, the
bounded queue at the API edge. The work here is applying each pattern to the
unit of a tool call, where the failure modes have MCP-specific shapes.

**Per-tool timeouts.** Every tool declares a positive timeout
(exercise rule MCP007), budgeted from the session deadline the way the
reliability track budgets request deadlines: the tool gets a share, never
the whole. DevMate declares no timeouts (FACT) — a slow embedding call in
`_search_code` holds the session open indefinitely. The fix is a schema
field plus enforcement, with the timeout value in the manifest so the
auditor sees it.

**Cancellation.** A timed-out tool call must actually stop: close the
retrieval request, abandon the embedding call, release the worker. Timeout
without cancellation only stops waiting; the work continues consuming the
shared pool. On stdio this means killing the child; on HTTP it means
propagating the client disconnect to the handler.

**Idempotent tool calls.** Reads are naturally idempotent; the danger is
retrying the first future write tool. Every destructive tool takes an
idempotency key (client-generated, per approval id) and the server dedups on
it, so a retried call after a lost response performs the effect once. The
approval id from concept 7 doubles as the key material: same approval,
same key, one effect.

**Retries only for safe tools.** Classify before retrying: safe
(read-only, side-effect-free) tools may retry on timeout or network error
with the reliability track's jittered backoff; destructive tools never retry
automatically — a retry is a second effect the human did not approve.
Unknown errors never retry: they route to the model as structured errors
(concept 2) so the model can replan instead of hammering.

Budgeting works downward from the session deadline. A 60-second session budget
with three planned tool calls does not give each call 60 seconds; it gives
each a share — say 15 seconds per call with 15 held in reserve for the
model's final synthesis. DevMate's `_search_code` chains an embedding call
plus a retrieval call plus an optional rerank inside one invocation, so its
honest budget splits further: 5 seconds to embed, 8 to retrieve, margin for
formatting. Without declared timeouts none of this arithmetic exists, and
the session's worst case is unbounded. Cancellation completes the pattern:
the timeout fires, the in-flight embedding request is abandoned, the worker
returns to the pool, and the receipt records the cancellation so the model
replans instead of re-issuing blindly.

Idempotency keys close the retry loop. The approval id already binds tool to
arguments, so deriving the key from it costs nothing: same approval, same
key, one effect even if the response was lost and the call re-issued. The
server stores completed keys with their results for the session window and
returns the stored result on repeat — at-least-once delivery with
exactly-once effects, the same guarantee the reliability track teaches for
queues, applied to tool calls.

### 9. Registry and Supply Chain — Admission, Drift, Rollback

A registry is the trust root that makes discovery (concept 6) safe: no
server reaches a client session until it is admitted, and admission is
version-specific. **Pin everything:** server name to exact version, and the
server's dependencies to exact versions alongside it. `latest` is not a
version — it is permission for tomorrow's code to run under today's audit,
which is why the exercise's rule MCP008 rejects empty or unpinned versions.

**Admission checks** run before the first session: schema lint (every tool
carries a non-empty inputSchema, descriptions meet the length floor —
MCP001/MCP002 as gate, not suggestion), capability audit (declared versus
observed: does the server only do what the manifest says — MCP006-class
checks with real traffic), destructive-tool review (every write/delete/
network tool has its approval binding demonstrated, MCP003), and a timeout
and error-shape review (MCP007 plus concept 10's tests). A server that fails
any check is not admitted; there is no provisional trust.

**Drift detection** re-runs admission on every change: version bump,
re-advertised capabilities, or a periodic re-audit on a schedule. The client
caches discovery output per pinned version, so a server that quietly adds a
tool or widens a schema is speaking outside its admission — the session is
refused until re-audit passes. The registry keeps the last audited version
precisely so **rollback** is one pointer move: on a failed re-audit or an
incident, traffic returns to the previous admission while the new version
goes back through the gate. Rollback is practiced, not improvised — the same
discipline the reliability track applies to deploys, pointed at capability
servers.

An admission file for a DevMate-like server reads as a checklist with
verdicts, not vibes:

```text
server devmate@1.4.0
  schema lint ............ PASS (3/3 tools, 0 empty schemas)
  description floor ...... PASS (all >= 20 chars, declarative)
  capability audit ....... PASS (observed == declared, no sampling)
  destructive review ..... PASS (0 destructive tools declared)
  timeout review ......... FAIL (no per-tool timeouts declared)
  error-shape review ..... FAIL (plain-text errors, no codes)
verdict: NOT ADMITTED — fix timeouts and error shape, re-submit
```

The FAIL rows are the lecture's honest DevMate gaps wearing admission
clothes. Drift detection re-runs exactly this file on version or capability
change; rollback points at the last file stamped PASS. Nothing about the
process requires trusting the server — every row is reproducible from the
advertisement, observed traffic, and the test logs.

### 10. Conformance and Evals — Prove the Server, Then Prove the Model

Two measurement layers, in order. **Conformance** proves the server keeps
its contract; five tests, all automated, all gating admission:

1. **Schema validity** — every advertised inputSchema parses, every required
   argument is typed, and the enforcement code validates against the same
   schema the advertisement carries (no drift between list_tools and
   call_tool).
2. **Error-shape test** — invalid arguments, unknown tools, and failed
   preconditions return the documented error shape with a machine-readable
   code, never a bare string the model must parse. DevMate's plain-text
   errors (concept 2) fail this test today — honestly recorded as the first
   fix before admission.
3. **Approval-path test** — a destructive call without approval is denied, a
   fresh approval allows exactly once, and a replayed approval is denied.
   The exercise's approval demo is the executable form of this test.
4. **Timeout test** — a tool that sleeps past its declared timeout is
   cancelled and reported, and the session survives. DevMate's missing
   timeouts (concept 8) fail this test today — the second fix before
   admission.
5. **Audit-log test** — every call emits a receipt with tool name, request
   hash, decision, and approval consumption, with no raw arguments or
   secrets. DevMate's absent audit log fails this test today — the third
   fix.

**Evals** then prove the model uses the admitted tools correctly, on a
golden set of tasks with known-good tool choices: **tool-choice accuracy**
(the model picks the right tool, or correctly picks none), **argument
validity rate** (calls pass schema validation first try), and error
recovery (the model replans sensibly after a typed error). Score per tool
and per version, re-run on every server or model change, and gate rollout
on the scores — a server that passes conformance but confuses the model
(weak descriptions, overlapping tools) is not shippable either. The
registry stores both verdicts together: the server's conformance report and
the model's eval report for that pinned version. That pair is what
"shippable" means in this track.

---

A minimal golden set for DevMate's three tools fits on one screen: "find the
retry helper" (expects `search_code` with a query naming retries),
"show me the traversal guard" (expects `read_file` with the server path),
"how big is the index" (expects `get_repo_stats` with no arguments). Each
task records the expected tool, the schema-valid argument set, and the
acceptable recovery after an injected error (unknown tool name, missing
argument). Scoring is per task — right tool, valid first-try arguments,
sensible replan — aggregated per tool and per pinned version:

| Tool | Choice accuracy | Argument validity | Recovery |
|---|---|---|---|
| search_code | 5/5 | 4/5 | 5/5 |
| read_file | 4/5 | 5/5 | 4/5 |
| get_repo_stats | 3/5 | 5/5 | 5/5 |

The `get_repo_stats` row tells its story plainly: an empty schema leaves the
model unsure when the tool applies, so choice accuracy sags while argument
validity stays perfect (there is nothing to get wrong). The fix is a
description and schema upgrade, re-scored — evals driving design, the loop
the track exists to create.

## Common Mistakes to Avoid

1. ❌ Letting the server decide policy ("this tool is safe, skip approval") / ✅ Policy lives in the host; the server declares facts, the host decides
2. ❌ Shipping tools with empty schemas because "the model figures it out" / ✅ Non-empty inputSchema validated on entry — DevMate's `get_repo_stats` empty schema is the recorded counterexample
3. ❌ One-line descriptions like "search stuff" / ✅ Descriptions name the action, the inputs, and the output shape so routing has signal
4. ❌ Returning errors as bare English strings / ✅ Typed error codes the model can branch on, tested by the error-shape test
5. ❌ Blanket approvals ("always allow read_file") / ✅ Single-use ids bound to the exact argument hash; replay denied
6. ❌ Logging raw tool arguments for debuggability / ✅ Log the request hash; arguments stay out of logs, receipts, and eval sets
7. ❌ Retrying destructive tools with backoff / ✅ Retries for safe tools only; destructive calls need a new approval, never an automatic second attempt
8. ❌ Pinning `latest` and auditing once / ✅ Exact versions, re-audit on change, one-pointer rollback to the last good admission

---

## Best Practices

1. Declare every capability in the manifest; runtime behavior outside it is refused.
2. Keep inputSchema and enforcement code generated from one source so they cannot drift.
3. Write descriptions for the choosing model: action, inputs, output shape, and when not to use the tool.
4. Return structured errors with codes, the offending argument, and what valid looks like.
5. Validate on entry, before any work: required arguments, types, traversal bounds, sizes.
6. Mark every destructive tool and bind it to single-use, argument-scoped approvals.
7. Give every tool a positive timeout budgeted from the session deadline, with real cancellation.
8. Make destructive tools idempotent on the approval id so a retried call has one effect.
9. Retry safe tools with classified, jittered backoff; never auto-retry destructive ones.
10. Authenticate and log remote transports; keep secrets and raw arguments out of every log.
11. Admit servers by exact version with schema lint, capability audit, and the five conformance tests.
12. Detect drift by re-auditing on version or capability change, on a schedule, and refuse unaudited sessions.
13. Evaluate the model side on a golden set: tool-choice accuracy, argument validity, error recovery.
14. Record gaps honestly: an absent resource, timeout, or audit log is a tracked defect, not a simplification.

---

## Practice Exercises

1. Audit DevMate's real server against the eight MCP rules by hand, then confirm with the exercise script: predict which rules `server.py` trips before running.
2. Write the inputSchema and description for a fourth DevMate tool (`get_file_history`) that passes MCP001/MCP002, then extend the auditor with a ninth rule for a defect class of your choice.
3. Convert DevMate's plain-text errors into a typed error shape (`code`, `argument`, `hint`) and update the error-shape test to prove the model can branch on each code.
4. Add a 15-second timeout plus cancellation to `_search_code` following the reliability track's deadline-budget pattern, then write the timeout test from concept 10 against it.
5. Build a three-task golden set (one search, one read, one stats question), score a model's tool-choice accuracy and argument validity by hand, and state which description change would fix each miss.

---

## Summary

- Host decides, client routes, server executes — trust flows one way, from host down.
- Stateless JSON-RPC makes every call loggable, replayable, and testable.
- Tools act, resources address, prompts template — classify by what it does, not what it is called.
- Schemas are contracts, descriptions are routing UX, errors are machine-readable signals.
- DevMate's real server shows the pattern and the gaps: three honest tools, real validation, missing timeouts, auth, and audit log.
- stdio for local sessions, HTTP with auth and logging for anything on a network.
- Discovery is untrusted input until admission makes it otherwise; sampling must be declared.
- Security is seven controls: declarative descriptions, name uniqueness, gated destructive tools, single-use approvals, hashed logging, refused undeclared behavior, pinned supply chain.
- Reliability is inherited per tool: timeouts, cancellation, idempotency keys, safe-only retries.

**Next lecture:** transports in depth — session management, authentication patterns, and observability pipelines for remote MCP deployments.
