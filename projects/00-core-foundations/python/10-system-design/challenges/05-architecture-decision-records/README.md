# Challenge 05: Architecture Decision Records — The Decision Ledger

"Postgres is the source of truth; the vector index is derived." Six months
later a new teammate asks why. If the answer lives in a Slack thread, the
decision gets re-made — differently. Build the ledger that keeps it.

## 🥉 Bronze — Render the ADR (~15 min)

**Task:** Implement `render_adr(adr)`, producing the markdown form:

```
# ADR 0001: <title>

**Status:** <status>

## Context

<context>

## Decision

<decision>

## Alternatives considered

- **<name>** — <why_not>

## Consequences

- <item>

## Links

- <link>
```

(`Links` section omitted when the list is empty.)

**Signature:**
```python
def render_adr(adr: dict) -> str
```

| Input | Expected |
|---|---|
| full adr dict | contains `# ADR 0001:`, `**Status:**`, all four sections |
| empty links | no `## Links` heading |

**Constraints:** fields: `number, title, status, context, decision,
alternatives (list of [name, why_not]), consequences (list), links (list)`.
Any correct rendering passes.

---

## 🥈 Silver — The Completeness Validator (~35 min)

**Task:** Implement `validate_adr(md)`, returning **all** problems: missing
required sections (`## Context`, `## Decision`, `## Alternatives considered`,
`## Consequences`), missing or malformed `**Status:**` line, unknown status
value (only `proposed/accepted/deprecated/superseded`), an empty alternatives
list, and a decision not phrased as `"we will ..."` or `"we shall ..."`.

**Signature:**
```python
def validate_adr(md: str) -> list[str]
```

| Input | Expected |
|---|---|
| a complete valid ADR | `[]` |
| missing `## Decision` | a problem naming the section |
| `**Status:** maybe` | a problem naming the status |
| no alternatives | a problem about alternatives |
| decision phrased "we choose" | a problem about phrasing |

**Constraints:** deterministic matching only. **Guards:** (a) 12 seeded
defective ADRs (each with exactly one known defect) must ALL be flagged with
the matching reason — a partial validator that checks only sections fails;
(b) a valid ADR yields `[]` (no false positives). **Adversarial case:** a
document with three simultaneous defects must report all three.

---

## 🥇 Gold — The Lifecycle (~75 min)

**Task:** Implement `manage_lifecycle(ledger, action)` mutating and returning
the ledger of ADR dicts `{"number", "topic", "title", "status", "context",
"decision", "superseded_by"}`:
- `{"type": "propose", "adr": {...}}` → append with `status="proposed"`.
- `{"type": "accept", "number": N}` → that ADR becomes `"accepted"`.
- `{"type": "deprecate", "number": N}` → `"deprecated"`.
- `{"type": "supersede", "number": N, "new_adr": {...}}` → the old ADR becomes
  `"superseded"` with `superseded_by` = the new number; the new ADR is appended
  as `"accepted"`.

And `effective_decision(ledger, topic)` returning the currently binding ADR —
the **highest-numbered** `"accepted"` ADR for the topic (`None` if none).

**Signature:**
```python
def manage_lifecycle(ledger: list[dict], action: dict) -> list[dict]
def effective_decision(ledger: list[dict], topic: str) -> dict | None
```

| Scenario | Expected |
|---|---|
| 5-deep supersession chain | `effective_decision` returns ADR 5 |
| chain shuffled in the list | still ADR 5 (not the last element) |
| only proposed ADRs | `None` |
| after 200 mixed actions | every ADR's `context`/`decision` text unchanged |

**Constraints:** 50-ADR ledgers, 200 actions, memory ceiling 8 MB peak
(`tracemalloc`) — deep-copying the ledger per action blows it; in-place
mutation stays flat. **Guards:** (a) **immutability** — text fields hash
identically before and after (only `status`/`superseded_by` may change);
(b) **chain resolution** — the newest accepted wins regardless of list order;
(c) memory ceiling. **Follow-up:** what breaks first at 500 ADRs? *(Answer:
lookup becomes a linear scan — you need an index by topic, exactly like
`registries/decision-log.yaml`.)*

---

## Running

```bash
python -m pytest 10-system-design/challenges/05-architecture-decision-records/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 10-system-design/challenges/05-architecture-decision-records/test_challenge.py -q
```
