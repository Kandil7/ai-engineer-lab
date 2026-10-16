# Glossary 01: MCP Deep — Quick Reference

Forty terms in one table for scanning, then full definitions. Every entry
is grounded in this repository's real server at
`projects/04-ai-engineering/devmate/src/devmate/mcp/server.py`, in the
reliability track at `projects/06-devops/reliability/`, or in the named
security lecture — or it states the repo's gap explicitly.

**How to use:** scan the table to place an unfamiliar term, then read its
full definition before citing it in a review. Terms marked as gaps name
work to do, not behavior to rely on — never cite a gap entry as evidence
that the behavior exists.

---

## Quick-Reference Table

| Term | One-line meaning |
|------|------------------|
| Host | Trusted app the user runs; owns policy and the audit log |
| Client | One-session protocol speaker routing model requests to one server |
| Server | Untrusted capability process advertising tools, resources, prompts |
| Session | One client-to-server connection with discovery and receipts |
| JSON-RPC Request | Id-carrying message expecting a matching response |
| JSON-RPC Response | Result or error carrying the request's id |
| Notification | Fire-and-forget message expecting no response |
| Tool | Function the model calls; may change the world |
| inputSchema | JSON Schema contract for a tool's arguments |
| Tool Description | Routing UX the model reads to choose between tools |
| Resource | Addressable context the model reads but never executes |
| URI Scheme | Prefix naming which handler and permission set serves a resource |
| Prompt | Stored template with validated arguments the model instantiates |
| Prompt Argument | Declared, validated input a prompt template interpolates |
| Sampling | Server asking the model back mid-call; must be declared |
| Discovery | Client learning capabilities via list calls at session start |
| Dispatch | Server routing a call by exact tool name |
| Entry Validation | Argument and bounds checks before any work happens |
| Traversal Guard | Path check confining file access under the repo root |
| stdio Transport | Local pipe transport: one process pair, no ports |
| SSE Transport | HTTP push transport DevMate serves via uvicorn |
| Streamable HTTP | Remote transport family needing auth, TLS, and logging |
| Approval | Human grant for one gated call with one argument set |
| Approval Id | Single-use identifier binding tool name to request hash |
| Request Hash | SHA-256 digest identifying the exact call without logging secrets |
| Replay Attack | Re-presenting a consumed approval id for an unreviewed second call |
| Destructive Tool | Write, delete, or network tool requiring human approval |
| Gated Tool | Any tool needing an approval id before execution |
| Tool Shadowing | Two servers claiming the same tool name |
| Poisoned Description | Malicious instruction smuggled inside a tool description |
| Capability Lie | Behavior outside the manifest, e.g. undeclared sampling |
| Audit Log | Host-kept receipts: tool, hash, decision, consumption |
| Admission | Version-specific gate before a server reaches any session |
| Schema Lint | Static check: schemas present, descriptions long enough |
| Drift Detection | Re-audit on version or capability change |
| Rollback | One-pointer return to the last audited version |
| Version Pin | Exact version reference; `latest` is never a pin |
| Conformance Suite | Five tests proving a server keeps its contract |
| Error Shape | Machine-readable error code, argument, and hint |
| Golden-Set Eval | Scored tasks measuring the model's tool use |

---

## Full Definitions

### Host

The application the user runs — an IDE plugin, a desktop app, an agent
loop. The host is the only trusted party in the MCP split: it creates
clients, enforces approval policy, and keeps the audit log. Policy lives
here because the host is the one the user installed and can hold
accountable; pushing policy into servers lets the least trusted party grade
its own homework. Lecture concept 1; admission and evals report to the host.
When a review asks "who approves this call," the answer is always a host
component — if no host component can answer, the design is incomplete.

### Client

The protocol speaker holding exactly one session with one server. The client
discovers capabilities, routes model requests to the right tool, validates
arguments against the advertised schema, checks approvals for gated tools,
and returns results plus receipts to the host. DevMate's server side
assumes this counterpart: its `list_tools` handler exists to be discovered
and its `call_tool` dispatch exists to be routed to. Clients never execute
tools themselves.

### Server

The capability process exposing tools, resources, and prompts over a
transport. Servers are untrusted by design: they advertise what they can do
and execute what they are asked, but no claim they make is accepted without
verification — admission checks the advertisement, approvals gate the
dangerous calls, and the audit log records what actually happened. DevMate's
`DevMateMCPServer` (`server.py:19-24`) is a real, minimal instance: three
tools, two transports, no resources or prompts.

### Session

One client-to-server connection from initialization through capability
discovery to call receipts and teardown. Sessions scope everything: approval
ids are consumed within a session's audit trail, discovery output is cached
per pinned version per session, and cancellation ends the session's
outstanding calls. On stdio the session lifetime equals the child process;
on HTTP it is managed with session tokens that must expire.

### JSON-RPC Request

A message with protocol marker, id, method, and params that obligates a
matching response. The id is the linchpin: it pairs responses to requests
across interleaved traffic and lets tests replay exact exchanges. Lecture
concept 1 shows the `tools/call` shape. Statelessness means any request can
be logged by hash and re-run in a conformance test without hidden context.

### JSON-RPC Response

The server's answer carrying the request's id with either a result or an
error. A well-formed error carries a machine-readable code the caller can
branch on — the property DevMate's plain-text `TextContent` errors lack,
and the property the error-shape conformance test demands. Timeouts are
client-side judgments that no response arrived in budget, not server
messages.

### Notification

A method-plus-params message that expects nothing back: progress updates,
cancellation signals, log forwarding. Because there is no response to
correlate, notifications must be idempotent on receipt — a duplicated
progress note changes nothing, and a duplicated cancellation is harmless.
Cancellation in concept 8 travels this channel on transports that support
it.

### Tool

A function the model calls that runs code and may change the world. Tools
are the only primitive with side effects, which is why every security and
reliability control in this track binds at the tool boundary: schemas,
descriptions, approvals, timeouts, idempotency keys, retries. DevMate
exposes exactly three — `search_code`, `read_file`, `get_repo_stats`
(`server.py:31-77`) — all reads, which bounds its blast radius to
information disclosure rather than state corruption.

### inputSchema

The JSON Schema object that is a tool's argument contract: property names,
types, required list, and ideally bounds. The model shapes calls from it;
the server validates against it on entry. An empty or missing schema
(`"properties": {}` on `get_repo_stats` at `server.py:69-76`) disables both
sides at once — the defect rule MCP001 exists to reject. Best practice
generates the schema and the enforcement code from one source so they
cannot drift. In review, read the schema before the handler: if the two
disagree about what is required, the schema is the bug report.

### Tool Description

The sentence or two the model reads when choosing between tools — routing
UX, not documentation. It must name the action, the inputs, and the output
shape, and say when not to use the tool. Under ~20 characters it carries no
signal (rule MCP002); written as imperatives or stuffed with URLs it
becomes injection surface (poisoned description). DevMate's three
single-sentence descriptions (`server.py:34,57,71`) are adequate and
declarative — the floor, not the ceiling.

### Resource

Addressable context the model reads but never executes: files, rows,
configs, served by URI. Resources separate "context the model needs" from
"actions the model takes," so read-only data never pays the approval and
timeout cost of tools. DevMate exposes none — a recorded gap, with the
admission question attached: which schemes may be served, and which paths
inside each scheme are in bounds.

### URI Scheme

The prefix (`repo://`, `db://`) naming which handler and which permission
set serves a resource. The scheme is the routing and policy decision in one
token: it selects the reader, the bounds check, and the log category. A URI
without one (`repo/files/config`) is unresolvable by the client and
unauditable by the host — rule MCP004 rejects it. Schemes are allow-listed
at admission, never inferred from the string.

### Prompt

A stored template with a declared argument list that the client fills and
the model runs — a reusable workflow, not free text. Prompts move
well-tested instruction patterns out of ad-hoc chat and under version
control, where admission and evals can see them. DevMate exposes none; the
first one ships only with every placeholder declared and validated (rule
MCP005) and the injection review from the security track's prompt-injection
lecture applied to its template text.

### Prompt Argument

One declared, validated input a prompt template interpolates. Every
`{placeholder}` in the template must appear in the argument list, and every
argument value must be validated before interpolation — type, length, and
character policy. An unlisted placeholder is unvalidated interpolation:
caller-controlled text entering a template the model treats as instruction.
The exercise's MCP005 pack (`{audience}` missing from `args`) is the
canonical specimen.

### Sampling

The direction reversal: the server asking the model back mid-call for a
completion it needs to proceed. Sampling gives the server influence over
model output, so it must be declared in the manifest before first use; an
undeclared sampler gains model access the host never granted — a capability
lie (rule MCP006, critical). DevMate neither declares nor uses sampling, so
its calls flow one way. Keep it that way until a use case justifies the
surface, with the declaration wired first.

### Discovery

The session-start phase where the client calls `list_tools` (and the
resource/prompt equivalents) and caches the advertisement. Discovery output
is untrusted input: it feeds routing, so a lying advertisement misroutes
the model. Admission (schema lint plus capability audit) exists to make
discovery trustworthy, and the client caches per pinned version so a server
cannot widen its advertisement mid-session without re-audit.

### Dispatch

The server's exact-name routing of a call to its handler — DevMate's
`call_tool` if-chain with `ValueError` on unknown names (`server.py:79-87`).
Dispatch is a security surface precisely because it is exact string match on
model-produced text: with two servers claiming one name, the call lands
wherever precedence resolves (tool shadowing). Dispatch must also never
execute before validation and approval checks run.

### Entry Validation

All argument and bounds checks performed inside the server before any work:
required-argument presence, types against the schema, path confinement,
size caps. DevMate validates query and file_path presence (`server.py:95-96,
145-146`) with hand-written checks returning English strings — the right
place, the weakest shape. The conformance suite's schema-validity test
requires the same schema to drive advertisement and enforcement.

### Traversal Guard

The check confining file access under an allowed root — DevMate's
`relative_to(repo_root)` at `server.py:155-158` plus existence and is-file
checks. It is one real guard against one real attack (escaping the repo via
`..` segments), and the lecture is explicit about what it is not: no
symlink policy, no size cap on reads, no scheme allow-list. Name the rest as
admission conditions when the server grows resources.

### stdio Transport

The local transport: the client spawns the server as a child process and
speaks JSON-RPC over pipes — DevMate's `run_stdio` (`server.py:193-200`),
the default its CLI documents for local clients. One process pair, no
ports, credentials inherited from the local user; a crashed server takes
the session with it. Log to standard error only: standard output carries
the protocol, and a stray print corrupts the session.

### SSE Transport

The HTTP push transport DevMate serves via uvicorn on port 8001 with routes
`/sse` and `/messages/` (`server.py:202-234`). It proves the remote pattern
— many clients, reconnectable sessions, observable traffic — while exposing
its gaps honestly: no authentication, no TLS in-process, no request log. The
lecture's rule is that this mode never faces a network without those three
added; as shipped it is a local demo transport.

### Streamable HTTP

The remote transport family for production: session management, reconnect,
per-client limits, with auth, TLS, and structured request logging built in,
not bolted on. Choosing it buys multi-client operation and observability at
the price of building everything stdio inherits: session tokens with
expiry, rate limits, and an audit trail keyed by session id. The lecture's
selection rule stays local-first until a second client justifies the cost.

### Approval

A human grant permitting one gated call with one exact argument set. The
grant is scoped (this tool, these arguments), conditional (reviewed the
rendered call, not the category), and recorded (receipt to the audit log).
Blanket grants ("always allow deletes") are the failure mode: they convert
one reviewed decision into unlimited unreviewed effects. Every destructive
tool requires one; the exercise's rule MCP003 makes it a critical finding
when it does not.

### Approval Id

The single-use identifier naming one grant: `{tool}:{request_hash}`. The
client presents it with the call, the host consumes it on decision, and any
second presentation is denied as replay. Binding the id to the hash (not
the tool alone) is what stops argument substitution — the approved `read_file
README.md` cannot become an approved `read_file` of anything else. The
exercise's `decide_call` mints, consumes, and refuses these ids.

### Request Hash

The SHA-256 digest (truncated to 16 hex chars in the exercise) over the
canonical tool name plus arguments. It identifies the exact call everywhere
a receipt, log row, or eval record needs to — without storing the arguments
themselves, which routinely contain file contents and config text. Hash,
then log; the raw arguments live only in the live call path.

### Replay Attack

Re-presenting a consumed approval id to authorize an unreviewed second call.
Single-use consumption is the whole defense: the first presentation burns
the id, so the attacker's window is exactly zero already-authorized calls.
The approval demo proves the property end to end — ALLOW once, DENY on
replay — and the approval-path conformance test automates the proof for
admission.

### Destructive Tool

Any tool that writes, deletes, or reaches the network. The category is
deliberately broad: cache rotation, file writes, outbound fetches, and
anything with an external side effect all qualify. The obligations attach at
declaration — `destructive=True` implies `requires_approval=True`,
idempotency keying, no automatic retries — and rule MCP003 flags any breach
as critical. DevMate's three read-only tools carry no destructive surface,
which is a scope fact, not a safety proof for future tools.

### Gated Tool

Any tool the host refuses to run without a presented approval id — all
destructive tools plus sensitive reads (credentials, private data, full-repo
exfiltration shaped reads). Gating is host enforcement, not server advice:
the server declares `requires_approval`, the client refuses to dispatch
without the id, and the receipt records the consumption. DevMate's GOOD pack
models a gated read (`read_file` with `requires_approval=True`).

### Tool Shadowing

Two servers claiming the same tool name, so the model's call can land on
the wrong implementation — the registry's problem, the client's emergency.
The controls are registry-wide name uniqueness (or explicit precedence with
a visible warning at resolution) plus admission-time collision checks across
all pinned servers. DevMate's exact-match dispatch is correct only under
the uniqueness the registry must guarantee.

### Poisoned Description

A tool description carrying imperative language, URLs, or instructions that
steer the model — injection surface wearing documentation clothes. Because
descriptions feed the model's tool choice directly, a compromised server (or
its compromised dependency) can promote its own tools or demote others'.
Admission lints for the pattern; high-stakes tools pin host-reviewed
descriptions instead of accepting advertised text. Mechanics depth: the
security track's prompt-injection lecture.

### Capability Lie

Any runtime behavior outside the manifest: undeclared sampling, hidden
network egress, subprocess execution the advertisement never mentions. The
manifest is a sworn statement, and behavior outside it breaches the
admission contract — refused at runtime, not merely flagged. Rule MCP006
(undeclared sampling) is the exercise's representative; the capability
audit in admission generalizes it with observed-traffic comparison.

### Audit Log

The host-kept, append-only record of every call: tool name, request hash,
decision (ALLOW, DENY, AUDIT), approval consumption, latency — never raw
arguments, never secrets. The log is the evidence for incident review, the
dataset for tool-choice evals, and the artifact the audit-log conformance
test inspects. DevMate keeps no audit log: the lecture records this as the
third fix before admission, with the receipt shape specified so the fix is
mechanical.

### Admission

The version-specific gate no server passes before reaching a session:
schema lint, capability audit, destructive-tool review, timeout and
error-shape review, and the five conformance tests. Failure means no
admission — there is no provisional trust, no "ship now, audit later." The
registry stores the verdict with the pinned version, and drift detection
decides when the verdict expires. A PASS means nothing without the version
string attached, and re-audit on drift is what keeps old verdicts from
covering new code.

### Schema Lint

The static half of admission: every tool carries a non-empty inputSchema,
every description clears the length floor, every resource URI parses with
a scheme, every prompt placeholder is declared. The exercise auditor is a
runnable schema lint — rules MCP001, MCP002, MCP004, MCP005, MCP008 run
without executing anything. Lint gates admission; it never substitutes for
the runtime half (capability audit, approval-path test).

### Drift Detection

Re-running admission on every version bump, re-advertised capability set,
or schedule tick — because `latest` moves under you and servers change.
The client caches discovery per pinned version, so widening an
advertisement mid-session speaks outside the admission and the session is
refused until re-audit passes. Detection without enforcement is telemetry;
this track pairs them: detect, refuse, re-audit, or roll back.

### Rollback

The one-pointer return to the last audited version on failed re-audit or
incident. The registry retains prior admissions precisely for this move, and
the move is practiced before it is needed — the same discipline the
reliability track applies to deploys, pointed at capability servers. A
registry that cannot roll back cannot safely admit anything new.

### Version Pin

An exact version reference (`1.4.0`, never `latest`) for a server and its
dependencies. Pins make audits refer to something: the verdict, the eval
scores, and the rollback pointer all key on the pinned string. Rule MCP008
rejects empty or floating versions at lint time because everything
downstream — drift detection, rollback, incident review — assumes the pin
means one immutable artifact.

### Conformance Suite

The five automated tests proving a server keeps its contract: schema
validity, error shape, approval path, timeout, audit log. All five gate
admission; all five re-run on drift. DevMate as shipped fails three
(plain-text errors, no timeouts, no audit log) — the lecture names each
failure with its fix, so conformance reads as a work list, not a verdict.
The exercise's demos are the executable sketches of the approval-path and
schema-validity tests.

### Error Shape

The machine-readable error contract: a stable code, the offending argument,
and a hint stating what valid looks like — returned for invalid arguments,
unknown tools, and failed preconditions alike. The model can branch on a
code; it can only guess at a sentence. DevMate returns English strings
inside `TextContent` (the recorded weakness), so its first conformance fix
is typing these errors without changing what they report.

### Golden-Set Eval

The model-side measurement on scored tasks with known-good tool choices:
tool-choice accuracy (right tool, or correctly none), argument validity rate
(first-try schema pass), and error recovery (sensible replan after a typed
error). Scored per tool per pinned version, re-run on every server or model
change, gating rollout alongside conformance. A conformant server that
confuses the model — weak descriptions, overlapping tools — fails here, and
that failure blocks shipping exactly like a failed test.

---

## Where Each Term Is Enforced

Terms split into three enforcement points — check new servers against all
three before admission:

- **Static (auditor and lint):** inputSchema, Tool Description floor,
  URI Scheme, Prompt Argument coverage, Version Pin. The exercise script
  runs these as rules MCP001, MCP002, MCP004, MCP005, MCP008.
- **Runtime (client and host):** Approval, Approval Id consumption,
  Replay refusal, Sampling declaration match, Error Shape. Proven by the
  approval-path, error-shape, and timeout conformance tests.
- **Process (registry and schedule):** Admission, Drift Detection,
  Rollback, Golden-Set Eval. Owned by the registry operator on version
  change, capability change, and calendar tick.

*AI Engineer Lab — DevOps track, MCP lane.*
