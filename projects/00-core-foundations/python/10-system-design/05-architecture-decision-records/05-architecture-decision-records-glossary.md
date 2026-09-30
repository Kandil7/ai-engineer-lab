# Architecture Decision Records Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| ADR | Architecture Decision Record: one document, one significant decision |
| Decision log | Index of all ADRs; the architecture's table of contents |
| Context | ADR section: facts, forces, constraints (not opinions) |
| Decision | ADR section: the choice, phrased "we will ..." |
| Alternatives considered | ADR section: rejected options with reasons |
| Consequences | ADR section: what becomes easier, harder, riskier |
| Links | ADR section: tests/config/alerts enforcing the decision |
| Status | Lifecycle marker: proposed / accepted / deprecated / superseded |
| Proposed | ADR written, under review |
| Accepted | ADR merged; decision is binding |
| Deprecated | Decision withdrawn, no replacement |
| Superseded | Replaced by a newer ADR (which links back) |
| Immutable content | Accepted ADR text never edits; supersede instead |
| Superseding | Recording a re-decision as a new linked ADR |
| Re-litigation | The same decision re-argued because the record is missing |
| Threshold test | Rules for when an ADR is warranted |
| Hard to reverse | Decision property justifying an ADR |
| Cross-component | Decision affecting multiple modules/teams |
| Enforcement link | The test/alert/config that keeps a decision true |
| Source of truth | The canonical example decision (Postgres vs vector index) |
| Derived store | Rebuildable store; the other half of ADR-0001 |
| Governance artifact | Document that binds future work, not just describes |
| Decision review | Reviewing the ADR before the implementing code |
| MADR | Markdown ADR template this format is informed by |
| Decision phrasing | "We will ..." commitment form required by validation |
| History trail | Chain of superseding ADRs showing how thinking evolved |
| Design doc | Longer document; ADR extracts just the decision |
| Forces | External constraints shaping the decision (traffic, team, SLA) |

---

## Detailed Definitions

### ADR
One significant architecture decision per document: context (facts and forces), decision ("we will ..."), alternatives with rejection reasons, consequences, and enforcement links. Written at decision time, reviewed like code, versioned in the repo.

### Status lifecycle
proposed → accepted → superseded/deprecated. Status is the only mutable field after acceptance; content changes are superseding ADRs, keeping the history trail intact.

### Alternatives considered
The highest-value section: what was rejected and why. It answers the future re-litigation ("what about a vector DB as truth?") with the recorded reasons instead of a new debate.

### Threshold test
An ADR is warranted when the decision is hard to reverse or cross-component, real alternatives exist, and a future "why?" is likely. Routine picks belong in code comments, not ADRs.

### Enforcement links
Every decision names the mechanism that keeps it true (rebuild test, invariant test, contract tests, DLQ alerts). A decision without enforcement is a wish.

### Superseding
The way decisions evolve: a new ADR re-decides and links back ("superseded by 0002"). Never edit accepted content.

### Governance artifact
An ADR binds future work: reviews check code against recorded decisions, and "why?" questions resolve to links. The decision log is the architecture's one-screen map.

### Worked example (ADR-0001)
"PostgreSQL is the source of truth; the vector index is derived" — with alternatives (vector DB as truth, dual-write, SQLite) rejected for stated reasons, and consequences (rebuild as recovery, mandatory lineage keys, drift monitoring).
