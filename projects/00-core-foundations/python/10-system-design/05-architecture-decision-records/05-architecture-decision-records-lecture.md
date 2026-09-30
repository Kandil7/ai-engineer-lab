# System Design Lecture 05: Architecture Decision Records

## Topic Overview

The most expensive words in a codebase are "I don't know why we did it this way." A decision like "PostgreSQL is the source of truth, the vector index is derived" shapes backups, recovery, testing, and every future schema change — and it will be questioned by every new teammate who finds the index is not backed up. If the reasoning lives in a Slack thread, the question gets re-litigated (or silently reversed). An Architecture Decision Record (ADR) is the durable artifact: context, decision, rejected alternatives, consequences — written at decision time, reviewed like code, immutable once accepted. This lecture covers the ADR format, the threshold for when one is warranted, the status lifecycle, and the discipline that keeps decisions *enforced* rather than merely documented.

The theme: **an unrecorded decision is a decision your team will make again, differently.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write a complete ADR: context, decision, alternatives, consequences, links.
2. Apply the threshold test to decide when an ADR is warranted.
3. Manage the status lifecycle (proposed → accepted → deprecated/superseded).
4. Record alternatives with rejection reasons — where the real value lives.
5. Link decisions to their enforcement (tests, config, alerts).
6. Validate ADR documents mechanically (the completeness rules).

---

## Prerequisites

| Need | Where |
|---|---|
| Component contracts | `10-system-design/01-component-contracts/` |
| Source of truth / derived | `10-system-design/03-consistency-and-staleness/` |
| Documentation conventions | repo `AGENTS.md` (docs/ + decision logs) |

---

## 1. What an ADR is

An **Architecture Decision Record** is one document, one decision, written when the decision is made. It is:

- **Short** — one to two pages. If it needs more, it is a design document first, with an ADR for the decision at the end.
- **Versioned** — it lives in the repo (`docs/decisions/NNNN-slug.md`) and travels in the same PR as the code that implements the decision.
- **Immutable in content** — once accepted, the text never changes. If reality changes, a new ADR supersedes it; the old one stays as history.
- **Reviewed like code** — a PR, not a meeting.

It is *not* a wiki page (rot), a meeting note (unstructured), or a design doc (too big).

## 2. The structure

The minimal complete shape (the exercise validates exactly these):

```markdown
# ADR 0001: Use PostgreSQL as the source of truth; vector index is derived

**Status:** accepted

## Context
... facts and forces: what problem, what constraints ...

## Decision
We will ... (the choice, stated as a commitment)

## Alternatives considered
- **Vector DB as source of truth** — rejected: no transactions over citations ...
- **Dual-write to both stores** — rejected: divergence is inevitable ...

## Consequences
- Index rebuild is the universal recovery for index problems.
- ...

## Links
- tests: data_invariants_hold ...
```

Two rules make the difference between useful and noise:

- **Context is facts, not opinions.** "Both stores can write the same facts; citations must not diverge" is force and constraint. "We feel Postgres is better" is not context.
- **Alternatives with rejection reasons** are the *highest-value section* — they prevent the re-litigation that happens when someone proposes the rejected option six months later without knowing it was considered.

## 3. When to write one (the threshold test)

Write an ADR when **all** hold:

1. **Hard to reverse or cross-component** — schema ownership, store selection, auth model, contract versioning.
2. **Real alternatives exist** — reasonable engineers could have chosen differently. If only one option is defensible, the answer is a code comment.
3. **A future "why?"** — someone will ask in six months.

Do **not** write ADRs for style choices (linters own those), routine library picks with one obvious answer, or decisions already covered by an existing ADR's consequences. ADR inflation kills the practice as surely as ADR absence.

## 4. The status lifecycle

```
proposed → accepted → superseded by NNNN
              ↘ deprecated (withdrawn, no replacement)
```

- **Proposed** — written, under review in the PR.
- **Accepted** — merged; the decision is binding on the codebase.
- **Deprecated** — withdrawn; no replacement (usually the forces changed).
- **Superseded by NNNN** — a newer ADR re-decided; the link back keeps the history readable.

Status is the *only* field that changes after acceptance. Content edits mean you are rewriting history; write a new ADR instead.

## 5. Decisions must link to enforcement

An ADR without an enforcement link is a wish. The pattern: every decision names the test, config, or alert that keeps it true.

| Decision | Enforcement |
|---|---|
| Postgres is source of truth | rebuild-from-source test; backup excludes index |
| Lineage keys immutable | data invariant: `source_ref` carried through pipeline |
| Contracts are versioned | contract tests in producer + consumer CI |
| Retries capped | queue `max_attempts` + DLQ depth alert |

The Links section carries these. Review's job: check that the enforcement exists. This turns the ADR from documentation into a *governance* artifact — the decision is only as real as the test that fails when it is violated.

## 6. The worked example

The exercise writes the real Athar decision end-to-end: Context (both stores write the same facts; citations must not diverge), Decision (Postgres authoritative; index derived and rebuildable), Alternatives (vector DB as truth — no transactions over citations; dual-write — divergence inevitable; SQLite — single-writer limits), Consequences (rebuild is the universal recovery; lineage keys mandatory; drift monitoring mandatory). The validator confirms the document is acceptable — and demonstrates rejecting an incomplete one.

## 7. ADRs in the team workflow

- **Write the ADR in the same PR** as the implementation. A decision recorded after the fact loses the alternatives while they are still fresh.
- **Review the ADR first** in the PR; if the ADR is wrong, the code following it is wrong.
- **The decision log** (`docs/decisions/` index, or `registries/decision-log.yaml` in this repo) is the table of contents — every significant decision findable in one screen.
- **When a decision is questioned**, the answer is the ADR link. If the ADR does not answer it, the ADR was incomplete — amend by superseding.

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| One decision per ADR | findable, citable, supersedable |
| Written at decision time | alternatives and context are fresh |
| Alternatives with rejection reasons | re-litigation has an answer |
| Context as facts and forces | no opinion wars in the record |
| Status lifecycle, content immutable | history stays truthful |
| Links to tests/alerts/config | decisions are enforced, not wished |
| Same PR as implementation | review checks decision and code together |
| Decision log index | the whole architecture is one screen |
| Supersede, never edit | the "why changed" trail exists |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Decision made in a meeting, never written | ADR in the same PR as the code |
| ADR as a design doc (10 pages) | design doc + a short ADR for the decision |
| Alternatives section empty | name what was rejected and why |
| Accepted ADR edited later | new ADR that supersedes it |
| ADRs for every library pick | threshold test: hard to reverse + real alternatives |
| No enforcement link | link the test that keeps it true |
| Decision log missing | maintain the index; the map is the value |
| "We'll write it after" | context and alternatives are gone by then |

---

## Mastery Check

You can claim this topic when you can:

1. Write a complete ADR for a real decision in your pipeline, validated by the completeness rules.
2. Say which of your team's recent decisions needed an ADR and which did not.
3. Point at the enforcement link for a recorded decision (the test that keeps it true).
4. Supersede an ADR correctly, with the new one linking back.
5. Answer "why is the index not backed up?" with an ADR link instead of a memory.

---

## Next Steps

- The full skills-to-topics map: `SKILLS_MASTERY_MAP.md` at the module root.
- The Athar decision's consistency mechanics: `03-consistency-and-staleness/`.
- Record contracts as versioned artifacts: `01-component-contracts/`.
