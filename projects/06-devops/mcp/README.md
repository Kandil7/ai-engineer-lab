# MCP Deep — Protocol, Servers, Security, and Conformance

Model Context Protocol from the wire up: the host/client/server split,
stateless JSON-RPC messages, the tools/resources/prompts primitives, Python
server construction, stdio versus Streamable HTTP transports, the client side,
and the track's spine — security (injection surfaces, shadowing, approvals) —
composed with the reliability track's timeout/retry/idempotency discipline, plus
registry admission and conformance evals. Every example is grounded in the real
DevMate MCP server in this repository; its gaps are named as gaps.

---

## Architecture: Host, Client, Server

```text
                    +------------------- HOST -------------------+
                    |  trusted runtime: the app the user runs    |
                    |  (IDE plugin, desktop app, agent loop)     |
                    +--------+---------------+------------------+
                             |               |
                    creates  |               | enforces policy
                             v               v
                    +--------+------+ +------+--------+      +--------------+
                    |   CLIENT 1    | |   CLIENT 2    | ...  |  audit log   |
                    |  one session  | |  one session  |      |  allow/deny  |
                    +---+-----+-----+ +---+-----+-----+      +------+-------+
                        |     |           |     |                   ^
          JSON-RPC      |     |           |     |     receipts      |
          request/      |     |           |     |                   |
          response      v     v           v     v                   |
                    +---+-----+-----+ +---+-----+-----+             |
                    |   SERVER A    | |   SERVER B    |  approvals--+
                    |  3 tools,     | |  pinned       |
                    |  stdio pipe   | |  HTTP+sess    |
                    +---------------+ +---------------+
```

The host owns policy and the audit log. Each client holds one server session and
routes model requests to the right tool. Each server exposes tools, resources, or
prompts and validates every call on entry. Approval receipts flow back to the host.

---

## Track Contents

| File | What it covers |
|------|----------------|
| `lectures/01-mcp-deep-lecture.md` | Ten concepts end to end: architecture and primitives, tool design, Python server construction mapped to DevMate's real server, resources and prompts, transports, client discovery/routing/sampling, security spine, reliability composition, registry and supply chain, conformance and evals |
| `lectures/01-mcp-deep-glossary.md` | 40-term quick-reference table plus detailed definitions, each grounded in this repo's server or naming the repo's gap explicitly |
| `quizzes/01-mcp-deep-quiz.md` | 15 questions (5 Easy, 7 Medium, 3 Hard) with inline answers and explanations, score tracking, answer key |
| `exercises/01-mcp-deep.py` | Offline manifest auditor: 8 MCP rules over a manifest pack (BAD trips all 8, GOOD raises zero) plus a single-use approval-flow demo with replay denial — stdlib only, no network |
| `README.md` | This page |

---

## What Is Grounded (FACT)

Verified at the cited paths before this track was written:

- **Three tools, honestly described:** `search_code` (query required, language/top_k optional), `read_file` (file_path required), `get_repo_stats` (empty input schema) —
  registered in `projects/04-ai-engineering/devmate/src/devmate/mcp/server.py:30-77`,
  dispatched in `call_tool` at `server.py:79-87`, unknown names raising
  `ValueError` at `server.py:87`.
- **Entry validation returns text, not typed errors:** missing query at
  `server.py:95-96`, missing file_path at `server.py:145-146`, wrapped as
  `TextContent` strings (`Search error:`, `Read error:`, `Stats error:`).
- **One real guard, several real gaps:** the path-traversal check
  (`relative_to(repo_root)`) lives at `server.py:155-158`; there are **no**
  resources, **no** prompts, **no** sampling declaration, **no** per-tool
  timeouts, **no** auth on the HTTP transport, and **no** audit log anywhere
  in `devmate/mcp/` — verified by reading the whole file; the lecture records
  each as a gap with the rule that would catch it.
- **Two transports, both real:** stdio for local clients (opencode,
  Claude Desktop) at `server.py:193-200`; SSE over HTTP via uvicorn
  (default port 8001, routes `/sse` and `/messages/`) at `server.py:202-234`;
  CLI entry `python -m devmate.mcp.server [stdio|http]` at `server.py:266-278`
  with host/port from settings at `server.py:260-263`.

Sources: `source-index#23` (Hugging Face Agents Course — tool use),
`source-index#28` (Chip Huyen, *AI Engineering* — reliability framing).

---

## Complements (Not Duplicates)

This track applies registered knowledge at the **model-to-tool boundary**.
Adjacent territory stays where it is:

- `projects/06-devops/reliability/` — timeouts, retries, breakers, idempotency at the
  **service call boundary**, inherited per tool here, never restated.
- `projects/04-ai-engineering/security/lectures/01-prompt-injection-lecture.md`
  and `04-output-filtering-lecture.md` — injection and output defense for
  **model behavior**. This track covers the MCP-specific surfaces (tool
  descriptions, shadowing, approvals) and points at those lectures for depth.
- `agents.mcp` (knowledge-registry) — the protocol's existence, taught in
  `docs/curriculum/lectures/03-agents.md` from `source-index#23`. This track
  is the deep companion: server construction, transports, supply chain,
  conformance.

---

## Verification

Run from the repository root:

```powershell
python -m py_compile projects\06-devops\mcp\exercises\01-mcp-deep.py
python projects\06-devops\mcp\exercises\01-mcp-deep.py
powershell -NoProfile -ExecutionPolicy Bypass -File tests\repo-structure\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests\knowledge\validate.ps1
```

Expected: compile exits 0; the demo exits 0 (BAD trips all 8 MCP rules, GOOD raises
zero, replay denied, self-check passed); both validators exit 0. The exercise is
stdlib-only, offline, and deterministic — reruns are identical.

---

*AI Engineer Lab — DevOps track, MCP lane.*
