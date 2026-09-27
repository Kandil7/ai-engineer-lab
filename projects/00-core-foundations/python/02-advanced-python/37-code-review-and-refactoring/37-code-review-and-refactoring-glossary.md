# Code Review and Refactoring Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Code review | Human quality gate on a change before merge |
| Review lens | Priority order for review attention (correctness first) |
| Correctness review | Checking behavior against the requirement, at the edges |
| Structure review | Checking responsibilities, contracts, blast radius |
| Security review | Checking trust boundaries, secrets, authz, injection |
| Style review | Naming/formatting — automated, never manually reviewed |
| Smell | Measurable symptom of structural decay |
| God function | Function fused with many concerns and many reasons to change |
| Cyclomatic complexity | Number of independent execution paths through a unit |
| Threshold | Mechanical limit (lines, params, branches) enforced in CI |
| Extract method | Refactor: move a responsibility block into its named unit |
| Strategy pattern | Refactor: replace behavior conditionals with polymorphism |
| Lock test | Golden test captured before a refactor to prove behavior preserved |
| Characterization test | Test pinning current behavior, quirks included |
| Golden output | Byte-identical expected output used as regression anchor |
| Refactoring | Structure change with zero behavior change |
| Behavior change | Deliberate output change — a product decision, separate PR |
| Review comment | Artifact: severity + location + problem + fix |
| BLOCK / SHOULD / NIT | Comment severities: must-fix / plan-or-fix / optional |
| Tautological test | Assertion that cannot fail (assert result == result) |
| Structural delta | Per-PR metrics: functions, total lines, max branches |
| Blast radius | Code that must re-test when one thing changes |
| Probe input | Edge-case input included in a lock test |
| Input validation | Rejecting untrusted data at the trust boundary |
| Prompt injection | Untrusted text that the model treats as instructions |
| Rollback plan | Defined path to undo a change (flag, config, prior index) |
| Cost at 10x | Review question: what does this cost when traffic grows |
| radon / ruff / mypy | Complexity, lint/format, type tools used as review backstops |

---

## Detailed Definitions

### Review lens
The priority order for review attention: correctness, structure, tests, security, style. Stop at the first failing layer — style debates on a buggy PR waste the review.

### Smell measurement
Replacing taste with numbers: function length, parameter count, branch count, cyclomatic complexity. Thresholds are team agreements enforced in CI (ruff, radon, mypy), not wiki rules.

### Extract method
Moving a responsibility into a named unit with plain-data inputs/outputs. Extract by concern, not by line count. Immediate tests per extracted unit.

### Strategy pattern (replace conditional with polymorphism)
Turning `if/elif` behavior switches into classes behind a small Protocol; the only switch left is in the composition root. New retrieval engines become new classes.

### Lock / characterization / golden tests
Tests captured from *current* behavior before a structural move, asserting byte-identical outputs on probe inputs (including quirks). They are the referee of the "behavior preserved" claim. A failing lock means the refactor drifted.

### Review comment
A four-part artifact: severity (BLOCK/SHOULD/NIT), location, problem, suggested fix. Complete without the fix only when it is a question of intent.

### Structural delta
Per-PR summary of function count, total lines, max branches. Monotonic growth signals decay; diff-based budgets in CI keep it from spreading.

### Correctness vs behavior change
A refactor keeps outputs identical (verified by locks). A behavior change alters outputs and belongs in its own PR with product sign-off.

### Security review concerns in AI systems
Untrusted text at trust boundaries (queries, retrieved documents), prompt injection, secrets in logs, missing authz, and unbounded-cost endpoints.

### Rollback plan
The defined way to undo a change: feature flag, config value, or previous index. An unrollbackable model/prompt change is an experiment running in production.
